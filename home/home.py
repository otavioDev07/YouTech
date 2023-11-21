from flask import Flask, render_template, Blueprint
from database.conexao import iniciar_db, get_db_conexao
from session.session import verifica_sessao

home_blueprint = Blueprint('home', __name__, template_folder='templates')


@home_blueprint.route("/")
def index():
    global verifica_sessao
    iniciar_db()
    conexao = get_db_conexao()
    produtos = conexao.execute('SELECT * FROM produtos ORDER BY id DESC').fetchall()
    conexao.close() 
    titulo = 'PÁGINA INICIAL'
    #Verifica a sessão
    if verifica_sessao():
        login = True
    else:
        login = False
    return render_template('index.html', titulo=titulo, produtos=produtos, login=login)