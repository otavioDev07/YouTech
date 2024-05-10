# Projeto Integrador: CRUD em Programação Web


## Descrição


Este é um projeto integrador entre as disciplinas de Programação Web Front-End e Programação Web Back-End feito em parceria. O objetivo principal é construir a página de divulgação de vagas de uma empresa fictícia de tecnologia, com operações CRUD (Criar, Ler, Atualizar, Excluir) para gerenciar a postagem de vagas. As funções foram divididas entre a dupla, enquanto meu foco foi no back-end, meu parceiro (Adillan07) trabalhou no front-end. O projeto enfatiza a integração de tecnologias e conceitos aprendidos em ambas as disciplinas, incluindo o uso do Git e do GitHub para controle de versão, extensão LiveShare do VSCode para trabalhar em parceria, Flask como o framework back-end, e HTML/CSS com Bootstrap para o front-end. Como diferencial, utilizo o Blueprint (Design Pattern) do Flask.


## Tecnologias Utilizadas


- Git: Sistema de controle de versão para gerenciar o código do projeto.
- GitHub: Plataforma online para hospedar o repositório do projeto e facilitar a colaboração.
- Flask: Framework web em Python para o desenvolvimento do lado do servidor.
- HTML e CSS (Bootstrap): Linguagens de marcação e estilização para criar o front-end do aplicativo.
- SQLite (Banco de Dados): Utilizaremos um banco de dados SQL para armazenar e recuperar informações sobre os produtos. Isso inclui a criação de tabelas, inserção de dados e consulta de informações.
- Blueprint: Design Pattern para divisão do projeto em módulos, a fim de facilitar a organização e visualização.

## Funcionalidades Principais


O aplicativo terá as seguintes funcionalidades:


- **Visualização de Vagas**: Os usuários podem visualizar a lista de vagas disponíveis.

- **Pesquisa de Vagas**: Os usuários podem pesquisar vagas com base no nome do produto.

- **Filtração**: Os usuários podem filtrar as vagas que deseja com base em dois campos, setor e modalidade da vaga.

- **Vizualização e Currículo**: Ao clicar sobre a vaga, o usuário poderá observar as informações vaga e enviar seu currículo em um formulário.

- **Administração de Vagas**: O administrador do sistema pode (Usuário: adm; Senha: 1234):
  - Cadastrar novas vagas (Diferecial de uma função específica para horário, se a data expirar, a vaga desaparece para o usuário).
  - Editar informações de vagas existentes.
  - Excluir vagas do sistema.
  - Vizualizar currículos enviados e apagá-los.


## Instruções de Configuração


Para configurar e executar o projeto em sua máquina local, siga estas etapas:


1. **Clone o Repositório**:
   1. git clone https://github.com/otavioDev07/YouTech.git
   2. cd YouTech
2. **Instale Dependências**:
   1. Em seu console digite o comando: 'pip install Flask'
3. **Execute o Aplicativo**:
   1. python app.py
4. **Acesse o Aplicativo no Navegador**:
   1. Abra um navegador da web e acesse `http://localhost:5000` para visualizar o aplicativo.
  
5. **Alternativa**
   1. Se preferir, acesse o [app em produção](otavioDev.pythonanywhere.com)

## Estrutura do Projeto


- `app.py`: O código principal do aplicativo Flask.
- `templates/`: Diretório contendo os modelos HTML.
- `static/`: Diretório contendo arquivos estáticos, como CSS, imagens e currículos.
- `database/`: Diretório contendo os arquivos referentes ao banco de dados.
- `esquema.sql`: Arquivo com dados iniciais de produtos.
- `home/`: Diretório contendo os arquivos referentes à página principal.
- `admin/`: Diretório contendo os arquivos referentes as funções de admnistrador (CRUD)
- `info/`: Diretório contendo os arquivos referentes a página de visualização da vaga.
- `model`: Diretório contendo os arquivos referentes à página modelo.
- `session`: Diretório contendo os arquivos referentes ao controle de sessão.

## Licença


Este projeto é fornecido sob a Licença [MIT](LICENSE).


## Contribuições


Contribuições são bem-vindas. Sinta-se à vontade para fazer um fork do repositório e abrir um Pull Request com melhorias, correções ou novos recursos.


## Contato


- Rafael Ribas: Instrutor de Programação Web Front-End.


- João Paulo: Instrutor de Programação Web Back-End.

- Otávio Neto: Autor
- Ádillan Soares: Autor
