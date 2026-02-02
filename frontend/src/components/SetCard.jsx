function SetCard({ set }) {
    return(
        <div className="set-card">
            <h3>{set.name}</h3>
            <div className="set-details">
                <span className="set-num">#{set.set_num}</span>
                <span className="year">📅 {set.year}</span>
                <span className="parts">🔩 {set.num_parts} pièces</span>
            </div>
        </div>
    )
}

export default SetCard;  