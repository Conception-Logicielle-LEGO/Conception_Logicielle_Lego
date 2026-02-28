import { useEffect } from 'react';
import { useNavigate } from 'react-router';
import { Heart, Bookmark, User } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';

export default function AccountPage() {
  const { user, isLoading } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (!isLoading && !user) {
      navigate('/login', { replace: true });
    }
  }, [user, isLoading, navigate]);

  if (isLoading) return null;
  if (!user) return null;

  return (
    <div className="space-y-8">
      {/* En-tête compte */}
      <div className="flex items-center gap-4">
        <div className="flex h-16 w-16 items-center justify-center rounded-full bg-red-100">
          <User size={28} className="text-red-600" />
        </div>
        <div>
          <h1 className="text-2xl font-bold text-gray-900">{user.username}</h1>
          <p className="text-gray-500">{user.email}</p>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
        {/* Favoris */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Heart size={18} className="text-red-500" />
              Mes favoris
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-gray-500 py-6 text-center">
              Vous n'avez pas encore de favoris.
              <br />
              Cliquez sur ❤ sur un set pour l'ajouter.
            </p>
          </CardContent>
        </Card>

        {/* Wishlist */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Bookmark size={18} className="text-blue-500" />
              Ma wishlist
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-gray-500 py-6 text-center">
              Votre wishlist est vide.
              <br />
              Cliquez sur 🔖 sur un set pour l'ajouter.
            </p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
