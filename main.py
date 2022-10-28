import sqlite3

from flask import Flask,render_template,redirect,url_for,request,session,send_file,send_from_directory,Response
from flask_mail import Mail,Message
from werkzeug.security import generate_password_hash,check_password_hash
import random
from random import randrange
import pandas as pd
import io
import xlwt
import xlsxwriter
import datetime

app = Flask(__name__)
app.secret_key = "adsceunsp2022"
mail = Mail(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'maxkev25@gmail.com'
app.config['MAIL_PASSWORD'] = 'yhafqwaoxxizzhxi'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

def gen_cod():
    code = []
    for n in range(5):
        code.append(randrange(10))
    # this line is for convert all the elemens in this list for integer~list
    string = [str(integer) for integer in code]
    a_string = "".join(string)
    code_convert = int(a_string)
    return code_convert

def env_conf(dest,cod):
    email = dest
    code = cod
    msg = Message('Verificação de email', sender = 'maxkev25@gmail.com', recipients = [email])
    msg.body = "Seu código de verificação é :  " + str(code)
    """ msg.html = "<b> Hey kevin </b> , sending you this message becase we need to talk man , call me <a href= "" >teste</a>,see"  """
    mail.send(msg)


@app.route("/" , methods = ['GET','POST'])
def home2():
    if request.method == 'POST':
        conn = sqlite3.connect('bd_dados.db')
        c = conn.cursor()

        user = request.form['email']
        password = request.form['password']

        mail = c.execute('SELECT * FROM login WHERE email = ?',([user])).fetchone()
        if mail:
            passw = c.execute('SELECT password FROM login WHERE email = ?', ([user])).fetchone()
            if check_password_hash(passw[0], password):
                u = c.execute('SELECT * FROM login WHERE email = ?', [user]).fetchone()
                n = c.execute('SELECT * FROM aluno WHERE email = ?',[user]).fetchone()
                session['logged'] = True
                session["id"] = u[0]
                session["user"] = n[2]

                conn.commit()
                conn.close()

                return redirect(url_for('user_page'))
            else:
                erro = "passw"
                print("erro na senha !")
        else:
            erro = "mail_wrong"
            msg1 = "E-mail incorreto !"
            print(msg1)

            # if user == 'admin':
            #     session["admin"] = "admin"
            #     return redirect(url_for('pag_admin'))

            conn.commit()
            conn.close()

            return render_template('login.html',msg = msg1)
    else:
        if "user" in session:
            return(redirect(url_for("user_page")))

    return render_template('login.html')

@app.route("/register", methods = ['GET','POST'])
def register():
    if request.method == 'POST':

        conn = sqlite3.connect('bd_dados.db')
        c = conn.cursor()

        nome = request.form['name1']
        nasc = request.form['born1']
        user = request.form['email']

        mail = c.execute('SELECT * FROM login WHERE email = ?',([user])).fetchone()

        if mail:
            print("Usuario já cadastrado !")
        else:
            c.execute('INSERT INTO login (email,password) VALUES (?,?)',
                      (user,generate_password_hash(request.form['password'],method='sha256')))

            u = c.execute('SELECT * FROM login WHERE email = ?', [user]).fetchone()

            c.execute('INSERT INTO aluno (id_log,nome,data_nasc,email) VALUES (?,?,?,?)',(u[0],nome.replace(" ","").lower(),nasc,user))

            session['logged'] = True
            session["id"] = u[0]
            session["user"] = nome

            conn.commit()
            conn.close()

            return redirect(url_for("user_page"))

    elif request.method == 'GET':
        if "user" in session:
            return (redirect(url_for("user_page")))

    return render_template('register.html')

@app.route("/usuarios", methods = ['GET','POST'])
def user_page():
    if "user" in session:
        user = session["user"]

        if request.method == 'POST':
            b = sqlite3.connect('bd_dados.db')
            c = b.cursor()
            dat = datetime.datetime.now()
            n = session["user"]
            date = dat.date()


            d_min = request.form.get('d_min')
            v_min = request.form.get('v_min')
            t_min = request.form.get('t_min')
            q_min = request.form.get('q_min')
            monit = request.form.get('monit')

            c.execute("""
                INSERT INTO form (data,nome_aluno,dez_min,vinte_min,trinta_min,quarenta_min,monitor) VALUES (?,?,?,?,?,?,?);
            """,(date,n,d_min,v_min,t_min,q_min,monit))


            print(n)
            print(date)

            b.commit()
            b.close()

        return render_template('user_interface.html',user = user)
    else:
        return redirect(url_for("home2"))

@app.route("/admin",methods = ['GET','POST'])
def pag_admin():
    if "user" in session:
            if session['user'] == 'kevinalvescorrea':
                banco = None
                relatorio = None
                format = None

                c = sqlite3.connect('bd_dados.db')
                c1 = c.cursor()

                banco = c1.execute("""
                        SELECT * FROM login order by id
                    """).fetchall()

                if request.method == 'POST':

                    conn = sqlite3.connect('bd_dados.db')
                    c = conn.cursor()

                    email = request.form['email']
                    password = request.form['password']

                    relatorio = c.execute('SELECT * FROM login WHERE email = ? AND password = ?',
                                          (email, password)).fetchall()
                    if relatorio:

                        format = relatorio[0]
                        print(format)
                    else:
                        print('nop')

                    conn.commit()
                    conn.close()
                return render_template("admin_interface(list).html",banco = banco,relatorio = relatorio)
            else:
                print('Voce não é o João !')
    else:
        return redirect(url_for("home2"))

@app.route("/logout" )
def logout():
    session.pop("logged",None)
    session.pop("id",None)
    session.pop("user",None)
    return redirect(url_for("home2"))

@app.route("/relatorio",methods=['GET','POST'])
def relatorio():
    if request.method == 'POST':
        b = sqlite3.connect('bd_dados.db')
        c = b.cursor()

        df = pd.read_sql("select * from form", c)
        df.to_excel("excel/saida2.xlsx", index=False)

        b.commit()
        b.close()

        return True

@app.route("/download", methods=['GET'])
def download():
    return send_from_directory(directory='excel',path='',filename='saida2.xlsx')

@app.route("/report", methods=['GET','POST'])
def report():

    # funciona muito bem pq ele gera em XLS
    b = sqlite3.connect('bd_dados.db')
    c = b.cursor()

    c.execute("select * from login")
    banco = c.fetchall()
    print(banco)

    outpout = io.BytesIO()

    workbook = xlwt.Workbook()

    sh = workbook.add_sheet('Report')

    sh.write(0,0,'id')
    sh.write(0,1,'email')
    sh.write(0,2,'pass')


    idx = 0
    for row in banco:
        print(row[0])
        sh.write(idx+1, 0, (row[0]))
        sh.write(idx+1, 1, (row[1]))
        sh.write(idx+1, 2, (row[2]))
        idx += 1

    workbook.save(outpout)
    outpout.seek(0)


    return  Response(outpout, mimetype="application/ms-excel", headers={"Content-Disposition":"attachment;filename=login_report.xls"})

@app.route("/excel",methods=['GET','POST'])
def excel():
    # utilizando o xlsxwriter porque ele gera arquivos em xlsx

    b = sqlite3.connect("bd_dados.db")
    c = b.cursor()

    # c.execute("SELECT * FROM form")
    # banco = c.fetchall()

    outpout = io.BytesIO()

    workbook = xlsxwriter.Workbook(outpout,{'in_memory': True})
    worksheet = workbook.add_worksheet()



    n_tabl = "form"
    t = c.execute("SELECT * FROM pragma_table_info(?);",[n_tabl]).fetchall()
    idx = 0
    for num in t:
        worksheet.write(0,idx, num[1])
        print(num[1])
        idx += 1


    t = c.execute("SELECT * FROM form")
    for i, row in enumerate(t):
        for j, value in enumerate(row):
            worksheet.write(i+1, j, value)


    workbook.close()

    outpout.seek(0)

    return Response(outpout, mimetype="application/ms-excel",
                    headers={"Content-Disposition": "attachment;filename=login_report.xlsx"})

@app.route("/radio", methods=['GET','POST'])
def radio():
    resp = None
    if request.method == 'POST':

        if (request.form.get('choice') != None):
            resp = request.form['choice']
        else:
            resp = "Resposta Inválida"

        print(resp)


    return render_template("radio.html", resp = resp)


@app.route("/cadastro", methods=['GET', 'POST'])
def cadastro():
    email = None
    if request.method == 'POST':
        email = request.form['mail']
        password = request.form['passw']
        session['email'] = email
        return redirect('/confirm_mail')
    return render_template('index_teste.html', email=email)


@app.route("/confirm_mail", methods=['GET', 'POST'])
def index():
    email = session.get('email')
    code = gen_cod()
    print(email, code)
    env_conf(email, code)
    if request.method == 'POST':
        code_user = int(request.form['code_user'])
        print(code_user)
        if (code == code_user):
            print('CORRETO')
            render_template('user.html', user=None, email=None, passw=None)
        else:
            print('INCORRETO')

    return render_template('confirm_mail.html')


if __name__ == "__main__":
    app.run(debug=True)

