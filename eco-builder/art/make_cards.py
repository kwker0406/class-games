"""라인 아트 카드 만들기: python3 make_cards.py → cards/<id>.svg
그림(ART)은 100×100 칸 안에 선으로만 그림. 카드 틀(위: 점수·할인 요소, 아래: 이름)은 frame()이 붙임."""
import math, os, json
INK = "#23262d"
L = f'fill="none" stroke="{INK}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"'
T = f'fill="none" stroke="{INK}" stroke-width="1" stroke-linecap="round" stroke-linejoin="round"'    # 가는 선(결·음영)
W = f'fill="#fff" stroke="{INK}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"'  # 겹친 선 가리기

# ---------- 비생물요소 아이콘(선) ----------
def ficon(f, x, y, r=7):
    if f == "L": return f'<circle cx="{x}" cy="{y}" r="{r*0.45}" {L}/>' + "".join(
        f'<path d="M{x+r*0.7*math.cos(a):.1f} {y+r*0.7*math.sin(a):.1f}L{x+r*math.cos(a):.1f} {y+r*math.sin(a):.1f}" {L}/>' for a in [i*math.pi/4 for i in range(8)])
    if f == "W": return f'<path d="M{x} {y-r} Q{x+r*0.8} {y+r*0.1} {x+r*0.6} {y+r*0.45} A{r*0.62} {r*0.62} 0 0 1 {x-r*0.6} {y+r*0.45} Q{x-r*0.8} {y+r*0.1} {x} {y-r}Z" {L}/>'
    if f == "T": return f'<path d="M{x-r*0.22} {y+r*0.35}V{y-r*0.75}a{r*0.22} {r*0.22} 0 0 1 {r*0.44} 0V{y+r*0.35}" {L}/><circle cx="{x}" cy="{y+r*0.62}" r="{r*0.38}" {L}/><path d="M{x} {y+r*0.5}V{y-r*0.3}" {L}/>'
    if f == "S": return "".join(f'<path d="M{x-r} {y+d}Q{x-r/2} {y+d-2} {x} {y+d}T{x+r} {y+d}" {L}/>' for d in (-r*0.55, 0, r*0.55))
    if f == "A": return "".join(f'<path d="M{x-r} {y+d}H{x+r*0.4}a{r*0.3} {r*0.3} 0 1 0 -{r*0.3} -{r*0.3}" {L}/>' for d in (-r*0.35, r*0.35))
FN = {"L": "빛", "W": "물", "T": "온도", "S": "토양", "A": "공기"}
TIERC = {1: "#4f8a3c", 2: "#b97a12", 3: "#b44a24", 4: "#6a2f80", 0: "#2d5b8a"}

def frame(art, name, pts, f, tier, sub=""):
    c = TIERC[tier]
    head = (f'<text x="12" y="20" font-size="15" font-weight="800" fill="{c}" font-family="sans-serif">{pts if pts else ""}</text>'
            if tier else f'<text x="12" y="20" font-size="15" font-weight="800" fill="{c}" font-family="sans-serif">3</text>')
    disc = (f'<circle cx="88" cy="14" r="9.5" fill="#fff" stroke="{c}" stroke-width="1.4"/>{ficon(f, 88, 14, 6.2)}' if f else sub)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 140">'
            f'<rect x="1" y="1" width="98" height="138" rx="7" fill="#fbfaf6" stroke="{c}" stroke-width="2"/>'
            f'<path d="M1 26H99" stroke="{c}" stroke-width="1"/>{head}{disc}'
            f'<g transform="translate(0 28)">{art}</g>'
            f'<path d="M1 122H99" stroke="{c}" stroke-width="1"/>'
            f'<text x="50" y="135" text-anchor="middle" font-size="11" font-weight="700" fill="{INK}" font-family="sans-serif">{name}</text></svg>')

