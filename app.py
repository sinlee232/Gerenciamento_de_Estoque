from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import verificar_credenciais, adicionar_usuario, listar_produtos, adicionar_produto, editar_produto, remover_produto, registrar_entrada, registrar_saida, gerar_relatorio_produtos, gerar_relatorio_movimentacoes
import logging

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configurar logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def index():
    logging.debug('Entrando na rota /')
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        logging.debug('Recebendo requisição POST em /login')
        username = request.form['username']
        password = request.form['password']
        role = verificar_credenciais(username, password)
        if role:
            session['username'] = username
            session['role'] = role
            flash('Login successful', 'success')
            logging.debug(f'Login bem-sucedido para usuário: {username}')
            return redirect(url_for('main'))
        else:
            flash('Invalid credentials', 'danger')
            logging.debug('Credenciais inválidas')
    logging.debug('Renderizando template login.html')
    return render_template('login.html')


@app.route('/logout')
def logout():
    logging.debug('Usuário deslogando')
    session.clear()
    flash('You have been logged out', 'success')
    return redirect(url_for('login'))

@app.route('/main')
def main():
    logging.debug('Entrando na rota /main')
    if 'username' not in session:
        logging.debug('Usuário não está na sessão, redirecionando para /login')
        return redirect(url_for('login'))
    return render_template('main.html', role=session['role'])

@app.route('/produtos', methods=['GET', 'POST'])
def produtos():
    logging.debug('Entrando na rota /produtos')
    if 'username' not in session:
        logging.debug('Usuário não está na sessão, redirecionando para /login')
        return redirect(url_for('login'))
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        preco = float(request.form['preco'])
        quantidade = int(request.form['quantidade'])
        logging.debug(f'Adicionando produto: {nome}, {descricao}, {preco}, {quantidade}')
        adicionar_produto(nome, descricao, preco, quantidade)
        flash('Produto adicionado com sucesso', 'success')
    produtos = listar_produtos()
    logging.debug(f'Produtos listados: {produtos}')
    return render_template('produtos.html', produtos=produtos)

@app.route('/produtos/editar/<int:id>', methods=['GET', 'POST'])
def editar_produto_view(id):
    logging.debug(f'Entrando na rota /produtos/editar/{id}')
    if 'username' not in session:
        logging.debug('Usuário não está na sessão, redirecionando para /login')
        return redirect(url_for('login'))
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        preco = float(request.form['preco'])
        quantidade = int(request.form['quantidade'])
        editar_produto(id, nome, descricao, preco, quantidade)
        flash('Produto editado com sucesso', 'success')
        return redirect(url_for('produtos'))
    return render_template('editar_produto.html', produto_id=id)

@app.route('/produtos/remover/<int:id>', methods=['GET'])
def remover_produto_view(id):
    logging.debug(f'Entrando na rota /produtos/remover/{id}')
    if 'username' not in session:
        logging.debug('Usuário não está na sessão, redirecionando para /login')
        return redirect(url_for('login'))
    remover_produto(id)
    flash('Produto removido com sucesso', 'success')
    return redirect(url_for('produtos'))

@app.route('/estoque', methods=['GET', 'POST'])
def estoque():
    logging.debug('Entrando na rota /estoque')
    if 'username' not in session:
        logging.debug('Usuário não está na sessão, redirecionando para /login')
        return redirect(url_for('login'))
    if request.method == 'POST':
        produto_id = int(request.form['produto_id'])
        quantidade = int(request.form['quantidade'])
        tipo = request.form['tipo']
        if tipo == 'entrada':
            registrar_entrada(produto_id, quantidade)
            flash('Entrada registrada com sucesso', 'success')
        elif tipo == 'saida':
            registrar_saida(produto_id, quantidade)
            flash('Saída registrada com sucesso', 'success')
    produtos = listar_produtos()
    return render_template('estoque.html', produtos=produtos)

@app.route('/relatorios')
def relatorios():
    logging.debug('Entrando na rota /relatorios')
    if 'username' not in session:
        logging.debug('Usuário não está na sessão, redirecionando para /login')
        return redirect(url_for('login'))
    produtos = gerar_relatorio_produtos()
    movimentacoes = gerar_relatorio_movimentacoes()
    return render_template('relatorios.html', produtos=produtos, movimentacoes=movimentacoes)

if __name__ == '__main__':
    # Verifica se o usuário admin existe, caso contrário, cria um
    try:
        adicionar_usuario('admin', 'admin', 'admin')
    except Exception as e:
        logging.debug(f'Erro ao adicionar usuário admin: {e}')

    app.run(debug=True, port=8080)
