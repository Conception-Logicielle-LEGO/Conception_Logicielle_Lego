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
cp .env.template .env
```

**Avant de continuer**, éditer `.env` et renseigner :
- `POSTGRES_USER` et `POSTGRES_PASSWORD` — identifiants de votre instance PostgreSQL
- `REBRICKABLE_API_KEY` — clé obtenue sur https://rebrickable.com → *Mon compte → Settings → API → Generate key*

```bash
# 2. Installer les dépendances backend
cd backend
uv sync
cd ..

# 3. Installer les dépendances frontend
cd frontend
npm install
cd ..

# 4. Initialiser la base DuckDB — télécharge les données Rebrickable (~10 min)
#    Requiert REBRICKABLE_API_KEY dans .env
cd backend
python app/database/duckdb/init_db_lego.py
cd ..

# 5. Initialiser la base PostgreSQL
cd backend
python app/database/postgres/init_db_user.py
cd ..
```

### Lancer l'application

Ouvrir deux terminaux depuis la racine du projet :

```bash
# Terminal 1 — Backend
uvicorn backend.app.api.fast_api:app --reload --port 8000
```

```bash
# Terminal 2 — Frontend
cd frontend
npm run dev
```

- Backend : http://localhost:8000
- Frontend : http://localhost:5173

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

## Configuration PostgreSQL

Option A — PostgreSQL local avec Docker :

```bash
docker compose up -d db
```

Option B — PostgreSQL sur Onyxia (SSP Cloud) :

1. Lancer un service PostgreSQL sur [Onyxia](https://datalab.sspcloud.fr/launcher/databases/postgresql-cnpg)
2. Renseigner les identifiants dans `.env`
3. Aller dans *Mon compte → Connexion à Kubernetes*, copier le script et l'exécuter dans le terminal
4. Configurer le port-forward :

```bash
kubectl get pods
export POD=<nom_du_pod_postgresql>
kubectl port-forward $POD 5432:5432
```

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
