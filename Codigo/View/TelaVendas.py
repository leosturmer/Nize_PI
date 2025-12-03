from Controller import controller
from View.TelaInicial import SidebarMenu

from textual import on

from textual.app import (ComposeResult)
from textual.widgets import (Button, Input, TextArea, Footer, Header,
                             Label, Static, MaskedInput, Select, TabbedContent, TabPane, DataTable,
                             Collapsible, Switch, Checkbox, Rule)
from textual.screen import (Screen)
from textual.containers import (
    VerticalGroup, HorizontalGroup, ScrollableContainer)


class TelaVendas(Screen):
    'Tela de vendas do sistema'
    TITLE = 'Vendas'

    def __init__(self, name=None, id=None, classes=None):
        super().__init__(name, id, classes)

        self.LISTA_DE_PRODUTOS = controller.listar_produtos()
        self.ID_PRODUTO = int()
        self.PRODUTOS_QUANTIDADE = dict()
        self.PRODUTOS_BAIXA = dict()
        self.PRODUTO_SELECIONADO = dict()
        self.texto_static_produto = 'Selecione um produto para visualizar as informações'
        self.texto_static_venda = 'Adicione produtos para ver o valor total da venda'
        self.texto_static_alteracao = 'Selecione uma venda para ver as informações'
        self.VENDA_ALTERACAO = list()
        self.VALOR_TOTAL_VENDA = list()
        self.checkbox_list = list()

    def on_screen_resume(self):
        'Ações que ocorrem ao voltar para a TelaVendas.'
        self.atualizar_select_produtos()
        self.limpar_inputs()
        self.limpar_inputs_alteracao()
        self.resetar_tabela_cadastro_venda()
        self.resetar_tabela_vendas()
        self.PRODUTOS_BAIXA.clear()
        self.PRODUTOS_QUANTIDADE.clear()

    def on_mount(self):
        'Ações que ocorrem ao montar a TelaVendas.'
        tabela_cadastro_venda = self.query_one(
            "#tabela_cadastro_venda", DataTable)
        tabela_cadastro_venda.border_title = "Cadastro de venda"
        tabela_cadastro_venda.cursor_type = 'row'
        tabela_cadastro_venda.zebra_stripes = True
        tabela_cadastro_venda.add_columns(
            "ID", "Produto", "Quantidade vendida", "Dar baixa", "Valor unitário", "Valor total")

        tabela = self.query_one("#tabela_vendas", DataTable)
        tabela.border_title = "Vendas"
        tabela.cursor_type = 'row'
        tabela.zebra_stripes = True

        tabela.add_columns('ID venda', 'Produtos',
                           'Data', 'Comentário', 'Status', 'Valor final')
        self.atualizar_tabela_vendas()

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)

        yield SidebarMenu(id="sidebar")

        with TabbedContent(initial='tab_cadastrar_venda'):

            with TabPane('Cadastrar venda', id='tab_cadastrar_venda'):
                with HorizontalGroup(id='cnt_select_produtos'):
                    with Collapsible(title="Expandir para adicionar produtos à venda"):
                        with HorizontalGroup(id='cnt_select_produtos'):
                            with VerticalGroup():
                                with HorizontalGroup():
                                    yield Label('Selecione um produto:')
                                    yield Select(self.LISTA_DE_PRODUTOS,
                                                 type_to_search=True,
                                                 id='select_produtos_venda',
                                                 allow_blank=True,
                                                 prompt='Selecione o produto para adicionar à venda'
                                                 )

                                with HorizontalGroup():
                                    yield Static(self.texto_static_produto, id='static_produto')
                                    with VerticalGroup():
                                        with HorizontalGroup():
                                            yield Label("Dar baixa no estoque?")
                                            yield Switch(disabled=False, id="switch_baixa")

                                        with HorizontalGroup():
                                            yield Input(placeholder='Quantidade vendida...',
                                                        id='quantidade_venda',
                                                        max_length=3,
                                                        type="integer"
                                                        )
                                            yield Button('Adicionar',
                                                         disabled=True,
                                                         id='bt_adicionar_quantidade')
                yield Rule()

                with ScrollableContainer():
                    with VerticalGroup():
                        yield DataTable(id="tabela_cadastro_venda")
                        with HorizontalGroup():
                            yield Static(self.texto_static_venda, id="static_venda")
                            yield Button("Remover", id="bt_remover", disabled=True)

                        with HorizontalGroup():
                            yield Label('Data da venda[red]*[/red]')
                            yield MaskedInput(template='00/00/0000', placeholder='DD/MM/AAAA', id="data_venda")

                            yield Label('Status da venda[red]*[/red]')
                            yield Select([('Em andamento', 1),
                                          ('Aguardando pagamento', 2),
                                          ('Finalizada', 3),
                                          ('Cancelada', 4)],
                                         type_to_search=True,
                                         id='select_status_venda',
                                         allow_blank=False
                                         )

                        with HorizontalGroup():
                            yield Label("Comentários")
                            yield TextArea(
                                placeholder='Detalhes da venda, dos produtos, da entrega, quem comprou, entre outros',
                                id='text_comentario')

                    with HorizontalGroup(id='bt_tela_vendas'):
                        yield Button('Cadastrar',  id='bt_cadastrar', disabled=True)
                        yield Button('Limpar', id='bt_limpar', disabled=True)
                        yield Button('Voltar', id='bt_voltar')

            with TabPane('Atualizar venda', id='tab_atualizar_venda'):
                with Collapsible(title='Expandir tabela de venda', id="coll_vendas"):
                    with HorizontalGroup():
                        yield Checkbox("Em andamento", True, id="cbox_andamento")
                        yield Checkbox("Aguardando pagamento", True, id='cbox_pagamento')
                        yield Checkbox("Finalizada", True, id="cbox_finalizada")
                        yield Checkbox("Cancelada", True, id="cbox_cancelada")

                    yield DataTable(id='tabela_vendas', )

                    with HorizontalGroup():
                        yield Static(self.texto_static_alteracao, id="static_alteracao_venda")
                        yield Button('Preencher campos', id='bt_preencher_campos')

                yield Rule(orientation='horizontal', line_style='solid')

                with VerticalGroup():
                    yield Static("[b]Informações da venda selecionada:[/b]", id="stt_alteracao_produto")
                    with HorizontalGroup():
                        yield Label('Data da venda[red]*[/red]')
                        yield MaskedInput(template='00/00/0000', placeholder='DD/MM/AAAA', id="data_alterada")

                        yield Label('Status da venda[red]*[/red]')
                        yield Select([('Em andamento', 1),
                                      ('Aguardando pagamento', 2),
                                      ('Finalizada', 3),
                                      ('Cancelada', 4)],
                                     type_to_search=True,
                                     id='select_status_venda_alterada',
                                     allow_blank=False
                                     )

                    with HorizontalGroup():
                        yield Label("Comentários")
                        yield TextArea(
                            placeholder='Detalhes da venda, dos produtos, da entrega, quem comprou, entre outros',
                            id='text_comentario_alterado')

                with HorizontalGroup(id='bt_tela_encomendas'):
                    yield Button("Alterar", id='bt_alterar', disabled=True)
                    yield Button('Deletar', id='bt_deletar', disabled=True)
                    yield Button('Voltar', id='bt_voltar')

        yield Footer(show_command_palette=False)

    def verificar_data(self, data_inserida, formato="%d/%m/%Y"):
        'Verifica se a data inserida é válida.'
        from datetime import datetime
        try:
            datetime.strptime(data_inserida, formato)
            return True
        except ValueError:
            return self.notify(title="Data inválida", message="Insira uma data válida!", severity="warning")

    def cadastrar_venda(self):
        'Insere uma venda no banco de dados.'
        status = self.query_one(
            '#select_status_venda', Select).value
        data = self.query_one("#data_venda", MaskedInput).value
        comentario = self.query_one("#text_comentario", TextArea).text.strip()
        dar_baixa = self.query_one("#switch_baixa", Switch)
        produtos = self.PRODUTOS_QUANTIDADE

        verificacao_data = self.verificar_data(data_inserida=data)

        valor_final = sum(self.VALOR_TOTAL_VENDA)

        if len(produtos) == 0:
            self.notify(title="Nenhum produto selecionado",
                        message="Adicione pelo menos um produto!", severity='warning')
        elif len(data) < 10:
            self.notify(title="Data inválida!",
                        message="Preencha o prazo no formato DD/MM/AAAA", severity="warning")
        elif verificacao_data == True:
            controller.insert_venda(
                data=data, valor_final=valor_final, status=status, comentario=comentario, produtos=produtos)

            for produto in produtos.items():
                if produto[0] in self.PRODUTOS_BAIXA:
                    quantidade_estoque = controller.select_produto_id(
                        id_produto=produto[0])[2]

                    quantidade_atualizada = int(
                        quantidade_estoque) - int(produto[1])
                    controller.update_produto(
                        id_produto=produto[0], quantidade=quantidade_atualizada)

            self.notify(title="Feito!",
                        message='Venda cadastrada com sucesso!')
            self.PRODUTOS_QUANTIDADE.clear()
            self.PRODUTOS_BAIXA.clear()
            dar_baixa.value = False
            self.limpar_inputs()
            self.atualizar_tabela_vendas()
            self.resetar_tabela_vendas()

    def update_venda(self):
        'Atualiza uma venda no banco de dados.'
        id_venda = self.VENDA_ALTERACAO[0]

        data = self.query_one('#data_alterada', MaskedInput).value
        status = self.query_one('#select_status_venda_alterada', Select).value
        comentario = self.query_one(
            '#text_comentario_alterado', TextArea).text.strip()

        validacao_data = self.verificar_data(data_inserida=data)

        if validacao_data == True:
            controller.update_venda(
                id_venda=id_venda, status=status, data=data, comentario=comentario)
            self.notify(title="Feito!", message="Venda alterada com sucesso!")
            self.resetar_tabela_vendas()
            self.limpar_inputs_alteracao()

    def delete_venda(self):
        'Deleta uma venda do banco de dados.'
        id_venda = self.VENDA_ALTERACAO[0]
        controller.delete_venda(id_venda)
        self.notify(title="Já era!", message='Venda deletada com sucesso!')
        self.VENDA_ALTERACAO.clear()

        self.atualizar_static_alteracao()
        self.atualizar_static_alteracao_produto()

    def atualizar_select_produtos(self):
        'Atualiza o select de produtos com os novos produtos inseridos na TelaProdutos.'
        self.LISTA_DE_PRODUTOS = controller.listar_produtos()

        self.query_one("#select_produtos_venda", Select).set_options(
            self.LISTA_DE_PRODUTOS)

        return self.LISTA_DE_PRODUTOS

    def atualizar_static_produto(self):
        'Atualiza as informações do produto selecionado na TelaVendas.'
        try:
            id_produto = self.query_one("#select_produtos_venda", Select).value

            static = self.query_one("#static_produto", Static)

            id_produto, nome, quantidade, valor_unitario, valor_custo, aceita_encomenda, descricao, imagem = controller.select_produto_id(
                id_produto)

            novo_texto = f'[b]Informações do produto:[/b]\n\n[b] Produto selecionado:[/b] {nome}\n[b] Quantidade em estoque: [/b]{quantidade}\n [b]Valor unitário:[/b] R$ {valor_unitario}'

            static.update(novo_texto)
        except:
            pass

    def atualizar_static_venda(self):
        'Atualiza as informações dos produtos inseridos em uma venda na TelaVendas.'
        self.VALOR_TOTAL_VENDA.clear()
        static = self.query_one('#static_venda', Static)

        for item in self.PRODUTOS_QUANTIDADE.items():
            id_produto, quantidade = item

            if id_produto in self.PRODUTOS_BAIXA.keys():
                match self.PRODUTOS_BAIXA[id_produto]:
                    case True:
                        dar_baixa = "Sim"
                    case False:
                        dar_baixa = "Não"

            _id_produto, nome, _quantidade, valor_unitario, _valor_custo, _aceita_encomenda, _descricao, _imagem = controller.select_produto_id(
                id_produto)

            valor_produtos = (valor_unitario * int(quantidade))

            self.VALOR_TOTAL_VENDA.append(valor_produtos)

        valor_total = sum(self.VALOR_TOTAL_VENDA)

        static.update(
            f'[b]Total da venda:[/b] R$ {valor_total:.2f}')

    def atualizar_static_alteracao(self):
        'Atualiza as informações da tela de alteração de venda.'
        static = self.query_one('#static_alteracao_venda', Static)

        try:
            _id_venda, produtos, prazo, comentario, status, valor_final = self.VENDA_ALTERACAO

            if comentario == None:
                comentario = ''

            static.update(
                f'[b]Venda:[/b]\n\n [b]Produtos:[/b] {produtos}\n [b]Prazo:[/b] {prazo}\n [b]Status:[/b] {status}\n [b]Comentários:[/b] {comentario}\n [b]Valor total:[/b] {valor_final}')

        except ValueError:
            static.update(self.texto_static_alteracao)

    def atualizar_static_alteracao_produto(self):
        'Atualiza as informações de produtos na tela de alteração de produto.'

        static = self.query_one("#stt_alteracao_produto", Static)

        try:
            _id_venda, produtos, data, comentario, status, valor_final = self.VENDA_ALTERACAO

            novo_texto = f"[b]Venda selecionada:[/b]\n\n [b]Produtos e quantidades:[/b] {produtos}\n [b]Valor final:[/b] R$ {valor_final}"
            static.update(novo_texto)
        except ValueError:
            static.update("[b]Informações da venda selecionada:[/b]")

    def atualizar_tabela_cadastro_venda(self):
        'Atualiza os valores a serem preenchidos na tabela de cadastro da venda.'

        tabela = self.query_one("#tabela_cadastro_venda", DataTable)

        for item in self.PRODUTOS_QUANTIDADE.items():
            id_produto, quantidade = item

            if id_produto in self.PRODUTOS_BAIXA.keys():
                match self.PRODUTOS_BAIXA[id_produto]:
                    case True:
                        dar_baixa = "Sim"
                    case False:
                        dar_baixa = "Não"

            _id_produto, nome, _quantidade, valor_unitario, _valor_custo, _aceita_encomenda, _descricao, _imagem = controller.select_produto_id(
                id_produto)

            valor_produtos = (valor_unitario * int(quantidade))

            tabela.add_row(_id_produto, nome, quantidade, dar_baixa,
                           f"R$ {valor_unitario}", f"R$ {valor_produtos}")

    def resetar_tabela_cadastro_venda(self):
        'Reseta e atualiza a tabela de cadastro da venda.'

        tabela = self.query_one("#tabela_cadastro_venda", DataTable)
        tabela.clear()
        self.atualizar_tabela_cadastro_venda()
        self.query_one("#bt_remover", Button).disabled = True
        self.query_one('#quantidade_venda', Input).clear()

    def adicionar_dicionario_venda(self):
        'Adiciona produtos de uma venda em um dict().'

        try:
            id_produto = self.query_one(
                "#select_produtos_venda", Select).selection
            quantidade_vendida = self.query_one(
                "#quantidade_venda", Input).value

            if quantidade_vendida == "" or quantidade_vendida.startswith("0") or quantidade_vendida.startswith("-"):
                self.notify(title='Quantidade inválida',
                            message="Insira uma quantidade válida!", severity="warning")
                return

            dar_baixa = self.query_one("#switch_baixa", Switch).value

            quantidade_estoque = controller.select_produto_id(id_produto)[2]

            match dar_baixa:
                case True:
                    if int(quantidade_vendida) > int(quantidade_estoque):
                        self.notify(
                            "Quantidade maior do que a disponível no estoque!", severity="warning")

                    if int(quantidade_vendida) > int(quantidade_estoque) and id_produto in self.PRODUTOS_BAIXA.keys():
                        self.PRODUTOS_BAIXA.pop(id_produto)
                        self.PRODUTOS_QUANTIDADE.pop(id_produto)
                        self.resetar_tabela_cadastro_venda()
                        self.atualizar_static_venda()

                    if int(quantidade_vendida) <= int(quantidade_estoque):
                        if id_produto not in self.PRODUTOS_BAIXA.keys():
                            self.PRODUTOS_BAIXA[id_produto] = True
                            self.PRODUTOS_QUANTIDADE[id_produto] = quantidade_vendida
                            self.resetar_tabela_cadastro_venda()
                            self.atualizar_static_venda()

                        if id_produto in self.PRODUTOS_BAIXA.keys():
                            self.PRODUTOS_BAIXA[id_produto] = True
                            self.PRODUTOS_QUANTIDADE[id_produto] = quantidade_vendida
                            self.resetar_tabela_cadastro_venda()
                            self.atualizar_static_venda()

                case False:
                    if id_produto not in self.PRODUTOS_BAIXA.keys():
                        self.PRODUTOS_BAIXA[id_produto] = False
                        self.PRODUTOS_QUANTIDADE[id_produto] = quantidade_vendida
                        self.resetar_tabela_cadastro_venda()
                        self.atualizar_static_venda()

                    if id_produto in self.PRODUTOS_BAIXA.keys():
                        self.PRODUTOS_BAIXA[id_produto] = False
                        self.PRODUTOS_QUANTIDADE[id_produto] = quantidade_vendida
                        self.resetar_tabela_cadastro_venda()
                        self.atualizar_static_venda()

        except TypeError as e:
            self.notify(title="Nenhum produto selecionado",
                        message="Selecione um produto!", severity="warning")

    def remover_produto_venda(self):
        'Remove um produto adicionado em uma venda.'

        id_produto = self.PRODUTO_SELECIONADO[0]
        self.PRODUTOS_QUANTIDADE.pop(id_produto)
        self.PRODUTOS_BAIXA.pop(id_produto)
        self.atualizar_static_venda()
        self.resetar_tabela_cadastro_venda()
        self.notify(title="Removido!",
                    message="Produto removido da venda", severity="warning")

    def limpar_inputs(self):
        'Reseta os campos e informações da TelaVendas.'
        self.VALOR_TOTAL_VENDA.clear()
        self.PRODUTOS_QUANTIDADE.clear()
        self.PRODUTOS_BAIXA.clear()

        self.query_one("#data_venda", Input).clear()
        self.query_one("#select_status_venda", Select).value = 1
        self.query_one("#text_comentario", TextArea).clear()
        self.query_one("#select_produtos_venda", Select).clear()
        self.query_one('#quantidade_venda', Input).clear()
        self.query_one("#switch_baixa", Switch).value = False
        self.query_one('#static_produto', Static).update(
            self.texto_static_produto)
        self.query_one('#static_venda', Static).update(
            self.texto_static_venda)
        self.query_one("#tabela_cadastro_venda", DataTable).clear()

    def limpar_inputs_alteracao(self):
        'Reseta os campos e informações de alterações da TelaVendas.'
        self.query_one("#data_alterada", MaskedInput).clear()
        self.query_one("#select_status_venda_alterada", Select).value = 1
        self.query_one("#text_comentario_alterado", TextArea).clear()
        self.query_one("#static_alteracao_venda", Static).update(
            self.texto_static_alteracao)
        self.query_one("#stt_alteracao_produto", Static).update(
            "[b]Informações da venda selecionada:[/b]")
        self.query_one("#bt_alterar", Button).disabled = True
        self.query_one("#bt_deletar", Button).disabled = True

    def pegar_checkbox_venda(self):
        'Pega os valores dos Checkboxes da TelaVendas.'
        andamento = self.query_one("#cbox_andamento", Checkbox).value
        pagamento = self.query_one("#cbox_pagamento", Checkbox).value
        finalizada = self.query_one("#cbox_finalizada", Checkbox).value
        cancelada = self.query_one("#cbox_cancelada", Checkbox).value

        if andamento:
            self.checkbox_list.append(1)

        if pagamento:
            self.checkbox_list.append(2)

        if finalizada:
            self.checkbox_list.append(3)

        if cancelada:
            self.checkbox_list.append(4)

    def atualizar_tabela_vendas(self):
        'Atualiza os valores a serem preenchidos na tabela da TelaVendas.'
        tabela = self.query_one("#tabela_vendas", DataTable)

        dados_vendas = controller.listar_vendas()

        self.pegar_checkbox_venda()

        for id_encomenda, detalhes in dados_vendas.items():
            nome_produtos = [''.join([f'{nome}, ({quantidade}) | \n '])
                             for nome, quantidade, _valor_unitario in detalhes['produtos']]

            status = detalhes['status']
            valor_final = detalhes['valor_final']

            if status in self.checkbox_list:

                if detalhes['status'] == 1:
                    status = 'Em produção'
                elif detalhes['status'] == 2:
                    status = 'Aguardando pagamento'
                elif detalhes['status'] == 3:
                    status = 'Finalizada'
                elif detalhes['status'] == 4:
                    status = 'Cancelada'

                if id_encomenda not in tabela.rows:
                    tabela.add_row(id_encomenda, ''.join(nome_produtos),
                                   detalhes['data'], detalhes['comentario'], status, f"R$ {valor_final}")

    def resetar_tabela_vendas(self):
        'Reseta e preenche a tabela da TelaVendas.'
        tabela = self.query_one("#tabela_vendas", DataTable)

        tabela.clear()

        self.atualizar_tabela_vendas()

    def preencher_alteracoes_venda(self):
        'Preenche os valores de uma venda na parte de Atualização de Venda na TelaVendas.'
        novo_prazo = self.query_one("#data_alterada", MaskedInput)
        novo_status = self.query_one("#select_status_venda_alterada", Select)
        novo_comentario = self.query_one("#text_comentario_alterado", TextArea)

        _id_encomenda, _produtos, prazo, comentario, status, _valor_total = self.VENDA_ALTERACAO

        comentario = str(comentario)

        if status == 'Em produção':
            status = 1
        elif status == 'Aguardando pagamento':
            status = 2
        elif status == 'Finalizada':
            status = 3
        elif status == 'Cancelada':
            status = 4

        if comentario == 'None':
            comentario = ''

        novo_prazo.value = prazo
        novo_status.value = status
        novo_comentario.text = comentario

        self.query_one("#coll_vendas", Collapsible).collapsed = True
        self.atualizar_static_alteracao_produto()

    @on(Checkbox.Changed)
    async def on_checkbox_change(self, event: Checkbox.Changed):
        'Ações que ocorrem ao selecionar um Checkbox.'
        if len(self.checkbox_list) > 0:
            self.checkbox_list.clear()

        self.resetar_tabela_vendas()

    @on(DataTable.RowSelected)
    async def on_row_selected(self, event: DataTable.RowSelected):
        'Ações que ocorrem ao selecionar as linhas de uma tabela.'
        match event.data_table.id:
            case "tabela_vendas":

                encomenda = self.query_one('#tabela_vendas', DataTable)
                self.VENDA_ALTERACAO = encomenda.get_row(event.row_key)
                self.atualizar_static_alteracao()
                self.query_one("#bt_alterar", Button).disabled = False
                self.query_one("#bt_deletar", Button).disabled = False

            case "tabela_cadastro_venda":
                self.query_one("#bt_remover", Button).disabled = False
                encomenda = self.query_one('#tabela_cadastro_venda', DataTable)
                self.PRODUTO_SELECIONADO = encomenda.get_row(event.row_key)

    @on(Select.Changed)
    async def on_select(self, event: Select.Changed):
        'Ações que ocorrem ao selecionar um item do Select.'
        match event.select.id:
            case 'select_produtos_venda':
                self.ID_PRODUTO = event.select.value
                self.atualizar_static_produto()

            case 'select_id_venda':
                self.atualizar_static_alteracao()

    @on(Input.Changed)
    async def on_input(self, event: Input.Changed):
        'Ações que ocorrem ao preencher um Input.'
        match event.input.id:
            case 'quantidade_venda':
                self.query_one("#bt_adicionar_quantidade",
                               Button).disabled = False

            case 'data_venda':
                if event.input.value == '':
                    self.query_one("#bt_cadastrar", Button).disabled = True
                    self.query_one("#bt_limpar", Button).disabled = True
                else:
                    self.query_one("#bt_cadastrar", Button).disabled = False
                    self.query_one("#bt_limpar", Button).disabled = False

    @on(TextArea.Changed)
    async def on_textarea(self, event: TextArea.Changed):
        'Ações que ocorrem ao preencher uma TextArea.'
        if event.text_area.id == 'text_comentario':
            self.query_one("#bt_limpar", Button).disabled = False

    @on(Button.Pressed)
    async def on_button(self, event: Button.Pressed):
        'Ações que ocorrem ao pressionar um botão na TelaVendas.'
        match event.button.id:
            case 'bt_adicionar_quantidade':
                self.adicionar_dicionario_venda()

            case 'bt_remover':
                self.remover_produto_venda()

            case 'bt_voltar':
                self.app.switch_screen('tela_inicial')

            case 'bt_cadastrar':
                self.cadastrar_venda()

            case 'bt_preencher_campos':
                try:
                    self.preencher_alteracoes_venda()
                except ValueError:
                    self.notify(
                        title="Ops!", message="Você precisa selecionar uma venda", severity='warning')

            case 'bt_alterar':
                self.update_venda()

            case 'bt_deletar':
                self.delete_venda()
                self.resetar_tabela_vendas()

            case 'bt_limpar':
                self.limpar_inputs()
