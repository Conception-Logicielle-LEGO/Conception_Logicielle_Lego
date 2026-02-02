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
uv venv
uv sync
```

## Requirements :
### run :
```bash
pip install -r requirements.txt
```


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

```bash
export PYTHONPATH=$(pwd)/app
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