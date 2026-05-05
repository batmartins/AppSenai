import asyncio

import flet
from flet import ThemeMode, Text, Button, TextField, OutlinedButton, Column, CrossAxisAlignment, Container, Colors, \
    FontWeight, View, AppBar


def main(page: flet.Page):
    # Configurações
    page.title = "Primeiro APP"
    page.theme_mode = ThemeMode.DARK
    page.window.width = 400
    page.window.height = 700

    # Funções

    def salvar_tudo():
        page.update()
        mostrar_nome_text.value = f"Usuário cadastrado: {input_nome.value}"
        mostrar_cpf_text.value = f"CPF cadastrado: {input_cpf.value}"
        mostrar_email_text.value = f"Email cadastrado: {input_email.value}"
        mostrar_salario_text.value = f"Salário cadastrado: R${input_salario.value}"

        tem_erro = False

        if input_nome.value:
            input_nome.error = ""
        else:
            tem_erro = True
            input_nome.error = "campo obrigatório"

        if input_cpf.value:
            input_cpf.error = ""
        else:
            tem_erro = True
            input_cpf.error = "campo obrigatório"

        if input_email.value:
            input_email.error = ""
        else:
            tem_erro = True
            input_email.error = "campo obrigatório"

        if input_salario.value:
            input_salario.error = ""
        else:
            tem_erro = True
            input_salario.error = "campo obrigatório"


        if tem_erro == False:
            input_nome.value = ''
            input_cpf.value = ''
            input_email.value = ''
            input_salario.value = ''

            navegar("/segunda_tela")

    # Navegar
    def navegar(route):
        asyncio.create_task(
            page.push_route(route)
        )

    # Gerenciar as telas(routes)
    def route_change():
        page.views.clear()
        page.views.append(
            View(
                route="/",
                controls=[
                    AppBar(
                        title="Primeira página",
                        bgcolor=Colors.DEEP_PURPLE_700
                    ),
                    cadastrar_text,
                    input_nome,
                    input_cpf,
                    input_email,
                    input_salario,
                    btn_salvar_tudo
                ]
            )
        )
        if page.route == "/segunda_tela":
            page.views.append(
                View(
                    route="/segunda_tela",
                    controls=[
                        Column([
                            AppBar(
                                title="Segunda página"
                            ),
                            mostrar_nome_text,
                            mostrar_cpf_text,
                            mostrar_email_text,
                            mostrar_salario_text
                        ],
                            horizontal_alignment=CrossAxisAlignment.CENTER,
                        )

                    ]
                )
            )

    async def view_pop(e):
        if e.view is not None:
            page.views.remove(e.view)
            top_view = page.views[-1]
            await page.push_route(top_view.route)

    # Componentes
    # pag 1
    cadastrar_text = Text("insira suas informações:")
    input_nome = TextField(label="Nome")
    input_cpf = TextField(label="CPF")
    input_email = TextField(label="E-mail")
    input_salario = TextField(label="Salário")
    btn_salvar_tudo = OutlinedButton("Salvar", on_click=salvar_tudo)



    # pag 2
    mostrar_nome_text = Text()
    mostrar_cpf_text = Text()
    mostrar_email_text = Text()
    mostrar_salario_text = Text()

    # Eventos
    page.on_route_change = route_change
    page.on_view_pop = view_pop

    route_change()


flet.run(main)