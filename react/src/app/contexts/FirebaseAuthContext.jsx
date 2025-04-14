// src/app/contexts/FirebaseAuthContext.jsx
import { createContext, useEffect, useReducer } from "react";
import { initializeApp } from "firebase/app";
import {
  getAuth,
  signOut,
  signInWithPopup,
  GoogleAuthProvider,
  onAuthStateChanged,
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
  sendPasswordResetEmail
} from "firebase/auth";
import { 
  getFirestore, 
  doc, 
  getDoc, 
  setDoc 
} from "firebase/firestore";
// FIREBASE CONFIGURATION
import { firebaseConfig } from "app/config";
// GLOBAL CUSTOM COMPONENT
import Loading from "app/components/MatxLoading";

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);

const initialAuthState = {
  user: null,
  isInitialized: false,
  isAuthenticated: false
};

const reducer = (state, action) => {
  switch (action.type) {
    case "FB_AUTH_STATE_CHANGED": {
      const { isAuthenticated, user } = action.payload;
      return { ...state, isAuthenticated, isInitialized: true, user };
    }

    default: {
      return state;
    }
  }
};

const AuthContext = createContext({
  ...initialAuthState,
  method: "FIREBASE",
  resetPassword: () => Promise.resolve()
});

export const AuthProvider = ({ children }) => {
  const [state, dispatch] = useReducer(reducer, initialAuthState);

  // Função para buscar a role do usuário do Firestore
  const getUserRole = async (uid) => {
    try {
      const userRef = doc(db, "users", uid);
      const userSnap = await getDoc(userRef);
      
      if (userSnap.exists()) {
        return userSnap.data().role || "GUEST"; // Default to GUEST if no role found
      } else {
        // Se o documento não existir, crie-o com a role padrão
        await setDoc(userRef, { role: "GUEST" });
        return "GUEST";
      }
    } catch (error) {
      console.error("Error fetching user role:", error);
      return "GUEST"; // Default role if error
    }
  };

  const signInWithEmail = async (email, password) => {
    try {
      const result = await signInWithEmailAndPassword(auth, email, password);
      return result;
    } catch (error) {
      console.error("Error signing in with email:", error);
      throw error;
    }
  };

  const signInWithGoogle = async () => {
    try {
      const provider = new GoogleAuthProvider();
      const result = await signInWithPopup(auth, provider);
      
      // Verificar se é um novo usuário
      const isNewUser = result._tokenResponse?.isNewUser;
      
      if (isNewUser) {
        // Criar documento do usuário com role padrão para novos usuários
        await setDoc(doc(db, "users", result.user.uid), {
          email: result.user.email,
          name: result.user.displayName || result.user.email,
          role: "FREE" // Default role for new Google users
        });
      }
      
      return result;
    } catch (error) {
      console.error("Error signing in with Google:", error);
      throw error;
    }
  };

  const createUserWithEmail = async (email, password, role = "FREE") => {
    try {
      console.log("Iniciando criação de usuário:", email);
      const userCredential = await createUserWithEmailAndPassword(auth, email, password);
      console.log("Usuário criado com sucesso:", userCredential.user.uid);
      
      console.log("Criando documento no Firestore com role:", role);
      await setDoc(doc(db, "users", userCredential.user.uid), {
        email: email,
        role: role
      });
      console.log("Documento criado com sucesso");
      
      return userCredential.user;
    } catch (error) {
      console.error("Erro detalhado:", error.code, error.message);
      throw error;
    }
  };

  const logout = () => signOut(auth);

  const resetPassword = (email) => {
    return sendPasswordResetEmail(auth, email);
  };

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, async (user) => {
      if (user) {
        // Buscar a role do usuário quando ele estiver autenticado
        const role = await getUserRole(user.uid);
        
        dispatch({
          type: "FB_AUTH_STATE_CHANGED",
          payload: {
            isAuthenticated: true,
            user: {
              id: user.uid,
              email: user.email,
              avatar: user.photoURL,
              name: user.displayName || user.email,
              role: role // Adicionar a role do usuário
            }
          }
        });
      } else {
        dispatch({
          type: "FB_AUTH_STATE_CHANGED",
          payload: { isAuthenticated: false, user: null }
        });
      }
    });

    return () => unsubscribe();
  }, []);

  if (!state.isInitialized) return <Loading />;

  return (
    <AuthContext.Provider
      value={{
        ...state,
        logout,
        signInWithGoogle,
        method: "FIREBASE",
        signInWithEmail,
        createUserWithEmail,
        resetPassword
      }}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthContext;