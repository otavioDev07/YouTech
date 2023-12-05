from flask import render_template, Blueprint, request
from database.conexao import iniciar_db, get_db_conexao
from session.session import verifica_sessao
from datetime import date

home_blueprint = Blueprint('home', __name__, template_folder='templates')

@home_blueprint.route('/')
@home_blueprint.route('/home')
def index():
    iniciar_db()
    titulo = 'YOUTECH'
    conexao = get_db_conexao()
    vagas = conexao.execute('SELECT * FROM vagas ORDER BY id DESC').fetchall()
    conexao.close()

    # Verifica a sessão
    if verifica_sessao():
        login = True
    else:
        login = False

    hoje = date.today()
    validos = []  # Lista para armazenar a validade de cada vaga

    for row in vagas:
        data = row['data']
        year, month, day = map(int, data.split('-'))
        real_date = date(year, month, day)

        # Verifica se a data da vaga é posterior à data atual
        valido = real_date > hoje
        validos.append(valido)

    #Compreensão de lista para evitar o uso da função zip no template
    #A função zip vai agrupar esses elementos em tuplas onde o primeiro elemento é a vaga e o segundo é a validade dela. O loop 'for vaga, valido in' descompacta essa tupla nas variáveis vaga e valido. 'if valido' filtra as tuplas onde só há valido=TRUE. 'Vaga' é a variável final que será adicionada na lista válidos.
    validos = [vaga for vaga, valido in zip(vagas, validos) if valido]
    return render_template('index.html', titulo=titulo, login=login, validos=validos)


@home_blueprint.route('/filtro', methods=['post'])
def filtrar():
    titulo = 'YouTech'
    setor = request.form.get('setor', '')
    modalidade = request.form.get('modalidade', '')
    conexao = get_db_conexao()

#Verificações dos filtros
    if modalidade == '':
        vagas = conexao.execute('SELECT * FROM vagas WHERE setor = ?', (setor,)).fetchall() 
        validos = verifica_data(vagas)
        
    elif setor == '':
        vagas = conexao.execute('SELECT * FROM vagas WHERE modalidade = ?', (modalidade,)).fetchall()
        validos = verifica_data(vagas)
    else:
        vagas = conexao.execute('SELECT * FROM vagas WHERE setor = ? AND modalidade = ?', (setor, modalidade,)).fetchall()
        validos = verifica_data(vagas)

    conexao.close()

    return render_template('index.html', validos=validos, titulo=titulo)


def verifica_data(vagas):
    hoje = date.today()
    validos = []  # Lista para armazenar a validade de cada vaga

    for row in vagas:
        data = row['data']
        year, month, day = map(int, data.split('-'))
        real_date = date(year, month, day)

        # Verifica se a data da vaga é posterior à data atual
        valido = real_date > hoje
        validos.append(valido)

    #Compreensão de lista para evitar o uso da função zip no template
    #A função zip vai agrupar esses elementos em tuplas onde o primeiro elemento é a vaga e o segundo é a validade dela. O loop 'for vaga, valido in' descompacta essa tupla nas variáveis vaga e valido. 'if valido' filtra as tuplas onde só há valido=TRUE. 'Vaga' é a variável final que será adicionada na lista válidos.
    validos = [vaga for vaga, valido in zip(vagas, validos) if valido]
    return validos