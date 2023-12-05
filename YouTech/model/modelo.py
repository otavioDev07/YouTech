from flask import render_template, Blueprint
from session.session import verifica_sessao

modelo_blueprint = Blueprint('modelo', __name__, template_folder='templates')

@modelo_blueprint.route('/modelo')
def modelo():
    global verifica_sessao
    titulo = 'PÁGINA MODELO'
    #Verifica a sessão
    if verifica_sessao():
        login = True
    else:
        login = False
    return render_template('model.html', titulo=titulo, login=login)