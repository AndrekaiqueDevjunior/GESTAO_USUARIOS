import sqlite3
from flask import Flask, request, render_template, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'  # Altere para uma chave secreta segura
DATABASE = 'database.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    # Verifique se a tabela já existe
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='usuarios'")
    if not cursor.fetchone():
        # Se a tabela não existir, crie-a
        with app.open_resource('schema.sql', mode='r') as f:
            conn.executescript(f.read())
    conn.commit()
    conn.close()

@app.route('/')
def index():
    if 'user_id' in session:
        return render_template('index.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        db = get_db()
        cur = db.execute('SELECT * FROM usuarios WHERE email = ?', (email,))
        usuario = cur.fetchone()
        if usuario and check_password_hash(usuario['senha'], senha):
            session['user_id'] = usuario['id']
            session['username'] = usuario['nome']
            return redirect(url_for('index'))
        flash('Email ou senha incorretos')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/usuarios/new', methods=['GET', 'POST'])
def criar_usuario():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = generate_password_hash(request.form['senha'])
        db = get_db()
        try:
            db.execute('INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)', 
                       (nome, email, senha))
            db.commit()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Email já registrado')
    return render_template('criar_usuario.html')


@app.route('/usuarios')
def lista_usuarios():
    db = get_db()
    cur = db.execute('SELECT id, nome, email FROM usuarios')
    usuarios = cur.fetchall()
    return render_template('lista_usuarios.html', usuarios=usuarios)

if __name__ == '__main__':
    init_db()  # Inicializa o banco de dados
    app.run(debug=True)
