import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router';
import { Wrench } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import SetCard from '../components/SetCard';
import Loader from '../components/Loader';
import api from '../api/api_test';

// Aplatit un BuildableSet.to_dict() en objet compatible SetCard
function flattenBuildable(item) {
  return {
    ...item.set,
    coverage_pct: item.buildability.completion_percentage,
  };
}

export default function BuildablePage() {
  const { user, isLoading } = useAuth();
  const navigate = useNavigate();
  const [buildable, setBuildable] = useState([]);
  const [partial, setPartial] = useState([]);
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
      .then((r) => {
        setBuildable((r.data.buildable ?? []).map(flattenBuildable));
        setPartial((r.data.partial ?? []).map(flattenBuildable));
      })
      .catch(() => setError('Impossible de charger les sets constructibles.'))
      .finally(() => setLoading(false));
  }, [user]);

  if (isLoading) return null;
  if (!user) return null;

  const total = buildable.length + partial.length;

  return (
    <div className="space-y-8">
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
      ) : total === 0 ? (
        <p className="py-12 text-center text-gray-500">
          Aucun set constructible trouvé.
          <br />
          Ajoutez des pièces à votre collection pour commencer.
        </p>
      ) : (
        <>
          {buildable.length > 0 && (
            <section>
              <h2 className="mb-3 text-lg font-semibold text-green-700">
                ✅ Constructibles à 100 % ({buildable.length})
              </h2>
              <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
                {buildable.map((set) => (
                  <SetCard key={set.set_num} set={set} />
                ))}
              </div>
            </section>
          )}

          {partial.length > 0 && (
            <section>
              <h2 className="mb-3 text-lg font-semibold text-yellow-700">
                🔨 Presque constructibles ≥ 80 % ({partial.length})
              </h2>
              <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
                {partial.map((set) => (
                  <SetCard key={set.set_num} set={set} />
                ))}
              </div>
            </section>
          )}

        </>
      )}
    </div>
  );
}
