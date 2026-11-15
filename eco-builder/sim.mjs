// 시뮬레이션: node eco-builder/sim.mjs  — 단순 전략 플레이어 4명으로 한 판이 몇 차례에 끝나는지 본다.
import { newGame, act, current, CARDS, F, TK, canBuy, canTake, canReserve, toPay, hasFood, tokenCount, shortage, ranking, WIN, MAX_TOKENS, MAX_ROUNDS } from "./game.js";
const mul = s => () => (s = Math.imul(s ^ (s >>> 15), 2246822507) ^ 0x9e3779b9, ((s >>> 0) % 1e9) / 1e9);
function bot(g, uid) {
  const me = g.p[uid], board = Object.values(g.board).flat().filter(Boolean), pool = [...board, ...me.res].map(id => CARDS[id]);
  const buyable = pool.filter(c => canBuy(me, c)).sort((a, b) => b.pts - a.pts || b.tier - a.tier);
  if (buyable.length) return { type: "buy", id: buyable[0].id };
  const score = c => shortage(me, c) - c.pts * 0.8 - (me.res.includes(c.id) ? 1 : 0);   // 가까우면서 점수 높은 카드
  const goal = pool.filter(c => hasFood(me, c.tier)).sort((a, b) => score(a) - score(b))[0];
  const want = goal ? F.filter(f => toPay(me, goal)[f] > me.t[f]) : [];
  const order = [...want, ...F.filter(f => !want.includes(f))].filter(f => g.supply[f] > 0);
  let picks = null;
  for (const n of [3, 2, 1]) { const m = order.slice(0, n); if (canTake(g, me, m)) { picks = m; break; } }
  if (want[0] && g.supply[want[0]] >= 4 && want.length === 1) picks = [want[0], want[0]];
  // 가져올 게 쓸모없고 찜할 수 있으면 목표 카드를 찜(만능 토큰)
  if ((!picks || !picks.some(f => want.includes(f))) && goal && canReserve(me) && board.includes(goal.id)) picks = null;
  const ret = add => {   // 10개 넘으면 목표에 필요 없는 토큰부터 반납
    const after = { ...me.t }; add.forEach(f => after[f]++);
    const r = [], over = TK.reduce((s, f) => s + after[f], 0) - MAX_TOKENS;
    for (const f of [...F.filter(f => !want.includes(f)), ...want, "J"]) while (r.length < over && after[f] > 0) { after[f]--; r.push(f); }
    return r;
  };
  if (picks) return { type: "take", picks, ret: ret(picks) };
  if (goal && canReserve(me) && board.includes(goal.id)) return { type: "reserve", id: goal.id, ret: ret(g.supply.J > 0 ? ["J"] : []) };
  return { type: "pass" };
}
const rounds = [], top = [], last = [], nobles = [], t4 = [], res = [], capped = [];
for (let k = 1; k <= 2000; k++) {
  let g = newGame([1, 2, 3, 4].map(i => ({ uid: "u" + i, nick: "학생" + i })), mul(k));
  while (!g.over) g = act(g, current(g), bot(g, current(g)));
  const r = ranking(g), ps = Object.values(g.p);
  rounds.push(g.round); top.push(g.p[r[0]].pts); last.push(g.p[r[3]].pts); capped.push(g.p[r[0]].pts < WIN);
  nobles.push(ps.reduce((s, p) => s + p.nob.length, 0)); t4.push(ps.reduce((s, p) => s + p.cards.filter(id => CARDS[id].tier === 4).length, 0));
}
const avg = a => (a.reduce((x, y) => x + y, 0) / a.length).toFixed(1), q = (a, p) => [...a].sort((x, y) => x - y)[Math.floor(a.length * p)];
console.log(`승리 ${WIN}점: 한 사람당 차례 평균 ${avg(rounds)} (중앙 ${q(rounds, .5)}, 90% ${q(rounds, .9)}) · ${MAX_ROUNDS}바퀴 시간 종료 ${Math.round(capped.filter(Boolean).length / 20)}% · 1등 ${avg(top)}점 · 꼴찌 ${avg(last)}점 · 보호종 ${avg(nobles)}마리/판 · 4줄 카드 ${avg(t4)}장/판`);
