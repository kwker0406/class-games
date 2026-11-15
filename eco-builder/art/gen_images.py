"""제미나이 이미지 생성(나노 바나나)으로 카드 그림 만들기 — 선생님 컴퓨터에서 실행.
키는 이 파일에 적지 말고 터미널 환경 변수로만 넣는다(파일·채팅에 키가 남지 않게).

  export GEMINI_API_KEY="여기에_키"
  python3 gen_images.py              # 53장 전부(이미 있는 파일은 건너뜀)
  python3 gen_images.py 4-4 4-0 2-0  # 몇 장만(범고래·매·꿀벌)

결과: 같은 폴더의 images/<카드 번호>.png. 추가 설치 없이 파이썬 기본 기능만 씀.
"""
import base64, json, os, re, sys, time, urllib.request, urllib.error

MODEL = os.environ.get("GEMINI_IMAGE_MODEL", "gemini-2.5-flash-image")   # 모델 이름이 바뀌었으면 환경 변수로 바꿔 넣기
KEY = os.environ.get("GEMINI_API_KEY") or sys.exit("GEMINI_API_KEY 환경 변수를 먼저 넣으세요.")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "images")
os.makedirs(OUT, exist_ok=True)

# prompts.md에서 (카드 번호, 이름, 프롬프트) 읽기
md = open(os.path.join(HERE, "prompts.md"), encoding="utf-8").read()
items = re.findall(r"## (.+?) · 파일 `(.+?)\.png`\n\n```\n(.+?)\n```", md, re.S)
want = set(sys.argv[1:])
todo = [(fid, name, p) for name, fid, p in items if (not want or fid in want)]
if want - {fid for fid, _, _ in todo}: sys.exit(f"없는 카드 번호: {sorted(want - {f for f, _, _ in todo})}")

def generate(prompt):
    body = json.dumps({"contents": [{"parts": [{"text": prompt}]}],
                       "generationConfig": {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": "1:1"}}}).encode()
    req = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent",
                                 data=body, headers={"Content-Type": "application/json", "x-goog-api-key": KEY})
    with urllib.request.urlopen(req, timeout=120) as r:
        res = json.load(r)
    for part in res.get("candidates", [{}])[0].get("content", {}).get("parts", []):
        if "inlineData" in part: return base64.b64decode(part["inlineData"]["data"])
    raise RuntimeError("그림이 오지 않음: " + json.dumps(res, ensure_ascii=False)[:300])

ok = fail = 0
for fid, name, prompt in todo:
    path = os.path.join(OUT, f"{fid}.png")
    if os.path.exists(path) and not want: print(f"건너뜀  {fid} {name} (이미 있음)"); continue
    for attempt in range(3):   # 일시 오류·사용량 제한이면 잠깐 쉬고 다시
        try:
            open(path, "wb").write(generate(prompt)); print(f"완료    {fid} {name}"); ok += 1; break
        except urllib.error.HTTPError as e:
            msg = e.read().decode(errors="ignore")[:200]
            if e.code in (429, 500, 503) and attempt < 2: time.sleep(20 * (attempt + 1)); continue
            print(f"실패    {fid} {name}: HTTP {e.code} {msg}"); fail += 1; break
        except Exception as e:
            print(f"실패    {fid} {name}: {e}"); fail += 1; break
print(f"\n완료 {ok}장, 실패 {fail}장 → {OUT}")
