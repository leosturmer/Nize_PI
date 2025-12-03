import sqlite3

# ------------------------------ SQL ------------------------------
#
# ----------- Criação das tabelas
#

sql_table_vendedor = '''
    CREATE TABLE IF NOT EXISTS vendedor (
            id_vendedor INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            login TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL,
            nome TEXT NOT NULL,
            nome_loja TEXT NULL
    );
    '''

sql_table_produtos = '''
    CREATE TABLE IF NOT EXISTS produtos (
            id_produto INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            nome TEXT NOT NULL,
            valor_unitario REAL NOT NULL,

            quantidade INTEGER NULL,
            imagem TEXT NULL,
            aceita_encomenda INTEGER NULL,
            descricao TEXT NULL,
            valor_custo REAL NULL
    );
    '''

sql_table_encomendas = '''
    CREATE TABLE IF NOT EXISTS encomendas (
            id_encomenda INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            prazo TEXT NULL,
            status NOT NULL,
            comentario TEXT NULL
    );
    '''

sql_table_vendas = '''
    CREATE TABLE IF NOT EXISTS vendas (
            id_venda INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            data TEXT NOT NULL,
            valor_final REAL NOT NULL,
            status NOT NULL,
            comentario TEXT NULL
    );
    '''

# // Tabelas relacionais

sql_table_encomenda_produto = '''
    CREATE TABLE IF NOT EXISTS encomenda_produto (
        id_encomenda INTEGER NOT NULL,
        id_produto INTEGER NOT NULL,
        quantidade INTEGER NULL,

        FOREIGN KEY (id_encomenda)
                REFERENCES encomendas (id_encomenda)
        FOREIGN KEY (id_produto)
                REFERENCES produtos (id_produto)
    );
    '''

sql_table_venda_produtos = '''
    CREATE TABLE IF NOT EXISTS venda_produto (
        id_venda INTEGER NOT NULL,
        id_produto INTEGER NOT NULL,
        quantidade INTEGER NOT NULL,
        valor_unitario REAL NOT NULL,

        FOREIGN KEY (id_venda)
            REFERENCES vendas (id_venda)
        FOREIGN KEY (id_produto)
            REFERENCES produtos (id_produto)
    );
    '''

# // Views das tabelas

sql_view_produtos = '''
    CREATE VIEW IF NOT EXISTS view_produtos AS
        SELECT id_produto, nome, quantidade, valor_unitario, valor_custo, aceita_encomenda, descricao, imagem
        FROM produtos;
    '''

sql_view_encomendas = '''
    CREATE VIEW IF NOT EXISTS view_encomendas AS
        SELECT encomendas.id_encomenda, produtos.nome, encomenda_produto.quantidade, encomendas.prazo,  encomendas.status, encomendas.comentario

        FROM encomendas

        INNER JOIN encomenda_produto ON encomendas.id_encomenda = encomenda_produto.id_encomenda

        INNER JOIN produtos ON encomenda_produto.id_produto = produtos.id_produto;
    '''

sql_view_vendas = '''
    CREATE VIEW IF NOT EXISTS view_vendas AS 
        SELECT vendas.id_venda, produtos.nome, venda_produto.quantidade, vendas.data,  venda_produto.valor_unitario, vendas.valor_final, vendas.status, vendas.comentario

        FROM vendas

        INNER JOIN venda_produto ON vendas.id_venda = venda_produto.id_venda
        INNER JOIN produtos ON venda_produto.id_produto = produtos.id_produto;
    '''

# ----------- Inserção de tabelas no banco


def create_banco():

    with sqlite3.connect('nize_database.db') as conexao:
        conexao.execute(sql_table_vendedor)
        conexao.execute(sql_table_produtos)
        conexao.execute(sql_table_encomendas)
        conexao.execute(sql_table_vendas)
        conexao.execute(sql_table_encomenda_produto)
        conexao.execute(sql_table_venda_produtos)
        conexao.execute(sql_view_produtos)
        conexao.execute(sql_view_encomendas)
        conexao.execute(sql_view_vendas)

