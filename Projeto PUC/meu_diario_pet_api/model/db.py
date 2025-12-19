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
            tipo TEXT,
            foto TEXT
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

    cur.execute("""
        CREATE TABLE IF NOT EXISTS observacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pet_id INTEGER,
            data TEXT,
            texto TEXT,
            FOREIGN KEY (pet_id) REFERENCES pets(id)
        )
    """)

    # Add foto column if not exists
    try:
        cur.execute("ALTER TABLE pets ADD COLUMN foto TEXT")
    except:
        pass  # Column already exists

    conn.commit()
    conn.close()