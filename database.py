import sqlite3
import os

DB_PATH = os.environ.get('DB_PATH', 'stock.db')


def init_db():
    """Crée la base de données et la table si elles n'existent pas."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS product_status (
            id           TEXT PRIMARY KEY,
            is_available INTEGER NOT NULL DEFAULT 0,
            last_updated TEXT    DEFAULT (datetime('now'))
        )
    ''')
    conn.commit()
    conn.close()


def get_status(product_id: str) -> bool:
    """Retourne True si le produit était disponible lors de la dernière vérification."""
    conn = sqlite3.connect(DB_PATH)
    row = conn.execute(
        'SELECT is_available FROM product_status WHERE id = ?', (product_id,)
    ).fetchone()
    conn.close()
    # Si le produit n'est pas encore en base → considéré indisponible (première fois)
    return bool(row[0]) if row else False


def set_status(product_id: str, is_available: bool):
    """Enregistre ou met à jour le statut d'un produit."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''
        INSERT INTO product_status (id, is_available, last_updated)
        VALUES (?, ?, datetime('now'))
        ON CONFLICT(id) DO UPDATE SET
            is_available = excluded.is_available,
            last_updated = excluded.last_updated
    ''', (product_id, int(is_available)))
    conn.commit()
    conn.close()
