"""모든 게임 기본 시험(가짜 Firebase). 실행: python3 test/smoke.py [게임폴더 ...]  (없으면 _template + games.json의 게임 전부)
선생님 로그인 → 방 만들기 → 학생 3명 입장 → 시작 → 정답 1개 → 점수 반영 → 끝내기. 페이지 오류가 하나라도 나면 실패."""
import sys, pathlib, json
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import fakeserver as fs
from playwright.sync_api import sync_playwright

games = sys.argv[1:] or ["_template"] + [g["id"] for g in json.loads((fs.root / "games.json").read_text()) if not g.get("url")]
fails = []
with sync_playwright() as p:
    b = p.chromium.launch()
    for g in games:
        errors = []
        ctx = b.new_context()
        ctx.route("https://www.gstatic.com/firebasejs/**", lambda r: r.fulfill(body=fs.fake, content_type="text/javascript"))
        def page():
            pg = ctx.new_page(); pg.on("pageerror", lambda e: errors.append(str(e))); return pg
        try:
            t = page(); t.goto(f"{fs.URL}{g}/teacher.html"); t.click("#loginBtn"); t.wait_for_selector("#main:not(.hidden)")
            t.click("#newRoom"); t.wait_for_function("document.getElementById('code').textContent.length === 4")
            code = t.inner_text("#code")
            # 없는 코드는 막히는지
            s0 = page(); s0.goto(f"{fs.URL}{g}/"); s0.fill("#code", "ZZZZ"); s0.fill("#nick", "없음"); s0.click("#go")
            s0.wait_for_function("document.getElementById('msg').textContent.length > 0"); s0.close()
            ss = []
            for i in range(3):   # 학생마다 다른 uid가 되도록 창마다 새 sessionStorage(새 context)
                c2 = b.new_context(); c2.route("https://www.gstatic.com/firebasejs/**", lambda r: r.fulfill(body=fs.fake, content_type="text/javascript"))
                s = c2.new_page(); s.on("pageerror", lambda e: errors.append(str(e)))
                s.goto(f"{fs.URL}{g}/"); s.fill("#code", code.lower()); s.fill("#nick", f"학생{i}"); s.click("#go")
                s.wait_for_selector("#wait:not(.hidden)"); ss.append((c2, s))
            t.wait_for_function("document.getElementById('count').textContent === '3'", timeout=10000)
            t.click("#start")
            s = ss[0][1]; s.wait_for_selector("#play:not(.hidden)")
            if g == "_template":   # 예시 1번 문제의 정답(100 °C) → 교사 화면 점수 1
                s.click("#choices button >> nth=2")
                t.wait_for_function("[...document.querySelectorAll('#players b')].some(b => b.textContent === '1')", timeout=10000)
            if g == "science-dial":   # 출제 → 단서 고르기 → 가리기 → 바늘 확정 → 해설 → 다음 라운드
                s.click("#peek"); s.click("#hand button >> nth=0"); s.click("#toTeam")
                s.click("#plus"); s.click("#lock"); s.wait_for_selector("#reveal:not(.hidden)")
                assert s.inner_text("#gain").startswith("+"), "점수 표시 없음"
                s.click("#next"); s.wait_for_selector("#pass:not(.hidden)")
                assert s.inner_text("#round") == "2", "라운드가 넘어가지 않음"
            t.click("#stop"); s.wait_for_selector("#end:not(.hidden)")
            for c2, _ in ss: c2.close()
            if errors: raise RuntimeError("페이지 오류: " + "; ".join(errors[:3]))
            print("통과:", g)
        except Exception as e:
            fails.append(g); print("실패:", g, "→", str(e).splitlines()[0])
        ctx.close()
    b.close()
fs.srv.shutdown()
sys.exit(1 if fails else 0)
