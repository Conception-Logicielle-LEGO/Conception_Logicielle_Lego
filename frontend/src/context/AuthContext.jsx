import { createContext, useContext, useState, useEffect } from 'react';

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

  function login(email, password) {
    // Mock auth — accepte n'importe quel email/mot de passe
    const mockUser = {
      id: 1,
      email,
      username: email.split('@')[0],
    };
    setUser(mockUser);
    localStorage.setItem('lego_user', JSON.stringify(mockUser));
    return mockUser;
  }

  function logout() {
    setUser(null);
    localStorage.removeItem('lego_user');
  }

  return (
    <AuthContext.Provider value={{ user, isLoading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth doit être utilisé dans un AuthProvider');
  return ctx;
}
