"""
Enrichissement des images depuis l'API Rebrickable.

Script à exécuter une fois après init_db_lego.py, depuis backend/ :
    python app/database/duckdb/fetch_images.py

Pour chaque set dont img_url est NULL ou vide dans lego.duckdb,
appelle GET https://rebrickable.com/api/v3/lego/sets/{set_num}/
et met à jour la colonne img_url avec le champ set_img_url retourné.

Rate limit Rebrickable : 100 requêtes / minute.
Stratégie : pause de 0.65 s entre chaque requête + retry automatique sur HTTP 429.

Variable d'environnement requise : REBRICKABLE_API_KEY
"""

import json
import os
from pathlib import Path
import sys
import time
import urllib.error
import urllib.request


sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from dotenv import load_dotenv
import duckdb

from app.database.connexion_duckdb import DB_PATH


load_dotenv()

API_BASE = "https://rebrickable.com/api/v3/lego/sets"
RATE_LIMIT_DELAY = 0.65  # 100 req/min → ~0.65 s entre requêtes
RETRY_DELAY = 62  # pause (s) après un HTTP 429


def _fetch_set_image(set_num: str, api_key: str) -> str | None:
    """Appelle l'API Rebrickable et retourne l'URL de l'image du set.

    Args:
        set_num: Identifiant du set (ex. "10497-1").
        api_key: Clé API Rebrickable.

    Returns:
        URL de l'image, ou None si introuvable / erreur réseau.

    Raises:
        urllib.error.HTTPError: avec code 429 si le rate limit est atteint
                                (le caller se charge du retry).
    """
    url = f"{API_BASE}/{set_num}/"
    req = urllib.request.Request(url, headers={"Authorization": f"key {api_key}"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
            return data.get("set_img_url") or None
    except urllib.error.HTTPError as e:
        if e.code == 429:
            raise  # propagé pour retry
        if e.code != 404:
            print(f"⚠️  HTTP {e.code}", end=" ")
        return None
    except Exception as e:
        print(f"⚠️  {e}", end=" ")
        return None


def fetch_images(conn: duckdb.DuckDBPyConnection | None = None) -> None:
    """Enrichit img_url pour les sets dont la valeur est manquante.

    Args:
        conn: Connexion DuckDB ouverte en mode WRITE.
              Si None, ouvre DB_PATH en écriture (usage standalone).
    """
    api_key = os.getenv("REBRICKABLE_API_KEY")
    if not api_key:
        print("❌ Variable d'environnement REBRICKABLE_API_KEY manquante.")
        print("   Ajoutez-la dans votre fichier .env, puis relancez.")
        sys.exit(1)

    standalone = conn is None
    if standalone:
        if not DB_PATH.exists():
            print(f"❌ Base DuckDB introuvable : {DB_PATH}")
            print("   Lancez d'abord : python app/database/duckdb/init_db_lego.py")
            sys.exit(1)
        print(f"Ouverture de {DB_PATH} en mode écriture...")
        conn = duckdb.connect(str(DB_PATH), read_only=False)

    try:
        rows = conn.execute(
            "SELECT set_num FROM sets WHERE img_url IS NULL OR img_url = ''"
        ).fetchall()
        set_nums = [r[0] for r in rows]
        total = len(set_nums)

        print(f"\n🖼️  {total} set(s) sans image à enrichir.")

        if total == 0:
            print("✅ Toutes les images sont déjà renseignées.")
            return

        updated = 0
        for i, set_num in enumerate(set_nums, 1):
            print(
                f"  [{i:>{len(str(total))}}/{total}] {set_num:20}", end=" ", flush=True
            )

            # Retry automatique sur rate limit
            while True:
                try:
                    img_url = _fetch_set_image(set_num, api_key)
                    break
                except urllib.error.HTTPError as e:
                    if e.code == 429:
                        print(
                            f"⏳ rate limit, attente {RETRY_DELAY}s...",
                            end=" ",
                            flush=True,
                        )
                        time.sleep(RETRY_DELAY)
                    else:
                        img_url = None
                        break

            if img_url:
                conn.execute(
                    "UPDATE sets SET img_url = ? WHERE set_num = ?",
                    [img_url, set_num],
                )
                updated += 1
                display_url = img_url if len(img_url) <= 70 else img_url[:67] + "..."
                print(f"✅ {display_url}")
            else:
                print("— aucune image")

            if i < total:
                time.sleep(RATE_LIMIT_DELAY)

        print(f"\n✅ {updated}/{total} image(s) mise(s) à jour dans {DB_PATH.name}.")

    finally:
        if standalone:
            conn.close()


if __name__ == "__main__":
    fetch_images()
