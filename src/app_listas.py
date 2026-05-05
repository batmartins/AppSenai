import asyncio

import flet
from flet import ThemeMode, Text, Button, TextField, OutlinedButton, Column, CrossAxisAlignment, Container, Colors, \
    FontWeight, View, AppBar, FloatingActionButton, Icons, ListView, Card, Row, Icon, ListTile, PopupMenuButton, \
    PopupMenuItem, DropdownOption, Dropdown
from sqlalchemy import select

from src.models import Pessoa, SessionLocalExemplo


def main(page: flet.Page):

    #Configurações
    page.title = "Listas APP"
    page.theme_mode = ThemeMode.DARK
    page.window.width = 400
    page.window.height = 700

    lista_dados = []

    # Funções

    def montar_lista_texto():
        list_view.controls.clear()

        for item in lista_dados:
            list_view.controls.append(
                Text(item)
            )

    def montar_lista_card():
        list_view.controls.clear()

        for item in lista_dados:
            list_view.controls.append(
                Card(
                    height=50,
                    content=Row([
                        Icon(Icons.PERSON),
                        Text(item)
                    ],
                    margin=8
                    ),
                )
            )

    def montar_lista_padrao():
        list_view.controls.clear()

        db = SessionLocalExemplo()
        try:
            stmt = select(Pessoa)
            pessoas = db.execute(stmt).scalars().all()  # .scalars().all() para obter uma lista de objetos


            for item in pessoas:

                list_view.controls.append(
                    ListTile(
                        leading= Icon(Icons.MALE, color=Colors.BLUE) if item.sexo == "Masculino" else Icon(Icons.FEMALE, color=Colors.PINK),
                        title=item.nome,
                        subtitle=item.profissao,
                        trailing=PopupMenuButton(
                            icon=Icons.MORE_VERT,
                            items=[
                                PopupMenuItem("Ver Detalhes", icon=Icons.REMOVE_RED_EYE),
                                PopupMenuItem("Excluir", icon=Icons.DELETE, on_click=lambda: excluir(item)),
                            ]
                        ),

                    )
                )
        finally:
            db.close()

    def salvar_dados():
        nome = input_nome.value.strip()
        profissao = input_profissao.value.strip()
        sexo = input_sexo.value.strip()

        tem_erro = False

        if nome:
            input_nome.error = None
        else:
            tem_erro = True
            input_nome.error = "Campo obrigatório"

        if sexo:
            input_sexo.error = None
        else:
            tem_erro = True
            input_profissao.error = "Campo obrigatório"

        if profissao:
            input_profissao.error = None
        else:
            tem_erro = True
            input_profissao.error = "Campo obrigatório"

        if tem_erro == False:
            page.update()
            pessoa = Pessoa(
                nome=input_nome.value,
                sexo=input_sexo.value,
                profissao=input_profissao.value)
            db = SessionLocalExemplo()
            db.add(pessoa)
            db.commit()
            db.close()
            input_nome.value = ''
            input_sexo.value = ''
            input_profissao.value = ''
            print(pessoa.nome)
            print(pessoa.sexo)
            print(pessoa.profissao)

        montar_lista_padrao()


    def excluir(item):
        lista_dados.remove(item)
        montar_lista_padrao()

    #Navegar
    def navegar(route):
        asyncio.create_task(
            page.push_route(route)
        )

    #Gerenciar as telas(routes)
    def route_change():
        page.views.clear()
        page.views.append(
            View(
                route="/",
                controls=[
                    AppBar(
                        title="Exemplos de listas",
                        bgcolor=Colors.DEEP_PURPLE_700
                    ),
                    Button("Lista de texto", on_click= lambda: navegar("/lista_texto")),
                    Button("Lista de card", on_click= lambda: navegar("/lista_card")),
                    Button("Lista padrão Android", on_click= lambda: navegar("/lista_padrao"))
                ]
            )
        )
        if page.route == "/lista_texto":
            montar_lista_texto()
            page.views.append(
                View(
                    route="/lista_texto",
                    controls=[
                        AppBar(
                            title="Lista de texto",
                        ),
                        input_nome,
                        btn_salvar,
                        list_view,
                    ]
                )
            )
        elif page.route == "/lista_card":
            montar_lista_card()
            page.views.append(
                View(
                    route="/lista_card",
                    controls=[
                        AppBar(
                            title="Lista de card",
                        ),
                        input_nome,
                        btn_salvar,
                        list_view,
                    ]
                )
            )
        elif page.route == "/lista_padrao":
            montar_lista_padrao()
            page.views.append(
                View(
                    route="/lista_padrao",
                    controls=[
                        AppBar(
                            title="Lista padrão Android",
                        ),
                        list_view
                    ],
                    floating_action_button=FloatingActionButton(
                        icon=Icons.ADD,
                        on_click=lambda: navegar("/form_cadastro")
                    )
                )
            )
        elif page.route == "/form_cadastro":
            page.views.append(
                View(
                    route="/form_cadastro",
                    controls=[
                        AppBar(
                            title="Lista de cadastro",
                        ),
                        input_nome,
                        input_sexo,
                        input_profissao,
                        btn_salvar,
                    ]
                )
            )

    async def view_pop(e):
        if e.view is not None:
            page.views.remove(e.view)
            top_view = page.views[-1]
            await page.push_route(top_view.route)

    # Componentes
    mostrar_nome_text = Text()
    mostrar_sexo_text = Text()
    mostrar_profissao_text = Text()
    input_sexo = Dropdown(
        label="Sexo",
        editable=True,
        options=[
            DropdownOption("Masculino"),
            DropdownOption("Feminino"),
        ],
    )
    input_profissao = TextField(label="Profissão", hint_text="Digite sua profissão", on_submit=salvar_dados)
    input_nome = TextField(label="Nome", hint_text="digite seu nome")
    btn_salvar = Button("Salvar", width=400, on_click=lambda: salvar_dados())
    list_view = ListView(height=500)


    # Eventos
    page.on_route_change = route_change
    page.on_view_pop = view_pop


    route_change()

flet.run(main)