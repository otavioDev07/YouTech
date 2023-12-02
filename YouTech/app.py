from flask import Flask
from home.home import home_blueprint
from admin.admin import admin_blueprint
from model.modelo import modelo_blueprint
from database.conexao import database_blueprint
from session.session import session_blueprint
from info.info_vaga import vaga_blueprint
    
app = Flask(__name__)
app.secret_key = 'YouTech'
#Conecta a blueprint importada no arquivo principal
app.register_blueprint(home_blueprint)
app.register_blueprint(admin_blueprint)
app.register_blueprint(modelo_blueprint)
app.register_blueprint(database_blueprint)
app.register_blueprint(session_blueprint)
app.register_blueprint(vaga_blueprint)


if __name__ == '__main__': # garante que o código dentro dele só será executado se este script estiver sendo executado diretamente como o programa principal.
    app.run(debug=True)