import sqlite3


class Encomenda():
    def __init__(self, status, prazo=None, comentario=None, produtos=[]):

        self.status = status
        self.prazo = prazo
        self.comentario = comentario
        self.produtos = produtos


def insert_encomenda(encomenda: Encomenda):
    'Insere uma encomenda no banco de dados.'

    sql_insert_encomenda = '''INSERT INTO encomendas (status, prazo, comentario) 
            VALUES (?, ?, ?)
            RETURNING id_encomenda
            '''

    sql_insert_encomenda_produto = '''
            INSERT INTO encomenda_produto (id_encomenda, id_produto, quantidade)
            VALUES (?, ?, ?);
            '''

    sql_values_encomenda = [encomenda.status,
                            encomenda.prazo, encomenda.comentario]

    with sqlite3.connect('nize_database.db') as conexao:
        cursor = conexao.execute(sql_insert_encomenda, sql_values_encomenda)

        id_encomenda = cursor.fetchone()[0]

        produtos = encomenda.produtos

        lista = []

        for item in produtos.items():
            id_produto, quantidade = item
            lista.append((id_encomenda, id_produto, quantidade))

        cursor.executemany(sql_insert_encomenda_produto, lista)

def select_encomenda_id(id_encomenda):
    'Seleciona uma encomenda pelo ID no banco de dados.'
    sql = '''
    SELECT id_encomenda, prazo, nome, quantidade, comentario, status

    FROM view_encomendas
    WHERE id_encomenda = ?;
    '''

    with sqlite3.connect('nize_database.db') as conexao:
        cursor = conexao.execute(sql, (id_encomenda,))
        encomenda = cursor.fetchone()
        return encomenda

def select_encomenda_status(status):
    'Seleciona encomenda pelo status no banco de dados.'
    sql = '''
    SELECT id_encomenda, prazo, nome, quantidade, comentario, status

    FROM view_encomendas
    
    WHERE status = ?;
    '''

    with sqlite3.connect('nize_database.db') as conexao:
        cursor = conexao.execute(sql, (f'%{status}%',))
        select_all = cursor.fetchall()

        encomendas_dict = {}

        for id_encomenda, prazo, nome, quantidade, comentario, status in select_all:
            if id_encomenda not in encomendas_dict:
                encomendas_dict[id_encomenda] = {
                    'produtos': [],
                    'prazo': prazo,
                    'comentario': comentario,
                    'status': status
                }

            encomendas_dict[id_encomenda]['produtos'].append(
                (nome, quantidade))

        return encomendas_dict

def listar_encomendas():
    sql = '''
    SELECT id_encomenda, prazo, nome, quantidade, comentario, status

    FROM view_encomendas;
    '''

    with sqlite3.connect('nize_database.db') as conexao:
        cursor = conexao.execute(sql)
        select_all = cursor.fetchall()

        encomendas_dict = {}

        for id_encomenda, prazo, nome, quantidade, comentario, status in select_all:
            if id_encomenda not in encomendas_dict:
                encomendas_dict[id_encomenda] = {
                    'produtos': [],
                    'prazo': prazo,
                    'comentario': comentario,
                    'status': status
                }

            encomendas_dict[id_encomenda]['produtos'].append(
                (nome, quantidade))

        return encomendas_dict

def update_encomendas(id_encomenda, encomenda: Encomenda):
    'Atualiza uma encomenda no banco de dados.'
    consulta_valores = []
    valores = []

    if encomenda.status is not None:
        consulta_valores.append('status = ?')
        valores.append(encomenda.status)

    if encomenda.prazo is not None:
        consulta_valores.append('prazo = ?')
        valores.append(encomenda.prazo)

    if encomenda.comentario is not None:
        consulta_valores.append('comentario = ?')
        valores.append(encomenda.comentario)

    sql = f'''  
    UPDATE encomendas

    SET {', '.join(consulta_valores)}

    WHERE id_encomenda = {id_encomenda}
    '''

    with sqlite3.connect('nize_database.db') as conexao:
        conexao.execute(sql, valores)

def delete_encomenda(id_encomenda):
    'Deleta uma encomenda do banco de dados.'
    sql_delete_tabela = '''
    DELETE FROM encomendas
    WHERE id_encomenda = ?;
    '''

    sql_delete_relacao = '''
    DELETE FROM encomenda_produto
    WHERE id_encomenda = ?;
    '''

    with sqlite3.connect('nize_database.db') as conexao:
        conexao.execute(sql_delete_tabela, (id_encomenda, ))
        conexao.execute(sql_delete_relacao, (id_encomenda, ))

