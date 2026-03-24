from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import flet
from flet import ThemeMode, Text, Button, TextField, OutlinedButton, Column, CrossAxisAlignment
from flet.controls import page
from flet.controls.border_radius import horizontal


def main(page: flet.Page):

    #Configurações
    page.title = "Primeiro APP"
    page.theme_mode = ThemeMode.DARK
    page.window.width = 400
    page.window.height = 700

    #Funções
    def salvar_nome_completo():
        text.value = f"Olá {input_nome.value} {input_sobrenome.value}"
        page.update()

    def par_impar():
        if int(input_numero.value) % 2 == 0:
            numero.value = f"{input_numero.value} é Par"

        else:
            numero.value = f"{input_numero.value} é Impar"

    def maior_menor():
        data_convertida = datetime.strptime(input_data.value, "%d/%m/%Y")
        idade_do_sujeito = datetime.now().year - data_convertida.year
        print(f"idade em anos:{idade_do_sujeito}")
        if data_convertida.month > datetime.now().month:
            idade_do_sujeito -= 1
        if idade_do_sujeito < 18:
            idade.value = f"a sua idade é:{idade_do_sujeito} anos, você é menor de idade"
        else:
            idade.value = f"a sua idade é:{idade_do_sujeito} anos, você é maior de idade"


    #Componentes
    text = Text()
    input_nome = TextField(label="Nome")
    input_sobrenome = TextField(label="Sobrenome")
    btn_salvar = OutlinedButton("Salvar", on_click=salvar_nome_completo)

    numero = Text()
    texto_parimpar = Text('Insira um número para saber se ele é impar ou par')
    input_numero = TextField(label="Numero")
    btn_calcular = OutlinedButton("Calcular", on_click=par_impar)

    idade = Text()
    texto_data = Text('Insira sua data de nascimento')
    input_data = TextField(label="Idade")
    btn_calcular_idade = OutlinedButton("Calcular Idade", on_click=maior_menor)

    #Construção da tela
    page.add(
        Column(
            [
                input_nome,
                input_sobrenome,
                btn_salvar,
                text,
                texto_parimpar,
                input_numero,
                btn_calcular,
                numero,
                texto_data,
                input_data,
                btn_calcular_idade,
                idade

            ],
            horizontal_alignment=CrossAxisAlignment.CENTER
        )
    )



flet.app(main)