###################################################################################################

# ------------------------------ Classes ------------------------------

# // Classes banco de dados

###################################################################################################

# ------------------------------ Banco de dados ------------------------------

# ------------ Vendedor ------------
# ------------ Encomendas ------------
# ------------ Vendas ------------

# ////////// Não utilizados

# def visualizar_estoque():

#     sql = '''
#     SELECT nome, valor_unitario, quantidade, imagem, descricao, valor_custo 
#     FROM view_produtos
#     WHERE quantidade > 0;
#     '''

#     with sqlite3.connect('nize_database.db') as conexao:
#         cursor = conexao.execute(sql)
#         select_all = cursor.fetchall()

#         for nome, valor_unitario, quantidade, imagem, descricao, valor_custo in select_all:
#             print(f'''
#         Nome do produto: {nome} | Quantidade: {quantidade} 
#         Valor unitário: {valor_unitario} | Imagem: {imagem}
#         Valor de custo: {valor_custo} | Descrição: {descricao}
#         ''')


# def visualizar_esgotados():
#     sql = '''
#     SELECT nome, valor_unitario, quantidade, imagem, descricao, valor_custo 
#     FROM view_produtos
#     WHERE quantidade = 0 OR quantidade = Null;
#     '''
#     with sqlite3.connect('nize_database.db') as conexao:
#         cursor = conexao.execute(sql)
#         select_all = cursor.fetchall()

#         for nome, valor_unitario, quantidade, imagem, descricao, valor_custo in select_all:
#             print(f'''
#     Nome do produto: {nome} | Quantidade: {quantidade} 
#     Valor unitário: {valor_unitario} | Imagem: {imagem}
#     Valor de custo: {valor_custo} | Descrição: {descricao}
#     ''')

# def select_encomenda_produto(nome_produto):
#     sql = '''
#     SELECT id_encomenda, prazo, nome, quantidade, comentario, status

#     FROM view_encomendas
#     WHERE nome LIKE ?;
#     '''
#     with sqlite3.connect('nize_database.db') as conexao:
#         cursor = conexao.execute(sql, (f'%{nome_produto}%',))
#         select_all = cursor.fetchall()

#         for id_encomenda, prazo, nome, quantidade, comentario, status in select_all:
#             print(
#                 f'ID: {id_encomenda} | Produto: {nome} | Quantidade: {quantidade} | Prazo: {prazo} | Status: {status} | Comentário: {comentario}')


# def select_encomenda_prazo(prazo_encomenda):
#     sql = '''
#     SELECT id_encomenda, prazo, nome, quantidade, comentario, status

#     FROM view_encomendas
    
#     WHERE prazo LIKE ?;
#     '''

#     with sqlite3.connect('nize_database.db') as conexao:
#         cursor = conexao.execute(sql, (f'%{prazo_encomenda}%',))
#         select_all = cursor.fetchall()

#         for id_encomenda, prazo, nome, quantidade, comentario, status in select_all:
#             print(
#                 f'ID: {id_encomenda} | Nome: {nome} | Quantidade: {quantidade} | Prazo: {prazo} | Status: {status} | Comentário: {comentario}')

# ---------- Vendas



# def update_quantidade(quantidade_vendida, produto: Produto):
#     'Atualiza a quantidade de um produto no banco de dados.'
#     sql = '''UPDATE quantidade 
#     SET quantidade = ?
#     WHERE id_produto = ?;'''

#     sql_quantidade = "SELECT quantidade FROM produtos WHERE id_produto = ?;"
    
#     sql_subtracao = "SELECT ? - ? as difference;"


#     with sqlite3.connect('nize_database.db') as conexao:
#         quantidade_total = conexao.execute(sql_quantidade)

#         cursor = conexao.execute()


#     # https://www.beekeeperstudio.io/blog/sqlite-subtract

