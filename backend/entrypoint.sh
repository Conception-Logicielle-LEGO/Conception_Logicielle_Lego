#!/bin/bash
set -e

DUCKDB_FILE="/backend/app/database/duckdb/lego.duckdb"

# ──────────────────────────────────────────────
# Init DuckDB si absent (aucune connexion réseau impliquée)
# ──────────────────────────────────────────────
if [ ! -f "$DUCKDB_FILE" ]; then
  echo "[init] lego.duckdb absent — téléchargement des données Rebrickable..."
  cd /backend && PYTHONPATH=/backend uv run python app/database/duckdb/init_db_lego.py
  echo "[init] DuckDB prêt."
else
  echo "[init] DuckDB déjà présent."
fi

# ──────────────────────────────────────────────
# Lancer l'application
# La connexion PostgreSQL est établie dans le lifespan FastAPI
# (première connexion = kubectl port-forward frais = succès garanti)
# ──────────────────────────────────────────────
echo "[init] Démarrage de l'application..."
exec uv run main.py
