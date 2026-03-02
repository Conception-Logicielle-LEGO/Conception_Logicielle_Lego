import { Link, useLocation } from 'react-router';
import { Home, Search, User, LogIn, LogOut, Wrench } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { Button } from './ui/button';
import { cn } from '../lib/utils';

const navLinks = [
  { to: '/', label: 'Catalogue', icon: Home },
  { to: '/search', label: 'Recherche', icon: Search },
  { to: '/buildable', label: 'Constructibles', icon: Wrench },
  { to: '/account', label: 'Mon compte', icon: User },
];

export default function Navbar() {
  const { pathname } = useLocation();
  const { user, logout } = useAuth();

  return (
    <nav className="sticky top-0 z-50 border-b border-gray-200 bg-white shadow-sm">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3">
        {/* Logo */}
        <Link to="/" className="flex items-center gap-2 font-bold text-red-600 text-xl">
          <span className="text-2xl">🧱🐟</span>
          LEGO Finder
        </Link>

        {/* Nav links */}
        <div className="flex items-center gap-1">
          {navLinks.map(({ to, label, icon: Icon }) => (
            <Link
              key={to}
              to={to}
              className={cn(
                'flex items-center gap-1.5 rounded-md px-3 py-2 text-sm font-medium transition-colors',
                pathname === to
                  ? 'bg-red-50 text-red-600'
                  : 'text-gray-600 hover:bg-gray-100 hover:text-gray-900',
              )}
            >
              <Icon size={16} />
              {label}
            </Link>
          ))}
        </div>

        {/* Auth */}
        <div className="flex items-center gap-2">
          {user ? (
            <>
              <span className="text-sm text-gray-600">Bonjour, {user.username}</span>
              <Button variant="ghost" size="sm" onClick={logout}>
                <LogOut size={16} />
                Déconnexion
              </Button>
            </>
          ) : (
            <Link to="/login">
              <Button size="sm">
                <LogIn size={16} />
                Connexion
              </Button>
            </Link>
          )}
        </div>
      </div>
    </nav>
  );
}
