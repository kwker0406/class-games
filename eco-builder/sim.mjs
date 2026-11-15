// 시뮬레이션: node eco-builder/sim.mjs  — 단순 전략 플레이어 4명으로 한 판이 몇 차례에 끝나는지 본다.
import { newGame, act, current, CARDS, F, canBuy, canTake, toPay, hasFood, tokenCount, ranking, WIN } from "./game.js";
const mul = s => () => (s = Math.imul(s ^ (s >>> 15), 2246822507) ^ 0x9e3779b9, ((s >>> 0) % 1e9) / 1e9);
function bot(g, uid) {
  const me = g.p[uid], cards = Object.values(g.board).flat().filter(Boolean).map(id => CARDS[id]);
  const buyable = cards.filter(c => canBuy(me, c)).sort((a, b) => b.pts - a.pts || b.tier - a.tier);
  if (buyable.length) return { type: "buy", id: buyable[0].id };
  // 목표: 먹이 조건을 채운 카드 중 모자란 토큰이 가장 적은 것(같으면 점수 높은 것)
  const need = c => F.reduce((s, f) => s + Math.max(0, toPay(me, c)[f] - me.t[f]), 0);
  const goal = cards.filter(c => hasFood(me, c.tier)).sort((a, b) => need(a) - need(b) || b.pts - a.pts)[0];
  const want = goal ? F.filter(f => toPay(me, goal)[f] > me.t[f]) : [];
  const pick = [...want, ...F.filter(f => !want.includes(f))].filter(f => g.supply[f] > 0);
  for (const n of [3, 2, 1]) { const m = pick.slice(0, n); if (canTake(g, me, m)) return { type: "take", picks: m }; }
  if (want[0] && canTake(g, me, [want[0], want[0]])) return { type: "take", picks: [want[0], want[0]] };
  return { type: "pass" };
}
for (const win of [WIN]) {
  const rounds = [], top = [], last = [], nobles = [], t4 = [];
  for (let k = 1; k <= 2000; k++) {
    let g = newGame([1, 2, 3, 4].map(i => ({ uid: "u" + i, nick: "학생" + i })), mul(k));
    while (!g.over) g = act(g, current(g), bot(g, current(g)));
    const r = ranking(g); rounds.push(g.round); top.push(g.p[r[0]].pts); last.push(g.p[r[3]].pts);
    nobles.push(Object.values(g.p).reduce((s, p) => s + p.nob.length, 0)); t4.push(Object.values(g.p).reduce((s, p) => s + p.cards.filter(id => CARDS[id].tier === 4).length, 0));
  }
  const avg = a => (a.reduce((x, y) => x + y, 0) / a.length).toFixed(1), q = (a, p) => [...a].sort((x, y) => x - y)[Math.floor(a.length * p)];
  console.log(`승리 점수 ${win}: 한 사람당 차례 평균 ${avg(rounds)} (중앙 ${q(rounds, .5)}, 90% ${q(rounds, .9)}, 10바퀴 시간 종료 ${(rounds.filter((r, i) => r >= 10 && top[i] < win).length / 20).toFixed(0)}%) · 1등 ${avg(top)}점 · 꼴찌 ${avg(last)}점 · 보호종 ${avg(nobles)}마리/판 · 4줄 카드 ${avg(t4)}장/판`);
}
