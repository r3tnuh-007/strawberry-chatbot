import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from carregar_pdf import processar_pdf
from sql_connection.sql_connection import *
import asyncio

app = Flask(__name__)
CORS(app)  # Permite CORS para comunicação com o frontend

# Configurações
UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

clientes = [
    {
        "nif": "245889123",
        "conta": "PT50 0001 0000 1234 5678 9",
        "morada": "Rua Antiga, 123",
        "codigo_postal": "1000-001",
        "localidade": "Lisboa",
        "telemovel": "910000000",
        "email": "antigo@exemplo.com"
    }
]

@app.route('/clientes', methods=['GET'])
def listar_clientes():
    return jsonify(clientes)

@app.route('/clientes/<string:nif>', methods=['PUT'])
def atualizar_cliente(nif):
    dados = request.json
    
    # Procura o cliente pelo NIF
    for cliente in clientes:
        if cliente['nif'] == nif:
            # Atualiza os campos enviados
            cliente.update({
                "morada": dados.get('morada', cliente['morada']),
                "codigo_postal": dados.get('codigo_postal', cliente['codigo_postal']),
                "localidade": dados.get('localidade', cliente['localidade']),
                "telemovel": dados.get('telemovel', cliente['telemovel']),
                "email": dados.get('email', cliente['email'])
            })
            return jsonify({"message": "Cliente atualizado com sucesso!", "cliente": cliente}), 200
            
    return jsonify({"message": "Cliente não encontrado"}), 404

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def index():
    return """<h1>API is running</h1>
              <p>Use POST /api/cadastrar_client to send data.</p>
              <p>Use POST /api/transferencia_internacional to send transfer data.</p>
           """

@app.route('/api/transferencia_internacional', methods=['POST'])
def transferencia_internacional():
    data = {
        "iban_debito": request.form.get('ibanDebito'),
        "nome_exportador": request.form.get('nomeExportador'),
        "iban_beneficiario": request.form.get('ibanBeneficiario'),
        "bic_swift": request.form.get('bicSwift'),
        "montante_pagamento": request.form.get('montantePagamento'),
        "moeda": request.form.get('moeda')
    }
    conn = create_connection("data/database.db")
    insert_transference(conn, data)
    conn.close()
    print("🟢 - Received transfer data")
    return jsonify({"message": "Transfer data received successfully!", "data": data}), 200

# Rota para receber os dados
@app.route('/api/cadastrar_client', methods=['POST'])
def cadastrar_client():
    # Verifica se há ficheiros no formulário
    if 'documentos[id][file]' not in request.files:
        return jsonify({"error": "No file part"}), 400

    id_file = request.files['documentos[id][file]']
    #morada_file = request.files['documentos[morada][file]']

    if id_file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if id_file and allowed_file(id_file.filename):
        id_filename = secure_filename(id_file.filename)
        #morada_filename = secure_filename(morada_file.filename)
        id_file.save(os.path.join(app.config['UPLOAD_FOLDER'], id_filename))
        #morada_file.save(os.path.join(app.config['UPLOAD_FOLDER'], morada_filename))
        bi_data = processar_pdf(id_filename, rule="BI").split("|")
        #morada_data = processar_pdf(morada_filename, rule="Morada").split("|")
        print("🟢 - Extracted BI data:", bi_data)
        #print("🟢 - Extracted Morada data:", morada_data)

        data = {
            "nome": bi_data[0],
            "identificacao": bi_data[1],
            "morada": bi_data[2],
            "data_nascimento": bi_data[3],
            "tipo_conta": request.form.get('tipoConta'),
            "finalidade": request.form.get('finalidade'),
            "finalidade_outros": request.form.get('finalidadeOutros'),
            "situacao_profissional": request.form.get('situacaoProfissional'),
            "profissao": request.form.get('profissao'),
            "rendimento": request.form.get('rendimento'),
            "documentos": {
                "id": {"status": request.form.get('documentos[id][status]'), "file": id_filename}
            },
            "consentimentos": {
                "termos": request.form.get('consentimentos[termos]') == 'true',
                "veracidade": request.form.get('consentimentos[veracidade]') == 'true'
            }
        }
        print()
        conn = create_connection("data/database.db")
        insert_client(conn, data)
        conn.close()
        return jsonify({"message": "Data received successfully!", "data": data}), 200

    return jsonify({"error": "Invalid file type"}), 400

if __name__ == '__main__':
    # Cria o diretório de upload, se não existir
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    app.run(host='0.0.0.0', port=5000, debug=True)
