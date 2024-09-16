from flet import *
import flet as ft
import pymysql
import popup1 
import popup2
def main(page: ft.Page):
    page.window_width = 350
    page.window_height = 450
    page.window_resizable = False
    page.window_always_on_top = True
    page.scroll = 'auto'
    page.title = 'Gestão de Atleta'

    

    # Conectar ao banco de dados MySQL
    conn = pymysql.connect(
        host='banco',
        user='usuario',
        passwd='senha',
        database='base de dados',
                  
        )
    cursor = conn.cursor()
    

    # Função para criar a página principal
    def pagina_principal():
        atleta = ft.Row([
            ft.Container(
                content=ft.Text("Novo Atleta"),
                margin=3,
                padding=10,
                alignment=ft.alignment.center,
                bgcolor=ft.colors.CYAN_200,
                width=150,
                height=150,
                border_radius=10,
                ink=True,
                on_click=lambda _: page.go("/adicionar"),
            ),
            ft.Container(
                content=ft.Text("Todos Atletas"),
                margin=3,
                padding=10,
                alignment=ft.alignment.center,
                bgcolor=ft.colors.CYAN_200,
                width=150,
                height=150,
                border_radius=10,
                ink=True,
                on_click=lambda _: page.go("/listar"),
            ),
        ])

        turmas = ft.Row([
            ft.Container(
                content=ft.Text("Time Azul"),
                margin=3,
                padding=10,
                alignment=ft.alignment.center,
                bgcolor=ft.colors.CYAN_200,
                width=150,
                height=150,
                border_radius=10,
                ink=True,
                on_click=lambda _: page.go("/turmacinco"),
            ),
            ft.Container(
                content=ft.Text("Time Vinho"),
                margin=3,
                padding=10,
                alignment=ft.alignment.center,
                bgcolor=ft.colors.CYAN_200,
                width=150,
                height=150,
                border_radius=10,
                ink=True,
                on_click=lambda _: page.go("/turmaseis"),
            ),
        ])

        # Adiciona a linha de ícones à página
        page.add(atleta, turmas)
    
      
    def add_atleta():
        nome = ft.TextField(label="Nome")
        idade = ft.TextField(label="Idade")
        modalidade = ft.TextField(label="Modalidade")
        page.update()

        cabecario=ft.Row(
            controls=[
            ft.IconButton(icon='home', on_click=lambda _: page.go("/")),
            ft.Text("Cadastro de atleta")       
            ]
        )
        page.add(cabecario,nome, idade, modalidade)
        page.add(ft.TextButton("Adicionar Atleta", on_click=lambda e: validar_atleta()))
        
        def validar_atleta():
            if not nome.value.strip():
                page.add(ft.Text("Nome obrigatório", color="red"))
            elif not idade.value.strip():
                page.add(ft.Text("Idade obrigatório", color="red"))
            elif not modalidade.value.strip():
                page.add(ft.Text("Modalidade obrigatório", color="red"))
            else:
                page.add(ft.Text("atleta cadastrado", color="green"))
                        
                query= "INSERT atleta (nome,idade,modalidade) VALUES (%s,%s,%s)"
                valor= nome.value,idade.value,modalidade.value
                cursor.execute(query,valor)
                
                nome.value=""
                idade.value=""
                modalidade.value=""
                conn.commit()
                page.update()        
   
   
    def listar_todosatletas():
        cabecario=ft.Row(
            controls=[
            ft.IconButton(icon='home', on_click=lambda _: page.go("/")),
            ft.Text("Todos Atletas")       
            ]
        )
        data_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Nome")),
                ft.DataColumn(ft.Text("Idade")),
                ft.DataColumn(ft.Text("Modalidade"))
            ],
            rows=[]
        )

        # Carregar dados do banco de dados
        cursor.execute("SELECT id, nome, idade, modalidade FROM atleta")
        for id, nome, idade, modalidade in cursor.fetchall():
            data_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(id))),
                        ft.DataCell(ft.Text(nome)),
                        ft.DataCell(ft.Text(str(idade))),
                        ft.DataCell(ft.Text(modalidade))
                    ]
                )
            )
        page.add(cabecario, data_table)
        page.update()
    
    
    def buscarporid():
        cabecario=ft.Row(
            controls=[
            ft.IconButton(icon='home', on_click=lambda _: page.go("/")),
            ft.Text("Time Azul")       
            ])
        page.add(cabecario)
        popup2.confirmar(page)
        
    def buscarporid2():
        cabecario=ft.Row(
            controls=[
            ft.IconButton(icon='home', on_click=lambda _: page.go("/")),
            ft.Text("Time Vinho")       
            ])
        page.add(cabecario)
        popup1.confirmar(page)
        
            
    def carregar_rota(e):
        page.controls.clear()
        if page.route == "/adicionar":
            add_atleta()
        elif page.route == "/listar":
            listar_todosatletas()
        elif page.route == "/turmacinco":
            buscarporid()
        elif page.route == "/turmaseis":
            buscarporid2()
        else:
            pagina_principal()
        page.update()

    # Definir a rota padrão
    page.route = "/"
    page.on_route_change = carregar_rota
    page.go(page.route)

    # Fechar a conexão quando a página é encerrada
    def fechar_conexao(e):
        conn.close()

    page.on_close = fechar_conexao
    
    
ft.app(target=main) 
