import { useState, useEffect } from 'react';
import './App.css';
import Header from './components/Header';
import Loader from './components/Loader';
import ErrorMessage from './components/ErrorMessage';
import StatsCard from './components/StatsCard';
import SetsList from './components/SetsList';
import api from './api/api_test';

function App() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [sets, setSets] = useState([]);
  const [stats, setStats] = useState({ totalSets: 0, totalParts: 0, totalThemes: 0 });

  useEffect(() => {
    loadData();
  }, []);

  async function loadData() {
    try {
      const [setsRes, statsRes] = await Promise.all([
        api.get('/sets/recent'),
        api.get('/stats')
      ]);
      
      setSets(setsRes.data);
      setStats(statsRes.data);
      setLoading(false);
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  }

  if (loading) {
    return (
      <div className="App">
        <Header />
        <Loader message="Chargement des sets LEGO..." />
      </div>
    );
  }

  if (error) {
    return (
      <div className="App">
        <Header />
        <ErrorMessage error={error} />
      </div>
    );
  }

  return (
    <div className="App">
      <Header />
      <div className="container">
        <section className="stats">
          <StatsCard title="Total Sets" value={stats.totalSets} icon="🧱" />
          <StatsCard title="Pièces" value={stats.totalParts} icon="🔩" />
          <StatsCard title="Thèmes" value={stats.totalThemes} icon="🎨" />
        </section>
        <SetsList sets={sets} title="🎨 Sets LEGO populaires" />
      </div>
    </div>
  );
}

export default App;