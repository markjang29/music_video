import argparse
import hmac
import json
import os
import subprocess
import sys
import threading
import urllib.error
import urllib.request
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parent
CONTENT_PATH = ROOT / "content.json"
ALLOWED_LANGUAGES = {"ko", "en", "vi"}
LANGUAGE_ORDER = ("ko", "en", "vi")
ALLOWED_DAYS = {"0809", "0810", "0811", "0812", "0813", "0814", "0815"}
WRITE_LOCK = threading.Lock()


def load_content():
    with CONTENT_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def run_git(*args, timeout=90):
    env = os.environ.copy()
    ssh_key = env.get("MUSIC_VIDEO_GIT_SSH_KEY")
    if ssh_key:
        env["GIT_SSH_COMMAND"] = (
            f"ssh -i {ssh_key} -o IdentitiesOnly=yes "
            "-o StrictHostKeyChecking=accept-new"
        )
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )


def current_commit():
    result = run_git("rev-parse", "--short", "HEAD")
    return result.stdout.strip() if result.returncode == 0 else None


def validate_shots(shots):
    if not isinstance(shots, list) or not 1 <= len(shots) <= 30:
        raise ValueError("Shots must contain between 1 and 30 items")

    cleaned = []
    for index, shot in enumerate(shots):
        if not isinstance(shot, list) or len(shot) != 5:
            raise ValueError(
                f"Shot {index + 1} must have title, detail, technique, length, and transition"
            )
        title, detail, technique, clip_length, transition = shot
        if not all(isinstance(value, str) for value in shot):
            raise ValueError(f"Shot {index + 1} contains invalid text")
        title = title.strip()
        detail = detail.strip()
        technique = technique.strip()
        clip_length = clip_length.strip()
        transition = transition.strip()
        if not title or not detail or not technique or not clip_length or not transition:
            raise ValueError(f"Shot {index + 1} has an empty field")
        if (
            len(title) > 100
            or len(detail) > 500
            or len(technique) > 80
            or len(clip_length) > 80
            or len(transition) > 300
        ):
            raise ValueError(f"Shot {index + 1} is too long")
        cleaned.append([title, detail, technique, clip_length, transition])

    return cleaned


def validate_update(payload):
    if not isinstance(payload, dict):
        raise ValueError("Invalid request body")

    language = payload.get("language")
    day_id = payload.get("dayId")
    if language not in ALLOWED_LANGUAGES:
        raise ValueError("Unsupported language")
    if day_id not in ALLOWED_DAYS:
        raise ValueError("Unsupported date")

    return language, day_id, validate_shots(payload.get("shots"))


def load_llm_config():
    token = os.environ.get("MUSIC_VIDEO_LLM_TOKEN", "").strip()
    base_url = os.environ.get("MUSIC_VIDEO_LLM_BASE_URL", "").strip()
    model = os.environ.get("MUSIC_VIDEO_LLM_MODEL", "").strip()
    settings_path = Path(
        os.environ.get(
            "MUSIC_VIDEO_LLM_SETTINGS_FILE",
            str(Path.home() / ".claude" / "settings.json"),
        )
    ).expanduser()

    if settings_path.exists() and (not token or not base_url or not model):
        with settings_path.open("r", encoding="utf-8") as handle:
            settings_env = json.load(handle).get("env", {})
        token = token or str(settings_env.get("ANTHROPIC_AUTH_TOKEN", "")).strip()
        base_url = base_url or str(settings_env.get("ANTHROPIC_BASE_URL", "")).strip()
        model = model or str(settings_env.get("ANTHROPIC_DEFAULT_HAIKU_MODEL", "")).strip()

    if not token:
        raise RuntimeError("GLM authentication is not configured")

    return {
        "token": token,
        "url": f"{(base_url or 'http://127.0.0.1:8788').rstrip('/')}/v1/messages",
        "model": model or "glm-4.7",
    }


