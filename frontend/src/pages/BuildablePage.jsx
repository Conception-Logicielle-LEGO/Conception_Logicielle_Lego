import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router';
import { Wrench } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import SetCard from '../components/SetCard';
import Loader from '../components/Loader';
import api from '../api/api_test';

export default function BuildablePage() {
  const { user, isLoading } = useAuth();
  const navigate = useNavigate();
  const [sets, setSets] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!isLoading && !user) {
      navigate('/login', { replace: true });
    }
  }, [user, isLoading, navigate]);

  useEffect(() => {
    if (!user) return;
    setLoading(true);
    setError(null);
    api
      .get(`/users/${user.id}/buildable`, { params: { limit: 50 } })
      .then((r) => setSets(r.data))
      .catch(() => setError('Impossible de charger les sets constructibles.'))
      .finally(() => setLoading(false));
  }, [user]);

  if (isLoading) return null;
  if (!user) return null;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="flex items-center gap-2 text-3xl font-bold text-gray-900">
          <Wrench size={28} className="text-red-600" />
          Sets constructibles
        </h1>
        <p className="mt-1 text-gray-500">
          Sets que vous pouvez construire avec vos pièces actuelles.
        </p>
      </div>

      {loading ? (
        <Loader message="Calcul des sets constructibles…" />
      ) : error ? (
        <p className="py-12 text-center text-red-500">{error}</p>
      ) : sets.length === 0 ? (
        <p className="py-12 text-center text-gray-500">
          Aucun set constructible trouvé.
          <br />
          Ajoutez des pièces à votre collection pour commencer.
        </p>
      ) : (
        <>
          <p className="text-sm text-gray-500">{sets.length} set(s) constructible(s)</p>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
            {sets.map((set) => (
              <SetCard key={set.set_num} set={set} />
            ))}
          </div>
        </>
      )}
    </div>
  );
}
