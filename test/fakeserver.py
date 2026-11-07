"""시험용 서버: 저장소 전체를 보여 주고 /__db 에 가짜 Firebase 데이터를 경로별로 저장(창끼리 덮어쓰지 않게).
earth-escape의 시험 도구를 그대로 가져옴. 보안 규칙은 흉내 내지 않는다."""
import pathlib, json, threading, functools
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
root = pathlib.Path(__file__).resolve().parent.parent
DB, LOCK = {}, threading.Lock()
def _at(o, p):
    for k in [k for k in p.split("/") if k]: o = o.get(k) if isinstance(o, dict) else None
    return o
def _put(p, v):
    global DB
    ks = [k for k in p.split("/") if k]
    if not ks: DB = v or {}; return
    o, chain = DB, []
    for k in ks[:-1]:
        if not isinstance(o.get(k), dict): o[k] = {}
        chain.append((o, k)); o = o[k]
    if v is None: o.pop(ks[-1], None)
    else: o[ks[-1]] = json.loads(json.dumps(v))
    for parent, k in reversed(chain):
        if parent[k] == {}: parent.pop(k)
class H(SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
    def _send(self, code=200):
        body = json.dumps(DB).encode(); self.send_response(code); self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "no-store"); self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)
    def do_GET(self):
        if self.path.startswith("/__db"):
            with LOCK: return self._send()
        return super().do_GET()
    def do_POST(self):
        b = json.loads(self.rfile.read(int(self.headers["Content-Length"])) or b"{}")
        with LOCK:
            if "replace" in b: _put("", b["replace"])
            elif "set" in b: _put(b["set"], b["v"])
            elif "update" in b:
                for k, v in b["obj"].items(): _put(b["update"] + "/" + k, v)
            elif "cas" in b:
                if json.dumps(_at(DB, b["cas"]), sort_keys=True) != json.dumps(json.loads(b["expect"]), sort_keys=True): return self._send(409)
                _put(b["cas"], b["v"])
            return self._send()
ThreadingHTTPServer.request_queue_size = 256
srv = ThreadingHTTPServer(("localhost", 8766), functools.partial(H, directory=str(root)))
srv.handle_error = lambda *a: None
threading.Thread(target=srv.serve_forever, daemon=True).start()
fake = (root / "test/fake-firebase.js").read_text()
URL = "http://localhost:8766/"
