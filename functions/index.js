const functions = require('firebase-functions');
const admin = require('firebase-admin');
const { initializeApp } = require('firebase/app');
const { getAuth, createUserWithEmailAndPassword, signInWithEmailAndPassword, signOut } = require('firebase/auth');

// Inisialisasi Firebase Admin SDK
admin.initializeApp();

// Konfigurasi Firebase untuk klien
const firebaseConfig = {
    apiKey: "AIzaSyCJmhr7OGZx_R-WeNWJI3fzp0alPl9Ilgc",
    authDomain: "compfest-1b96e.firebaseapp.com",
    databaseURL: "https://compfest-1b96e-default-rtdb.firebaseio.com",
    projectId: "compfest-1b96e",
    storageBucket: "compfest-1b96e.appspot.com",
    messagingSenderId: "397558428328",
    appId: "1:397558428328:web:fe920c2edd48e857f0489d"
};

// Inisialisasi Firebase Client SDK
const firebaseApp = initializeApp(firebaseConfig);
const auth = getAuth(firebaseApp);

// Fungsi untuk menangani CORS
function handleCors(req, res) {
  res.set('Access-Control-Allow-Origin', '*');
  res.set('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.set('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') {
    res.status(204).send('');
    return true; // CORS handled, no need to process further
  }
  return false; // Proceed with main logic
}

// Register
exports.register = functions.https.onRequest(async (req, res) => {
  if (handleCors(req, res)) return;

  const { email, password, name } = req.body;
  try {
    const userCredential = await createUserWithEmailAndPassword(auth, email, password);
    const user = userCredential.user;

    // Menyimpan data tambahan ke Firestore
    await admin.firestore().collection('users').doc(user.uid).set({
      name: name,
      email: email,
      createdAt: admin.firestore.FieldValue.serverTimestamp()
    });

    res.status(200).send({ uid: user.uid, message: 'Registration successful' });
  } catch (error) {
    res.status(400).send({ error: error.message });
  }
});

// Login
exports.login = functions.https.onRequest(async (req, res) => {
  if (handleCors(req, res)) return;

  const { email, password } = req.body;
  try {
    const userCredential = await signInWithEmailAndPassword(auth, email, password);
    const user = userCredential.user;
    const token = await user.getIdToken();

    res.status(200).send({ token });
  } catch (error) {
    res.status(400).send({ error: error.message });
  }
});

// Logout
exports.logout = functions.https.onRequest(async (req, res) => {
  if (handleCors(req, res)) return;

  try {
    await signOut(auth);
    res.status(200).send({ message: "Logout successful" });
  } catch (error) {
    res.status(400).send({ error: error.message });
  }
});
