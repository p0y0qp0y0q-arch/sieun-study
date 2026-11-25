/* 자동 동기화용 Firebase 설정 (Firebase 콘솔 → 프로젝트 설정 → 내 앱 → SDK 설정 및 구성 → '구성').
   이 값들은 비밀번호가 아니라 '어느 저장소인지' 알려 주는 주소예요. 보안은 데이터베이스 규칙과 가족 코드로 지켜요.
   비어 있으면(null) 동기화 없이 폰마다 따로 저장돼요. */
window.FIREBASE_CONFIG = window.FIREBASE_CONFIG || {
  apiKey: "AIzaSyCv2rOFcco1Mcsdf29QFgTaJKVVERCFvsM",
  authDomain: "sieun-study-824ff.firebaseapp.com",
  databaseURL: "https://sieun-study-824ff-default-rtdb.asia-southeast1.firebasedatabase.app",
  projectId: "sieun-study-824ff",
  storageBucket: "sieun-study-824ff.firebasestorage.app",
  messagingSenderId: "576166905244",
  appId: "1:576166905244:web:0854ec7be0b412ce267459"
};