A = {}
# ---------- 1줄: 해바라기 ----------
pet = "".join(f'<path d="M50 40 Q{50+10*math.cos(a-0.25):.1f} {40+10*math.sin(a-0.25):.1f} {50+22*math.cos(a):.1f} {40+22*math.sin(a):.1f} Q{50+10*math.cos(a+0.25):.1f} {40+10*math.sin(a+0.25):.1f} 50 40Z" {W}/>'
              for a in [i*math.pi/7 for i in range(14)])
seeds = "".join(f'<circle cx="{50+r*math.cos(t):.1f}" cy="{40+r*math.sin(t):.1f}" r="0.7" fill="{INK}"/>' for k in range(60) for r, t in [(math.sqrt(k)*1.25, k*2.4)])
A["sunflower"] = (f'<path d="M50 52 Q48 72 51 94" {L}/><path d="M50 74 Q66 62 78 70 Q66 82 50 74Z" {W}/><path d="M52 74 Q64 70 74 70" {T}/>'
                  f'<path d="M50 82 Q34 72 22 80 Q36 90 50 82Z" {W}/><path d="M48 82 Q36 79 26 80" {T}/>{pet}<circle cx="50" cy="40" r="11" {W}/>{seeds}')
# ---------- 2줄: 꿀벌(옆모습) ----------
A["bee"] = (f'<path d="M50 40 Q40 12 22 16 Q24 34 50 40Z" {W}/><path d="M50 40 Q32 22 26 20 M44 34 Q34 26 28 26" {T}/>'
            f'<path d="M54 40 Q60 10 78 12 Q78 32 54 40Z" {W}/><path d="M56 38 Q66 22 74 16" {T}/>'
            f'<ellipse cx="66" cy="56" rx="20" ry="14" {W}/><path d="M60 43 Q56 56 60 69 M70 42 Q66 56 70 70 M79 46 Q76 56 79 66" {L}/><path d="M86 56 L93 58 L86 60" {L}/>'
            f'<ellipse cx="44" cy="52" rx="10" ry="9" {W}/><path d="M38 48 Q44 46 49 49" {T}/>'
            f'<circle cx="28" cy="50" r="8" {W}/><ellipse cx="26" cy="48" rx="2.6" ry="3.6" {L}/><path d="M23 43 Q16 32 10 30 M27 42 Q24 30 20 26" {L}/>'
            f'<path d="M40 60 L34 74 L30 76 M46 61 L44 76 L40 80 M52 62 L56 76 L60 80" {L}/>')
