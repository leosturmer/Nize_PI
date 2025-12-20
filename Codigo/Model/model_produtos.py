import sqlite3

class Estoque():
    def __init__(self, produtos=[]):
        self.produtos = produtos

class Produto():
    def __init__(self, id_produto, nome=None, valor_unitario=None, quantidade=0, imagem=None, aceita_encomenda=0, descricao=None, valor_custo=None):
        self.id_produto = id_produto
        self.nome = nome
        self.valor_unitario = valor_unitario
        self.quantidade = quantidade
        self.imagem = imagem
        self.aceita_encomenda = aceita_encomenda
        self.descricao = descricao
        self.valor_custo = valor_custo


# ------------ Produtos ------------


def insert_produto(produto: Produto):
    'Insere um produto no banco de dados.'

    sql = '''
    INSERT INTO produtos (id_produto, nome, valor_unitario, quantidade, imagem, aceita_encomenda, descricao, valor_custo) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    '''

    if produto.imagem == '':
        produto.imagem = None

    if produto.aceita_encomenda == '':
        produto.aceita_encomenda = 2

    if produto.descricao == '':
        produto.descricao = None

    if produto.valor_custo == '':
        produto.valor_custo = None

    with sqlite3.connect('nize_database.db') as conexao:
        conexao.execute(sql, (produto.id_produto, produto.nome, produto.valor_unitario, produto.quantidade,
                        produto.imagem, produto.aceita_encomenda, produto.descricao, produto.valor_custo))

def update_produto(produto: Produto):
    'Atualiza um produto no banco de dados.'

    consulta_valores = []
    valores = []

    if produto.nome is not None:
        consulta_valores.append('nome = ?')
        valores.append(produto.nome)

    if produto.valor_unitario is not None:
        consulta_valores.append('valor_unitario = ?')
        valores.append(produto.valor_unitario)

    if produto.quantidade is not None:
        consulta_valores.append('quantidade = ?')
        valores.append(produto.quantidade)

    if produto.imagem is not None:
        consulta_valores.append('imagem = ?')
        valores.append(produto.imagem)

    if produto.aceita_encomenda is not None:
        consulta_valores.append('aceita_encomenda = ?')
        valores.append(produto.aceita_encomenda)

    if produto.descricao is not None:
        consulta_valores.append('descricao = ?')
        valores.append(produto.descricao)

    if produto.valor_custo is not None:
        consulta_valores.append('valor_custo = ?')
        valores.append(produto.valor_custo)

    sql = f'''
    UPDATE produtos

    SET {', '.join(consulta_valores)}

    WHERE id_produto = {produto.id_produto}
    '''

    with sqlite3.connect('nize_database.db') as conexao:
        conexao.execute(sql, valores)

def delete_produto(produto: Produto):
    'Deleta um produto do banco de dados.'
    sql_delete = '''
    DELETE FROM produtos
    WHERE id_produto = ?;
    '''

    with sqlite3.connect('nize_database.db') as conexao:
        conexao.execute(sql_delete, (produto.id_produto,))

def listar_produtos(estoque: Estoque):
    'Seleciona todos os produtos do banco de dados.'
    sql = '''
    SELECT id_produto, nome, valor_unitario, quantidade, imagem, aceita_encomenda, descricao, valor_custo
        FROM view_produtos;
    '''
    produtos_dict = dict()
    lista_de_produtos = []

    with sqlite3.connect('nize_database.db') as conexao:
        cursor = conexao.execute(sql)
        select_all = cursor.fetchall()

    for id_produto, nome, valor_unitario, quantidade, imagem, aceita_encomenda, descricao, valor_custo in select_all:
        if id_produto not in produtos_dict:
            produtos_dict[id_produto] = {
                'nome': nome,
                'valor_unitario': valor_unitario,
                'quantidade': quantidade,
                'imagem': imagem,
                'aceita_encomenda': aceita_encomenda,
                'descricao': descricao,
                'valor_custo': valor_custo
            }
            lista_de_produtos.append((nome, id_produto))

            estoque.produtos = lista_de_produtos

    return estoque.produtos

def listar_produtos_encomenda(estoque: Estoque):
    'Seleciona todos os produtos que aceiam encomenda no banco de dados.'
    sql = '''
    SELECT id_produto, nome, valor_unitario, quantidade, imagem, aceita_encomenda, descricao, valor_custo
        FROM view_produtos
        
    WHERE aceita_encomenda = 1;
    '''
    produtos_dict = dict()
    lista_de_produtos = list()

    with sqlite3.connect('nize_database.db') as conexao:
        cursor = conexao.execute(sql)
        select_all = cursor.fetchall()

    for id_produto, nome, valor_unitario, quantidade, imagem, aceita_encomenda, descricao, valor_custo in select_all:
        if id_produto not in produtos_dict:
            produtos_dict[id_produto] = {
                'nome': nome,
                'valor_unitario': valor_unitario,
                'quantidade': quantidade,
                'imagem': imagem,
                'aceita_encomenda': aceita_encomenda,
                'descricao': descricao,
                'valor_custo': valor_custo
            }
            lista_de_produtos.append((nome, id_produto))

            estoque.produtos = lista_de_produtos

    return estoque.produtos

