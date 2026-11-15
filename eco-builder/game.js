// 생태계 짓기: 비생물요소 토큰을 모아 생물 카드를 사고, 그 생물이 적응한 비생물요소만큼 다음 카드가 싸진다.
// 4줄 = 생산자·분해자 / 1차 소비자 / 2차 소비자 / 3차·최상위 소비자. 보호종(천연기념물)은 조건을 채우면 찾아온다.
// 화면·통신 없이 규칙만 담은 순수 함수 모음(학생 화면, 교사 화면, 시뮬레이션이 같이 씀).
export const GAME = "eco-builder";   // Firebase 주소에 쓰는 영어 이름(바꾸면 기존 방 기록과 끊김)
export const NAME = "생태계 짓기";     // 화면에 보이는 이름
export const WIN = 15;               // 이 점수에 먼저 닿은 바퀴가 끝나면 게임 끝(원작과 같음)
export const MAX_ROUNDS = 18;        // 안전장치: 18바퀴에서 끝(sim.mjs: 한 사람당 평균 14.5차례 ≈ 25초×4명×14.5 ≈ 24분)
export const MAX_TOKENS = 10;        // 넘으면 차례 끝에 반납
export const MAX_RESERVE = 3;        // 찜한 카드는 3장까지
export const SUPPLY = { 2: 4, 3: 5, 4: 7 };   // 인원별 요소마다 토큰 수
export const JOKERS = 5;             // 만능 토큰(변이) 수

export const F = ["L", "W", "T", "S", "A"];
export const FACTOR = { L: ["빛", "☀️"], W: ["물", "💧"], T: ["온도", "🌡️"], S: ["토양", "🟫"], A: ["공기", "💨"], J: ["변이(만능)", "🧬"] };
export const TK = [...F, "J"];   // 손에 드는 토큰 종류(만능 포함)
// 카드 그림이 있는 카드(img/<id>.webp). 없으면 이모지로 보임
export const ART = new Set(["2-0", "4-0", "4-4"]);
export const TIER = { 1: "생산자·분해자", 2: "1차 소비자", 3: "2차 소비자", 4: "3차·최상위 소비자" };

