from flask import render_template, Blueprint
from database.conexao import iniciar_db, get_db_conexao
from session.session import verifica_sessao

home_blueprint = Blueprint('home', __name__, template_folder='templates')

@home_blueprint.route('/')
def index():
    iniciar_db()
    titulo = 'YOUTECH'
    conexao = get_db_conexao()
    vagas = conexao.execute('SELECT * FROM vagas ORDER BY id DESC').fetchall() #Seleciona todas as vagas do database e ordena-os em ordem decrescente
    conexao.close()
    #Verifica a sessão
    if verifica_sessao():
        login = True
    else:
        login = False
    return render_template('index.html', titulo=titulo, vagas=vagas, login=login)