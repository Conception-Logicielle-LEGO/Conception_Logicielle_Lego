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

### Création de l’environnement et installation des dépendances

Depuis la racine du projet, exécutez les commandes suivantes;

```bash
cd backend
uv venv
uv sync
```

## Requirements :
Géré par le Dockerfile et pyproject.toml
Pour ajouter un package aux requirements, écrire "uv add <nom package>" dans le bash


Exécuter :

```bash
python3 -m venv .venv
source .venv/bin/activate

python3 -m pip install --upgrade pip
python3 -m pip --version
python3 -m pip install requests
python3 -m pip install -r requirements.txt
```



## setup pythonpath
### run (dans le terminal) :

On set le pythonpath dans le dossier backend. Placez vous dans /Conception_Logicielle_Lego et exécutez:

```bash
export PYTHONPATH=$(pwd)/backend
```

### vérifier avec :

```bash
echo $PYTHONPATH
```


## Variables d'environnement :
Copier la template dans un fichier .env

```bash
cp .env.template .env
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