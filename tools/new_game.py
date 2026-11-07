"""새 게임 폴더 만들기. 사용: python3 tools/new_game.py 영어이름 "화면 이름" [과목]
예) python3 tools/new_game.py cell-quiz "세포 퀴즈 대결" 생명과학
_template을 복사하고 __GAME__·__NAME__을 바꾼 뒤 games.json에 한 줄 추가한다."""
import sys, re, json, shutil, pathlib

root = pathlib.Path(__file__).resolve().parent.parent
gid, name = sys.argv[1], sys.argv[2]
subject = sys.argv[3] if len(sys.argv) > 3 else "통합과학"
# Firebase 주소에 못 쓰는 글자(. # $ [ ] /)가 섞이지 않게 영어 소문자·숫자·- 만
if not re.fullmatch(r"[a-z0-9][a-z0-9-]{1,30}", gid): sys.exit("영어 이름은 소문자·숫자·- 만 (2~31자)")
dst = root / gid
if dst.exists() or gid in {"common", "tools", "test"}: sys.exit(f"{gid} 는 이미 있거나 쓸 수 없는 이름")
shutil.copytree(root / "_template", dst)
for f in dst.rglob("*"):
    if f.suffix in {".html", ".js"}:
        f.write_text(f.read_text().replace("__GAME__", gid).replace("__NAME__", name))
games = json.loads((root / "games.json").read_text())
games.append({"id": gid, "name": name, "subject": subject})
(root / "games.json").write_text(json.dumps(games, ensure_ascii=False, indent=2) + "\n")
print(f"만듦: {gid}/  →  https://kwker0406.github.io/class-games/{gid}/")
