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

    def salvar_nome():
        page.update()
        mostrar_nome_text.value = f"Olá {input_nome.value}!"
        input_nome.value = ''
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
                    nome_text,
                    input_nome,
                    btn_salvar_nome
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
                            mostrar_nome_text
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
    nome_text = Text("insira o seu nome:")
    input_nome = TextField(label="Nome")
    btn_salvar_nome = OutlinedButton("Salvar", on_click=salvar_nome)

    # pag 2
    mostrar_nome_text = Text()

    # Eventos
    page.on_route_change = route_change
    page.on_view_pop = view_pop

    route_change()


flet.run(main)
