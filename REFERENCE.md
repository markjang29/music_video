# 아로하 여행 MV 촬영 콜시트 참고서

## 이 웹앱이 하는 일

이 웹앱은 2026년 8월 9일부터 8월 15일까지의 후쿠오카·벳푸 여행 일정에 맞춰, 여자친구와의 결혼반지/프로포즈링 중심 아로하 뮤직비디오를 찍기 위한 촬영 콜시트입니다.

왼쪽의 접힌 날짜 레일에서 날짜를 선택하면 그날 필요한 촬영 컷을 먼저 볼 수 있습니다. `프로포즈와 반지 연출`은 별도 탭이 아니라 촬영 체크리스트 아래에 함께 표시됩니다. 촬영 완료 체크는 휴대폰 브라우저에 저장되므로 일본 현장에서 같은 브라우저로 다시 열면 이어서 사용할 수 있습니다.

촬영 탭 맨 위의 `오늘의 MV 러프컷`은 이 앱을 일반 여행 체크리스트가 아니라 뮤직비디오용으로 만드는 핵심입니다. 각 날짜를 인트로, 1절, 프리코러스, 메인 후렴, 2절, 브리지, 아웃트로로 나누고, 각 컷의 실제 사용 길이와 박자, 다음 컷으로 넘어가는 화면 동작이나 현장음을 표시합니다. 촬영한 순서와 상관없이 이 순서대로 CapCut 같은 편집 앱의 타임라인에 놓으면 됩니다.

## 일본에서 쓰는 법

1. 호텔에서 출발하기 전에 오늘 날짜를 열고 필수 컷 3개만 먼저 기억합니다.
2. 이동 중에는 Insta360 X2, 휴대폰, 빌린 카메라 중 손에 잡히는 장비로 5-8초짜리 짧은 영상을 남깁니다.
3. 식당, 공항, 역에서는 직원과 다른 손님 얼굴이 크게 나오지 않게 찍습니다.
4. 촬영 금지 표지가 있거나 직원이 제지하면 바로 멈춥니다.
5. 하루가 끝나면 완료한 컷을 체크하고, 부족한 컷은 다음날 비슷한 장소에서 보충합니다.

## 촬영 장비 기준

- 일반 여행 컷: X2는 360 모드 5.7K 30fps, 휴대폰은 기본 카메라의 4K 30fps를 우선합니다.
- 걷는 컷: FlowState 안정화를 믿고 천천히 움직입니다.
- 셀피스틱 위치: 두 사람 사이 또는 살짝 앞쪽, 얼굴보다 조금 높은 위치.
- 반지 클로즈업: X2만 믿지 말고 휴대폰으로 보조 촬영을 같이 남깁니다.
- 프로포즈 순간: X2는 고정 구도로 30초 이상 계속 촬영하고, 휴대폰은 손과 반지 클로즈업 담당으로 둡니다.
- 매일 확인: 배터리, 렌즈 청소, 메모리 여유, 셀피스틱 잠금, 방수 필요 여부.

X2 전용 촬영법만 고집할 필요는 없습니다. `참고` 탭의 촬영 기법 라이브러리에는 휩 팬, 포어그라운드 와이프, 패럴랙스 워크, 프레임 인 프레임, 매치 온 액션, J/L 컷, 사운드 브리지처럼 휴대폰이나 일반 카메라에도 적용되는 방법이 포함되어 있습니다.

## 촬영 목록 수정과 자동 번역

1. 원하는 날짜의 `촬영 편집`을 누릅니다.
2. 촬영 내용, 찍는 방법, 촬영 기법, 편집에 쓸 길이와 박자, 다음 컷 연결법을 수정하거나 항목을 추가·삭제·정렬합니다.
3. 서버 관리자가 텔레그램으로 전달한 편집 키를 입력합니다. 키는 현재 브라우저 탭에만 보관됩니다.
4. `번역 후 Git 저장`을 누르면 AWS의 GLM이 현재 언어를 기준으로 한국어·영어·베트남어 목록을 함께 만듭니다.
5. 세 언어의 항목 수와 형식 검증이 모두 끝나야 `content.json`이 한 번에 커밋되고 GitHub `main`에 푸시됩니다.

장소명, 예약번호, 시간, 카메라 모드와 fps는 번역 중에도 유지하도록 지시합니다. GLM 호출이나 Git push가 실패하면 일부 언어만 저장하지 않고 전체 저장을 취소합니다.

## B-roll 영감 보드와 편집 레시피

`참고` 탭의 `B-roll 영감 보드`에는 이동의 리듬, 여행 디테일, 장소 전환, 둘 사이의 순간 네 보드가 있습니다. 각 버튼을 누르면 고정된 사진 네 장과 그 구도에서 실제로 찍어 볼 행동이 함께 열립니다. 사진을 그대로 복제하기보다 빛, 거리, 화면 방향, 손동작을 골라 쓰는 용도입니다.

`짧은 영상 편집 레시피`는 CapCut 같은 편집 앱에 옮겨 담을 컷 순서를 제안합니다. 15초 비트 몽타주, 문 동작 매치 컷, 프로포즈 감정 빌드업, J/L 컷 사운드 연결을 먼저 제공하며 실제 영상 편집이나 렌더링 기능은 아닙니다.

