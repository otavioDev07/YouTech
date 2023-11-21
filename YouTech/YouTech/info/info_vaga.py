from flask import Blueprint, render_template
from database.conexao import get_db_conexao, iniciar_db

vaga_blueprint = Blueprint('vaga', __name__, template_folder='templates')

@vaga_blueprint.route('/ver_vaga')
def ver_vaga():
        titulo = 'DESCRIÇÃO DA VAGA'
        iniciar_db()
        conexao = get_db_conexao()
        conexao.execute('SELECT * FROM vagas ORDER BY id DESC').fetchall()
        conexao.close()
        return render_template('vaga.html', titulo=titulo)