#     #         sql_total_venda = '''SELECT SUM(venda_produto.valor_unitario * venda_produto.quantidade) as total_venda
#     #     FROM venda_produto
#     #     WHERE venda_produto.id_venda = ?;   
#     # '''



# def select_produto_nome(nome_do_produto):
#     'Seleciona um produto pelo nome.'

#     sql = '''
#     SELECT id_produto, nome, quantidade, valor_unitario, valor_custo, aceita_encomenda, descricao, imagem
#     FROM view_produtos
#     WHERE nome LIKE ?;
#     '''

#     with sqlite3.connect('nize_database.db') as conexao:
#         cursor = conexao.execute(sql, (f'%{nome_do_produto}%',))
#         select_all = cursor.fetchall()

#         for id_produto, nome, quantidade, valor_unitario, valor_custo, aceita_encomenda, descricao, imagem in select_all:
#             print(f'''
#             Produto ID: {id_produto}
#             Nome: {nome} | Quantidade: {quantidade}
#             Valor unitário: {valor_unitario} | Valor custo: {valor_custo}
#             Aceita encomenda: {aceita_encomenda} | Descrição: {descricao}
#             ''')


# def select_produto_valor(valor_produto):  
    
#     sql = '''
#     SELECT id_produto, nome, quantidade, valor_unitario, valor_custo, aceita_encomenda, descricao, imagem 
#     FROM view_produtos
#     WHERE valor_unitario LIKE ?;
#     '''

#     with sqlite3.connect('nize_database.db') as conexao:
#         cursor = conexao.execute(sql, (f'%{valor_produto}%',))
#         select_all = cursor.fetchall()

#         for id_produto, nome, quantidade, valor_unitario, valor_custo, aceita_encomenda, descricao, imagem in select_all:
#             print(f'''
#             Produto ID: {id_produto}
#             Nome: {nome} | Quantidade: {quantidade}
#             Valor unitário: {valor_unitario} | Valor custo: {valor_custo}
#             Aceita encomenda: {aceita_encomenda} | Descrição: {descricao}
#             ''')


# def select_produto_quantidade(quantidade_produto):
#     sql = '''
#     SELECT id_produto, nome, quantidade, valor_unitario, valor_custo, aceita_encomenda, descricao, imagem 
#     FROM view_produtos
#     WHERE quantidade LIKE ?;
#     '''

#     with sqlite3.connect('nize_database.db') as conexao:
#         cursor = conexao.execute(sql, (f'%{quantidade_produto}%',))
#         select_all = cursor.fetchall()

#         for id_produto, nome, quantidade, valor_unitario, valor_custo, aceita_encomenda, descricao, imagem in select_all:
#             print(f'''
#             Produto ID: {id_produto}
#             Nome: {nome} | Quantidade: {quantidade}
#             Valor unitário: {valor_unitario} | Valor custo: {valor_custo}
#             Aceita encomenda: {aceita_encomenda} | Descrição: {descricao}
#             ''')


# def select_produto_descricao(descricao_produto):
#     sql = '''
#     SELECT id_produto, nome, quantidade, valor_unitario, valor_custo, aceita_encomenda, descricao, imagem 
#     FROM view_produtos
#     WHERE descricao LIKE ?;
#     '''
#     with sqlite3.connect('nize_database.db') as conexao:
#         cursor = conexao.execute(sql, (f'%{descricao_produto}%',))
#         select_all = cursor.fetchall()

#         for id_produto, nome, quantidade, valor_unitario, valor_custo, aceita_encomenda, descricao, imagem in select_all:
#             print(f'''
#             Produto ID: {id_produto}
#             Nome: {nome} | Quantidade: {quantidade}
#             Valor unitário: {valor_unitario} | Valor custo: {valor_custo}
#             Aceita encomenda: {aceita_encomenda} | Descrição: {descricao}
#             ''')


# def select_venda_data(data_venda):
#     sql = '''
#     SELECT id_venda, data, valor_final, comentario, nome, quantidade, valor_unitario, status