// [이름, 그림, 적응한 비생물요소, 적응 설명]
const C = {
  1: [["해바라기", "🌻", "L", "어린 해바라기는 해를 따라 꽃봉오리 방향을 바꿈"], ["소나무", "🌲", "L", "강한 빛에서 잘 자라는 양지 식물"],
      ["고사리", "🌿", "L", "약한 빛에서도 광합성을 하는 음지 식물"], ["선인장", "🌵", "W", "잎이 가시로 변해 물 손실을 줄이고 줄기에 물을 저장"],
      ["부레옥잠", "🪷", "W", "잎자루의 공기주머니로 물에 떠서 삶"], ["검정말", "🌱", "W", "물속에 잠겨 사는 수생 식물"],
      ["은행나무", "🍂", "T", "기온이 내려가면 단풍이 들고 잎을 떨궈 겨울을 남"], ["보리", "🌾", "T", "겨울 추위를 겪어야 봄에 꽃이 핌"],
      ["자작나무", "🌳", "T", "추운 북쪽 지방에서 잘 자람"], ["버섯", "🍄", "S", "분해자: 죽은 생물을 분해해 무기 양분을 흙으로 돌려보냄"],
      ["곰팡이", "🧫", "S", "분해자: 유기물을 분해함"], ["세균", "🦠", "S", "분해자: 흙 속에서 유기물을 무기물로 분해"],
      ["식물성 플랑크톤", "🟢", "A", "바다에서 광합성으로 많은 산소를 만듦"], ["맹그로브", "🌴", "A", "물 위로 솟은 공기뿌리로 호흡"],
      ["연꽃", "🌸", "A", "잎자루와 뿌리줄기의 구멍으로 물속 뿌리에 공기를 보냄"]],
  2: [["꿀벌", "🐝", "L", "태양의 위치로 방향을 찾음"], ["닭", "🐔", "L", "낮의 길이가 길어지면 알을 더 많이 낳음"],
      ["양", "🐑", "L", "낮이 짧아지는 가을에 짝짓기를 함"], ["낙타", "🐫", "W", "물을 적게 잃고 오래 버팀"],
      ["캥거루쥐", "🐭", "W", "물을 거의 마시지 않고 먹이에서 물을 얻음"], ["달팽이", "🐌", "W", "건조하면 껍데기 입구를 막고 쉼"],
      ["다람쥐", "🐿️", "T", "추운 겨울에 겨울잠을 잠"], ["북극토끼", "🐇", "T", "귀가 작아 몸의 열을 덜 잃음"],
      ["순록", "🫎", "T", "두꺼운 털로 추위를 견딤"], ["지렁이", "🪱", "S", "흙을 먹으며 굴을 파 흙에 공기가 통하게 함"],
      ["쇠똥구리", "🪲", "S", "동물의 배설물을 먹고 땅에 묻어 흙을 기름지게 함"], ["흰개미", "🐜", "S", "죽은 나무를 먹고 흙 속에 집을 지음"],
      ["야크", "🐂", "A", "산소가 희박한 높은 산에서 큰 폐로 호흡"], ["올챙이", "🐸", "A", "아가미로 물속 산소를 얻음"],
      ["장구벌레", "🦟", "A", "숨관을 물 밖으로 내밀어 공기를 마심"]],
  3: [["올빼미", "🦉", "L", "큰 눈으로 약한 빛에서도 밤에 사냥"], ["박쥐", "🦇", "L", "빛이 없는 동굴에서 초음파로 먹이를 찾음"],
      ["개구리", "🐸", "W", "피부로도 호흡해 축축한 곳에서 삶"], ["물총새", "🐦", "W", "물속으로 뛰어들어 물고기를 잡음"],
      ["사막여우", "🦊", "T", "큰 귀로 몸의 열을 내보냄"], ["뱀", "🐍", "T", "변온 동물이라 추운 겨울에 겨울잠을 잠"],
      ["두더지", "🐀", "S", "땅속에 굴을 파고 지렁이를 잡아먹음"], ["오소리", "🦡", "S", "땅굴을 파서 살고 지렁이·곤충을 먹음"],
      ["잠자리", "🪽", "A", "애벌레는 물속에서 아가미로, 어른벌레는 공기로 호흡"], ["물방개", "🪲", "A", "날개 밑에 공기 방울을 저장해 잠수"]],
  4: [["매", "🦅", "L", "뛰어난 눈으로 높은 곳에서 먹이를 찾음"], ["물수리", "🪶", "W", "물고기를 낚아채는 맹금류"],
      ["북극곰", "🐻‍❄️", "T", "두꺼운 지방층과 털로 극지방 추위를 견딤"], ["삵", "🐈", "S", "바위틈과 굴을 보금자리로 삼는 우리나라 숲의 최상위 포식자"],
      ["범고래", "🐋", "A", "폐로 호흡해 물 위로 올라와 숨을 쉼"]],
};
// 비용 무늬(자기 요소를 뺀 나머지 4요소에 차례로 배치)와 점수. 같은 줄 안에서 돌려 씀.
const COST = { 1: [[1, 1, 1, 0, 0], [2, 1, 0, 0, 0], [1, 1, 1, 1, 0], [3, 0, 0, 0, 0], [2, 2, 0, 0, 1]],
               2: [[2, 1, 1, 0, 2], [2, 2, 0, 0, 2], [2, 2, 1, 0, 3], [3, 1, 0, 0, 2], [3, 2, 0, 0, 3]],
               3: [[3, 2, 2, 0, 4], [3, 2, 1, 0, 3], [4, 2, 0, 0, 4], [2, 2, 2, 1, 4]],
               4: [[4, 3, 2, 0, 5], [4, 3, 1, 0, 5], [5, 2, 1, 0, 5]] };   // 마지막 수 = 점수. 값은 새로 정함(줄이 4개라 30분에 맞게 sim.mjs로 조정)
export const CARDS = {};
for (const t of [1, 2, 3, 4]) C[t].forEach(([n, e, f, why], i) => {
  const pat = COST[t][i % COST[t].length], o = F.filter(x => x !== f), others = o.map((_, k) => o[(k + i) % 4]);   // 카드마다 비용 요소를 돌려 고르게
  const cost = {}; pat.slice(0, 4).forEach((c, k) => { if (c) cost[others[k]] = c; });
  CARDS[`${t}-${i}`] = { id: `${t}-${i}`, tier: t, n, e, f, why, pts: pat[4], cost };
});
// 보호종: 필요한 비생물요소 보너스(서식지 조건을 게임용으로 단순화), 모두 3점
export const NOBLES = {
  otter: { n: "수달", e: "🦦", need: { W: 2, S: 2, A: 2 }, why: "하천에 사는 천연기념물" },
  goral: { n: "산양", e: "🐐", need: { T: 3, S: 3 }, why: "험한 바위 산에 사는 천연기념물" },
  bear: { n: "반달가슴곰", e: "🐻", need: { L: 2, T: 2, S: 2 }, why: "숲에서 겨울잠을 자는 천연기념물" },
  stork: { n: "황새", e: "🦢", need: { W: 3, L: 3 }, why: "습지에 사는 천연기념물" },
  spoonbill: { n: "저어새", e: "🐦", need: { W: 2, A: 2, L: 2 }, why: "갯벌에 사는 천연기념물" },
  beetle: { n: "장수하늘소", e: "🪲", need: { L: 2, S: 2, T: 2 }, why: "오래된 숲에 사는 천연기념물" },
  mandarin: { n: "원앙", e: "🦆", need: { W: 3, A: 3 }, why: "숲속 냇가에 사는 천연기념물" },
  squirrel: { n: "하늘다람쥐", e: "🐿️", need: { T: 2, A: 2, L: 2 }, why: "나무 구멍에 사는 천연기념물" },
};

