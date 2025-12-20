from Model import (model_vendedor, model_vendas, model_encomendas, model_produtos)

# // Inserts

def insert_vendedor(login, senha, nome, nome_loja=None):
    'Encapsula informações para inserir vendedor no banco de dados.'
    novo_vendedor = model_vendedor.Vendedor(login=login, senha=senha, nome=nome, nome_loja=nome_loja)

    model_vendedor.insert_vendedor(novo_vendedor)

def insert_produto(id_produto, nome, valor_unitario, quantidade, imagem, aceita_encomenda, descricao, valor_custo):
    'Encapsula informações para inserir produto no banco de dados.'

    novo_produto = model_produtos.Produto(id_produto, nome, valor_unitario,
                                 quantidade, imagem, aceita_encomenda, descricao, valor_custo)

    model_produtos.insert_produto(novo_produto)

def insert_encomenda(status, prazo, comentario, produtos):
    'Encapsula informações para inserir uma encomenda no banco de dados.'

    if comentario == '':
        comentario = None

    encomenda = model_encomendas.Encomenda(
        status=status, prazo=prazo, comentario=comentario, produtos=produtos)

    model_encomendas.insert_encomenda(encomenda)

def insert_venda(data, valor_final, status, produtos, comentario):
    'Encapsula informações para inserir uma venda no banco de dados.'

    venda = model_vendas.Venda(data=data, valor_final=valor_final,
                        status=status,  produtos=produtos, comentario=comentario)
    model_vendas.insert_venda(venda)

# // Selects

def listar_produtos():
    'Encapsula informações para listar produtos do banco de dados.'

    estoque = model_produtos.Estoque()
    produtos = model_produtos.listar_produtos(estoque)

    return produtos

def listar_produtos_encomenda():
    'Encapsula informações para listar produtos que aceitam encomenda do banco de dados.'

    estoque = model_produtos.Estoque()
    produtos = model_produtos.listar_produtos_encomenda(estoque)

    return produtos

def listar_encomendas():
    'Encapsula informações para listar as encomendas do banco de dados.'
    encomendas = model_encomendas.listar_encomendas()

    return encomendas

def listar_vendas():
    'Encapsula informações para listar as vendas do banco de dados.'
    vendas = model_vendas.listar_vendas()
    return vendas

def select_vendedor(login):
    'Encapsula informações para selecionar vendedor no banco de dados.'

    vendedor = model_vendedor.select_vendedor(login)

    return vendedor

def select_produto_id(id_produto: int):
    'Encapsula informações para selecionar um produto pelo ID no banco de dados.'

    return model_produtos.select_produto_id(model_produtos.Produto(id_produto))

def select_produto_nome(nome: str):
    'Encapsula informações para selecionar um produto pelo nome no banco de dados.'
    return model_produtos.select_produto_nome(nome)

def select_produto_nome_all(nome):
    estoque = model_produtos.Estoque()
    return model_produtos.select_produto_nome_all(nome, estoque)

def select_produto_quantidade_minima(quantidade_produto):
    estoque = model_produtos.Estoque()
    return model_produtos.select_produto_quantidade_minima(quantidade_produto, estoque)

def select_produto_quantidade_maxima(quantidade_produto):
    estoque = model_produtos.Estoque()
    return model_produtos.select_produto_quantidade_maxima(quantidade_produto, estoque)

def select_produto_descricao(descricao):
    estoque = model_produtos.Estoque()
    return model_produtos.select_produto_descricao(descricao, estoque)




def select_encomenda_status(status):
    'Encapsula informações para selecionar uma encomenda pelo status no banco de dados.'

    encomendas = model_encomendas.select_encomenda_status(status)

    return encomendas

def select_encomenda_id(id_encomenda: int):
    'Encapsula informações para selecionar uma encomenda pelo ID no banco de dados.'

    return model_encomendas.select_encomenda_id(model_encomendas.Encomenda(id_encomenda))



# // Updates

def update_produto(id_produto, nome=None, valor_unitario=None,
                            quantidade=None, imagem=None, aceita_encomenda=None, descricao=None, valor_custo=None):
    'Encapsula informações para atualizar um produto pelo ID no banco de dados.'

    produto = model_produtos.Produto(id_produto, nome, valor_unitario,
                            quantidade, imagem, aceita_encomenda, descricao, valor_custo)

    model_produtos.update_produto(produto)

    return produto

def update_encomendas(id_encomenda, status, prazo=None, comentario=None):
    'Encapsula informações para atualizar uma encomenda pelo ID no banco de dados.'

    encomenda = model_encomendas.Encomenda(status, prazo, comentario)
    model_encomendas.update_encomendas(id_encomenda, encomenda)

    return encomenda

def update_venda(id_venda, status, data=None, comentario=None):
    'Encapsula informações para selecionar uma venda pelo ID no banco de dados.'

    venda = model_vendas.Venda(data=data, status=status, comentario=comentario)
    model_vendas.update_venda(id_venda, venda)

    return venda

# // Deletes

def delete_produto(id_produto):
    'Encapsula informações para deletar um produto pelo ID no banco de dados.'

    produto = model_produtos.Produto(id_produto)

    return model_produtos.delete_produto(produto)

def delete_encomenda(id_encomenda):
    'Encapsula informações para deletar uma encomenda pelo ID no banco de dados.'

    encomenda = model_encomendas.delete_encomenda(id_encomenda)
    return encomenda

def delete_venda(id_venda):
    'Encapsula informações para selecionar uma venda pelo ID no banco de dados.'

    venda = model_vendas.delete_venda(id_venda)
    return venda

# //////////// Não utilizados

# def select_produto_quantidade():
#     produto = model.Produto()