def translate_shots(source_language, shots):
    config = load_llm_config()
    language_names = {"ko": "Korean", "en": "English", "vi": "Vietnamese"}
    source_json = json.dumps(shots, ensure_ascii=False)
    prompt = f"""
Translate this travel music-video shot list from {language_names[source_language]} into Korean,
English, and Vietnamese. Keep the meaning natural for a couple filming in Japan. Preserve place
names, product names, reservation codes, numbers, camera modes, fps, and established filmmaking
terms. Each shot must remain a five-string array: [shot title, filming direction, technique,
edit length and beat, connection to the next shot]. Translate all five fields naturally.
Keep exactly {len(shots)} shots in the same order. The {source_language} array must be identical to
the input. Return JSON only with exactly these keys: ko, en, vi.

Input:
{source_json}
""".strip()
    request_body = json.dumps(
        {
            "model": config["model"],
            "system": "You are a precise multilingual film-production translator. Output valid JSON only.",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 6000,
            "temperature": 0.1,
        },
        ensure_ascii=False,
    ).encode("utf-8")
    request = urllib.request.Request(
        config["url"],
        data=request_body,
        headers={
            "x-api-key": config["token"],
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            api_payload = json.load(response)
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as error:
        raise RuntimeError("GLM translation request failed") from error

    blocks = api_payload.get("content", [])
    response_text = "".join(
        block.get("text", "")
        for block in blocks
        if isinstance(block, dict) and block.get("type") == "text"
    ).strip()
    if response_text.startswith("```"):
        response_text = response_text.strip("`").removeprefix("json").strip()
    try:
        translated_payload = json.loads(response_text)
    except json.JSONDecodeError:
        start = response_text.find("{")
        end = response_text.rfind("}")
        if start < 0 or end <= start:
            raise RuntimeError("GLM returned invalid translation JSON")
        try:
            translated_payload = json.loads(response_text[start : end + 1])
        except json.JSONDecodeError as error:
            raise RuntimeError("GLM returned invalid translation JSON") from error

    if not isinstance(translated_payload, dict):
        raise RuntimeError("GLM returned an invalid translation object")

    translations = {}
    for language in LANGUAGE_ORDER:
        candidate = shots if language == source_language else translated_payload.get(language)
        cleaned = validate_shots(candidate)
        if len(cleaned) != len(shots):
            raise RuntimeError("GLM changed the number of shots")
        translations[language] = cleaned
    return translations


def save_and_push(day_id, translations):
    pull = run_git("pull", "--rebase", "origin", "main")
    if pull.returncode != 0:
        raise RuntimeError("Git sync failed before saving")

    content = load_content()
    overrides = content.setdefault("overrides", {})
    for language in LANGUAGE_ORDER:
        overrides.setdefault(language, {})[day_id] = {"shots": translations[language]}
    content["updatedAt"] = datetime.now(timezone.utc).isoformat()

    temporary_path = CONTENT_PATH.with_suffix(".json.tmp")
    with temporary_path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(content, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    os.replace(temporary_path, CONTENT_PATH)

    add = run_git("add", "--", CONTENT_PATH.name)
    if add.returncode != 0:
        raise RuntimeError("Git staging failed")

    diff = run_git("diff", "--cached", "--quiet", "--", CONTENT_PATH.name)
    if diff.returncode == 0:
        return content, current_commit()

    message = f"Update {day_id} multilingual shooting plan"
    commit = run_git("commit", "-m", message, "--", CONTENT_PATH.name)
    if commit.returncode != 0:
        raise RuntimeError("Git commit failed")

    push = run_git("push", "origin", "main")
    if push.returncode != 0:
        raise RuntimeError("Git push failed after committing")

    return content, current_commit()


class MusicVideoHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def end_headers(self):
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "strict-origin-when-cross-origin")
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, format_string, *args):
        if sys.stderr is None:
            return
        try:
            super().log_message(format_string, *args)
        except (AttributeError, OSError):
            pass

    def send_json(self, status, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/api/content":
            self.send_json(
                HTTPStatus.OK,
                {"content": load_content(), "commit": current_commit()},
            )
            return
        if path == "/api/health":
            try:
                llm_model = load_llm_config()["model"]
            except Exception:
                llm_model = None
            self.send_json(
                HTTPStatus.OK,
                {
                    "ok": True,
                    "git": (ROOT / ".git").exists(),
                    "translation": bool(llm_model),
                    "translationModel": llm_model,
                },
            )
            return
        if any(part.startswith(".") for part in Path(unquote(path)).parts):
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        super().do_GET()

    def do_POST(self):
        if urlparse(self.path).path != "/api/content":
            self.send_error(HTTPStatus.NOT_FOUND)
            return

        expected_token = os.environ.get("MUSIC_VIDEO_EDITOR_TOKEN", "")
        provided_token = self.headers.get("X-Editor-Token", "")
        if not expected_token:
            self.send_json(HTTPStatus.SERVICE_UNAVAILABLE, {"error": "Editing is not configured"})
            return
        if not provided_token or not hmac.compare_digest(provided_token, expected_token):
            self.send_json(HTTPStatus.UNAUTHORIZED, {"error": "Invalid editor key"})
            return

        try:
            content_length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            content_length = 0
        if content_length <= 0 or content_length > 1_000_000:
            self.send_json(HTTPStatus.BAD_REQUEST, {"error": "Invalid request size"})
            return

        try:
            payload = json.loads(self.rfile.read(content_length).decode("utf-8"))
            language, day_id, shots = validate_update(payload)
            with WRITE_LOCK:
                translations = translate_shots(language, shots)
                content, commit = save_and_push(day_id, translations)
            self.send_json(
                HTTPStatus.OK,
                {
                    "ok": True,
                    "content": content,
                    "commit": commit,
                    "translatedLanguages": list(LANGUAGE_ORDER),
                },
            )
        except (json.JSONDecodeError, UnicodeDecodeError, ValueError) as error:
            self.send_json(HTTPStatus.BAD_REQUEST, {"error": str(error)})
        except Exception as error:
            if sys.stderr is not None:
                print(f"Save error: {error}", file=sys.stderr, flush=True)
            self.send_json(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                {"error": "The edit could not be committed to Git"},
            )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8020)
    parser.add_argument("--bind", default="0.0.0.0")
    args = parser.parse_args()
    server = ThreadingHTTPServer((args.bind, args.port), MusicVideoHandler)
    if sys.stdout is not None:
        print(f"Music video editor listening on {args.bind}:{args.port}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
