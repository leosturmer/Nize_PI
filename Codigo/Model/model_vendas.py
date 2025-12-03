import sqlite3


class Venda():
    def __init__(self, data, status, valor_final=0, comentario=None, produtos={}):
        self.data = data
        self.status = status
        self.valor_final = valor_final
        self.comentario = comentario
        self.produtos = produtos


def insert_venda(venda: Venda):
    'Insere uma venda no banco de dados.'
    sql = '''INSERT INTO vendas (data, status, valor_final, comentario)
        VALUES (?, ?, ?, ?)
        RETURNING id_venda;
        '''
    valor_final = 0

    sql_values_venda = [venda.data, venda.status,
                        venda.valor_final, venda.comentario]

    with sqlite3.connect('nize_database.db') as conexao:
        cursor = conexao.execute(sql, sql_values_venda)
        id_venda = cursor.fetchone()[0]

        sql = f'''
                INSERT INTO venda_produto (id_venda, id_produto, quantidade, valor_unitario)
                VALUES (:id_venda, :id_produto, :quantidade, (SELECT produtos.valor_unitario FROM produtos WHERE produtos.id_produto = :id_produto));

                '''

        produtos_quantidades = list()

        for prod_quant in venda.produtos.items():
            produtos_quantidades.append(
                {
                    'id_venda': id_venda,
                    'id_produto': prod_quant[0],
                    'quantidade': prod_quant[1],
                }
            )

        cursor.executemany(sql, tuple(produtos_quantidades))

        sql_total_venda = '''SELECT SUM(venda_produto.valor_unitario * venda_produto.quantidade) as total_venda
        FROM venda_produto
        WHERE venda_produto.id_venda = ?;   
    '''

        cursor = conexao.execute(sql_total_venda, (id_venda,))

        valor_final = cursor.fetchone()[0]

        sql_update_venda = f'''
        UPDATE vendas
        SET valor_final = {valor_final}
        WHERE id_venda = {id_venda};
    '''

        cursor = conexao.execute(sql_update_venda)

def listar_vendas():
    'Seleciona todas as vendas do banco de dados.'
    sql = '''
    SELECT id_venda, quantidade, data, valor_final, comentario, nome, valor_unitario, status

    FROM view_vendas;
    '''

    with sqlite3.connect('nize_database.db') as conexao:
        cursor = conexao.execute(sql)
        select_all = cursor.fetchall()

        vendas_dict = dict()

        for id_venda, quantidade, data, valor_final, comentario, nome, valor_unitario, status in select_all:
            if id_venda not in vendas_dict:
                vendas_dict[id_venda] = {
                    'produtos': [],
                    'data': data,
                    'valor_final': valor_final,
                    'comentario': comentario,
                    'status': status
                }
            vendas_dict[id_venda]['produtos'].append(
                (nome, quantidade, valor_unitario))

        return vendas_dict

def update_venda(id_venda, venda: Venda):
    'Atualiza uma venda no banco de dados.'
    consulta_valores = []
    valores = []

    if venda.data is not None:
        consulta_valores.append('data = ?')
        valores.append(venda.data)

    if venda.status is not None:
        consulta_valores.append('status = ?')
        valores.append(venda.status)

    if venda.comentario is not None:
        consulta_valores.append('comentario = ?')
        valores.append(venda.comentario)

    sql = f'''  
    UPDATE vendas

    SET {', '.join(consulta_valores)}

    WHERE id_venda = {id_venda}
    '''

    with sqlite3.connect('nize_database.db') as conexao:
        conexao.execute(sql, valores)

def delete_venda(id_venda):
    'Deleta uma venda do banco de dados.'
    sql_delete_tabela = '''
    DELETE FROM vendas
    WHERE id_venda = ?;
    '''

    sql_delete_relacao = '''
    DELETE FROM venda_produto
    WHERE id_venda = ?;
    '''

    with sqlite3.connect('nize_database.db') as conexao:
        conexao.execute(sql_delete_tabela, (id_venda, ))
        conexao.execute(sql_delete_relacao, (id_venda, ))
