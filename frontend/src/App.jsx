import { useState, useEffect } from 'react';
import { apiService } from './services/api';
import Header from './components/Header';
import StatsCard from './components/StatsCard';
import SetsList from './components/SetsList';
import Loader from './components/Loader';
import ErrorMessage from './components/ErrorMessage';
import './App.css';

function App() {
  const [stats, setStats] = useState(null);
  const [sets, setSets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);
        
        // Vérifier la santé de l'API
        const health = await apiService.healthCheck();
        console.log('✅ API Status:', health);

        // Récupérer les stats
        const statsData = await apiService.getStats();
        setStats(statsData);
        console.log('📊 Stats:', statsData);

        // Récupérer quelques sets
        const setsData = await apiService.getSets({ limit: 12 });
        setSets(setsData);
        console.log('🎨 Sets:', setsData);

        setLoading(false);
      } catch (err) {
        console.error('❌ Error fetching data:', err);
        setError(err.message || 'Une erreur est survenue');
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return <Loader message="Chargement des données LEGO..." />;
  }

  if (error) {
    return <ErrorMessage error={error} />;
  }

  return (
    <div className="App">
      <Header />

      {/* Section Statistiques */}
      {stats && (
        <section className="stats-section">
          <h2>📊 Statistiques globales</h2>
          <div className="stats-grid">
            <StatsCard 
              title="Sets" 
              value={stats.total_sets} 
              icon="🎁"
            />
            <StatsCard 
              title="Pièces" 
              value={stats.total_parts} 
              icon="🧩"
            />
            <StatsCard 
              title="Couleurs" 
              value={stats.total_colors} 
              icon="🎨"
            />
            <StatsCard 
              title="Thèmes" 
              value={stats.total_themes} 
              icon="📚"
            />
          </div>
          
          {/* Informations supplémentaires */}
          <div className="extra-info">
            <div className="info-card">
              <h4>📅 Années couvertes</h4>
              <p>{stats.years_range.min} - {stats.years_range.max}</p>
            </div>
            {stats.largest_set && (
              <div className="info-card">
                <h4>🏆 Plus grand set</h4>
                <p>
                  <strong>{stats.largest_set[0]}</strong>
                  <br />
                  <span className="highlight">{stats.largest_set[1].toLocaleString()} pièces</span>
                </p>
              </div>
            )}
          </div>
        </section>
      )}

      {/* Section Sets */}
      <SetsList sets={sets} title="🎨 Sets les plus récents" />
    </div>
  );
}

export default App;