from Controller import controller
from View.TelaInicial import SidebarMenu

from textual import on

from textual.app import (ComposeResult)
from textual.widgets import (Button, Input, TextArea, Footer, Header,
                             Label, Static, MaskedInput,  Select, TabbedContent, TabPane, DataTable,
                             Collapsible, Checkbox, Rule)
from textual.screen import (Screen)
from textual.containers import (VerticalGroup, HorizontalGroup, Center, ScrollableContainer, VerticalScroll)

class TelaEncomendas(Screen):
    'Tela de cadastro, alteração e remoção de encomendas do sistema.'

    TITLE = 'Encomendas'

    def __init__(self, name=None, id=None, classes=None):
        super().__init__(name, id, classes)

        self.LISTA_DE_PRODUTOS = controller.listar_produtos_encomenda()
        self.ID_PRODUTO = int()
        self.PRODUTOS_QUANTIDADE = dict()
        self.texto_static_produto = 'Selecione um produto para visualizar as informações'
        self.texto_static_encomenda = 'Aqui vão as informações da encomenda'
        self.texto_static_alteracao = 'Selecione uma encomenda para ver as informações'
        self.ENCOMENDA_ALTERACAO = list()
        self.PRODUTO_SELECIONADO = dict()
        self.checkbox_list = list()

    def on_screen_resume(self):
        'Ações que ocorrem ao voltar para a TelaProdutos.'

        self.atualizar_select_produtos()
        self.limpar_inputs()
        self.limpar_inputs_alteracao()
        self.query_one("#coll_encomendas", Collapsible).collapsed = True

    def on_mount(self):
        tabela_cadastro_encomenda = self.query_one(
            "#tabela_cadastro_encomenda", DataTable)
        tabela_cadastro_encomenda.border_title = "Cadastro de encomenda"
        tabela_cadastro_encomenda.cursor_type = 'row'
        tabela_cadastro_encomenda.zebra_stripes = True
        tabela_cadastro_encomenda.add_columns("ID", "Produto", "Quantidade encomendada")

        tabela = self.query_one("#tabela_encomendas", DataTable)
        tabela.border_title = "Encomendas"
        tabela.cursor_type = 'row'
        tabela.zebra_stripes = True

        tabela.add_columns('ID encomenda', 'Produtos',
                           'Prazo', 'Comentário', 'Status')
        self.atualizar_tabela_encomendas()

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)

        yield SidebarMenu(id="sidebar")

        with TabbedContent(initial='tab_cadastrar_encomeda'):

            with TabPane('Cadastrar encomenda', id='tab_cadastrar_encomeda'):
                with Collapsible(title="Expandir para adicionar produtos à encomenda"):
                    with HorizontalGroup(id='cnt_select_produtos'):
                        yield Label('Selecione um produto:')
                        yield Select(self.LISTA_DE_PRODUTOS,
                                        type_to_search=True,
                                        id='select_produtos',
                                        allow_blank=True,
                                        prompt='Selecione o produto para adicionar à encomenda'
                                        )

                    with VerticalGroup():
                        with HorizontalGroup():
                            yield Static(self.texto_static_produto, id='static_produto')

                            with HorizontalGroup():
                                yield Input(placeholder='Quantidade encomendada...',
                                            id='quantidade_encomenda',
                                            max_length=3,
                                            type="integer"
                                            )
                                yield Button('Adicionar',
                                            disabled=True,
                                            id='bt_adicionar_quantidade')
                                
                yield Rule()

                with ScrollableContainer():
                    with HorizontalGroup():
                        yield DataTable(id="tabela_cadastro_encomenda")
                        yield Button("Remover", id="bt_remover", disabled=True)
                    with VerticalGroup():
                        with HorizontalGroup():
                            yield Label('Prazo de entrega[red]*[/red]')
                            yield MaskedInput(template='00/00/0000', placeholder='DD/MM/AAAA', id="prazo_encomenda")

                            yield Label('Status da encomenda[red]*[/red]')
                            yield Select([('Em produção', 1),
                                            ('Finalizada', 2),
                                            ('Vendida', 3),
                                            ('Cancelada', 4)],
                                            type_to_search=True,
                                            id='select_status_cadastro',
                                            allow_blank=False
                                            )

                        with HorizontalGroup():
                            yield Label("Comentários")
                            yield TextArea(
                                placeholder='Detalhes da encomenda, dos produtos, da entrega, quem comprou, entre outros',
                                id='text_comentario')

                    with HorizontalGroup(id='bt_tela_encomendas'):
                        yield Button('Cadastrar',  id='bt_cadastrar', disabled=True)
                        yield Button('Limpar', id='bt_limpar', disabled=True)
                        yield Button('Voltar', id='bt_voltar')

            with TabPane('Atualizar encomenda', id='tab_atualizar_encomenda'):
                with Collapsible(title='Expandir tabela de encomendas', id="coll_encomendas"):
                        with HorizontalGroup():
                            yield Checkbox("Em produção", True, id="cbox_producao")
                            yield Checkbox("Finalizada", True, id='cbox_finalizada')
                            yield Checkbox("Vendida", True, id="cbox_vendida")
                            yield Checkbox("Cancelada", True, id="cbox_cancelada")

                        with VerticalScroll():
                            yield DataTable(id='tabela_encomendas')

                            with HorizontalGroup(id="horizontal_alteracao_encomenda"):
                                yield Static(self.texto_static_alteracao, id="static_alteracao_encomenda")
                                
                                yield Button('Preencher dados', id='bt_preencher_campos', disabled=True)

                                with Center(id="tranformar_venda"):
                                    yield Button('Transformar em venda', id='bt_transformar_venda', disabled=True)
                                    yield Label('[blue]Isso não dá baixa no estoque![blue]', id="lbl_transformar_venda")
            
                yield Rule(orientation='horizontal', line_style='solid')

                with VerticalGroup():
                    yield Static("[b]Informações da encomenda selecionada:[/b]", id="stt_alteracao_produto")

                    with HorizontalGroup():
                        yield Label('Prazo de entrega[red]*[/red]')
                        yield MaskedInput(template='00/00/0000', placeholder='DD/MM/AAAA', id="prazo_alterado")

                        yield Label('Status da encomenda')
                        yield Select([('Em produção', 1),
                                      ('Finalizada', 2),
                                      ('Vendida', 3),
                                      ('Cancelada', 4)],
                                     type_to_search=True,
                                     id='select_status_alterado',
                                     allow_blank=False
                                     )

                    with HorizontalGroup():
                        yield Label("Comentários")
                        yield TextArea(
                            placeholder='Detalhes da encomenda, dos produtos, da entrega, quem comprou, entre outros',
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
            return self.notify(title="Data inválida", message="Preencha com uma data válida", severity='warning')
        
    def cadastrar_encomenda(self):
        'Cadastra a encomenda no banco de dados.'
        status = self.query_one(
            '#select_status_cadastro', Select).value
        prazo = self.query_one("#prazo_encomenda", Input).value
        comentario = self.query_one("#text_comentario", TextArea).text.strip()
        produtos = self.PRODUTOS_QUANTIDADE
        
        validacao_data = self.verificar_data(prazo)
    
        if len(produtos) == 0:
            self.notify(title="Nenhum produto adicionado", message="Adicione pelo menos um produto!", severity="warning")
        elif len(prazo) < 10:
            self.notify(title="Data inválida!", message="Preencha o prazo no formato DD/MM/AAAA", severity="warning")
        elif validacao_data == True:
            controller.insert_encomenda(
                status=status, prazo=prazo, comentario=comentario, produtos=produtos)

            self.notify(title="Feito!", message='Encomenda cadastrada com sucesso!')
            self.PRODUTOS_QUANTIDADE.clear()
            self.limpar_inputs()
            self.atualizar_tabela_encomendas()
            self.resetar_tabela_encomendas()

    def update_encomenda(self):
        'Envia ao banco de dados as alterações da encomenda.'
        id_encomenda = self.ENCOMENDA_ALTERACAO[0]

        prazo = self.query_one("#prazo_alterado", MaskedInput).value
        status = self.query_one("#select_status_alterado", Select).value
        comentario = self.query_one("#text_comentario_alterado", TextArea).text.strip()

        validacao_data = self.verificar_data(data_inserida=prazo)

        if validacao_data == True:
            controller.update_encomendas(
                id_encomenda=id_encomenda, prazo=prazo, comentario=comentario, status=status)
            
            self.notify(title="Feito!", message="Encomenda alterada com sucesso!")
            self.limpar_inputs_alteracao()
            self.resetar_tabela_encomendas()

    def deletar_encomenda(self):
        'Deleta do banco de dados a encomenda.'
        id_encomenda = self.ENCOMENDA_ALTERACAO[0]
        controller.delete_encomenda(id_encomenda)
        self.notify(title="Feito", message='Encomenda deletada com sucesso!')
        self.ENCOMENDA_ALTERACAO.clear()
        self.limpar_inputs_alteracao()
        self.atualizar_tabela_encomendas()
    
    def atualizar_select_produtos(self):
        'Atualiza o select de produtos quando um novo produto é cadastrado na TelaProdutos.'
        self.LISTA_DE_PRODUTOS = controller.listar_produtos_encomenda()
        self.query_one("#select_produtos", Select).set_options(
            self.LISTA_DE_PRODUTOS)

        return self.LISTA_DE_PRODUTOS

    def atualizar_static_produto(self):
        'Atualiza as informações referente ao produto selecionado.'
        try:
            id_produto = self.query_one("#select_produtos", Select).value

            static = self.query_one("#static_produto", Static)

            id_produto, nome, quantidade, valor_unitario, valor_custo, aceita_encomenda, descricao, imagem = controller.select_produto_id(
                id_produto)

            novo_texto = f'[b]Informações do produto:[/b]\n\n[b] Produto selecionado:[/b] {nome}\n[b] Quantidade em estoque: [/b]{quantidade}'

            static.update(novo_texto)
        except Exception as e:
            pass

    def atualizar_static_alteracao(self):
        'Atualiza as informações referente a encomenda selecionada na tela de Atualização de Encomenda.'
        static = self.query_one('#static_alteracao_encomenda', Static)
        novo_texto = f""

        _id_encomenda, produtos, prazo, comentario, status = self.ENCOMENDA_ALTERACAO

        if comentario == None:
            comentario = '--'

        novo_texto = f'''[b]Encomenda:[/b] \n\n[b]Produtos:[/b] {produtos}\n[b]Prazo:[/b] {prazo}\n[b]Status:[/b] {status}\n[b]Comentários:[/b] {comentario}'''

        static.update(novo_texto)

    def atualizar_static_alteracao_produto(self):
        'Atualiza as informações de produtos na tela de alteração de encomendas.'

        static = self.query_one("#stt_alteracao_produto", Static)
        produtos = self.ENCOMENDA_ALTERACAO[1]

        novo_texto = f"[b]Encomenda selecionada:[/b] \n [b]Produtos e quantidades:[/b] {produtos}"
        static.update(novo_texto)
        
    def adicionar_dicionario_encomenda(self):
        'Adiciona os produtos selecionados de uma encomenda para um dict().'
        id_produto = self.query_one("#select_produtos", Select).selection
        quantidade_encomendada = self.query_one(
            "#quantidade_encomenda", Input).value

        
        if id_produto is None:
            self.notify(title="Nenhum produto selecionado", message="Selecione um produto", severity='warning')

        elif quantidade_encomendada == 0 or quantidade_encomendada.startswith("0") or quantidade_encomendada.startswith("-") or quantidade_encomendada == "":
            self.notify(title="Quantidade inválida", message="Adicione uma quantidade válida!", severity='warning')
        else:
            self.PRODUTOS_QUANTIDADE[id_produto] = quantidade_encomendada

    def limpar_statics(self):
        'Limpa os textos dos statics.'
        static = self.query_one("#stt_alteracao_produto", Static)
        produtos = self.ENCOMENDA_ALTERACAO[1]

        novo_texto = f"[b]Encomenda selecionada:[/b] \n [b]Produtos e quantidades:[/b] {produtos}"
        static.update(novo_texto)

    def limpar_inputs(self):
        'Reseta os valores inseridos nos campos da tela de Cadastro de Encomendas.'
        self.query_one("#prazo_encomenda", Input).clear()
        self.query_one("#select_status_cadastro", Select).value = 1
        self.query_one("#text_comentario", TextArea).clear()
        self.query_one("#select_produtos", Select).clear()
        self.query_one('#quantidade_encomenda', Input).clear()
        self.query_one('#static_produto', Static).update(
            self.texto_static_produto)
        self.query_one("#tabela_cadastro_encomenda", DataTable).clear()
        self.query_one("#bt_remover", Button).disabled = True

    def limpar_inputs_alteracao(self):
        'Reseta os valores inseridos nos campos da tela de Atualização de Encomendas.'
        self.query_one("#prazo_alterado", MaskedInput).clear()
        self.query_one("#select_status_alterado", Select).value = 1
        self.query_one("#text_comentario_alterado", TextArea).clear()
        self.query_one("#static_alteracao_encomenda", Static).update(
            self.texto_static_encomenda)
        self.query_one("#stt_alteracao_produto", Static).update("[b]Informações da encomenda selecionada:[/b]")
        
        self.query_one("#bt_alterar", Button).disabled = True
        self.query_one("#bt_deletar", Button).disabled = True

    def pegar_checkbox(self):
        'Pega os valores preenchidos nos campos Checkbox para atualizar a tabela.'
        producao = self.query_one("#cbox_producao", Checkbox).value
        finalizada = self.query_one("#cbox_finalizada", Checkbox).value
        vendida = self.query_one("#cbox_vendida", Checkbox).value
        cancelada = self.query_one("#cbox_cancelada", Checkbox).value

        if producao:
            self.checkbox_list.append(1)

        if finalizada:
            self.checkbox_list.append(2)

        if vendida:
            self.checkbox_list.append(3)

        if cancelada:
            self.checkbox_list.append(4)

    def atualizar_tabela_encomendas(self):
        'Atualiza os valores a serem preenchidos na tabela de encomendas.'
        tabela = self.query_one("#tabela_encomendas", DataTable)

        dados_encomendas = controller.listar_encomendas()

        self.pegar_checkbox()

        for id_encomenda, detalhes in dados_encomendas.items():
            nome_produtos = [''.join([f'{nome}, ({quantidade}) | '])
                             for nome, quantidade in detalhes['produtos']]

            status = detalhes['status']
            comentario = detalhes['comentario']

            if status in self.checkbox_list:

                if detalhes['status'] == 1:
                    status = 'Em produção'
                elif detalhes['status'] == 2:
                    status = 'Finalizada'
                elif detalhes['status'] == 3:
                    status = 'Vendida'
                elif detalhes['status'] == 4:
                    status = 'Cancelada'

                if id_encomenda not in tabela.rows:
                    tabela.add_row(id_encomenda, ''.join(nome_produtos),
                                   detalhes['prazo'], comentario, status)

    def resetar_tabela_encomendas(self):
        'Reseta e atualiza a tela de encomendas.'
        tabela = self.query_one("#tabela_encomendas", DataTable)

        tabela.clear()

        self.atualizar_tabela_encomendas()

    def atualizar_tabela_cadastro_encomenda(self):
        'Atualiza os valores a serem preenchidos na tabela de cadastro da encomenda.'
        
        tabela = self.query_one("#tabela_cadastro_encomenda", DataTable)

        for item in self.PRODUTOS_QUANTIDADE.items():
            id_produto, quantidade = item

            _id_produto, nome, _quantidade, _valor_unitario, _valor_custo, _aceita_encomenda, _descricao, _imagem = controller.select_produto_id(
                id_produto)

            tabela.add_row(_id_produto, nome, quantidade)
        
    def resetar_tabela_cadastro_encomenda(self):
        'Reseta e atualiza a tabela de cadastro da encomenda.'

        tabela = self.query_one("#tabela_cadastro_encomenda", DataTable)
        tabela.clear()
        self.atualizar_tabela_cadastro_encomenda()
        self.query_one("#bt_remover", Button).disabled = True
        self.query_one('#quantidade_encomenda', Input).clear()

    def remover_produto_encomenda(self):
        'Remove um produto adicionado em uma encomenda.'

        id_produto = self.PRODUTO_SELECIONADO[0]
        self.PRODUTOS_QUANTIDADE.pop(id_produto)
        self.resetar_tabela_cadastro_encomenda()
        self.notify(title="Removido!", message="Produto removido da encomenda", severity="warning")

    def preencher_alteracoes_encomenda(self):
        'Preenche os campos com as informações da encomenda a ser alterada.'
        novo_prazo = self.query_one("#prazo_alterado", MaskedInput)
        novo_status = self.query_one("#select_status_alterado", Select)
        novo_comentario = self.query_one("#text_comentario_alterado", TextArea)

        _id_encomenda, _produtos, prazo, comentario, status = self.ENCOMENDA_ALTERACAO
        comentario = str(comentario)

        if status == 'Em produção':
            status = 1
        elif status == 'Finalizada':
            status = 2
        elif status == 'Vendida':
            status = 3
        elif status == 'Cancelada':
            status = 4

        if comentario == 'None':
            comentario = ''

        novo_prazo.value = prazo
        novo_status.value = status
        novo_comentario.text = comentario

        self.query_one("#coll_encomendas", Collapsible).collapsed = True
        self.query_one("#bt_alterar", Button).disabled = False
        self.query_one("#bt_deletar", Button).disabled = False
        self.atualizar_static_alteracao_produto()

    def transformar_em_venda(self):
        'Transforma uma encomenda em venda.'
        _id_encomenda, produtos, prazo, comentario, status = self.ENCOMENDA_ALTERACAO
        valor_total_venda = list()
        produtos_quantidade = dict()
        venda_produto_quantidade = dict()

        if status == 'Em produção':
            status = 1
        elif status == 'Finalizada':
            status = 2
        elif status == 'Vendida':
            status = 3
        elif status == 'Cancelada':
            status = 4

        nomes_produtos = produtos.strip(" |").split(" | ") 
        for item in nomes_produtos:
            produto, quantidade = item.split(", ")
            produtos_quantidade[produto] = int(quantidade.strip("()"))
        
        for produto, quantidade in produtos_quantidade.items():
            valor_unitario = controller.select_produto_nome(nome=produto)[3] 
            id_produto = controller.select_produto_nome(nome=produto)[0]
            venda_produto_quantidade[id_produto] = quantidade
            valor_total_venda.append(int(quantidade)*int(valor_unitario))


        valor_final = sum(valor_total_venda)

        controller.insert_venda(data=prazo, valor_final=valor_final, status=status, produtos=venda_produto_quantidade, comentario=comentario)

        self.notify(title="Feito!", message="Encomenda registrada nas vendas")

        produtos_quantidade.clear()
        valor_total_venda.clear()

    @on(Checkbox.Changed)
    async def on_checkbox_change(self, event: Checkbox.Changed):
        'Ações que ocorrem ao selecionar um Checkbox.'
        if len(self.checkbox_list) > 0:
            self.checkbox_list.clear()

        self.resetar_tabela_encomendas()

    @on(DataTable.RowSelected)
    async def on_row_selected(self, event: DataTable.RowSelected):
        'Ações que ocorrem ao selecionar uma linha da tabela.'

        match event.data_table.id:
            case "tabela_cadastro_encomenda":
                self.query_one("#bt_remover", Button).disabled = False 
                encomenda = self.query_one('#tabela_cadastro_encomenda', DataTable)
                self.PRODUTO_SELECIONADO = encomenda.get_row(event.row_key)
        
            case "tabela_encomendas":
                encomenda = self.query_one('#tabela_encomendas', DataTable)
                self.ENCOMENDA_ALTERACAO = encomenda.get_row(event.row_key)
                self.atualizar_static_alteracao()
                self.query_one("#bt_preencher_campos", Button).disabled = False
                self.query_one("#bt_transformar_venda", Button).disabled = False

    @on(Select.Changed)
    async def on_select(self, event: Select.Changed):
        'Ações que ocorrem ao selecionar um item no Select.'
        match event.select.id:
            case 'select_produtos':
                self.ID_PRODUTO = event.select.value
                self.atualizar_static_produto()
                self.query_one('#quantidade_encomenda', Input).clear()
                self.query_one("#bt_remover", Button).disabled = True
                self.query_one("#bt_adicionar_quantidade", Button).disabled = True

            case 'select_id_encomenda':
                self.atualizar_static_alteracao()

    @on(Input.Changed)
    async def on_input(self, event: Input.Changed):
        'Ações que ocorrem ao alterar um Input.'
        match event.input.id:
            case 'quantidade_encomenda':
                self.query_one("#bt_adicionar_quantidade",
                               Button).disabled = False

            case 'prazo_encomenda':
                if event.input.value == '':
                    self.query_one("#bt_cadastrar", Button).disabled = True
                    self.query_one("#bt_limpar", Button).disabled = True
                else:
                    self.query_one("#bt_cadastrar", Button).disabled = False
                    self.query_one("#bt_limpar", Button).disabled = False

    @on(TextArea.Changed)
    async def on_textarea(self, event: TextArea.Changed):
        'Ações que ocorrem ao alterar um campo TextArea.'
        if event.text_area.id == 'text_comentario':
            self.query_one("#bt_limpar", Button).disabled = False

    @on(Button.Pressed)
    async def on_button(self, event: Button.Pressed):
        'Ações que ocorrem ao pressionar botões da TelaEncomendas.'
        match event.button.id:
            case 'bt_adicionar_quantidade':

                self.adicionar_dicionario_encomenda()
                self.resetar_tabela_cadastro_encomenda()
                self.query_one('#static_produto', Static).update(self.texto_static_produto)
                self.query_one("#bt_adicionar_quantidade", Button).disabled = True
            
            case 'bt_remover':
                self.remover_produto_encomenda()

            case 'bt_voltar':
                self.app.switch_screen('tela_inicial')

            case 'bt_cadastrar':
                self.cadastrar_encomenda()

            case 'bt_preencher_campos':
                try:
                    self.preencher_alteracoes_encomenda()
                except:
                    self.notify(title="Ops!", message="Você precisa selecionar uma encomenda", severity='warning')

            case 'bt_transformar_venda':
                self.transformar_em_venda()

            case 'bt_alterar':
                prazo = self.query_one("#prazo_alterado", Input).value

                if len(prazo) < 10:
                    self.notify(title="Data inválida!", message="Preencha o prazo no formato DD/MM/AAAA", severity="warning")
                else:
                    self.update_encomenda()

            case 'bt_deletar':
                self.deletar_encomenda()
                self.resetar_tabela_encomendas()

            case 'bt_limpar':
                self.limpar_inputs()

