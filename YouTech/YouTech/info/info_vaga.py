from flask import Blueprint, render_template
from database.conexao import get_db_conexao, iniciar_db

vaga_blueprint = Blueprint('vaga', __name__, template_folder='templates')

@vaga_blueprint.route('/ver_vaga/<id>')
def ver_vaga(id):
        titulo = 'DESCRIÇÃO DA VAGA'
        iniciar_db()
        conexao = get_db_conexao()
        vaga = conexao.execute('SELECT * FROM vagas WHERE id = ?', (id,)).fetchall()
        conexao.close()
        return render_template('vaga.html', titulo=titulo, vaga=vaga)
