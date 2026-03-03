import { createContext, useContext, useState, useEffect } from 'react';
import api from '../api/api_test.js';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const stored = localStorage.getItem('lego_user');
    if (stored) {
      try {
        setUser(JSON.parse(stored));
      } catch {
        localStorage.removeItem('lego_user');
      }
    }
    setIsLoading(false);
  }, []);

  async function login(username, password) {
    const { data } = await api.post('/users/login', { username, password });
    const userObj = { id: data.id_user, username: data.username };
    setUser(userObj);
    localStorage.setItem('lego_user', JSON.stringify(userObj));
    return userObj;
  }

  async function register(username, password) {
    const { data } = await api.post('/users', { username, password });
    const userObj = { id: data.id_user, username: data.username };
    setUser(userObj);
    localStorage.setItem('lego_user', JSON.stringify(userObj));
    return userObj;
  }

  function logout() {
    setUser(null);
    localStorage.removeItem('lego_user');
  }

  return (
    <AuthContext.Provider value={{ user, isLoading, login, logout, register }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth doit être utilisé dans un AuthProvider');
  return ctx;
}
