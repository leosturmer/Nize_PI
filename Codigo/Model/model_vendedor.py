import sqlite3


class Vendedor():
    def __init__(self, login, senha, nome, nome_loja=None):
        self.login = login
        self.senha = senha
        self.nome = nome
        self.nome_loja = nome_loja


def insert_vendedor(vendedor: Vendedor):
    'Insere um vendedor no banco de dados.'
    sql = '''
    INSERT INTO vendedor (login, senha, nome, nome_loja)
        VALUES (?, ?, ?, ?)
    '''

    sql_values_vendedor = [vendedor.login, vendedor.senha, vendedor.nome, vendedor.nome_loja]

    with sqlite3.connect('nize_database.db') as conexao:
        conexao.execute(sql, (sql_values_vendedor))

def select_vendedor(login):
    'Seleciona um vendedor pelo login no banco de dados.'
    sql_vendedor = '''
    SELECT id_vendedor, login, senha, nome, nome_loja
    FROM vendedor
    WHERE login = ?;
    '''

    with sqlite3.connect("nize_database.db") as conexao:
        cursor = conexao.execute(sql_vendedor, (login,))
        vendedor = cursor.fetchone()
        
        return vendedor
