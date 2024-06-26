import sqlite3

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Verifique se a tabela já existe
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='usuarios'")
    if not cursor.fetchone():
        # Se a tabela não existir, crie-a
        with open('schema.sql', 'r') as f:
            conn.executescript(f.read())
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Banco de dados inicializado.")
