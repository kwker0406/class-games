# 수업 게임 모음

통합과학·생명과학 수업에서 쓰는 웹 게임을 모아 둔 저장소입니다.

- 첫 화면: https://kwker0406.github.io/class-games/
- 게임마다 폴더가 하나씩 있습니다. 학생은 `게임이름/`, 선생님은 `게임이름/teacher.html`로 들어갑니다.
- 새 게임은 Claude에게 "class-games에 새 게임 만들어 줘: 주제·과목·인원"이라고 요청하면 됩니다.

## 선생님이 알아 둘 것
- Firebase 규칙은 이 저장소의 `database.rules.json` 하나로 관리합니다. 과학실의 그림자(earth-escape) 규칙도 여기에 들어 있습니다.
- `common/config.js`는 Firebase 설정입니다. 고치지 마세요.
- 서비스 계정 열쇠는 GitHub Settings → Secrets에만 둡니다. 파일로 올리거나 채팅에 붙이지 마세요.
