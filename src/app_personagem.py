import asyncio

import flet
from flet import ThemeMode, Text, Button, TextField, OutlinedButton, Column, CrossAxisAlignment, Container, Colors, \
    FontWeight, View, AppBar, Icon, ListView, ListTile, PopupMenuButton, PopupMenuItem, FloatingActionButton, Row, \
    BorderRadius, Alignment, TextAlign, Divider
from flet.controls.core import list_view
from flet.controls.material.icons import Icons
from sqlalchemy import select

from src.models import Personagem, SessionLocalExemplo


def main(page: flet.Page):
    # Configurações
    page.title = "Primeiro APP"
    page.theme_mode = ThemeMode.DARK
    page.window.width = 400
    page.window.height = 700

    lista_dados = []

    # Funções

    def salvar_tudo():
        page.update()
        personagem = Personagem(
            nome=input_nome.value,
            universo=input_universo.value,
            forca=input_nivelforca.value,
            durabilidade=input_niveldurabilidade.value,
            velocidade=input_nivelvelocidade.value,
            poder=input_poder.value
        )
        db = SessionLocalExemplo()
        db.add(personagem)
        db.commit()
        db.close()

        mostrar_nome_text.value = f"Personagem cadastrado: {input_nome.value}"
        mostrar_universo_text.value = f"Universo cadastrado: {input_universo.value}"
        mostrar_forca_text.value = f"Nível de força cadastrado: {input_nivelforca.value}"
        mostrar_durabilidade_text.value = f"Nível de durabilidade cadastrado: {input_niveldurabilidade.value}"
        mostrar_velocidade_text.value = f"Nível de velocidade cadastrado: {input_nivelvelocidade.value}"
        mostrar_poder_text.value = f"Poder cadastrado: {input_poder.value}"

        tem_erro = False

        if input_nome.value:
            input_nome.error = None
        else:
            tem_erro = True
            input_nome.error = "campo obrigatório"

        if input_universo.value:
            input_universo.error = None
        else:
            tem_erro = True
            input_universo.error = "campo obrigatório"

        if input_nivelforca.value:
            input_nivelforca.error = None
        else:
            tem_erro = True
            input_nivelforca.error = "campo obrigatório"

        if input_niveldurabilidade.value:
            input_niveldurabilidade.error = None
        else:
            tem_erro = True
            input_niveldurabilidade.error = "campo obrigatório"

        if input_nivelvelocidade.value:
            input_nivelvelocidade.error = None
        else:
            tem_erro = True
            input_nivelvelocidade.error = "campo obrigatório"

        if input_poder.value:
            input_poder.error = None
        else:
            tem_erro = True
            input_poder.error = "campo obrigatório"

        if tem_erro == False:
            input_nome.value = ''
            input_universo.value = ''
            input_nivelforca.value = ''
            input_niveldurabilidade.value = ''
            input_nivelvelocidade.value = ''
            input_poder.value = ''

            navegar("/")

    def buscar_personagem(id):
        db = SessionLocalExemplo()
        try:
            stmt = select(Personagem).where(Personagem.id == id)
            personagem = db.execute(stmt).scalar_one_or_none()  # .scalars().all() para obter uma lista de objetos

            print(type(personagem))
            if personagem:
                mostrar_nome_text.value = f'Nome: {personagem.nome}'
                mostrar_universo_text.value = f'Universo: {personagem.universo}'
                mostrar_forca_text.value = f'Força: {personagem.forca}'
                mostrar_durabilidade_text.value = f'Durabilidade: {personagem.durabilidade}'
                mostrar_velocidade_text.value = f'Velocidade: {personagem.velocidade}'
                mostrar_poder_text.value = f'Poder: {personagem.poder}'

                navegar("/detalhes")


        finally:
            db.close()

    def montar_lista_personagens():
        list_view.controls.clear()

        db = SessionLocalExemplo()
        try:
            stmt = select(Personagem)
            personagens = db.execute(stmt).scalars().all()  # .scalars().all() para obter uma lista de objetos

            for item in personagens:
                list_view.controls.append(
                    ListTile(
                        leading=Icon(Icons.PERSON, color=Colors.BLUE),
                        title=item.nome,
                        subtitle=item.poder,
                        trailing=PopupMenuButton(
                            icon=Icons.MORE_VERT,
                            items=[
                                PopupMenuItem("Ver Detalhes", icon=Icons.REMOVE_RED_EYE, on_click=lambda _, personagem=item: buscar_personagem(personagem.id)),
                                PopupMenuItem("Excluir", icon=Icons.DELETE, on_click=lambda: excluir(item)),
                            ]
                        ),

                    )
                )
        finally:
            db.close()

    def excluir(item):
        lista_dados.remove(item)
        montar_lista_personagens()

    # Navegar
    def navegar(route):
        asyncio.create_task(
            page.push_route(route)
        )

    # Gerenciar as telas(routes)
    def route_change():
        page.views.clear()

        montar_lista_personagens()

        page.views.append(
            View(
                route="/",
                controls=[
                    Container(
                        Column([
                            AppBar(
                                title="Lista de personagens",
                                bgcolor=Colors.DEEP_PURPLE_700
                            ),

        list_view,

        ],
        horizontal_alignment = CrossAxisAlignment.CENTER,
        ),
        bgcolor = Colors.BLACK,
        padding = 15,
        border_radius = 10,
        width = 400,
        ),

        ],
                floating_action_button=FloatingActionButton(
                    icon=Icons.ADD,
                    on_click=lambda: navegar("/primeira_tela")),
        )
        ),
        if page.route == "/primeira_tela":
            page.views.append(
                View(
                    route="/primeira_tela",
                    controls=[
                        AppBar(
                            title="Cadastro",
                            bgcolor=Colors.BLACK
                        ),
                        cadastrar_text,
                        input_nome,
                        input_universo,
                        input_nivelforca,
                        input_niveldurabilidade,
                        input_nivelvelocidade,
                        input_poder,
                        btn_salvar_tudo,

                    ]
                )
            )
        elif page.route == "/detalhes":
            page.views.append(
                View(
                    route="/detalhes",
                    controls=[
                        flet.AppBar(
                            title="Detalhes",
                        ),
                        Container(
                            Column([
                                Row([
                                mostrar_nome_text,
                                ],
                                    height=30,
                                    width=300
                                ),
                                Divider(),
                                Row([
                                    mostrar_universo_text,

                                ],
                                height=20,
                                width=300
                                ),
                                Divider(),
                                Row([
                                    mostrar_forca_text,
                                ],
                                height=20,
                                width=300
                                ),
                                Divider(),
                                Row([
                                    mostrar_durabilidade_text,
                                ],
                                    height=20,
                                width=300
                                ),
                                Divider(),
                                Row([
                                    mostrar_velocidade_text,
                                ],
                                    height=20,
                                width=300
                                ),
                                Divider(),
                                Row([
                                    mostrar_poder_text,
                                ],
                                    height=20,
                                width=300
                                ),
                            ],
                            width=300,

                            ),
                            bgcolor=Colors.GREY_700,
                            border_radius=BorderRadius.all(5),
                            align=Alignment.CENTER,
                            height=340,
                            width=300
                        ),

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
    input_universo = TextField(label="Universo")
    input_nivelforca = TextField(label="Nível de força")
    input_niveldurabilidade = TextField(label="Nível de durabilidade")
    input_nivelvelocidade = TextField(label="Nível de velocidade")
    input_poder = TextField(label="Poder")
    btn_salvar_tudo = OutlinedButton("Salvar", on_click=salvar_tudo)

    # pag 2
    list_view = ListView(height=500)
    mostrar_nome_text = Text(text_align=TextAlign.CENTER,width=300, height=40)
    mostrar_universo_text = Text(text_align=TextAlign.CENTER,width=300)
    mostrar_forca_text = Text(text_align=TextAlign.CENTER,width=300)
    mostrar_durabilidade_text = Text(text_align=TextAlign.CENTER,width=300)
    mostrar_velocidade_text = Text(text_align=TextAlign.CENTER,width=300)
    mostrar_poder_text = Text(text_align=TextAlign.CENTER,width=300)

    # Eventos
    page.on_route_change = route_change
    page.on_view_pop = view_pop

    route_change()


flet.run(main)