# ---------- 3줄: 개구리 ----------
A["frog"] = (f'<path d="M14 84 Q20 52 50 50 Q80 52 86 84 Q70 92 50 92 Q30 92 14 84Z" {W}/>'
             f'<path d="M20 78 Q8 74 10 88 Q22 92 30 88" {W}/><path d="M80 78 Q92 74 90 88 Q78 92 70 88" {W}/>'
             f'<path d="M30 70 Q36 60 50 60 Q64 60 70 70" {T}/>'
             f'<circle cx="34" cy="46" r="10" {W}/><circle cx="66" cy="46" r="10" {W}/><ellipse cx="34" cy="47" rx="5" ry="3" fill="{INK}"/><ellipse cx="66" cy="47" rx="5" ry="3" fill="{INK}"/>'
             f'<path d="M24 60 Q50 72 76 60" {L}/><path d="M38 84 L32 94 M38 84 L38 95 M38 84 L44 94 M62 84 L56 94 M62 84 L62 95 M62 84 L68 94" {L}/>'
             + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" {T}/>' for x, y, r in [(44, 76, 2.2), (58, 79, 1.8), (28, 80, 1.6), (72, 74, 2), (50, 84, 1.4)]))
# ---------- 4줄: 범고래(비스듬히 솟구치는 옆모습) ----------
A["orca"] = (f'<path d="M2 90 Q14 84 26 90 T50 90 T74 90 T98 90" {L}/><path d="M8 96 Q20 92 32 96 T58 96 T86 96" {T}/>'
             f'<path d="M86 22 Q90 26 88 32 Q80 46 60 58 Q42 68 26 74 Q16 78 12 84 Q8 78 4 80 Q6 72 12 70 Q6 66 2 60 Q10 60 16 66 Q26 58 34 52 Q44 42 52 36 L46 8 Q58 18 62 30 Q72 22 86 22Z" {W}/>'
             f'<path d="M64 40 Q72 34 80 34 Q76 42 66 44Z" {L}/><circle cx="83" cy="30" r="1.4" fill="{INK}"/>'
             f'<path d="M86 32 Q76 50 58 62 Q44 70 30 74" {T}/><path d="M56 42 Q50 46 46 44" {T}/>'
             f'<path d="M46 50 Q40 58 30 62 M58 50 Q52 58 44 62" {T}/>'
             f'<path d="M20 82 l-6 8 M28 80 l-2 10 M88 40 l8 -4 M90 46 l8 0 M84 52 l6 4" {T}/>')
# ---------- 4줄: 매(날개를 활짝 편 앞모습) ----------
def wing(side):
    sx = -1 if side == "L" else 1
    X = lambda x: 50 + sx * x
    tips = "".join(f" L{X(46 - k*5.5):.1f} {38 + k*4.5 + (3 if k % 2 else 0):.1f}" for k in range(8))
    return f'<path d="M{X(6)} 40 Q{X(24)} 22 {X(48)} 30{tips} L{X(6)} 60Z" {W}/>' + "".join(
        f'<path d="M{X(10 + k*5)} {42 + k*0.5} L{X(44 - k*5.5 + 2)} {38 + k*4.5}" {T}/>' for k in range(5))
A["falcon"] = (wing("L") + wing("R") +
               f'<path d="M42 70 L36 92 Q50 98 64 92 L58 70Z" {W}/><path d="M46 74 L44 92 M50 74 V94 M54 74 L56 92" {T}/>'
               f'<path d="M40 44 Q40 30 50 28 Q60 30 60 44 Q62 66 50 76 Q38 66 40 44Z" {W}/>'
               + "".join(f'<path d="M{44+i*3} {48+j*6} q1.5 2 3 0" {T}/>' for i in range(4) for j in range(4)) +
               f'<path d="M42 22 Q42 10 50 10 Q58 10 58 22 Q56 30 50 30 Q44 30 42 22Z" {W}/>'
               f'<path d="M45 17 Q44 24 46 28 M55 17 Q56 24 54 28" {L}/>'
               f'<circle cx="46.5" cy="17" r="1.6" fill="{INK}"/><circle cx="53.5" cy="17" r="1.6" fill="{INK}"/>'
               f'<path d="M48 21 Q50 20 52 21 L50 26Z" fill="{INK}"/>'
               f'<path d="M44 70 L42 78 M56 70 L58 78 M42 78 l-3 2 M42 78 l0 3 M58 78 l3 2 M58 78 l0 3" {L}/>')
# ---------- 보호종: 수달 ----------
A["otter"] = (f'<path d="M6 86 Q20 80 34 86 T62 86 T94 86" {L}/><path d="M60 84 Q80 70 96 76 Q90 84 74 88" {W}/>'
              f'<path d="M28 88 Q24 56 40 46 Q58 40 66 58 Q72 74 66 88" {W}/><path d="M38 60 Q44 70 42 84 M56 58 Q60 70 58 84" {T}/>'
              f'<path d="M30 40 Q28 18 46 16 Q64 18 62 40 Q60 52 46 54 Q32 52 30 40Z" {W}/>'
              f'<path d="M32 22 Q28 16 34 14 M60 22 Q64 16 58 14" {L}/>'
              f'<circle cx="40" cy="31" r="1.8" fill="{INK}"/><circle cx="52" cy="31" r="1.8" fill="{INK}"/>'
              f'<path d="M43 37 Q46 35 49 37 Q46 40 43 37Z" fill="{INK}"/><path d="M46 40 V43 M42 44 Q46 46 50 44" {T}/>'
              f'<path d="M40 40 L24 38 M40 42 L26 44 M52 40 L68 38 M52 42 L66 44" {T}/>'
              f'<path d="M36 58 Q32 66 38 68 M56 58 Q60 66 54 68" {L}/>')