날짜별로 더 구체적인 연결은 `촬영` 탭의 `오늘의 MV 러프컷`에서 봅니다. `캐리어가 화면을 가릴 때 다음 장소로`, `다음 장소의 소리를 0.5초 먼저`, `같은 손 위치로 다음 날 컷과 매치`처럼 현장에서 끝 동작까지 찍어야 편집 가능한 지시가 적혀 있습니다. `촬영 편집`에서 이 연결 지시도 직접 바꿀 수 있습니다.

## 촬영 용어 쉬운 설명

웹앱의 `참고` 탭에서는 아래 용어를 실제 사진 구도로 보여줍니다. 사진을 누르면 Unsplash 원본과 사진가 정보를 확인할 수 있습니다.

- B-roll: 분위기를 이어주는 보조 영상입니다. 공항 표지판, 버스 창밖, 라멘 김, 캐리어 바퀴처럼 주인공 얼굴이 없어도 되는 컷입니다.
- 와이드: 사람과 장소가 같이 보이는 넓은 화면입니다. 하카타역 앞에서 둘이 걸어가는 뒷모습처럼 장소 설명에 좋습니다.
- 클로즈업: 손, 표정, 반지처럼 중요한 대상을 크게 잡는 화면입니다.
- 인서트: 편집 중간에 끼워 넣는 짧은 디테일 컷입니다. 승차권, 호텔 키카드, 메뉴판, 반지 반짝임을 2-5초 찍으면 됩니다.
- 전환 컷: 장소나 시간이 바뀔 때 이어주는 컷입니다. 문 열기, 엘리베이터 거울, 기차 창밖, 숙소 복도 같은 장면입니다.
- 감정 컷: 정보보다 마음을 보여주는 컷입니다. 말없이 웃는 얼굴, 고백 직전 숨 고르는 손, 같이 바라보는 시선이 여기에 들어갑니다.
- 링 컷: 반지가 이야기의 중심으로 보이는 컷입니다. 반지 낀 손으로 선물을 들거나, 케이스가 살짝 보이는 장면입니다.

## 언어 전환

웹앱 오른쪽 위의 `KO`, `EN`, `VI` 버튼으로 메뉴, 날짜별 일정, 촬영 지시, 프로포즈 연출, 링크 이름, 참고 설명을 한국어, 영어, 베트남어로 바꿀 수 있습니다. 지도와 예약 링크 주소, 예약 번호, 시간, 편명은 언어를 바꿔도 유지됩니다.

## 촬영 예시 사진 출처

- B-roll: [Alison Marras / Unsplash](https://unsplash.com/photos/bowl-of-ramen-SdS_XZ2CBqo)
- 와이드: [CHUTTERSNAP / Unsplash](https://unsplash.com/photos/man-and-woman-crossing-on-street-3IA-U2zhIEA)
- 클로즈업: [Matt Seymour / Unsplash](https://unsplash.com/photos/a-womans-hand-with-a-diamond-ring-on-it-AKLXCQaDPRQ)
- 인서트: [CardMapr.nl / Unsplash](https://unsplash.com/photos/a-passport-and-a-boarding-pass-are-on-a-bag-LVA3S6isNYQ)
- 전환 컷: [Joao Estrella / Unsplash](https://unsplash.com/photos/hallway-of-a-hotel-leading-to-a-window-JZ6nWjQ_SSY)
- 감정 컷: [Luis Quintero / Unsplash](https://unsplash.com/photos/BVrCdFJ5guA)
- 링 컷: [Hoi An Photographer / Unsplash](https://unsplash.com/photos/OPk3ynqLToI)

## English Quick Guide

This web app is a shooting call sheet for an Aloha-style proposal travel music video in Fukuoka and Beppu.

Use it every morning before leaving the hotel. Open today’s date, remember the top three shots, and check them off at night. The checklist is saved in your phone browser.

For the Insta360 X2, shoot general travel clips in 360 mode at 5.7K 30fps. A phone or another camera is also fine for every non-360 technique. `Today's MV rough cut` shows clip length, music beats, and the visual or audio connection into the next shot. Use `Edit shots` to change all of those fields, then `Translate & save to Git`; GLM updates Korean, English, and Vietnamese together. The inspiration boards provide fixed visual references and short-form edit recipes.

## Hướng Dẫn Nhanh Tiếng Việt

Ứng dụng này là call sheet để quay MV du lịch cầu hôn phong cách Aloha tại Fukuoka và Beppu.

Mỗi sáng trước khi rời khách sạn, mở ngày hôm đó, ghi nhớ 3 cảnh quan trọng nhất và cuối ngày tick các cảnh đã quay. Checklist sẽ được lưu trong trình duyệt điện thoại.

Với Insta360 X2, hãy quay cảnh du lịch bằng chế độ 360 ở 5.7K 30fps. Điện thoại hoặc máy quay khác đều dùng được cho các kỹ thuật không cần 360. `Bản dựng nháp MV hôm nay` cho biết độ dài cảnh, nhịp nhạc và cách nối hình hoặc âm thanh sang cảnh tiếp theo. Dùng `Sửa cảnh quay` để đổi các trường này, sau đó `Dịch và lưu vào Git`; GLM sẽ cập nhật tiếng Hàn, Anh và Việt cùng lúc. Bảng cảm hứng cung cấp ảnh cố định và công thức dựng video ngắn.
