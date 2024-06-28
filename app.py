from flask import Flask, request, render_template, redirect, url_for, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'  # Altere para uma chave secreta segura
DATABASE = 'database.db'
UPLOAD_PATH = 'uploads'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='usuarios'")
    if not cursor.fetchone():
        with app.open_resource('schema.sql', mode='r') as f:
            conn.executescript(f.read())
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='professores'")
    if not cursor.fetchone():
        with app.open_resource('schema_professores.sql', mode='r') as f:
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
        db.close()
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
        finally:
            db.close()
    return render_template('criar_usuario.html')

@app.route('/usuarios')
def lista_usuarios():
    db = get_db()
    cur = db.execute('SELECT id, nome, email FROM usuarios')
    usuarios = cur.fetchall()
    db.close()
    return render_template('lista_usuarios.html', usuarios=usuarios)

@app.route('/professores/new', methods=['GET', 'POST'])
def cadastro_professores():
    if request.method == 'POST':
        nome_completo = request.form['nome_completo']
        senha = generate_password_hash(request.form['senha'])
        email = request.form['email']
        telefone = request.form['telefone']
        formacao_academica = request.form['formacao_academica']
        areas_especializacao = request.form['areas_especializacao']
        numero_registro_profissional = request.form['numero_registro_profissional']
        experiencia_profissional = request.form['experiencia_profissional']
        foto_de_perfil = request.form['foto_de_perfil']
        
        db = get_db()
        try:
            db.execute('INSERT INTO professores (nome_completo, senha, email, telefone, formacao_academica, areas_especializacao, numero_registro_profissional, experiencia_profissional, foto_de_perfil) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                       (nome_completo, senha, email, telefone, formacao_academica, areas_especializacao, numero_registro_profissional, experiencia_profissional, foto_de_perfil))
            db.commit()
            return redirect(url_for('login_professor'))  # Ajuste aqui para redirecionar para a página correta após o cadastro
        except sqlite3.IntegrityError:
            flash('Erro ao cadastrar professor')
        finally:
            db.close()
    
    return render_template('professor_login/cadastro_professor.html')

@app.route('/professores/list')
def lista_professores():
    db = get_db()
    cur = db.execute('SELECT id, nome_completo, email FROM professores')
    professores = cur.fetchall()
    db.close()
    return render_template('lista_professores.html', professores=professores)

@app.route('/login_professor', methods=['GET', 'POST'])
def login_professor():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        db = get_db()
        cur = db.execute('SELECT * FROM professores WHERE email = ?', (email,))
        professor = cur.fetchone()
        db.close()
        if professor and check_password_hash(professor['senha'], senha):
            session['user_id'] = professor['id']
            session['username'] = professor['nome_completo']
            return redirect(url_for('index'))
        flash('Email ou senha incorretos')
    return render_template('login_professor.html')

if __name__ == '__main__':
    init_db()  # Inicializa o banco de dados
    app.run(debug=True)
