import flet as ft
import pymysql
import main
# Conectar ao banco de dados MySQL
conn = pymysql.connect(
        host='banco',
        user='usuario',
        passwd='senha',
        database='base de dados',
                  
        )
cursor = conn.cursor()
                
def confirmar(page: ft.Page):
    entrada_id = ft.TextField(label="ID")
    res_vazio = ft.Text("Campo obrigatório", color="red")
    res_azul = ft.Text("Confirmado no time azul", color="blue")
    page.add(entrada_id)
    
    def validar_id(e):
        # Limpa mensagem de erro e reinicia o diálogo
        res_vazio.visible = False
        res_azul.visible = False
        dlg.open = False
        
        if not entrada_id.value.strip():
            res_vazio.visible = True
            if res_vazio not in page.controls:
                page.add(res_vazio)
        else:
            page.dialog = dlg
            dlg.open = True
        
        page.update()
    def hidedlg(e):
        dlg.open = False
        conn.commit()
        page.update
        entrada_id.value = ""
        page.update()  # Atualiza a página
    
    def add_no_time():
        if not entrada_id.value.strip():
            res_vazio.visible = True
            if res_vazio not in page.controls:
                page.add(res_vazio)
        elif entrada_id.value.strip(): 
            input_id=int(entrada_id.value)
            query = "SELECT 1 FROM atleta WHERE id = %s"
            valor = (input_id,)  # Certifique-se de que isso seja uma tupla

            # Executa a consulta
            cursor.execute(query, valor)

            # Recupera os resultados
            record = cursor.fetchall()

                    # Verifica se o registro existe
            if record:
                res_azul.visible = True
                if res_azul not in page.controls:
                    page.add(res_azul)
                atualizar="UPDATE atleta SET id_usuario = 1 WHERE id= %s "
                cursor.execute(atualizar,valor)
            else:
                page.add(ft.Text("O registro não existe.", color="red"))
                conn.commit()
                page.update()
    def reniciar_time():
                atualizar="UPDATE atleta SET id_usuario = 3 WHERE id_usuario = 1 "
                cursor.execute(atualizar)
    dlg = ft.AlertDialog(
        modal=True,
        content=ft.Container(
            bgcolor='green200',
            padding=10,
            content=ft.Column([
                ft.Row([
                    ft.ElevatedButton('Check-In', on_click=lambda e: add_no_time()),
                    
                    ft.IconButton(
                        icon='close', 
                        on_click=hidedlg,
                        
                    )
                ], alignment='spaceBetween'),
                ft.ElevatedButton('Reniciar Time', on_click=lambda e: reniciar_time()),
                

            ])
            
        )
    )

    page.add(ft.TextButton("Confirmar", on_click=validar_id))
    page.update()

    data_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Nome"))
            ],
            rows=[]
        )

        # Carregar dados do banco de dados
    cursor.execute("SELECT id,nome FROM atleta WHERE id_usuario=1")
    for id, nome in cursor.fetchall():
            data_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(id))),
                        ft.DataCell(ft.Text(nome)),
                    ]
                )
            )
    page.add(data_table)
