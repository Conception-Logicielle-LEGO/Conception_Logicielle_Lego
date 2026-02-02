function ErrorMessage({ error }) {
  return (
    <div className="error-container">
      <h2>❌ Erreur de connexion</h2>
      <p className="error-message">{error}</p>
      <div className="error-help">
        <p>Assurez-vous que :</p>
        <ul>
          <li>Le backend est démarré sur <code>http://localhost:8000</code></li>
          <li>La base de données est initialisée</li>
          <li>Aucun firewall ne bloque la connexion</li>
        </ul>
      </div>
      <button onClick={() => window.location.reload()}>
        🔄 Réessayer
      </button>
    </div>
  );
}

export default ErrorMessage;