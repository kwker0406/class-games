// 모든 게임이 같이 쓰는 Firebase 통신. 게임 폴더에서 import * as net from "../common/net.js"
// 데이터 위치: games/{게임}/rooms/{방 코드}/{meta, players/{uid}, shared/...}
import config from "./config.js";
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.14.1/firebase-app.js";
import { getAuth, signInAnonymously, GoogleAuthProvider, signInWithPopup } from "https://www.gstatic.com/firebasejs/10.14.1/firebase-auth.js";
import { getDatabase, ref, set, get, update, onValue, onDisconnect } from "https://www.gstatic.com/firebasejs/10.14.1/firebase-database.js";

export const TEACHER = "k4366941@gmail.com";
const auth = getAuth(initializeApp(config));
const db = getDatabase();
export const R = p => ref(db, p);
export { set, get, update, onValue };
export const del = r => set(r, null); // 지우기(remove 대신: 시험용 가짜 Firebase와 같은 방식)

// 선생님: 이미 로그인돼 있으면 창을 띄우지 않음(popup=false면 확인만)
export async function teacherLogin(popup = true) {
  await auth.authStateReady();
  if (auth.currentUser?.email === TEACHER) return auth.currentUser;
  if (!popup) return null;
  const u = (await signInWithPopup(auth, new GoogleAuthProvider())).user;
  if (u.email !== TEACHER) throw new Error("NOTTEACHER");
  return u;
}

// 헷갈리는 글자(I, O, 0, 1) 뺀 4글자 방 코드
const ABC = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789";
export async function createRoom(game, meta = {}) {
  for (;;) {
    const code = Array.from({ length: 4 }, () => ABC[Math.floor(Math.random() * ABC.length)]).join("");
    if ((await get(R(`games/${game}/rooms/${code}/meta`))).exists()) continue;
    await set(R(`games/${game}/rooms/${code}/meta`), { state: "wait", createdAt: Date.now(), ...meta });
    return code;
  }
}

// 학생: 실패하면 Error("NOCODE"). 같은 기기는 같은 uid → 새로고침해도 같은 사람
export async function joinRoom(game, code, nick) {
  await auth.authStateReady();
  const uid = auth.currentUser?.uid ?? (await signInAnonymously(auth)).user.uid;
  code = code.trim().toUpperCase();
  const base = `games/${game}/rooms/${code}`;
  if (!(await get(R(`${base}/meta`))).exists()) throw new Error("NOCODE");
  const me = R(`${base}/players/${uid}`);
  await update(me, { nick: nick.trim().slice(0, 8), online: true });
  onDisconnect(me).update({ online: false });
  return { uid, code, base };
}
