function Loader({ message = "Chargement..." }) {
  return (
    <div className="loader-container">
      <div className="loader"></div>
      <p>{message}</p>
    </div>
  );
}

export default Loader;