#     FROM view_vendas 

#     WHERE data LIKE ?;
#     '''
#     vendas_dict = dict()

#     with sqlite3.connect('nize_database.db') as conexao:
#         cursor = conexao.execute(sql, (f'%{data_venda}%',))
#         select_all = cursor.fetchall()

#         for id_venda, data, valor_final, comentario, nome, quantidade, valor_unitario, status in select_all:
#             if id_venda not in vendas_dict:
#                 vendas_dict[id_venda] = {
#                     'produtos': [],
#                     'data': data,
#                     'valor_final': valor_final,
#                     'comentario': comentario,
#                     'status': status
#                 }
#             vendas_dict[id_venda]['produtos'].append(
#                 (nome, quantidade, valor_unitario))

#         for id_venda, detalhes in vendas_dict.items():
#             nome_produtos = [', '.join([f'Produto: {nome} | Quantidade: {quantidade} | Valor unitário: R${valor_unitario}'])
#                              for nome, quantidade, valor_unitario in detalhes['produtos']]

#             print(f'''
#     Venda ID {id_venda}:
#     Produtos:
#     {'\n'.join(nome_produtos)} 
#     Valor final: {valor_final} | Status: {status}
#     Data da venda: {data} | Comentários: {comentario}
#     ''')


# def select_venda_produto(nome_produto):
#     sql = '''
#     SELECT id_venda, data, valor_final, comentario, nome, quantidade, valor_unitario, status

#     FROM view_vendas 

#     WHERE nome LIKE ?;
#     '''

#     vendas_dict = dict()

#     with sqlite3.connect('nize_database.db') as conexao:
#         cursor = conexao.execute(sql, (f'%{nome_produto}%',))
#         select_all = cursor.fetchall()

#         for id_venda, data, valor_final, comentario, nome, quantidade, valor_unitario, status in select_all:
#             if id_venda not in vendas_dict:
#                 vendas_dict[id_venda] = {
#                     'produtos': [],
#                     'data': data,
#                     'valor_final': valor_final,
#                     'comentario': comentario,
#                     'status': status
#                 }
#             vendas_dict[id_venda]['produtos'].append(
#                 (nome, quantidade, valor_unitario))

#         for id_venda, detalhes in vendas_dict.items():
#             nome_produtos = [', '.join([f'Produto: {nome} | Quantidade: {quantidade} | Valor unitário: R${valor_unitario}'])

#                              for nome, quantidade, valor_unitario in detalhes['produtos']]

#             print(f'''
#     Venda ID {id_venda}:
#     Produtos:
#     {'\n'.join(nome_produtos)} 
#     Valor final: {valor_final} | Status: {status}
#     Data da venda: {data} | Comentários: {comentario}
#     ''')


# ------------ Updates ------------

# def update_vendedor(id_vendedor, login=None, senha=None, nome=None, nome_loja=None):
    # consulta_valores = []
    # valores = []

    # if login is not None:
    #     consulta_valores.append('login = ?')
    #     valores.append(login)

    # if senha is not None:
    #     consulta_valores.append('senha = ?')
    #     valores.append(senha)

    # if nome is not None:
    #     consulta_valores.append('nome = ?')
    #     valores.append(nome)

    # if nome_loja is not None:
    #     consulta_valores.append('nome_loja = ?')
    #     valores.append(nome_loja)

    # sql = f'''
    # UPDATE vendedor

    # SET {', '.join(consulta_valores)}

    # WHERE id_vendedor = {id_vendedor}
    # '''

    # with sqlite3.connect('nize_database.db') as conexao:
    #     conexao.execute(sql, valores)


# ------------ Deletes ------------


# def delete_vendedor(login):
#     sql_delete = '''
#     DELETE FROM produtos
#     WHERE login = ?;
#     '''
#     with sqlite3.connect("nize_database.db") as conexao:
#         conexao.execute(sql_delete, (login))