def select_produto_id(produto: Produto):
    'Seleciona um produto pelo ID no banco de dados.'

    sql = '''
    SELECT id_produto, nome, quantidade, valor_unitario, valor_custo, aceita_encomenda, descricao, imagem
    FROM view_produtos
    WHERE id_produto = ?;
    '''

    with sqlite3.connect('nize_database.db') as conexao:
        cursor = conexao.execute(sql, (produto.id_produto,))
        return cursor.fetchone()

def select_produto_nome(nome_do_produto):
    'Seleciona um produto pelo nome.'
    
    sql = '''
    SELECT id_produto, nome, quantidade, valor_unitario, valor_custo, aceita_encomenda, descricao, imagem
    FROM view_produtos
    WHERE nome = ?;
    '''

    with sqlite3.connect('nize_database.db') as conexao:
        cursor = conexao.execute(sql, (f'{nome_do_produto}',))
        produto = cursor.fetchone()
        return produto

def select_produto_nome_all(nome_pesquisado, estoque:Estoque):
    'Seleciona todos produto pelo nome digitado.'
    
    sql = '''
    SELECT id_produto, nome, valor_unitario, quantidade, imagem, aceita_encomenda, descricao, valor_custo
    FROM view_produtos
    WHERE nome LIKE ?;
    '''
    produtos_dict = dict()
    lista_de_produtos = []

    with sqlite3.connect('nize_database.db') as conexao:
        cursor = conexao.execute(sql, (f'%{nome_pesquisado}%',))
        select_all = cursor.fetchall()

    for id_produto, nome, valor_unitario, quantidade, imagem, aceita_encomenda, descricao, valor_custo in select_all:
        if id_produto not in produtos_dict:
            produtos_dict[id_produto] = {
                'nome': nome,
                'valor_unitario': valor_unitario,
                'quantidade': quantidade,
                'imagem': imagem,
                'aceita_encomenda': aceita_encomenda,
                'descricao': descricao,
                'valor_custo': valor_custo
            }
            lista_de_produtos.append((nome, id_produto))

            estoque.produtos = lista_de_produtos

    return estoque.produtos

def select_produto_quantidade_minima(quantidade_produto, estoque:Estoque): ##########################
    sql = '''
    SELECT id_produto, nome, quantidade, valor_unitario, valor_custo, aceita_encomenda, descricao, imagem 
    FROM view_produtos
    WHERE quantidade LIKE ?;
    '''

    produtos_dict = dict()
    lista_de_produtos = []

    with sqlite3.connect('nize_database.db') as conexao:
        cursor = conexao.execute(sql, (f'%{quantidade_produto}%',))
        select_all = cursor.fetchall()

    for id_produto, nome, valor_unitario, quantidade, imagem, aceita_encomenda, descricao, valor_custo in select_all:
        if id_produto not in produtos_dict:
            produtos_dict[id_produto] = {
                'nome': nome,
                'valor_unitario': valor_unitario,
                'quantidade': quantidade,
                'imagem': imagem,
                'aceita_encomenda': aceita_encomenda,
                'descricao': descricao,
                'valor_custo': valor_custo
            }
            lista_de_produtos.append((nome, id_produto))

            estoque.produtos = lista_de_produtos

    return estoque.produtos


def select_produto_quantidade_maxima(quantidade_produto, estoque:Estoque): #########################
    sql = '''
    SELECT id_produto, nome, quantidade, valor_unitario, valor_custo, aceita_encomenda, descricao, imagem 
    FROM view_produtos
    WHERE quantidade = ?;
    '''

    produtos_dict = dict()
    lista_de_produtos = []

    with sqlite3.connect('nize_database.db') as conexao:
        cursor = conexao.execute(sql, (f'%{quantidade_produto}%',))
        select_all = cursor.fetchall()

    for id_produto, nome, valor_unitario, quantidade, imagem, aceita_encomenda, descricao, valor_custo in select_all:
        if id_produto not in produtos_dict:
            produtos_dict[id_produto] = {
                'nome': nome,
                'valor_unitario': valor_unitario,
                'quantidade': quantidade,
                'imagem': imagem,
                'aceita_encomenda': aceita_encomenda,
                'descricao': descricao,
                'valor_custo': valor_custo
            }
            lista_de_produtos.append((nome, id_produto))

            estoque.produtos = lista_de_produtos

    return estoque.produtos

def select_produto_descricao(descricao_produto, estoque:Estoque):
    sql = '''
    SELECT id_produto, nome, quantidade, valor_unitario, valor_custo, aceita_encomenda, descricao, imagem 
    FROM view_produtos
    WHERE descricao LIKE ?;
    '''

    produtos_dict = dict()
    lista_de_produtos = []

    with sqlite3.connect('nize_database.db') as conexao:
        cursor = conexao.execute(sql, (f'%{descricao_produto}%',))
        select_all = cursor.fetchall()

    for id_produto, nome, valor_unitario, quantidade, imagem, aceita_encomenda, descricao, valor_custo in select_all:
        if id_produto not in produtos_dict:
            produtos_dict[id_produto] = {
                'nome': nome,
                'valor_unitario': valor_unitario,
                'quantidade': quantidade,
                'imagem': imagem,
                'aceita_encomenda': aceita_encomenda,
                'descricao': descricao,
                'valor_custo': valor_custo
            }
            lista_de_produtos.append((nome, id_produto))

            estoque.produtos = lista_de_produtos

    return estoque.produtos