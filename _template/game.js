// 이 게임의 이름표와 문제. 새 게임을 만들면 tools/new_game.py가 __GAME__·__NAME__을 바꿔 넣는다.
export const GAME = "__GAME__";   // Firebase 주소에 쓰는 영어 이름(바꾸면 기존 방 기록과 끊김)
export const NAME = "__NAME__";   // 화면에 보이는 이름

// 예시 문제(바꿔 쓰기). answer는 choices 안의 번호(0부터)
export const QUESTIONS = [
  { q: "1기압에서 물이 끓는 온도는?", choices: ["0 °C", "50 °C", "100 °C"], answer: 2 },
  { q: "식물 세포에서 광합성이 일어나는 곳은?", choices: ["미토콘드리아", "엽록체", "핵"], answer: 1 },
];
