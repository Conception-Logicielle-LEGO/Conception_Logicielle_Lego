import { useState, useEffect } from 'react';
import './App.css';
import api from './api/api_test';

function App() {
  const [message, setMessage] = useState('Chargement...');

  useEffect(() => {
    api.get('/endpoint_entrainement')
      .then(response => setMessage(response.data))
      .catch(error => setMessage(`Erreur: ${error.message}`));
  }, []);

  return (
    <div className="App">
      <h1>Test API</h1>
      <p>{message}</p>
    </div>
  );
}

export default App;