from flask import render_template, Blueprint, request, redirect, session
from session.session import verifica_sessao
from database.conexao import iniciar_db, get_db_conexao 
import uuid, os
from werkzeug.utils import secure_filename

usuario = 'adm'
senha = '1234'
admin_blueprint = Blueprint('admin', __name__, template_folder='templates')

