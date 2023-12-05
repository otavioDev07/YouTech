from flask import render_template, Blueprint, redirect, session

session_blueprint = Blueprint('session', __name__, template_folder='templates')

login = False
usuario = 'adm'
senha = '1234'
#GalerinhaDoRH
#4G4l3R1NH4D0RH3mU1T0l3G4l'
def verifica_sessao():
    if 'login' in session and session['login']: #Confirma se o indíce existe
        return True
    else:
        return False
    
if session:
    session.clear()


@session_blueprint.route("/login")
def login():
    titulo = 'LOGIN'
    return render_template('login.html', titulo=titulo)

@session_blueprint.route("/logoff")
def logoff():
    global login
    login = False
    session.clear()
    return redirect('/')