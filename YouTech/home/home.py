from flask import Flask, render_template, Blueprint
from database.conexao import iniciar_db, get_db_conexao
from session.session import verifica_sessao

home_blueprint = Blueprint('home', __name__, template_folder='templates')

@home_blueprint.route('/')
def index():
    title = 'YOUTECH'