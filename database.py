import sqlite3
import hashlib

# Função para criar uma nova conexão com o banco de dados
def get_db_connection():
    conn = sqlite3.connect('estoque.db', check_same_thread=False, timeout=10)
    return conn

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def adicionar_usuario(username, password, role):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO usuarios (username, password, role)
    VALUES (?, ?, ?)
    ''', (username, hash_password(password), role))
    conn.commit()
    conn.close()

def verificar_credenciais(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT password, role
    FROM usuarios
    WHERE username = ?
    ''', (username,))
    result = cursor.fetchone()
    conn.close()
    if result and result[0] == hash_password(password):
        return result[1]  # Retorna o papel do usuário ('admin' ou 'operador')
    return None

def adicionar_produto(nome, descricao, preco, quantidade):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO produtos (nome, descricao, preco, quantidade)
    VALUES (?, ?, ?, ?)
    ''', (nome, descricao, preco, quantidade))
    conn.commit()
    conn.close()

def editar_produto(id, nome, descricao, preco, quantidade):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE produtos
    SET nome = ?, descricao = ?, preco = ?, quantidade = ?
    WHERE id = ?
    ''', (nome, descricao, preco, quantidade, id))
    conn.commit()
    conn.close()

def remover_produto(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    DELETE FROM produtos
    WHERE id = ?
    ''', (id,))
    conn.commit()
    conn.close()

def listar_produtos():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM produtos')
    produtos = cursor.fetchall()
    conn.close()
    return produtos

def registrar_entrada(produto_id, quantidade):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO movimentacoes (produto_id, tipo, quantidade)
    VALUES (?, 'entrada', ?)
    ''', (produto_id, quantidade))
    cursor.execute('''
    UPDATE produtos
    SET quantidade = quantidade + ?
    WHERE id = ?
    ''', (quantidade, produto_id))
    conn.commit()
    conn.close()

def registrar_saida(produto_id, quantidade):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO movimentacoes (produto_id, tipo, quantidade)
    VALUES (?, 'saida', ?)
    ''', (produto_id, quantidade))
    cursor.execute('''
    UPDATE produtos
    SET quantidade = quantidade - ?
    WHERE id = ?
    ''', (quantidade, produto_id))
    conn.commit()
    conn.close()

def gerar_relatorio_produtos():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT id, nome, descricao, preco, quantidade
    FROM produtos
    ''')
    produtos = cursor.fetchall()
    conn.close()
    return produtos

def gerar_relatorio_movimentacoes():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT movimentacoes.id, produtos.nome, movimentacoes.tipo, movimentacoes.quantidade, movimentacoes.data
    FROM movimentacoes
    JOIN produtos ON movimentacoes.produto_id = produtos.id
    ''')
    movimentacoes = cursor.fetchall()
    conn.close()
    return movimentacoes
