#!/bin/bash
set -e

# ──────────────────────────────────────────────
# kubectl port-forward (doit tourner sur l'hôte)
# ──────────────────────────────────────────────
echo "Recherche du pod PostgreSQL..."
POD=$(kubectl get pods --no-headers | grep -i postgres | awk '{print $1}' | head -n1)

if [ -z "$POD" ]; then
  echo "Erreur : aucun pod PostgreSQL trouvé."
  echo "Vérifiez votre connexion au cluster Kubernetes."
  exit 1
fi

echo "Pod trouvé : $POD"
# Boucle de reconnexion automatique (CNPG coupe la connexion après chaque usage)
(while true; do
  kubectl port-forward "$POD" 5432:5432 2>/dev/null
done) &
PF_PID=$!
echo "Port-forward démarré (PID $PF_PID, reconnexion auto) → localhost:5432"
sleep 2

trap "echo 'Arrêt du port-forward...'; kill $PF_PID 2>/dev/null; pkill -P $PF_PID 2>/dev/null" EXIT INT TERM

# ──────────────────────────────────────────────
# docker compose (l'init BDD est dans entrypoint.sh)
# ──────────────────────────────────────────────
sudo docker compose up "$@"
