-- Schema PostgreSQL pour les utilisateurs
-- Tables relatives aux utilisateurs uniquement
-- Pas de foreign keys vers les tables Rebrickable (dans DuckDB)

-- Table des utilisateurs
CREATE TABLE IF NOT EXISTS users (
    id_user SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    salt VARCHAR(256),
    email VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des sets favoris
CREATE TABLE IF NOT EXISTS favorite_sets (
    id_user INTEGER NOT NULL,
    set_num VARCHAR(20) NOT NULL,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_user, set_num),
    FOREIGN KEY (id_user) REFERENCES users(id_user) ON DELETE CASCADE
    -- Pas de FK vers sets(set_num) car dans DuckDB
);

-- Table des wishlists (une par utilisateur)
CREATE TABLE IF NOT EXISTS wishlist (
    id_wishlist SERIAL PRIMARY KEY,
    id_user INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_user) REFERENCES users(id_user) ON DELETE CASCADE,
    UNIQUE(id_user)
);

-- Table des pièces dans la wishlist
CREATE TABLE IF NOT EXISTS wishlist_parts (
    id_wishlist INTEGER NOT NULL,
    part_num VARCHAR(20) NOT NULL,
    color_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_wishlist, part_num, color_id),
    FOREIGN KEY (id_wishlist) REFERENCES wishlist(id_wishlist) ON DELETE CASCADE
    -- Pas de FK vers parts(part_num) car dans DuckDB
    -- Pas de FK vers colors(id) car dans DuckDB
);

-- Table des sets dans la wishlist
CREATE TABLE IF NOT EXISTS wishlist_sets (
    id_wishlist INTEGER NOT NULL,
    set_num VARCHAR(20) NOT NULL,
    priority INTEGER DEFAULT 0,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_wishlist, set_num),
    FOREIGN KEY (id_wishlist) REFERENCES wishlist(id_wishlist) ON DELETE CASCADE
    -- Pas de FK vers sets(set_num) car dans DuckDB
);

-- Table des sets possédés par les utilisateurs
CREATE TABLE IF NOT EXISTS user_owned_sets (
    id_user INTEGER NOT NULL,
    set_num VARCHAR(20) NOT NULL,
    is_built BOOLEAN DEFAULT FALSE,
    acquired_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notes TEXT,
    PRIMARY KEY (id_user, set_num),
    FOREIGN KEY (id_user) REFERENCES users(id_user) ON DELETE CASCADE
    -- Pas de FK vers sets(set_num) car dans DuckDB
);

-- Table des pièces des utilisateurs
CREATE TABLE IF NOT EXISTS user_parts (
    id_user INTEGER NOT NULL,
    part_num VARCHAR(20) NOT NULL,
    color_id INTEGER NOT NULL,
    quantity INTEGER DEFAULT 1,
    status VARCHAR(20) CHECK (status IN ('owned', 'wished')) DEFAULT 'owned',
    is_used BOOLEAN DEFAULT FALSE,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_user, part_num, color_id),
    FOREIGN KEY (id_user) REFERENCES users(id_user) ON DELETE CASCADE
    -- Pas de FK vers parts(part_num) car dans DuckDB
    -- Pas de FK vers colors(id) car dans DuckDB
);

-- Index pour optimiser les performances
CREATE INDEX IF NOT EXISTS idx_favorite_sets_user ON favorite_sets(id_user);
CREATE INDEX IF NOT EXISTS idx_favorite_sets_set ON favorite_sets(set_num);

CREATE INDEX IF NOT EXISTS idx_wishlist_user ON wishlist(id_user);

CREATE INDEX IF NOT EXISTS idx_wishlist_parts_wishlist ON wishlist_parts(id_wishlist);
CREATE INDEX IF NOT EXISTS idx_wishlist_parts_part ON wishlist_parts(part_num, color_id);

CREATE INDEX IF NOT EXISTS idx_wishlist_sets_wishlist ON wishlist_sets(id_wishlist);
CREATE INDEX IF NOT EXISTS idx_wishlist_sets_set ON wishlist_sets(set_num);
CREATE INDEX IF NOT EXISTS idx_wishlist_sets_priority ON wishlist_sets(id_wishlist, priority);

CREATE INDEX IF NOT EXISTS idx_user_owned_sets_user ON user_owned_sets(id_user);
CREATE INDEX IF NOT EXISTS idx_user_owned_sets_set ON user_owned_sets(set_num);
CREATE INDEX IF NOT EXISTS idx_user_owned_sets_built ON user_owned_sets(is_built);

CREATE INDEX IF NOT EXISTS idx_user_parts_user ON user_parts(id_user);
CREATE INDEX IF NOT EXISTS idx_user_parts_part ON user_parts(part_num, color_id);
CREATE INDEX IF NOT EXISTS idx_user_parts_status ON user_parts(status);