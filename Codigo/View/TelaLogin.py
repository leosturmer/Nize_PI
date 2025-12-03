from Controller import controller

from View.TelaInicial import SidebarMenu


from textual.widgets import (Button, Input, Footer, Header, Label, Switch)
from textual.screen import (Screen)
from textual.containers import (VerticalGroup, HorizontalGroup, CenterMiddle)

from textual import on

class TelaLogin(Screen):
    'Tela de login do sistema.'

    def compose(self):
        'Composição da tela.'
        yield Header()

        with CenterMiddle(id="container_login"):
            with VerticalGroup():
                yield Label("Faça o seu login")
                yield Input(placeholder='Login', id="input_login")
                yield Input(placeholder='Senha', password=True, id="input_senha")

            with HorizontalGroup():
                yield Label("Mostrar senha?")
                yield Switch(id="switch_senha")

            with HorizontalGroup():
                yield Button("Entrar", id="bt_login")

            with HorizontalGroup():
                yield Label("Não tem cadastro?")
                yield Button("Cadastrar", id="bt_cadastrar")

            yield Button("Sair", id="bt_sair")

        yield Footer(show_command_palette=False)

    def verificar_login(self):
        'Função de validação do login. Ele faz a criptografia para validar a senha.'
        import hashlib
        from hashlib import sha256

        input_login = self.query_one("#input_login", Input).value.strip()
        input_senha = self.query_one("#input_senha", Input).value.strip()

        if not input_login or not input_senha:
            self.notify(title="Epa!", message="Preencha todos os campos obrigatórios", severity="warning")
            return

        try:
            id_vendedor, login, senha, nome, nome_loja = controller.select_vendedor(
                input_login)

            senha_hash = hashlib.sha256(input_senha.encode('utf-8')).digest()

            if input_login == login and senha_hash == senha:
                self.notify(title="Sucesso!", message="Login realizado")
                self.app.switch_screen('tela_inicial')

        except TypeError:
            self.notify(title="Ops!", message="Login ou senha incorretos!", severity='error')

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
            case 'bt_login':
                self.verificar_login()

            case "bt_sair":
                self.app.exit()

            case "bt_cadastrar":
                self.app.switch_screen("tela_cadastro")

