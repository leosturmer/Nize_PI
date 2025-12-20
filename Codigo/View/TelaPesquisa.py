from Controller import controller
from View.TelaInicial import SidebarMenu

from textual import on

from textual.widgets import (Button, Input, Footer, Header,
                             Select, TabbedContent, TabPane, DataTable,
                             Checkbox)
from textual.screen import (Screen, )
from textual.containers import (HorizontalGroup, VerticalScroll, ScrollableContainer)

from textual.suggester import SuggestFromList


class PesquisaProdutos(ScrollableContainer):
    pass 

class TelaPesquisa(Screen):
    TITLE = 'Pesquisa'

    def __init__(self, name=None, id=None, classes=None):
        super().__init__(name, id, classes)
        self.LISTA_DE_PRODUTOS = controller.listar_produtos()
        self.checkbox_list_produto = list()

    def on_mount(self):
        tabela = self.query_one("#tabela_produtos_pesquisa", DataTable)
        tabela.border_title = "Vendas"
        tabela.cursor_type = 'row'
        tabela.zebra_stripes = True

        tabela.add_columns("Nome", "Quantidade", "Valor unitário",
                           "Valor custo", "Aceita encomenda", "Descrição")
        self.resetar_tabela_produtos()

    def on_screen_resume(self):
        self.LISTA_DE_PRODUTOS = controller.listar_produtos()
        self.resetar_tabela_produtos()

    def compose(self):
        yield Header(show_clock=True)

        yield SidebarMenu(id="sidebar")

        with TabbedContent(initial='tab_produtos', id='tabbed_pesquisa'):
            with TabPane('Produtos', id='tab_produtos'):
                with VerticalScroll():

                    with HorizontalGroup():
                        yield Checkbox("Em estoque", True, id="cbox_estoque")
                        yield Checkbox("Fora de estoque", True, id="cbox_fora_estoque")
                        yield Checkbox("Aceita encomenda", True, id="cbox_encomenda")
                        yield Checkbox("Não aceita encomenda", True, id="cbox_nao_encomenda")

                with HorizontalGroup():
                    yield Select(prompt='Filtrar por:', options=[
                        ('nome', 1),
                        ("quantidade mínima", 2),
                        ('quantidade máxima', 3),
                        ('valor mínimo', 4),
                        ('valor valor máximo', 5),
                        ('descrição', 6)
                    ], id="select_produtos_pesquisa")
                    yield Input(id="input_produto_pesquisa")
                    yield Button("Pesquisar", id="bt_pesquisar_produto")
                    yield Button("Resetar tabela", id="bt_resetar_tabela_produtos")

                with VerticalScroll():
                    yield DataTable(id='tabela_produtos_pesquisa')

            with TabPane('Encomendas', id='tab_encomendas'):
                with VerticalScroll():

                    with HorizontalGroup():
                        yield Checkbox("Em produção", True, id="cbox_producao")
                        yield Checkbox("Finalizada", True, id='cbox_finalizada')
                        yield Checkbox("Vendida", True, id="cbox_vendida")
                        yield Checkbox("Cancelada", True, id="cbox_cancelada")

                    yield DataTable(id='tabela_encomendas_pesquisa')

            with TabPane('Vendas', id='tab_vendas'):
                with VerticalScroll():

                    with HorizontalGroup():
                        yield Checkbox("Em produção", True, id="cbox_producao")
                        yield Checkbox("Finalizada", True, id='cbox_finalizada')
                        yield Checkbox("Vendida", True, id="cbox_vendida")
                        yield Checkbox("Cancelada", True, id="cbox_cancelada")

                    yield DataTable(id='tabela_vendas_pesquisa')

        yield Button('Voltar', id='bt_voltar')

        yield Footer(show_command_palette=False)

    def pegar_checkbox_produtos(self):
        'Pega os valores dos Checkboxes da TelaVendas.'

        estoque = self.query_one("#cbox_estoque", Checkbox).value
        fora_estoque = self.query_one("#cbox_fora_estoque", Checkbox).value
        encomenda = self.query_one("#cbox_encomenda", Checkbox).value
        nao_encomenda = self.query_one("#cbox_nao_encomenda", Checkbox).value

        if estoque:
            self.checkbox_list_produto.append(1)

        if fora_estoque:
            self.checkbox_list_produto.append(2)

        if encomenda:
            self.checkbox_list_produto.append(3)

        if nao_encomenda:
            self.checkbox_list_produto.append(4)

    def atualizar_tabela_produtos(self):
        'Atualiza as informações para a tabela de produtos da TelaPesquisa.'

        tabela = self.query_one("#tabela_produtos_pesquisa", DataTable)

        self.pegar_checkbox_produtos()

        for produto in self.LISTA_DE_PRODUTOS:
            id_produto = produto[1]
            _id_produto, nome, quantidade, valor_unitario, valor_custo, aceita_encomenda, descricao, _imagem = controller.select_produto_id(
                id_produto)

            adicionar_na_tabela = list()

            if int(quantidade) > 0:
                adicionar_na_tabela.append(1)
            elif int(quantidade) == 0:
                adicionar_na_tabela.append(2)

            if aceita_encomenda == True:
                adicionar_na_tabela.append(3)
            elif aceita_encomenda == False:
                adicionar_na_tabela.append(4)

            if any(item in self.checkbox_list_produto for item in adicionar_na_tabela):
                if str(valor_custo) == 'None':
                    valor_custo = ''
                else:
                    valor_custo = f"R$ {valor_custo}"
                if str(descricao) == 'None':
                    descricao = ''
                if aceita_encomenda == False:
                    aceita_encomenda = 'Não'
                else:
                    aceita_encomenda = 'Sim'

                tabela.add_row(
                    nome, quantidade, f"R$ {valor_unitario}", valor_custo, aceita_encomenda, descricao)


    def resetar_tabela_produtos(self):
        'Reseta e preenche a tabela de produtos da TelaPesquisa.'
        tabela = self.query_one("#tabela_produtos_pesquisa", DataTable)

        tabela.clear()

        self.atualizar_tabela_produtos()

    def pesquisar_nome(self):
        pesquisa = self.query_one("#input_produto_pesquisa", Input).value.strip()
        self.LISTA_DE_PRODUTOS.clear()
        self.LISTA_DE_PRODUTOS = controller.select_produto_nome_all(nome=pesquisa)

        if len(self.LISTA_DE_PRODUTOS) == 0:
            self.notify(title="Tem certeza?", message=f"Você não tem nenhum produto com este nome!", severity="warning")
        else:
            self.resetar_tabela_produtos()

    def pesquisar_quantidade_minima(self): ############################################
        pesquisa = self.query_one("#input_produto_pesquisa", Input).value.strip()
        self.LISTA_DE_PRODUTOS.clear()

        try:
            int_pesquisa = int(pesquisa)
            self.LISTA_DE_PRODUTOS = controller.select_produto_quantidade_minima(quantidade_produto=pesquisa)

            if len(self.LISTA_DE_PRODUTOS) == 0:
                self.notify(title="Tem certeza?", message=f"Você não tem nenhum produto com esta quantidade!", severity="warning")
            else:
                self.resetar_tabela_produtos()

        except ValueError:
            self.notify(title="Epa!", message="Você precisa inserir um número!", severity="warning")

    def pesquisar_quantidade_maxima(self): #########################################
        pesquisa = self.query_one("#input_produto_pesquisa", Input).value.strip()
        self.LISTA_DE_PRODUTOS.clear()

        try:
            int_pesquisa = int(pesquisa)
            self.LISTA_DE_PRODUTOS = controller.select_produto_quantidade_maxima(quantidade_produto=pesquisa)

            if len(self.LISTA_DE_PRODUTOS) == 0:
                self.notify(title="Tem certeza?", message=f"Você não tem nenhum produto com esta quantidade!", severity="warning")
            else:
                self.resetar_tabela_produtos()

        except ValueError:
            self.notify(title="Epa!", message="Você precisa inserir um número!", severity="warning")

    def pesquisar_valor_minimo(self): #########################################
        pass

    def pesquisar_valor_maximo(self): #########################################
        pass

    def pesquisar_descricao(self):
        pesquisa = self.query_one("#input_produto_pesquisa", Input).value.strip()
        
        self.LISTA_DE_PRODUTOS.clear()
        self.LISTA_DE_PRODUTOS = controller.select_produto_descricao(descricao=pesquisa)

        if len(self.LISTA_DE_PRODUTOS) == 0:
            self.notify(title="Tem certeza?", message=f"Não tem nenhuma descrição com esse termo!", severity="warning")
        else:
            self.resetar_tabela_produtos()

    def fazer_pesquisa(self):
        select = self.query_one("#select_produtos_pesquisa", Select).value

        match select:
            case 1:
                self.pesquisar_nome()
            case 2:
                self.pesquisar_quantidade_minima()
            case 3:
                self.pesquisar_quantidade_maxima()
            case 4:
                self.pesquisar_valor_minimo()
            case 5:
                self.pesquisar_valor_maximo()
            case 6:
                self.pesquisar_descricao()
            case _:
                self.notify(title="Opa!", message="Você precisa selecionar uma opção!", severity="warning") 
        
    @on(Checkbox.Changed)
    async def on_checkbox_change(self, event: Checkbox.Changed):
        'Ações que ocorrem ao selecionar um Checkbox.'

        if len(self.checkbox_list_produto) > 0:
            self.checkbox_list_produto.clear()

        self.resetar_tabela_produtos()

    @on(Button.Pressed)
    async def on_button(self, event: Button.Pressed):
        match event.button.id:
            case 'bt_pesquisar_produto':
                self.fazer_pesquisa()

            case "bt_resetar_tabela_produtos":
                self.LISTA_DE_PRODUTOS = controller.listar_produtos()
                self.resetar_tabela_produtos()

            case 'bt_voltar':
                self.app.switch_screen('tela_inicial')
