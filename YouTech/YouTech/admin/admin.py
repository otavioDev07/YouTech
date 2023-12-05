from flask import render_template, Blueprint, request, redirect, session
from session.session import verifica_sessao
from database.conexao import iniciar_db, get_db_conexao
import uuid, os
from session.session import usuario, senha
from datetime import date
from shutil import rmtree

admin_blueprint = Blueprint('admin', __name__, template_folder='templates')


#Rota da página login
@admin_blueprint.route('/login')
def login():
    titulo = 'LOGIN'
    return render_template('login.html', titulo=titulo)

#Rota da validação do login
@admin_blueprint.route('/acesso', methods=['post'])
def valida_login():
    usuario_input = request.form['usuario']
    senha_input = request.form['senha']
    if usuario_input == usuario and senha_input == senha:
        session['login'] = True
        return redirect('/adm')
    else:
        return render_template('login.html', msg='Usuário/Senha estão incorretos!')

#Rota de renderização da página adm
@admin_blueprint.route('/adm')
def adm():
    if verifica_sessao():
        iniciar_db()
        conexao = get_db_conexao()
        vagas = conexao.execute('SELECT * FROM vagas ORDER BY id DESC').fetchall()
        conexao.close()
        titulo = 'ADMINISTRAÇÂO'

        hoje = date.today()
        invalidos = []  # Lista para armazenar a invalidade de cada vaga

        for row in vagas:
            data = row['data']
            year, month, day = map(int, data.split('-'))
            real_date = date(year, month, day)

            # Verifica se a data da vaga é anterior à data atual
            invalido = hoje > real_date
            invalidos.append(invalido)

            #Compreensão de lista para evitar o uso da função zip no template
            #A função zip vai agrupar esses elementos em tuplas onde o primeiro elemento é a vaga e o segundo é a validade dela. O loop 'for vaga, valido in' descompacta essa tupla nas variáveis vaga e valido. 'if valido' filtra as tuplas onde só há valido=TRUE. 'Vaga' é a variável final que será adicionada na lista válidos.
            invalidos = [vaga for vaga, validade in zip(vagas, invalidos) if validade]
        return render_template('adm.html', vagas=vagas, titulo=titulo, invalidos=invalidos)
    else:
        return redirect('/login')

#Rota para renderizar página de cadastro
@admin_blueprint.route('/cadvagas')
def cadvagas():
    if verifica_sessao():
        title = "CADASTRO DE VAGAS"
        return render_template('cadastro.html', title=title)
    else:
        return redirect('/login')

