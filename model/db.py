import sqlite3

def conectar():
    return sqlite3.connect("database.db")

def criar_tabelas():
    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS pets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            idade INTEGER,
            tipo TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS diario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pet_id INTEGER,
            comida_preferida TEXT,
            veterinario TEXT,
            data_vacinacao TEXT,
            peso REAL,
            observacoes TEXT,
            FOREIGN KEY (pet_id) REFERENCES pets(id)
        )
    """)

    conn.commit()
    conn.close()