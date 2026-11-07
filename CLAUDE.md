# class-games 작업 규칙 (Claude용)

예술고 통합과학·생명과학 수업용 웹 게임 모음. 사용자는 이 학교 교사(k4366941@gmail.com).

## 말하기
- 항상 한국어, 짧은 문장. 영어로 답하지 않는다.
- 과학 개념·수치에는 근거를 붙이고 [사실]/[추측]/[의견] + 확신도(높음/중간/낮음)를 표시한다.
- 계획·초안에는 빠진 점·위험부터 짚고, 대안 2~3개와 추천안을 낸다.
- 고친 것이 있으면 끝에 "자체 점검: ..." 한 줄.

## 구조
- `common/` 모든 게임이 같이 쓰는 것: `config.js`(Firebase 설정), `net.js`(통신), `style.css`.
- `_template/` 새 게임 뼈대(학생 `index.html`, 교사 `teacher.html`, `game.js`).
- `<게임이름>/` 게임마다 폴더 하나. 데이터는 Firebase `games/<게임이름>/rooms/<방 코드>/` 아래에만.
- `games.json` 첫 화면 게임 목록.
- earth-escape(과학실의 그림자)는 별도 저장소 `kwker0406/earth-escape`. 데이터 경로 `sessions`·`classes`·`codes`.

## 새 게임
1. `python3 tools/new_game.py <영어이름> "<화면 이름>" <과목>`
2. `<영어이름>/game.js`와 화면을 고친다. Firebase는 `../common/net.js`로만 쓴다.
3. 데이터 구역이 더 필요하면 `database.rules.json`의 `games` 아래에 추가한다.

## 꼭 지킬 것
- `common/config.js`는 바꾸지 않는다(실제 Firebase 설정).
- `database.rules.json`은 Firebase 규칙 전체다. 이 저장소만 규칙을 배포한다. `sessions`·`classes`·`codes`(earth-escape) 구역을 지우거나 바꾸면 그 게임이 멈춘다.
- 서비스 계정 열쇠는 GitHub Secrets `FIREBASE_SERVICE_ACCOUNT`에만 있다. 파일로 만들거나 채팅으로 받지 않는다.
- 학생이 입력한 글(닉네임 등)은 `textContent`로만 화면에 넣는다(innerHTML 금지).
- 저작권 캐릭터·음악을 쓰지 않는다. 그림·소리는 직접 만든다.

## 시험과 배포
- 시험: `python3 test/smoke.py` (Playwright + 가짜 Firebase. 보안 규칙은 시험하지 않음).
- 시험 통과 → main에 push → GitHub Pages가 1~2분 안에 반영.
- 규칙 파일이 바뀌면 Actions "Firebase 규칙 배포"가 자동 실행. 결과는 `gh run list -R kwker0406/class-games`로 확인.
- 주소: https://kwker0406.github.io/class-games/<게임이름>/ (교사: .../teacher.html)
