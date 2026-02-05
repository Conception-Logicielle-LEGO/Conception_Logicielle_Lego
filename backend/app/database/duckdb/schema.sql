-- Schéma de la base de données LEGO

-- Tables issues de la BDD Rebrickable

CREATE TABLE IF NOT EXISTS themes (
    id INTEGER PRIMARY KEY,
    name VARCHAR(40),
    parent_id INTEGER
);

CREATE TABLE IF NOT EXISTS colors (
    id INTEGER PRIMARY KEY,
    name VARCHAR(200),
    rgb VARCHAR(6),
    is_trans BOOLEAN
);

CREATE TABLE IF NOT EXISTS part_categories (
    id INTEGER PRIMARY KEY,
    name VARCHAR(200)
);

CREATE TABLE IF NOT EXISTS parts (
    part_num VARCHAR(20) PRIMARY KEY,
    name VARCHAR(250),
    part_cat_id INTEGER,
    FOREIGN KEY (part_cat_id) REFERENCES part_categories(id)
);

CREATE TABLE IF NOT EXISTS part_relationships (
    rel_type VARCHAR(1),
    child_part_num VARCHAR(20),
    parent_part_num VARCHAR(20),
    FOREIGN KEY (child_part_num) REFERENCES parts(part_num),
    FOREIGN KEY (parent_part_num) REFERENCES parts(part_num)
);

CREATE TABLE IF NOT EXISTS elements (
    element_id VARCHAR(10) PRIMARY KEY,
    part_num VARCHAR(20),
    color_id INTEGER,
    FOREIGN KEY (part_num) REFERENCES parts(part_num),
    FOREIGN KEY (color_id) REFERENCES colors(id)
);

CREATE TABLE IF NOT EXISTS sets (
    set_num VARCHAR(20) PRIMARY KEY,
    name VARCHAR(256),
    year INTEGER,
    theme_id INTEGER,
    num_parts INTEGER,
    FOREIGN KEY (theme_id) REFERENCES themes(id)
);

CREATE TABLE IF NOT EXISTS minifigs (
    fig_num VARCHAR(20) PRIMARY KEY,
    name VARCHAR(256),
    num_parts INTEGER
);

CREATE TABLE IF NOT EXISTS inventories (
    id INTEGER PRIMARY KEY,
    version INTEGER,
    set_num VARCHAR(20),
    -- retrait de la foreign key : FOREIGN KEY (set_num) REFERENCES sets(set_num)
);

CREATE TABLE IF NOT EXISTS inventory_parts (
    inventory_id INTEGER,
    part_num VARCHAR(20),
    color_id INTEGER,
    quantity INTEGER,
    is_spare BOOLEAN,
    FOREIGN KEY (inventory_id) REFERENCES inventories(id),
    FOREIGN KEY (part_num) REFERENCES parts(part_num),
    FOREIGN KEY (color_id) REFERENCES colors(id)
);

CREATE TABLE IF NOT EXISTS inventory_sets (
    inventory_id INTEGER,
    set_num VARCHAR(20),
    quantity INTEGER,
    FOREIGN KEY (inventory_id) REFERENCES inventories(id),
    FOREIGN KEY (set_num) REFERENCES sets(set_num)
);

CREATE TABLE IF NOT EXISTS inventory_minifigs (
    inventory_id INTEGER,
    fig_num VARCHAR(20),
    quantity INTEGER,
    FOREIGN KEY (inventory_id) REFERENCES inventories(id),
    FOREIGN KEY (fig_num) REFERENCES minifigs(fig_num)
);

-- Tables utilisateur (initialement vides)

CREATE TABLE IF NOT EXISTS users (
    id_user SERIAL PRIMARY KEY,
    username VARCHAR(20),
    hashed_password VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS favorite_sets (
    id_user INTEGER,
    set_num VARCHAR(20),
    FOREIGN KEY (id_user) REFERENCES users(id_user),
    FOREIGN KEY (set_num) REFERENCES sets(set_num),
    PRIMARY KEY (id_user, set_num)
);

CREATE TABLE IF NOT EXISTS user_owned_sets (
    id_user INTEGER,
    set_num VARCHAR(20),
    is_built BOOLEAN,
    FOREIGN KEY (id_user) REFERENCES users(id_user),
    FOREIGN KEY (set_num) REFERENCES sets(set_num),
    PRIMARY KEY (id_user, set_num)
);

CREATE TABLE IF NOT EXISTS user_parts (
    id_user INTEGER,
    part_num VARCHAR(20),
    status_owned_wished VARCHAR(20),
    is_used BOOLEAN,
    FOREIGN KEY (id_user) REFERENCES users(id_user),
    FOREIGN KEY (part_num) REFERENCES parts(part_num),
    PRIMARY KEY (id_user, part_num)
);

-- Index pour améliorer les performances

CREATE INDEX IF NOT EXISTS idx_parts_cat ON parts(part_cat_id);
CREATE INDEX IF NOT EXISTS idx_elements_part ON elements(part_num);
CREATE INDEX IF NOT EXISTS idx_elements_color ON elements(color_id);
CREATE INDEX IF NOT EXISTS idx_sets_theme ON sets(theme_id);
CREATE INDEX IF NOT EXISTS idx_sets_year ON sets(year);
CREATE INDEX IF NOT EXISTS idx_inventories_set ON inventories(set_num);
CREATE INDEX IF NOT EXISTS idx_inv_parts_inv ON inventory_parts(inventory_id);
CREATE INDEX IF NOT EXISTS idx_inv_parts_part ON inventory_parts(part_num);
CREATE INDEX IF NOT EXISTS idx_inv_parts_color ON inventory_parts(color_id);
CREATE INDEX IF NOT EXISTS idx_inv_sets_inv ON inventory_sets(inventory_id);
CREATE INDEX IF NOT EXISTS idx_inv_minifigs_inv ON inventory_minifigs(inventory_id);
CREATE INDEX IF NOT EXISTS idx_favorite_sets_user ON favorite_sets(id_user);
CREATE INDEX IF NOT EXISTS idx_user_owned_sets_user ON user_owned_sets(id_user);
CREATE INDEX IF NOT EXISTS idx_user_parts_user ON user_parts(id_user);