// ---------- 규칙 ----------
const shuffle = (a, rnd) => { a = [...a]; for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(rnd() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
const zero = (keys = F) => Object.fromEntries(keys.map(f => [f, 0]));
export function newGame(players, rnd = Math.random) {   // players: [{uid, nick}]
  const n = players.length, decks = {}, board = {};
  for (const t of [1, 2, 3, 4]) {
    const d = shuffle(Object.keys(CARDS).filter(id => CARDS[id].tier === t), rnd);
    board[t] = d.splice(0, 4); decks[t] = d;
  }
  return {
    order: shuffle(players.map(p => p.uid), rnd), names: Object.fromEntries(players.map(p => [p.uid, p.nick])),
    turn: 0, round: 1, endRound: 0, over: false, last: "게임 시작!",
    supply: { ...Object.fromEntries(F.map(f => [f, SUPPLY[Math.max(2, Math.min(4, n))]])), J: JOKERS },
    decks, board, nobles: shuffle(Object.keys(NOBLES), rnd).slice(0, n + 1),
    p: Object.fromEntries(players.map(p => [p.uid, { t: zero(TK), b: zero(), cards: [], res: [], pts: 0, nob: [] }])),
  };
}
export const current = g => g.order[g.turn];
// Firebase는 빈 배열·빈칸을 지워서 돌려줌 → 받은 상태를 원래 모양으로 되돌림
export function norm(g) {
  for (const t of [1, 2, 3, 4]) { g.decks[t] = Object.values(g.decks?.[t] || {}); g.board[t] = [0, 1, 2, 3].map(i => g.board?.[t]?.[i] || ""); }
  g.nobles = Object.values(g.nobles || {});
  for (const u of g.order) { const p = g.p[u]; p.cards = Object.values(p.cards || {}); p.nob = Object.values(p.nob || {}); p.res = Object.values(p.res || {}); }
  return g;
}
export const tokenCount = me => TK.reduce((s, f) => s + (me.t[f] || 0), 0);
// 먹이 조건: 1줄은 언제나, 2~4줄은 바로 아래 줄 카드를 1장 이상 가지고 있어야 함
export const hasFood = (me, tier) => tier === 1 || me.cards.some(id => CARDS[id].tier === tier - 1);
export const toPay = (me, card) => Object.fromEntries(F.map(f => [f, Math.max(0, (card.cost[f] || 0) - me.b[f])]));
// 모자란 만큼은 만능 토큰으로 냄
export const shortage = (me, card) => F.reduce((s, f) => s + Math.max(0, toPay(me, card)[f] - me.t[f]), 0);
export const canBuy = (me, card) => hasFood(me, card.tier) && shortage(me, card) <= me.t.J;

// 가져오기: 서로 다른 요소 최대 3개(남은 요소가 적으면 그만큼), 또는 4개 이상 남은 요소 2개
// (10개를 넘게 가져와도 되고, 넘은 만큼 차례 끝에 반납 — 원작 규칙)
export function canTake(g, me, picks) {
  if (!picks.length || picks.some(f => !F.includes(f))) return false;
  const uniq = new Set(picks);
  if (uniq.size === 1 && picks.length === 2) return g.supply[picks[0]] >= 4;
  const avail = F.filter(f => g.supply[f] > 0).length;
  return uniq.size === picks.length && picks.length <= 3 && picks.every(f => g.supply[f] > 0) && (picks.length === 3 || picks.length === avail);
}
export const canReserve = me => me.res.length < MAX_RESERVE;
// 반납: 10개를 넘은 만큼 정확히, 가진 토큰에서
function giveBack(g, me, ret = []) {
  const over = tokenCount(me) - MAX_TOKENS;
  if (over <= 0) { if (ret.length) throw new Error("반납할 필요가 없습니다"); return; }
  if (ret.length !== over) throw new Error(`토큰 ${over}개를 반납해야 합니다`);
  for (const f of ret) { if (!(me.t[f] > 0)) throw new Error("없는 토큰은 반납할 수 없습니다"); me.t[f]--; g.supply[f]++; }
}

// 행동 하나를 적용해 새 상태를 돌려줌(잘못된 행동이면 Error)
export function act(g0, uid, move) {
  const g = norm(structuredClone(g0)), me = g.p[uid], nick = g.names[uid];
  if (g.over || current(g) !== uid) throw new Error("내 차례가 아닙니다");
  if (move.type === "take") {
    if (!canTake(g, me, move.picks)) throw new Error("가져올 수 없는 조합입니다");
    for (const f of move.picks) { g.supply[f]--; me.t[f]++; }
    giveBack(g, me, move.ret);
    g.last = `${nick}: ${move.picks.map(f => FACTOR[f][0]).join("·")} 토큰을 가져옴` + (move.ret?.length ? ` (${move.ret.length}개 반납)` : "");
  } else if (move.type === "reserve") {   // 판의 카드(id) 또는 덱 맨 위(tier)를 찜하고 만능 토큰 1개
    if (!canReserve(me)) throw new Error(`찜은 ${MAX_RESERVE}장까지입니다`);
    let id = move.id;
    if (id) { const row = g.board[CARDS[id]?.tier] || [], i = row.indexOf(id); if (i < 0) throw new Error("판에 없는 카드입니다"); row[i] = g.decks[CARDS[id].tier].shift() ?? ""; }
    else { id = g.decks[move.tier]?.shift(); if (!id) throw new Error("그 줄의 덱이 비었습니다"); }
    me.res.push(id);
    if (g.supply.J > 0) { g.supply.J--; me.t.J++; }
    giveBack(g, me, move.ret);
    g.last = `${nick}: ${move.id ? CARDS[id].n : `${move.tier}줄 덱 카드`}을(를) 찜함`;
  } else if (move.type === "buy") {
    const card = CARDS[move.id], fromRes = me.res.includes(move.id), row = g.board[card?.tier] || [], i = row.indexOf(move.id);
    if (!card || (i < 0 && !fromRes)) throw new Error("살 수 없는 카드입니다");
    if (!hasFood(me, card.tier)) throw new Error(`먹이가 없습니다: ${TIER[card.tier - 1]} 카드가 먼저 필요해요`);
    if (!canBuy(me, card)) throw new Error("토큰이 모자랍니다");
    const pay = toPay(me, card);
    for (const f of F) { const use = Math.min(pay[f], me.t[f]), j = pay[f] - use; me.t[f] -= use; g.supply[f] += use; me.t.J -= j; g.supply.J += j; }
    me.b[card.f]++; me.pts += card.pts; me.cards.push(card.id);
    if (fromRes) me.res = me.res.filter(x => x !== move.id);
    else row[i] = g.decks[card.tier].shift() ?? "";   // 빈자리는 덱에서 채움(덱이 비면 빈칸 "")
    g.last = `${nick}: ${card.n}${card.pts ? ` (+${card.pts}점)` : ""}을(를) 데려옴`;
  } else if (move.type === "pass") {
    g.last = `${nick}: 쉬어 감`;
  } else throw new Error("알 수 없는 행동");
  const nb = g.nobles.find(k => F.every(f => me.b[f] >= (NOBLES[k].need[f] || 0)));   // 차례 끝에 보호종은 하나만
  if (nb) { g.nobles = g.nobles.filter(k => k !== nb); me.nob.push(nb); me.pts += 3; g.last += ` · 보호종 ${NOBLES[nb].n}이(가) 찾아옴 (+3점)`; }
  if (!g.endRound && me.pts >= WIN) g.endRound = g.round;   // 이 바퀴를 끝까지 돌고 끝냄(차례 수를 똑같이)
  g.turn = (g.turn + 1) % g.order.length;
  if (g.turn === 0) { if (g.endRound || g.round >= MAX_ROUNDS) g.over = true; else g.round++; }
  return g;
}
// 순위: 점수 높은 순, 같으면 카드 적은 순
export const ranking = g => [...g.order].sort((a, b) => g.p[b].pts - g.p[a].pts || g.p[a].cards.length - g.p[b].cards.length);

// 자체 점검
console.assert(Object.keys(CARDS).length === 45, "카드 45장");
for (const c of Object.values(CARDS)) console.assert(!c.cost[c.f] && Object.values(c.cost).reduce((a, b) => a + b, 0) >= 2, "비용 확인: " + c.n);
