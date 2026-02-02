import SetCard from './SetCard';

function SetsList({ sets, title = "🎨 Sets récents" }) {
  if (!sets || sets.length === 0) {
    return (
      <section className="sets">
        <h2>{title}</h2>
        <p className="no-data">Aucun set disponible</p>
      </section>
    );
  }

  return (
    <section className="sets">
      <h2>{title}</h2>
      <div className="sets-grid">
        {sets.map((set) => (
          <SetCard key={set.set_num} set={set} />
        ))}
      </div>
    </section>
  );
}

export default SetsList;