# IMPORTAÇÕES E INSTÂNCIAS DO FLASK
from flask import Flask, jsonify, request
app = Flask(__name__)

# ROTAS DA API
Criação de Rotas:
@app.route('/'): A rota principal, que neste exemplo retorna uma mensagem de boas-vindas.
@app.route('/api/transferencia_internacional', methods=['POST']): Uma rota que responde a um pedido HTTP POST.
@app.route('/api/cadastrar_client', methods=['POST']): Uma rota que responde a um pedido HTTP POST e recebe dados em formato JSON para o cadastro do client.

# DEFINIÇÃO DE FUNCÕES
home: Função que retorna uma mensagem simples.
hello: Função que retorna uma mensagem em formato JSON.
post_data: Função que recebe dados via POST, processa esses dados e os retorna em formato JSON com um código de status 201 (Created).

# RODAR A APLICAÇÃO
if __name__ == "__main__":
    app.run(host=172.31.43.173, port=5000, debug=True)

# BANCO DE DADOS

## SQLLITE
O banco de dados que está sendo usado é o SQLITE que se encontra na pasta data com  nome database.db


# PROBLEMAS
## CORS [Resolviso]
Parece que está a encontrar um problema relacionado com CORS (Cross-Origin Resource Sharing), que impede que o seu frontend faça uma requisição para um endpoint em um domínio diferente (ou seja, http://127.0.0.1:5500 para http://127.0.0.1). Para resolver isso, você pode configurar sua API para permitir requisições vindas de fontes diferentes.
Caso esteja a usar Flask, pode usar a extensão flask-cors para permitir requisições CORS. Veja como fazer isso:

# QUERIES
seguindo o mesmo método, como fazer as restantes requisicoes como Patch, put, post e delete?
