from flask import Blueprint, render_template, request, redirect
from session.session import verifica_sessao
import uuid, os
from database.conexao import get_db_conexao, iniciar_db

vaga_blueprint = Blueprint('vaga', __name__, template_folder='templates')

@vaga_blueprint.route('/ver_vaga/<id>')
def ver_vaga(id):
        titulo = 'DESCRIÇÃO DA VAGA'
        if verifica_sessao():
                login = True
        else:
                login = False
        iniciar_db()
        conexao = get_db_conexao()
        vaga = conexao.execute('SELECT * FROM vagas WHERE id = ?', (id,)).fetchall()
        conexao.close()
        return render_template('vaga.html', titulo=titulo, vaga=vaga, login=login)


@vaga_blueprint.route('/pdf/<id>', methods=['post'])
def salvar_pdf(id):
        global cargo, caminho_curriculo
        pdf = request.files['pdf']
        if pdf:
                if pdf.filename != '':
                        iniciar_db()
                        conexao = get_db_conexao()
                        cargo = conexao.execute('SELECT cargo FROM vagas WHERE id = ?', (id,)).fetchone()
                        cargo = cargo['cargo']
                        id_pdf = str(uuid.uuid4().hex)
                        name_pdf = f"{id_pdf}_{cargo}.pdf"
                        caminho_curriculo = os.path.join('YouTech/static/pdf/', cargo)
                        if os.path.exists(caminho_curriculo):
                                pdf.save(caminho_curriculo + '/' + name_pdf)
                        return redirect('/')
                else:
                        return redirect('/')


        


