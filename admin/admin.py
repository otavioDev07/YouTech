from flask import render_template, Blueprint, request, redirect, session
from session.session import verifica_sessao
from database.conexao import iniciar_db, get_db_conexao 
import uuid, os
from werkzeug.utils import secure_filename

usuario = 'adm'
senha = '1234'
admin_blueprint = Blueprint('admin', __name__, template_folder='templates')

@admin_blueprint.route('/login')
def login():
    titulo = 'LOGIN'
    return render_template('login.html', titulo=titulo)

#Rota da página de acesso
@admin_blueprint.route('/acesso', methods=['post'])
def acesso():
    global usuario, senha
    usuario_info = request.form['usuario']
    senha_info = request.form['senha']
    if usuario == usuario_info and senha == senha_info:
        session['login'] = True
        return redirect('/adm')
    else:
        return render_template('login.html', msg="Usuário/Senha estão incorretos!")
    

#Rota da página ADM
@admin_blueprint.route('/adm')
def adm():
    global verifica_sessao, iniciar_db, get_db_conexao
    if verifica_sessao():
        iniciar_db()
        conexao = get_db_conexao()
        produtos = conexao.execute('SELECT * FROM produtos ORDER BY id DESC').fetchall()
        conexao.close()
        title = 'administração'
        return render_template('adm.html', produtos=produtos, title=title)
    else:
        return redirect('/login')
    

#Rota para renderizar página de cadastro
@admin_blueprint.route('/cadprodutos')
def cadprodutos():
    if verifica_sessao():
        title = "CADASTRO DE PRODUTOS"
        return render_template('cadastro.html', title=title)
    else:
        return redirect('/login')
    
#Rota para cadastro no database
@admin_blueprint.route('/cadastro',methods=["post"])
def cadastro():
    if verifica_sessao():
        nome = request.form['nome']
        descricao = request.form['descricao']
        preco = request.form['preco']
        img = request.files['img']
        id_img = str(uuid.uuid4().hex)
        filename = secure_filename(img.filename)
        novo_nome = f"{id_img}_{filename}.png"
        caminho_imagem = os.path.join('static/img/produtos', novo_nome)
        img.save(caminho_imagem)
        conexao = get_db_conexao()
        conexao.execute('INSERT INTO produtos (nome, descricao, preco, img) VALUES (?, ?, ?, ?)', (nome, descricao, preco, novo_nome))
        conexao.commit()
        conexao.close()
        return redirect('/adm')
    else:
        return redirect('/login')
    
#Rota para exclusão
@admin_blueprint.route('/excluir/<id>')
def excluir(id):
    global img
    if verifica_sessao():
        id = int(id)
        conexao = get_db_conexao()
        imagem = conexao.execute('SELECT img FROM produtos WHERE id = ?', (id,)).fetchone()
        caminho_imagem = os.path.join('static/img/produtos', imagem['img'])
        os.remove(caminho_imagem)
        conexao.execute('DELETE FROM produtos WHERE id = ?', (id,))
        conexao.commit()
        conexao.close()
        return redirect('/adm')
    else:
        return redirect('/login')
    
#Rota para chamar a página de edição
@admin_blueprint.route('/editprodutos/<id>')
def chamar_editar(id):
    if verifica_sessao():
        iniciar_db()
        conexao = get_db_conexao()
        produtos = conexao.execute('SELECT * FROM produtos WHERE id = ?', (id,)).fetchall()
        conexao.close()
        title = 'Edição de Produtos'
        return render_template('editprodutos.html', produtos=produtos, title=title)
    else:
        return redirect('/login')

@admin_blueprint.route('/editarprodutos', methods=['POST'])
def editar():
    id = request.form['id']
    nome = request.form['nome']
    descricao = request.form['descricao']
    preco = request.form['preco']
    img = request.files['img']
    conexao = get_db_conexao()
    if img:
        id_img = str(uuid.uuid4().hex)
        filename = secure_filename(img.filename) #Usa o nome original da imagem com o ID único gerado
        novo_nome = f"{id_img}_{filename}.png"
        caminho_imagem = os.path.join('static/img/produtos', novo_nome)
        imagem_antiga = conexao.execute('SELECT img FROM produtos WHERE id = ?', (id,)).fetchone() # Remove a imagem antiga, se existir
        if imagem_antiga:
            caminho_imagem_antiga = os.path.join('static/img/produtos', imagem_antiga['img'])
            if os.path.exists(caminho_imagem_antiga):
                os.remove(caminho_imagem_antiga)
        img.save(caminho_imagem)
    else:
        novo_nome = conexao.execute('SELECT img FROM produtos WHERE id = ?', (id,)).fetchone()['img'] # Se nenhuma nova imagem for enviada, mantém a imagem existente

    # Atualiza os outros campos no banco de dados
    conexao.execute('UPDATE produtos SET nome = ?, descricao = ?, preco = ?, img = ? WHERE id = ?', (nome, descricao, preco, novo_nome, id))
    conexao.commit()
    conexao.close()
    return redirect('/adm')

#Rota de busca
@admin_blueprint.route('/busca', methods=['post'])
def busca():
    busca = request.form['buscar']
    conexao = get_db_conexao()
    produtos = conexao.execute('SELECT * FROM produtos WHERE nome LIKE "%" || ? || "%"', (busca,)).fetchall()
    title = 'QUITANDA DO ZÉ'
    return render_template('index.html', title=title, produtos=produtos)    
