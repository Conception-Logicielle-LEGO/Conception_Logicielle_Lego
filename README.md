# LEGO Set Finder

Application web permettant de trouver les sets LEGO assemblables à partir des pièces que vous possédez.

**Stack :** FastAPI (backend) · React/Vite (frontend) · DuckDB (catalogue LEGO Rebrickable) · PostgreSQL (données utilisateur)

---

## Quickstart

### Prérequis

- Python 3.13+ et [uv](https://docs.astral.sh/uv/)
- Node.js 18+ et npm
- Une instance PostgreSQL accessible (voir [Configuration PostgreSQL](#configuration-postgresql))
- Un compte [Rebrickable](https://rebrickable.com) pour obtenir une clé API (nécessaire avant l'initialisation de la base LEGO)

### Installation

```bash
# 1. Copier le fichier de configuration
cd backend
cp .env.template .env
```

**Avant de continuer**, éditer `.env` et renseigner :
- `POSTGRES_USER` et `POSTGRES_PASSWORD` — identifiants de votre instance PostgreSQL
- `REBRICKABLE_API_KEY` — clé obtenue sur https://rebrickable.com → *Mon compte → Settings → API → Generate key*

### Étape 1 — Initialisation des bases de données (première fois uniquement)

```bash
./init.sh
```

Ce script gère automatiquement un port-forward temporaire pour initialiser PostgreSQL, puis le ferme. Il initialise aussi DuckDB (téléchargement des données Rebrickable).

> ⚠️ Ne pas avoir de port-forward actif quand on lance `init.sh`.
> ⚠️ Réinitialise complètement PostgreSQL — ne pas relancer si des données doivent être conservées.

### Étape 2 — Port-forward PostgreSQL (terminal dédié, à laisser ouvert)

```bash
export POD=$(kubectl get pods --no-headers | grep -i postgres | awk '{print $1}' | head -n1)
kubectl port-forward $POD 5432:5432
```

### Étape 3 — Lancer l'application avec Docker Compose

```bash
sudo docker compose build
sudo docker compose up
```

- Frontend : http://localhost:5173
- Backend API : http://localhost:8000

---

## Scénario d'utilisation

1. **Accueil** — Ouvrir http://localhost:5173 pour consulter les statistiques du catalogue (nombre de sets, pièces, thèmes) et les derniers sets ajoutés.

2. **Recherche** — Aller sur `/search` pour chercher un set ou une pièce par nom. La recherche se déclenche automatiquement après quelques caractères.

3. **Gestion de sa collection** — Dans `/account` :
   - Ajouter des sets qu'on possède (déboîtés ou construits)
   - Marquer un set comme "construit" pour exclure ses pièces du stock disponible
   - Ajouter des pièces individuelles à sa collection

4. **Wishlist** — Ajouter des sets ou des pièces à une liste de souhaits pour un achat futur.

5. **Sets assemblables** — Consulter `/buildable` pour voir quels sets du catalogue peuvent être assemblés avec les pièces disponibles. Chaque set affiche un pourcentage de pièces disponibles.

6. **Favoris** — Depuis n'importe quelle fiche set, l'ajouter aux favoris pour la retrouver rapidement dans `/account`.

---

## Lancer les tests

```bash
cd backend
pytest test/ -v
```

Tests ciblés :

```bash
# Tests unitaires (business objects) — aucune base de données requise
pytest test/test_BO/ -v

# Tests de service
pytest test/test_service/ -v

# Tests DAO (requiert PostgreSQL)
pytest test/test_dao/ -v
```

> Les tests PostgreSQL nécessitent une instance configurée via les variables d'environnement.
> Les tests DuckDB sont ignorés automatiquement si `lego_test.duckdb` est absent.

Avec rapport de couverture :

```bash
cd backend
uv run pytest --cov=app --cov-report=term-missing -q
```

---

## Linting et formatage

```bash
cd backend
ruff check .          # vérification
ruff check --fix .    # correction automatique
ruff format .         # formatage
```

---

---

## Architecture

```
Conception_Logicielle_Lego/
├── backend/
│   └── app/
│       ├── api/              # Routes FastAPI
│       ├── business_object/  # Objets métier (User, Set, Part…)
│       ├── service/          # Logique métier
│       └── database/
│           ├── dao/          # Accès aux données
│           ├── duckdb/       # Catalogue LEGO (lecture seule)
│           └── postgres/     # Données utilisateur (lecture/écriture)
├── frontend/
│   └── src/
│       ├── pages/            # Pages de l'application
│       ├── components/       # Composants réutilisables
│       └── api/              # Client HTTP (axios)
├── docs/                     # Documentation technique (modèle de données)
└── .github/workflows/        # Pipelines CI (tests, lint)
```

Le catalogue LEGO est stocké dans DuckDB (lecture seule). Les données utilisateur (collection, wishlist, favoris) sont dans PostgreSQL. Les deux bases sont interrogées indépendamment, sans clés étrangères croisées.

Pour le modèle de données complet, voir [`docs/Physical_data_model.md`](docs/Physical_data_model.md).
