function StatsCard({ title, value, icon }) {
  return (
    <div className="stat-card">
      <div className="stat-icon">{icon}</div>
      <h3>{typeof value === 'number' ? value.toLocaleString() : value}</h3>
      <p>{title}</p>
    </div>
  );
}

export default StatsCard;