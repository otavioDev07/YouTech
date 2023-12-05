from flask import Blueprint
import sqlite3 as sql
import os

database_blueprint = Blueprint('database', __name__)

#Conexão com o banco de dados
def get_db_conexao():
    db_path = os.path.join(database_blueprint.root_path, 'dados.db')
    conexao = sql.connect(db_path)
    conexao.row_factory = sql.Row
    return conexao

def iniciar_db():
    conexao = get_db_conexao()
    with database_blueprint.open_resource('esquema.sql', mode='r') as comandos:
        conexao.cursor().executescript(comandos.read())
    conexao.commit()
    conexao.close()