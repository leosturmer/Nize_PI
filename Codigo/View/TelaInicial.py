from textual import on

from textual.widgets import (Button, Checkbox, Switch, Label)
from textual.screen import (Screen)
from textual.containers import (
    Container, VerticalGroup, HorizontalGroup)

class SidebarMenu(Container):
    'Menu lateral vertical do sistema.'

    def compose(self):

        with VerticalGroup(id="grupo_botoes_inicial"):
            yield Button("Produtos", id="bt_produtos", classes="botoes_inicial", variant="primary")
            yield Button("Encomendas", id="bt_encomendas", classes="botoes_inicial", variant="success")
            yield Button("Vendas", id="bt_vendas", classes="botoes_inicial", variant="warning")
            yield Button("Pesquisa", id="bt_pesquisa", classes="botoes_inicial", variant='error', disabled=True)
            yield Button("Tela inicial", id="bt_inicial", classes="botoes_inicial")

        return super().compose()

    def on_button_pressed(self, event: Button.Pressed):
        'Eventos que ocorrem ao apertar os botões.'
        match event.button.id:
            case "bt_produtos":
                self.app.switch_screen("tela_produtos")
            case "bt_encomendas":
                self.app.switch_screen("tela_encomendas")
            case "bt_vendas":
                self.app.switch_screen("tela_vendas")
            case "bt_pesquisa":
                self.app.switch_screen("tela_pesquisa")
            case "bt_inicial":
                self.app.switch_screen("tela_inicial")

class TelaInicial(Screen):
    'Tela Inicial do sistema.'

    def compose(self):
        with VerticalGroup(id="grupo_botoes_inicial"):
            yield Button("Produtos", id="bt_produtos", classes="botoes_inicial", variant="primary")
            yield Button("Encomendas", id="bt_encomendas", classes="botoes_inicial", variant="success")
            yield Button("Vendas", id="bt_vendas", classes="botoes_inicial", variant="warning")
            yield Button("Pesquisa", id="bt_pesquisa", classes="botoes_inicial", variant='error', disabled=True)
            yield Button("Sair", id="bt_sair", classes="botoes_inicial")
        
        with HorizontalGroup(id="trocar_cor"):
            yield Label(content="🌞🌛", id="sol_lua")
            yield Switch(id="switch_trocar_cor")

    @on(Switch.Changed)
    async def on_switch_changed(self, event: Switch.Changed):
        switch = self.query_one("#switch_trocar_cor", Switch)
                
        match self.app.theme:
            case 'textual-dark':
                self.app.theme = 'catppuccin-latte'
            case 'catppuccin-latte':
                self.app.theme = 'textual-dark'

    @on(Button.Pressed)
    async def on_button(self, event: Button.Pressed):
        'Ações que ocorrem ao clicar nos botões da tela.'

        match event.button.id:
            case "bt_produtos":
                self.app.switch_screen("tela_produtos")
            case "bt_encomendas":
                self.app.switch_screen("tela_encomendas")
            case "bt_vendas":
                self.app.switch_screen("tela_vendas")
            case "bt_pesquisa":
                self.app.switch_screen("tela_pesquisa")

            case "bt_sair":
                self.app.exit()

