# Conception_Logicielle_Lego
Faire une application ermettant de trouver les sets qu'il est possible de réaliser à partir de l'ensemble des pièces Lego possédées.

## Lancement de l’application

### Prérequis

Avant de lancer l’application, assurez-vous de disposer des éléments suivants :

* **Python 3.11 ou supérieur**
* **uv** installé et accessible depuis le terminal

### optionnel : visualisation des diagrammes

installer l'extension Mermaid Preview  v2.1.2 

---

## Variables d'environnement :
Copier la template dans un fichier .env

```bash
cp .env.template .env
```

### Création de l’environnement et installation des dépendances

Depuis la racine du projet, exécutez les commandes suivantes;

```bash
cd backend
uv venv
uv sync
```
lancer la commande 
source .venv/bin/activate


## Requirements :
Géré par le Dockerfile et pyproject.toml
Pour ajouter un package aux requirements, écrire "uv add <nom package>" dans le bash


## setup pythonpath
### run (dans le terminal) :

On set le pythonpath dans le dossier backend. Exécutez depuis le dossier backend :
```bash
export PYTHONPATH=$(pwd)
```

### vérifier avec :
```bash
echo $PYTHONPATH
```

# Mise en place BDD
## BDD rebrickable (duckDB local) :

Exécuter (toujours depuis backend)
# pour les urls image
Rebrickable API (https://rebrickable.com/api/ → Mon compte -> setting -> API → Clé API)


```python
python app/database/duckdb/init_db_lego.py
```

## BDD Users (postgreSQL) :

### Cas initialisation :

1) Lancer un service PostgreSQL sur onyxia avec ces paramètres :

https://datalab.sspcloud.fr/launcher/databases/postgresql-cnpg?name=postgresql-cnpg&version=0.4.2&extension.pgvector=true&storage.size=«20Gi»&resources.limits.memory=«80Gi»&security.networkPolicy.enabled=false&autoLaunch=true 

2) renseigner le nom d'utilisateur et le mot de passe du service dans le .env

3) Sur Onyxia : aller dans "Mon compte", puis "Connexion à Kubernetes". Copier le script et l'exécuter dans votre terminal.

4) ouvrir un terminal et exécuter :

```bash
kubectl get pods
```
Cette commande retourne les services onyxia lancés. Copier le nom du service postgresql et exécutez :

```bash
export POD=<nom_du_service>
echo $POD

kubectl port-forward $POD 5432:5432
```
5) Ouvrir un autre terminal et exécutez:

```python
cd backend
python app/database/postgres/init_db_user.py
```

### Cas où on veut accéder au port (autre utilisateur)

Exécuter à la racine du projet :

```bash
kubectl apply -f kubernetes/pg-proxy.yaml
kubectl port-forward pod/pg-proxy 5432:5432
```


# Mise en place frontend

npm install -g create-vite
npm create vite@latest frontend


Ignore files -> React -> Javascript -> no -> yes


### Lancer l'application

**Ouvrir 2 terminaux :**

#### Terminal 1 - Backend (API)
```bash
cd ~/Conception_Logicielle_Lego
uvicorn backend.app.api.fast_api:app --reload --port 8000
```
✅ Backend disponible sur : http://localhost:8000

#### Terminal 2 - Frontend (Interface)
```bash
cd ~/Conception_Logicielle_Lego/frontend
npm run dev
```
✅ Frontend disponible sur : http://localhost:5173

### Vérification

1. Ouvrir http://localhost:5173 dans le navigateur
2. Vous devriez voir :
   - Le header "🧱 LEGO Database Explorer"
   - Les statistiques (Total Sets, Pièces, Thèmes)
   - La liste des sets LEGO