@admin_blueprint.route('/cadastro', methods=['post'])
def cadastro():
    if verifica_sessao():
        cargo = request.form['cargo']
        descricao = request.form['descricao']
        requisitos = request.form['requisitos']
        img = request.files['img']
        modalidade = request.form['modalidade']
        local = request.form['local']
        salario = request.form['salario']
        email = request.form['email']
        setor = request.form['setor']
        data = request.form['data']

        if img:
            id_img = str(uuid.uuid4().hex)
            filename = f"{id_img}_{cargo}.png"
            img.save('YouTech/static/img/img_vagas/'+filename)
            iniciar_db()
            conexao = get_db_conexao()
            conexao.execute('INSERT INTO vagas (cargo, descricao, requisitos, img, modalidade, local, salario, email, setor, data) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (cargo, descricao, requisitos, filename, modalidade, local, salario, email, setor, data,))
            conexao.commit()
            conexao.close()
        else:
            filename = "padrao.png"
            iniciar_db()
            conexao = get_db_conexao()
            conexao.execute('INSERT INTO vagas (cargo, descricao, requisitos, img, modalidade, local, salario, email, setor, data) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (cargo, descricao, requisitos, filename, modalidade, local, salario, email, setor, data,))
            conexao.commit()
            conexao.close()

        #Criação da pasta dos curriculos
        caminho_curriculo = os.path.join('YouTech/static/pdf/', cargo)
        if not os.path.exists(caminho_curriculo):
            os.makedirs(caminho_curriculo)

        return redirect('/adm')
    else:
        return redirect('/login')

#Rota para excluir
@admin_blueprint.route('/excluir/<id>/<cargo>')
def excluir(id, cargo):
    if verifica_sessao():
        id = int(id)
        iniciar_db()
        conexao = get_db_conexao()
        try:
            imagem = conexao.execute('SELECT img FROM vagas WHERE id = ?', (id,)).fetchone()
            if imagem['img'] != "padrao.png":
                caminho_imagem = os.path.join('YouTech/static/img/img_vagas/', imagem['img'])
                os.remove(caminho_imagem)
            conexao.execute('DELETE FROM vagas WHERE id = ?', (id,))
        except:
            conexao.execute('DELETE FROM vagas WHERE id = ?', (id,))
        finally:
            conexao.commit()
            conexao.close()

        caminho = os.path.join('YouTech/static/pdf/', cargo)
        if os.path.exists(caminho):
            rmtree(caminho)
        return redirect('/adm')
    else:
        return redirect('/login')

#Rota para renderizar a página de edição
@admin_blueprint.route('/chamar_edit/<id>')
def chamar_edit(id):
    if verifica_sessao():
        iniciar_db()
        conexao = get_db_conexao()
        vagas = conexao.execute('SELECT * FROM vagas WHERE id = ?', (id,)).fetchall()
        conexao.close()
        titulo = 'EDIÇÃO'
        return render_template('editar.html', vagas=vagas, titulo=titulo)
    else:
        return redirect('/login')

#Rota para editar as vagas
@admin_blueprint.route('/edit_vagas', methods=['POST'])
def editar():
    id = request.form['id']
    cargo = request.form['cargo']
    descricao = request.form['descricao']
    requisitos = request.form['requisitos']
    img = request.files['img']
    modalidade = request.form['modalidade']
    local = request.form['local']
    salario = request.form['salario']
    email = request.form['email']
    setor = request.form['setor']
    data = request.form['data']
    data = request.form['data']

    conexao = get_db_conexao()
    if img:
        id_img = str(uuid.uuid4().hex)
        filename = f"{id_img}_{cargo}.png"
        caminho_imagem = os.path.join('YouTech/static/img/img_vagas/', filename)
        imagem_antiga = conexao.execute('SELECT img FROM vagas WHERE id = ?', (id,)).fetchone() # Remove a imagem antiga, se existir
        if imagem_antiga['img'] != 'padrao.png':
            caminho_imagem_antiga = os.path.join('YouTech/static/img/img_vagas/', imagem_antiga['img'])
            if os.path.exists(caminho_imagem_antiga):
                os.remove(caminho_imagem_antiga)
            img.save(caminho_imagem)

    else:
        filename = conexao.execute('SELECT img FROM vagas WHERE id = ?', (id,)).fetchone()['img'] # Se nenhuma nova imagem for enviada, mantém a imagem existente
    conexao.execute('UPDATE vagas SET cargo = ?, descricao = ?, requisitos = ?, img = ?, modalidade = ?, local = ?, salario = ?, email = ?, setor = ?, data = ? WHERE id = ?', (cargo, descricao, requisitos, filename, modalidade, local, salario, email, setor, data, id,))
    conexao.commit()
    conexao.close()
    return redirect('/adm')

#Rota para ver os pdfs
@admin_blueprint.route('/ver_pdf/<id>')
def ver_pdf(id):
    iniciar_db()
    conexao = get_db_conexao()
    nome_vaga = conexao.execute('SELECT cargo FROM vagas WHERE id = ?', (id,)).fetchone()[0]
    id = conexao.execute('SELECT id FROM vagas WHERE id = ?', (id,)).fetchone()[0]
    pdf_files = [f for f in os.listdir(os.path.join('YouTech', 'static', 'pdf', nome_vaga))]
    return render_template('curriculos.html', pdf_files=pdf_files, nome_vaga=nome_vaga, id=id)

@admin_blueprint.route('/excluir_pdf/<id>/<nome_vaga>/<pdf>')
def excluir_pdf(id, nome_vaga, pdf):
    caminho = os.path.join('YouTech', 'static', 'pdf', nome_vaga, pdf )
    if os.path.exists(caminho):
        os.remove(caminho)
    return redirect(f'/ver_pdf/{id}')
#Rota de busca
@admin_blueprint.route('/busca', methods=['post'])
def busca():
    busca = request.form['buscar']
    conexao = get_db_conexao()
    validos = conexao.execute('SELECT * FROM vagas WHERE cargo LIKE "%" || ? || "%"', (busca,)).fetchall()
    title = 'YOUTECH'
    return render_template('index.html', title=title, validos=validos)






