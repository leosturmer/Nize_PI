from Controller import controller

from textual.widgets import (Button, Input, Footer, Label, Switch)
from textual.screen import (Screen)
from textual.containers import (HorizontalGroup)

from textual import on

class TelaCadastro(Screen):
    'Tela de cadastro de usuário do sistema.'

    def compose(self):
        with HorizontalGroup():
            yield Label("Nome[red]*[/red]")
            yield Input(placeholder="Nome*", id="input_nome")

        with HorizontalGroup():
            yield Label("E-mail[red]*[/red]")
            yield Input(placeholder="Login*", id="input_login")

        with HorizontalGroup():
            yield Label("Senha[red]*[/red]")
            yield Input(placeholder="Mínimo 6 caracteres", password=True, max_length=50, id="input_senha")

        with HorizontalGroup():
            yield Label("Mostrar senha?")
            yield Switch(id="switch_senha")

        with HorizontalGroup():
            yield Label("Sua loja tem nome? (opcional)")
            yield Input(placeholder="Nome da loja", id="input_nome_loja")

        with HorizontalGroup():
            yield Button("Cadastrar", id="bt_cadastrar")
            yield Button("Voltar", id="bt_voltar")

        yield Footer(show_command_palette=False)

    def limpar_campos(self):
        'Reseta os campos preenchidos da TelaCadastro.'
        self.query_one("#input_login", Input).clear()
        self.query_one("#input_senha", Input).clear()
        self.query_one("#input_nome", Input).clear()
        self.query_one("#input_nome_loja", Input).clear()

    def pegar_dados_vendedor(self):
        'Pega as informações inseridas nos campos de cadastro de usuário.'
        login = self.query_one("#input_login", Input).value.strip()
        senha = self.query_one("#input_senha", Input).value.strip()
        nome = self.query_one("#input_nome", Input).value.strip().capitalize()
        nome_loja = self.query_one("#input_nome_loja", Input).value.strip().capitalize

        return login, senha, nome, nome_loja

    def insert_vendedor(self):
        'Insere os dados de novo usuário no banco de dados do sistema.'
        from hashlib import sha256

        login, senha, nome, nome_loja = self.pegar_dados_vendedor()

        senha_codificada = sha256(senha.encode('utf-8')).digest()

        try:
            controller.insert_vendedor(
                login, senha_codificada, nome, nome_loja)
            self.notify(title="Sucesso!", message="Usuário cadastrado")
            self.app.switch_screen('tela_login')
            self.limpar_campos()

        except:
            self.notify(title="Ops!", message="Algo deu errado", severity="warning")

    @on(Switch.Changed)
    async def on_switch(self, event: Switch.Changed):
        'Ações que ocorrem ao clicar no Switch da tela.'

        mostrar_senha = self.query_one("#switch_senha", Switch).value
        input_senha = self.query_one("#input_senha", Input)

        if mostrar_senha == True:
            input_senha.password = False
        else:
            input_senha.password = True

    @on(Button.Pressed)
    async def on_button(self, event: Button.Pressed):
        'Ações que ocorrem ao clicar nos botões da tela.'
        match event.button.id:
            case 'bt_voltar':
                self.app.switch_screen('tela_login')

            case "bt_cadastrar":
                login, senha, nome, nome_loja = self.pegar_dados_vendedor()

                if not nome or not login or not senha:
                    self.notify(title="Ops!", message="Insira todos os dados necessários", severity="warning")
                elif "@" not in login or ".com" not in login:
                    self.notify(title="Ops!", message="Insira um e-mail válido!", severity="warning")
                elif len(senha) < 6:
                    self.notify(title="Ops!", message="A senha deve ter no mínimo 6 caracteres!", severity="warning")
                else:
                    self.insert_vendedor()
