import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

const firebaseConfig = {
  apiKey: "AIzaSyD8M5BHwqaFjMurjwle6KQrBUv_7d00IQM",
  authDomain: "receiptiq-cfb7a.firebaseapp.com",
  projectId: "receiptiq-cfb7a",
  storageBucket: "receiptiq-cfb7a.firebasestorage.app",
  messagingSenderId: "199936512837",
  appId: "1:199936512837:web:bdf9ad83726bfae3ea642c",
  measurementId: "G-LTP00BWC43"
};

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
