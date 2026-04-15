import sqlite3

def create_connection(db_file="database.db"):
    """ create a database connection to the SQLite database specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"[Connected to database: {db_file}]")
    except sqlite3.Error as e:
        print(e)

    return conn

def create_client_table(conn):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :return:
    """
    try:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS client (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT,
                identificacao TEXT,
                morada TEXT,
                data_nascimento TEXT,
                tipo_conta TEXT,
                finalidade TEXT,
                situacao_profissional TEXT,
                profissao TEXT,
                rendimento TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        conn.commit()
        print("[Table 'client' created successfully.]")
    except sqlite3.Error as e:
        print(e)

def create_transference_table(conn):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :return:
    """
    try:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS transference (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                iban_debito TEXT,
                nome_exportador TEXT,
                iban_beneficiario TEXT,
                bic_swift TEXT,
                montante_pagamento REAL,
                moeda TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        conn.commit()
        print("[Table 'transference' created successfully.]")
    except sqlite3.Error as e:
        print(e)

def insert_transference(conn, transference_data):
    """ insert a new transference into the transference table
    :param conn: Connection object
    :param transference_data: dictionary containing transference information
    :return:
    """
    create_transference_table(conn)  # Ensure the table exists before inserting data
    sql = '''     INSERT INTO transference (iban_debito, nome_exportador, iban_beneficiario, bic_swift, montante_pagamento, moeda)
        VALUES (?, ?, ?, ?, ?, ?) '''
    try:
        cur = conn.cursor()
        cur.execute(sql, (
            transference_data['iban_debito'],
            transference_data['nome_exportador'],
            transference_data['iban_beneficiario'],
            transference_data['bic_swift'],
            transference_data['montante_pagamento'],
            transference_data['moeda']
        ))
        conn.commit()
        print("[Transference data inserted successfully.]")
    except sqlite3.Error as e:
        print(e)

def insert_client(conn, client_data):
    """ insert a new client into the client table
    :param conn: Connection object
    :param client_data: dictionary containing client information
    :return:
    """

    create_client_table(conn)  # Ensure the table exists before inserting data
    sql = '''
        INSERT INTO client (nome, identificacao, morada, data_nascimento, tipo_conta, finalidade, situacao_profissional, profissao, rendimento)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''
    try:
        cur = conn.cursor()
        cur.execute(sql, (
            client_data['nome'],
            client_data['identificacao'],
            client_data['morada'],
            client_data['data_nascimento'],
            client_data['tipo_conta'],
            client_data['finalidade'],
            client_data['situacao_profissional'],
            client_data['profissao'],
            client_data['rendimento']
        ))
        conn.commit()
        print("[Client data inserted successfully.]")
    except sqlite3.Error as e:
        print(e)
