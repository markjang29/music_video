# AWS Claude 작업 지시서

상태: 배포 인계 준비

## 목표

GitHub `markjang29/music_video`의 최신 `main`을 AWS에 배포해 `http://13.125.131.126:8020`에서 촬영 목록 편집, GLM 3개 언어 자동 번역, Git 커밋·푸시가 실제로 동작하게 한다.

서비스 범위는 공인 IP의 HTTP `8020`이다. HTTPS, 도메인, 인증서, Nginx/Caddy 같은 리버스 프록시는 추가하지 않는다.

## 먼저 읽을 파일

1. `AGENTS.md`
2. `REFERENCE.md`
3. `server.py`
4. `content.json`
5. `app.js`의 `localizeDay`, `saveShotEdits`, `loadRemoteContent`

## 현재 구현

- 촬영 목록 추가, 삭제, 순서 변경, 제목·촬영법·기법·사용 길이/박자·다음 컷 연결법 수정 대화상자
- 인트로부터 아웃트로까지 날짜별 역할과 컷 A에서 컷 B로 넘어가는 화면/소리 연결을 보여주는 MV 러프컷
- 날짜별·언어별 사용자 수정값을 `content.json`에서 읽는 구조
- 서버 편집 키 검증 후 `content.json`만 커밋·푸시하는 API
- 현재 편집 언어를 원문으로 보존하고 GLM이 한국어·영어·베트남어를 함께 생성하는 저장 흐름
- 일반 카메라에도 적용되는 촬영 기법과 X2 설정 참고
- 이동, 디테일, 전환, 감정별 고정 B-roll 영감 사진 보드
- 15초 몽타주, 매치 컷, 프로포즈 빌드업, 사운드 연결 편집 레시피

`content.json`에 저장되는 촬영 항목 스키마는 5개 문자열 배열이다: `[제목, 촬영법, 촬영 기법, 사용할 길이와 박자, 다음 컷 연결]`. 이전 3개 필드 구조로 축소하지 않는다.

## AWS 작업 범위

1. 에이전트 운영 레지스트리의 `aws-manager.repo_ids`에 `music_video`가 없으면, 이사님의 텔레그램 직접 지시에 포함된 범위 추가 승인을 근거로 먼저 등록한다. Notes에 다른 미커밋 변경이 있으면 함께 커밋하지 않는다.
2. 최신 `origin/main`을 별도 Git 작업 디렉터리에 clone 또는 pull한다. 기존 정적 배포 디렉터리는 검증 전까지 보존한다.
3. 원격 `origin`이 GitHub에 push 가능한 인증 경로인지 확인한다. 비밀값을 remote URL에 넣지 않는다.
4. 기존 AWS Claude용 로컬 `zai-proxy`와 Claude 설정을 재사용한다. 새 GLM 키를 만들거나 기존 토큰을 복사해 저장소에 넣지 않는다.
5. 무작위 편집 키를 생성해 Git 밖의 전용 환경 파일에 저장하고 권한을 `600`으로 둔다.
6. systemd `music-video.service`가 Git 작업 디렉터리에서 `python3 server.py --port 8020`을 실행하도록 바꾼다.
7. 서비스 재시작 후 정적 화면, `/api/content`, `/api/health`를 확인한다.
8. 격리된 임시 Git 저장소나 되돌릴 수 있는 테스트 데이터로 GLM 번역과 commit/push 경로를 검증한다. 사용자 촬영 계획을 테스트 문구로 오염시키지 않는다.
9. 모바일 390px와 데스크톱 화면에서 KO/EN/VI 전체 번역, 촬영 편집, 영감 보드, 여행 링크를 확인한다.
10. 편집 키는 이사님 텔레그램 개인 대화로 한 번 전달하고 Git, 로그, 작업 결과에는 적지 않는다.

## 런타임 설정

- `MUSIC_VIDEO_EDITOR_TOKEN`: 브라우저 편집 인증용 무작위 값
- `MUSIC_VIDEO_LLM_SETTINGS_FILE`: 필요할 때만 기존 Claude 설정 파일을 가리킨다. 기본값으로도 AWS의 표준 Claude 설정을 찾는다.
- `MUSIC_VIDEO_LLM_BASE_URL`: 기본 AWS 로컬 프록시와 다를 때만 지정한다.
- `MUSIC_VIDEO_LLM_MODEL`: 기본 모델과 다를 때만 지정한다.
- Git SSH 키를 사용할 경우 `MUSIC_VIDEO_GIT_SSH_KEY`에 GitHub write 권한이 있는 전용 키 경로를 지정한다.

## 완료 기준

- `http://13.125.131.126:8020`이 200으로 응답한다.
- `/api/health`가 `ok=true`, `git=true`, `translation=true`와 실제 GLM 모델을 반환한다.
- 한 언어에서 촬영 목록을 수정하면 응답에 `ko`, `en`, `vi`가 같은 항목 수로 저장된다.
- 언어를 바꾸면 방금 수정한 촬영 목록도 번역되어 보인다.
- 서버가 만든 `content.json` 커밋이 GitHub `main`에 존재한다.
- `.git`, 환경 파일, 키와 토큰이 HTTP나 Git에서 노출되지 않는다.
- 서비스 재시작 뒤에도 앱과 편집 기능이 유지된다.

## 금지 사항

- 비밀값을 문서, Git, systemd unit 본문, 명령 출력이나 텔레그램 단체방에 남기지 않는다.
- 사용자 일정·예약 정보·촬영 원안을 테스트 편의상 삭제하거나 축약하지 않는다.
- GLM 번역 실패 시 현재 언어만 부분 저장하지 않는다.
- 검증 전에 기존 8020 서비스를 제거하지 않는다.

## 결과 보고

한국어로 다음만 간단히 보고한다: 배포한 전체 Git commit, 서비스 상태, `/api/health` 공개 필드, 실행한 검증, 실제 Git push 증거, 남은 위험. 편집 키는 별도의 이사님 개인 텔레그램 메시지로만 전달한다.
