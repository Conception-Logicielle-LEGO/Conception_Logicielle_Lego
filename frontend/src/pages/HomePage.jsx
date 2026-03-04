import { useState, useEffect } from 'react';
import { TrendingUp, Package, Layers } from 'lucide-react';
import api from '../api/api_test';
import SetCard from '../components/SetCard';
import Loader from '../components/Loader';
import ErrorMessage from '../components/ErrorMessage';

function StatCard({ icon: Icon, label, value, color }) {
  return (
    <div className="flex items-center gap-4 rounded-xl border border-gray-200 bg-white p-5 shadow-sm">
      <div className={`rounded-lg p-3 ${color}`}>
        <Icon size={22} className="text-white" />
      </div>
      <div>
        <p className="text-2xl font-bold text-gray-900">{value ?? '—'}</p>
        <p className="text-sm text-gray-500">{label}</p>
      </div>
    </div>
  );
}

export default function HomePage() {
  const [sets, setSets] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function load() {
      try {
        const [setsRes, statsRes] = await Promise.all([
          api.get('/sets/recent'),
          api.get('/stats').catch(() => ({ data: null })),
        ]);
        setSets(setsRes.data);
        setStats(statsRes.data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  if (loading) return <Loader message="Chargement du catalogue LEGO..." />;
  if (error) return <ErrorMessage error={error} />;

  return (
    <div className="space-y-8">
      {/* En-tête */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">
          🎀 Catalogue LEGO
        </h1>
        <p className="mt-1 text-gray-500">
          Trouvez les sets que vous pouvez assembler avec vos pièces
        </p>
      </div>

      {/* Stats */}
      {stats && (
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
          <StatCard
            icon={Layers}
            label="Sets"
            value={stats.totalSets?.toLocaleString()}
            color="bg-red-500"
          />
          <StatCard
            icon={Package}
            label="Pièces"
            value={stats.totalParts?.toLocaleString()}
            color="bg-blue-500"
          />
          <StatCard
            icon={TrendingUp}
            label="Thèmes"
            value={stats.totalThemes?.toLocaleString()}
            color="bg-green-500"
          />
        </div>
      )}

      {/* Sets */}
      <section>
        <h2 className="mb-4 text-xl font-semibold text-gray-800">
          Sets récents
        </h2>
        {sets.length === 0 ? (
          <p className="text-center text-gray-500 py-12">Aucun set trouvé.</p>
        ) : (
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
            {sets.map((set) => (
              <SetCard key={set.set_num} set={set} />
            ))}
          </div>
        )}
      </section>
    </div>
  );
}
