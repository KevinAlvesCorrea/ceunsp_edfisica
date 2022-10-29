import sqlite3
from werkzeug.security import generate_password_hash,check_password_hash

b = sqlite3.connect('bd_dados.db')
c = b.cursor()

"comnando usado para listar as tabelas criadas no banco de dados "
c.execute("""
    SELECT name FROM sqlite_master
     WHERE type='table';
""")

q2 = """
    SELECT * FROM login;
"""

q1 = """
    INSERT INTO login(id,email,password) VALUES (1,"kevin@kevin.com","123")
"""

"comnando usado para listar as tabelas criadas no banco de dados "
consult = """
    SELECT name FROM sqlite_master  
    WHERE type='table';
"""


table_login = """
    CREATE TABLE login(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
    );
"""

table_aluno = """
    CREATE TABLE aluno(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_log INTEGER,
    nome VARCHAR(60) NOT NULL,
    data_nasc TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    FOREIGN KEY (id_log) REFERENCES login(id)
    );
"""

table_form = """
    CREATE TABLE IF NOT EXISTS form (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data TEXT NOT NULL,
        nome_aluno VARCHAR(60) NOT NULL,
        dez_min INTEGER NOT NULL,
        vinte_min INTEGER NOT NULL,
        trinta_min INTEGER NOT NULL,
        quarenta_min INTEGER NOT NULL,
        monitor VARCHAR(10) NOT NULL
        );
"""

id_user = 1
user = "seguranca@seguranca.com"

'mostra somente os primeiros 5 caracters de uma string (muito legal esse comando !)'
# print(user[0:5])

'''
u = cursor.execute('SELECT * FROM login WHERE email = ?',[user]).fetchone()
print(u)
'''

# table = cursor.execute('SELECT * FROM login')

# df = pd.read_sql("select * from form",conn)
# df.to_excel("saida2.xlsx", index=False)

# t = cursor.execute("INSERT INTO ALUNO (id_log,nome,data_nasc,email) VALUES (1,'kevin','2001-04-

# t = cursor.execute("SELECT * FROM login")
# for i,row in enumerate(t):
#     for j,value in enumerate(row):
#         worksheet.write(i,j,value)
'listar campos de um tabela '
# t = cursor.execute("SELECT * FROM pragma_table_info('form');").fetchall()
# for num in t:
#     print(num[1])

s = 'Ceunsp@2022'
c.execute("""
    INSERT INTO login (email,password) VALUES (?,?)
""",("professor@sistema.com",generate_password_hash(s,method='sha256')))
print(c.fetchall())

b.commit()
b.close()






