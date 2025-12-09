from Controller import controller
from View.TelaInicial import SidebarMenu

from textual import on

from textual.app import (ComposeResult)
from textual.widgets import (Button, Input, TextArea, Footer, Header,
                             Label, Static, Select, TabbedContent, TabPane, DataTable,
                             Collapsible, Switch, Checkbox, Rule, Placeholder)
from textual.screen import (Screen)
from textual.containers import (HorizontalGroup, ScrollableContainer, VerticalScroll)

from textual.suggester import Suggester, SuggestFromList


class TelaProdutos(Screen):
    'Tela de cadastro, alteração e remoção de produtos do sistema.'

    TITLE = 'Produtos'

    def __init__(self, name=None, id=None, classes=None):
        super().__init__(name, id, classes)

        self.LISTA_DE_PRODUTOS = controller.listar_produtos()
        self.lista_de_nomes = self.preencher_lista_de_nomes()
        self.ID_PRODUTO = int()
        self.checkbox_list_produto = list()
        
    def on_mount(self):
        tabela = self.query_one("#tabela_produtos_pesquisa", DataTable)
        tabela.border_title = "Vendas"
        tabela.cursor_type = 'row'
        tabela.zebra_stripes = True

        tabela.add_columns("Nome", "Quantidade", "Valor unitário", "Valor custo", "Aceita encomenda", "Descrição") 
        self.atualizar_tabela_produtos()
        self.preencher_lista_de_nomes()

    def on_screen_resume(self):
        'Ações que ocorrem ao voltar para a TelaProdutos.'
        self.limpar_texto_static()
        self.atualizar_select_produtos()
        self.resetar_tabela_produtos()
        self.limpar_inputs_produtos()

    def compose(self) -> ComposeResult:

        yield Header(show_clock=True)

        yield SidebarMenu(id="sidebar")

        with TabbedContent(initial='tab_cadastro', id='tabbed_pesquisa'):
            with TabPane("Cadastro de produtos", id="tab_cadastro"):
                with ScrollableContainer(id='tela_produtos'):
                    with Collapsible(title="Expandir para alterar um produto cadastrado", id="collapsible_produtos"):
                        with HorizontalGroup(id='class_select_produtos'):
                            yield Label('Selecione o produto')
                            yield Select(self.LISTA_DE_PRODUTOS,
                                        type_to_search=True,
                                        id='select_produtos',
                                        allow_blank=True,
                                        prompt='Selecione o produto'
                                        )

                        with HorizontalGroup():
                            yield Static(f'\n\nSelecione o produto para visualizar as informações', id='stt_info_produto')
                            yield Button('Preencher campos', id='bt_preencher_campos')

                    yield Rule(orientation='horizontal', line_style='solid')

                    with ScrollableContainer(id='inputs_cadastro'):
                        with HorizontalGroup():

                            yield Label("Nome do produto[red]*[/red]")
                            yield Input(
                                placeholder='Nome do produto*',
                                type='text',
                                max_length=50,
                                id='input_nome',
                                suggester=SuggestFromList(suggestions=self.lista_de_nomes, case_sensitive=False)
                            )
                            self.notify(f"{self.lista_de_nomes}")

                            yield Label("Quantidade[red]*[/red]")
                            yield Input(
                                placeholder='Quantidade*',
                                type='integer',
                                max_length=4,
                                id='input_quantidade'
                            )

                        with HorizontalGroup():
                            yield Label("Valor unitário[red]*[/red]")
                            yield Input(
                                placeholder='Valor unitário*',
                                type='number',
                                max_length=7,
                                id='input_valor_unitario'
                            )

                            yield Label("Valor de custo")
                            yield Input(
                                placeholder='Valor de custo',
                                type='number',
                                max_length=7,
                                id='input_valor_custo'
                            )

                        with HorizontalGroup():
                            yield Label('Imagem')
                            yield Input(
                                placeholder='Imagem',
                                type='text',
                                id='input_imagem', disabled=True
                            )
                            yield Label('Aceita encomendas?')
                            yield Switch(value=False, id='select_encomenda')

                        with HorizontalGroup():

                            yield Label("Descrição do produto")
                            yield TextArea(
                                placeholder='Descrição',
                                id='text_descricao', )

                    with HorizontalGroup(id='bt_tela_produtos'):
                        yield Button('Cadastrar',  id='bt_cadastrar', disabled=True)
                        yield Button("Alterar", id='bt_alterar', disabled=True)
                        yield Button('Limpar', id='bt_limpar', disabled=True)
                        yield Button('Deletar', id='bt_deletar', disabled=True)
                        yield Button('Voltar', id='bt_voltar')

            with TabPane('Lista de produtos', id='tab_produtos'):
                with VerticalScroll():

                    with HorizontalGroup():
                        yield Checkbox("Em estoque", True, id="cbox_estoque", )
                        yield Checkbox("Fora de estoque", True, id="cbox_fora_estoque")
                        yield Checkbox("Aceita encomenda", False, id="cbox_encomenda")
                        yield Checkbox("Não aceita encomenda", False, id="cbox_nao_encomenda")

                with VerticalScroll():
                    yield DataTable(id='tabela_produtos_pesquisa')
                    yield Button('Voltar', id='bt_voltar')

        yield Footer(show_command_palette=False)

    def preencher_lista_de_nomes(self):
        lista_de_nomes = list()

        for item in self.LISTA_DE_PRODUTOS:
            lista_de_nomes.append(item[0])
        return lista_de_nomes


    def pegar_inputs_produtos(self):
        'Pega os campos da TelaProdutos.'
        nome = self.query_one("#input_nome", Input)
        quantidade = self.query_one("#input_quantidade", Input)
        valor_unitario = self.query_one("#input_valor_unitario", Input)
        valor_custo = self.query_one("#input_valor_custo", Input)
        imagem = self.query_one("#input_imagem", Input)
        aceita_encomenda = self.query_one("#select_encomenda", Switch)
        descricao = self.query_one("#text_descricao", TextArea)

        return nome, quantidade, valor_unitario, valor_custo, imagem, aceita_encomenda, descricao

    def pegar_valores_inputs(self):
        'Pega os valores inseridos nos campos da TelaProdutos.'
        nome, quantidade, valor_unitario, valor_custo, imagem, aceita_encomenda, descricao = self.pegar_inputs_produtos()

        nome = nome.value.strip().capitalize()
        quantidade = quantidade.value
        valor_unitario = valor_unitario.value
        valor_custo = valor_custo.value
        imagem = imagem.value
        aceita_encomenda = aceita_encomenda.value
        descricao = descricao.text.strip()

        return nome, quantidade, valor_unitario, valor_custo, imagem, aceita_encomenda, descricao

    def limpar_inputs_produtos(self):
        'Reseta os valores dos campos da TelaProdutos.'
        nome, quantidade, valor_unitario, valor_custo, imagem, aceita_encomenda, descricao = self.pegar_inputs_produtos()
        nome.clear()
        quantidade.clear()
        valor_unitario.clear()
        valor_custo.clear()
        imagem.clear()
        aceita_encomenda.value = False
        descricao.clear()

        self.query_one("#bt_cadastrar", Button).disabled = True
        self.query_one("#bt_limpar", Button).disabled = True
        self.query_one("#bt_alterar", Button).disabled = True
        self.query_one("#bt_deletar", Button).disabled = True
        self.query_one("#select_produtos", Select).value = Select.BLANK

    def atualizar_texto_static(self):
        'Atualiza as informações do produto selecionado na TelaProdutos.'
        id_produto = self.query_one("#select_produtos", Select).value

        texto_static = self.query_one("#stt_info_produto", Static)

        id_produto, nome, quantidade, valor_unitario, valor_custo, aceita_encomenda, descricao, imagem = controller.select_produto_id(
            id_produto)

        if str(valor_custo) == 'None':
            valor_custo = 'Não informado'
        if str(descricao) == 'None':
            descricao = 'Sem descrição'
        if aceita_encomenda == False:
            aceita_encomenda = 'Não'
        else:
            aceita_encomenda = 'Sim'

        texto_static.update(
            f'Informações do produto selecionado:\n\n[b]  Nome:[/b] {nome}\n[b]  Quantidade disponível:[/b] {quantidade}\n[b]  Valor unitário:[/b] R$ {valor_unitario}\n  [b]Valor de custo:[/b] R$ {valor_custo}\n  [b]Aceita encomenda:[/b] {aceita_encomenda}\n  [b]Descrição:[/b] {descricao}')

    def limpar_texto_static(self):
        'Reseta as informações do produto selecionado na TelaProdutos.'
        texto_static = self.query_one("#stt_info_produto", Static)
        texto_static.update(f"Selecione o produto para visualizar as informações")

    def cadastrar_produto(self):
        'Cadastra o produto.'

        nome, quantidade, valor_unitario, valor_custo, imagem, aceita_encomenda, descricao = self.pegar_valores_inputs()

        if nome == '' or quantidade == '' or valor_unitario == '':
            self.notify(
                title="Ops!", message="Insira todos os dados obrigatórios", severity='warning')
        else:
            validacao_nome = controller.select_produto_nome(nome=nome)            
            if validacao_nome != None:
                self.notify(title="Eita!", message="Nome de produto já cadastrado", severity="error")
            else:
                id_produto = None
                controller.insert_produto(
                    id_produto, nome, valor_unitario, quantidade, imagem, aceita_encomenda, descricao, valor_custo)
                self.notify(title='Feito!',
                            message=f"{nome} cadastrado com sucesso!")

                self.atualizar_select_produtos()
                self.limpar_inputs_produtos()
                self.limpar_texto_static()
                self.resetar_tabela_produtos()

    def atualizar_select_produtos(self):
        'Atualiza o Select de produtos.'
        self.LISTA_DE_PRODUTOS = controller.listar_produtos()

        self.query_one(Select).set_options(self.LISTA_DE_PRODUTOS)

        return self.LISTA_DE_PRODUTOS

    def preencher_campos(self):
        'Preenche os campos da TelaProdutos com as informações do produto selecionado.'
        id_produto = self.query_one(
            "#select_produtos", Select).value

        self.ID_PRODUTO = id_produto

        _, nome, quantidade, valor_unitario, valor_custo, aceita_encomenda, descricao, imagem = controller.select_produto_id(
            id_produto)

        input_nome, input_quantidade, input_valor_unitario, input_valor_custo, input_imagem, input_aceita_encomenda, input_descricao = self.pegar_inputs_produtos()
        if imagem is None:
            imagem = ""
        if descricao is None:
            descricao = ""
        if valor_custo is None:
            valor_custo = ""

        input_nome.value = str(nome)
        input_quantidade.value = str(quantidade)
        input_valor_unitario.value = str(valor_unitario)
        input_valor_custo.value = str(valor_custo)
        input_imagem.value = str(imagem)
        input_aceita_encomenda.value = aceita_encomenda
        input_descricao.text = str(descricao)

        self.query_one("#collapsible_produtos", Collapsible).collapsed = True
        self.query_one("#bt_alterar", Button).disabled = False
        self.query_one("#bt_deletar", Button).disabled = False

    def alterar_produto(self):
        id_produto = self.query_one("#select_produtos", Select).value

        nome, quantidade, valor_unitario, valor_custo, imagem, aceita_encomenda, descricao = self.pegar_valores_inputs()

        if nome == '' or quantidade == '' or valor_unitario == '':
            self.notify(
                title="Ops!", message="Insira todos os dados obrigatórios", severity='warning')

        else:
            controller.update_produto(
                id_produto, nome, valor_unitario, quantidade, imagem, aceita_encomenda, descricao, valor_custo)

            self.atualizar_select_produtos()

            self.limpar_inputs_produtos()
            self.limpar_texto_static()
            self.resetar_tabela_produtos()

            self.notify(title="Feito!", message=f"Produto {nome} alterado com sucesso!")

            self.query_one("#collapsible_produtos", Collapsible).expand = False

    def deletar_produto(self):
        id_produto = self.ID_PRODUTO

        if id_produto > 0:
            controller.delete_produto(id_produto)
            self.notify(title="Já era!", message="Produto excluído com sucesso")

            self.atualizar_select_produtos()
            self.limpar_inputs_produtos()
            self.limpar_texto_static()
            self.resetar_tabela_produtos()

            self.ID_PRODUTO = 0

        else:
            self.notify(title="Ops!", message="Você precisa selecionar um produto!", severity='warning')


    
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

    def atualizar_tabela_produtos(self): #### Não filtra se dois checkboxes diferentes são apertados.
        'Atualiza as informações para a tabela de produtos da TelaPesquisa.'

        tabela = self.query_one("#tabela_produtos_pesquisa", DataTable)
        self.LISTA_DE_PRODUTOS = controller.listar_produtos()

        self.pegar_checkbox_produtos()

        for produto in self.LISTA_DE_PRODUTOS:
            id_produto = produto[1]
            _id_produto, nome, quantidade, valor_unitario, valor_custo, aceita_encomenda, descricao, _imagem = controller.select_produto_id(id_produto)

            adicionar_na_tabela = list()

            if int(quantidade) > 0:
                adicionar_na_tabela.append(1)
            else:
                adicionar_na_tabela.append(2)
            
            if aceita_encomenda == True:
                adicionar_na_tabela.append(3)
            else:
                adicionar_na_tabela.append(4)
                            
            if any(item in adicionar_na_tabela for item in self.checkbox_list_produto):                
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

                tabela.add_row(nome, quantidade, f"R$ {valor_unitario}", valor_custo, aceita_encomenda, descricao)

    def resetar_tabela_produtos(self):
        'Reseta e preenche a tabela de produtos da TelaPesquisa.'
        tabela = self.query_one("#tabela_produtos_pesquisa", DataTable)

        tabela.clear()

        self.atualizar_tabela_produtos()

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
                self.resetar_tabela_produtos_pesquisa()

            case 'bt_voltar':
                self.app.switch_screen('tela_inicial')


    @on(Input.Changed)
    async def on_input(self, event: Input.Changed):
        'Ações que ocorrem ao preencher o Input.'
        match event.input.value:

            case '':
                self.query_one("#bt_cadastrar", Button).disabled = True
                self.query_one("#bt_limpar", Button).disabled = True
            case str():
                self.query_one("#bt_cadastrar", Button).disabled = False
                self.query_one("#bt_limpar", Button).disabled = False

    @on(Select.Changed)
    async def on_select(self, event: Select.Changed):
        'Ações que ocorrem ao trocar o item selecioando no Select.'
        self.ID_PRODUTO = event.select.value
        if event.select.value == Select.BLANK:
            pass
        else:
            self.atualizar_texto_static()

    @on(Button.Pressed)
    async def on_button(self, event: Button.Pressed):
        'Ações que ocorrem ao clicar nos botões da tela.'

        match event.button.id:
            case 'bt_cadastrar':
                self.cadastrar_produto()

            case 'bt_limpar':
                self.limpar_inputs_produtos()
                self.limpar_texto_static()

            case 'bt_voltar':
                self.app.switch_screen('tela_inicial')
                self.limpar_inputs_produtos()
                self.limpar_texto_static()

            case 'bt_preencher_campos':
                try:
                    self.preencher_campos()
                except:
                    self.notify(
                        title="Ops!", message="Nenhum produto selecionado!", severity='warning')

            case 'bt_alterar':
                self.alterar_produto()

            case 'bt_deletar':
                self.deletar_produto()

