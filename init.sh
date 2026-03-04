#!/bin/bash
set -e

# ──────────────────────────────────────────────
# Script d'initialisation des bases de données
# À exécuter une seule fois avant le premier lancement
# Le port-forward permanent (terminal dédié) ne doit PAS être actif
# ──────────────────────────────────────────────

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$SCRIPT_DIR/backend"

# 1. Init DuckDB (pas besoin de PostgreSQL)
echo "==> Init DuckDB..."
(cd "$BACKEND_DIR" && PYTHONPATH=. uv run python app/database/duckdb/init_db_lego.py)
echo "==> DuckDB OK"

# 2. Port-forward temporaire pour l'init PostgreSQL
echo ""
echo "==> Recherche du pod PostgreSQL..."
POD=$(kubectl get pods --no-headers | grep -i postgres | awk '{print $1}' | head -n1)

if [ -z "$POD" ]; then
  echo "Erreur : aucun pod PostgreSQL trouvé. Vérifiez kubectl."
  exit 1
fi

echo "==> Pod : $POD — démarrage du port-forward temporaire..."
kubectl port-forward "$POD" 5432:5432 &
PF_PID=$!
sleep 2

# 3. Init PostgreSQL
echo "==> Init PostgreSQL..."
(cd "$BACKEND_DIR" && PYTHONPATH=. uv run python app/database/postgres/init_db_user.py) || true

# 4. Nettoyage (le port-forward a peut-être déjà crashé — c'est normal)
kill $PF_PID 2>/dev/null || true
wait $PF_PID 2>/dev/null || true

echo ""
echo "==> Initialisation terminée."
echo "==> Vous pouvez maintenant lancer votre port-forward permanent et démarrer l'application."
