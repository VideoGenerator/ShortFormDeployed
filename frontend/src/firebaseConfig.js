import { initializeApp } from 'firebase/app'
import { getAuth } from 'firebase/auth'
import { getFirestore } from 'firebase/firestore'
import { getStorage } from 'firebase/storage'

const firebaseConfig = {
  apiKey: "AIzaSyAMw1hpMnl-s7YzUZyCHV3FbtVo1qga8MU",
  authDomain: "brainrot-24a7a.firebaseapp.com",
  projectId: "brainrot-24a7a",
  storageBucket: "brainrot-24a7a.appspot.com",
  messagingSenderId: "656401624605",
  appId: "1:656401624605:web:b89d95924064c1d1b460f4"
};

// const firebaseConfig = {
//   apiKey: 'AIzaSyAUUnFDd2RnuHNle-x2pvpS5vwWtjaua4k',
//   authDomain: 'brainrot-41d72.firebaseapp.com',
//   projectId: 'brainrot-41d72',
//   storageBucket: 'brainrot-41d72.appspot.com',
//   messagingSenderId: '500124590793',
//   appId: '1:500124590793:web:fe762c07f3d13de2c6a318',
//   measurementId: 'G-0YKX8EZY2H'
// }
// origianl config ^^ 

export const app = initializeApp(firebaseConfig)
export const auth = getAuth(app)
export const db = getFirestore(app)
export const storage = getStorage(app)