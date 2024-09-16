
import pymysql
conexao =pymysql.connect(
        host='localhost',
        user='root',
        passwd='',
        database='cadastroalunos',
     
)
conn = conexao.cursor()
# Definir o comando SQL para criar a tabela
conn.execute("CREATE TABLE IF NOT EXISTS aula(id INT AUTO_INCREMENT PRIMARY KEY)")
conn.execute("INSERT INTO aula(id) VALUES(1)")
conn.execute("INSERT INTO  aula(id) VALUES(2)")
conn.execute("INSERT INTO  aula(id) VALUES(3)")
conn.execute("CREATE TABLE IF NOT EXISTS atleta(id INT AUTO_INCREMENT PRIMARY KEY, nome VARCHAR(40), idade INT(2), modalidade VARCHAR(20),id_usuario INT, FOREIGN KEY (id_usuario) REFERENCES aula(id))")