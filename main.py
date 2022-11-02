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

def troca_mail(m_old,m_new):

    b = sqlite3.connect('bd_dados.db')
    c = b.cursor()

    exist = c.execute('SELECT email FROM login WHERE email = ? ',(m_old))
    if exist:
        c.execute("""
            UPDATE login
            SET email = ?
            WHERE email = ?;
        """, (m_new, m_old))


    else:
        return

    b.commit()
    b.close()

    return True

def troca_senha(p_old,p_new,email):

    b = sqlite3.connect('bd_dados.db')
    c = b.cursor()

    conf = c.execute("""
        SELECT password FROM login WHERE email = ?;
    """, [email]).fetchall()

    chave = ''
    for n in conf:
        chave = n[0]

    mail = c.execute("""SELECT email FROM login WHERE email = ? """,[email])

    if mail:
        if check_password_hash(chave,p_old) == True:

          n_pass1 = generate_password_hash(p_new,method='sha256')
          c.execute("""
            UPDATE login SET 
            password = ? 
            WHERE email = ?;
          """,(n_pass1,email)).fetchall()

          return "Success"

        else:
            return "Senha não confere ! "
    else:
        return "Email não confere ! "


@app.route("/" , methods = ['GET','POST'])
def home2():
    if request.method == 'POST':
        conn = sqlite3.connect('bd_dados.db')
        c = conn.cursor()

        user = request.form['email']
        password = request.form['password']

        mail = c.execute('SELECT * FROM login WHERE email = ?',([user])).fetchone()
        if mail:
            if user != 'professor@sistema.com':
                passw = c.execute('SELECT password FROM login WHERE email = ?', ([user])).fetchone()
                if check_password_hash(passw[0], password):
                    u = c.execute('SELECT * FROM login WHERE email = ?', [user]).fetchone()
                    session['logged'] = True
                    session["id"] = u[0]
                    session["user"] = u[1]
                    print(u[1])
                    session["mail"] = user

                    conn.commit()
                    conn.close()

                    return redirect(url_for('user_page'))
                else:
                    erro = "passw"
                    print("erro na senha !")
            else:
                passw = c.execute('SELECT password FROM login WHERE email = ?', ([user])).fetchone()
                if check_password_hash(passw[0], password):
                    u = c.execute('SELECT * FROM login WHERE email = ?', [user]).fetchone()
                    session['logged'] = True
                    session["id"] = u[0]
                    session["mail"] = user

                    conn.commit()
                    conn.close()

                    return redirect(url_for('pag_admin'))

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
        passw = request.form['password']

        mail = c.execute('SELECT * FROM login WHERE email = ?',([user])).fetchone()

        if mail:
            print("Usuario já cadastrado !")
        else:

            session['n'] = nome
            session['nas'] = nasc
            session['u'] = user
            session['p'] = passw
            session['cad'] = 'y'

            return redirect(url_for("enviar"))

    elif request.method == 'GET':
        if "user" in session:
            return (redirect(url_for("user_page")))

    return render_template('register.html')

@app.route("/redefinirSenha ",methods=['POST','GET'])
def redef_senha():
    if request.method == 'POST':

        email = request.form.get('email')

        b = sqlite3.connect('bd_dados.db')
        c = b.cursor()

        m_sess = c.execute("""SELECT email FROM login WHERE email = ?""", [email]).fetchall()
        if (m_sess):
            for n in m_sess[0]:
                session['mail'] = n
            return redirect(url_for("enviar"))
        else:
            print("Email não existe !")



    return render_template("email.html")

@app.route("/enviar",methods =['GET'])
def enviar():
    if session.get('cad'):
        print("vim do cadastro")
        mail = session.get('u')
        code = gen_cod()
        session['cod'] = code
        print("Codigo gerado e o email  ",mail , code )
        env_conf(mail,code)
        print("Email enviado !")
        return redirect(url_for("conf_mail"))
    else:
        print("vim da recuperação de senha ")
        mail = session.get('mail')
        code = gen_cod()
        session['cod'] = code
        print("Codigo gerado e o email  ", mail, code)
        env_conf(mail, code)
        print("Email enviado !")
        return redirect(url_for("conf_mail"))


@app.route("/confirm_mail/", methods=['GET','POST'])
def conf_mail():
    code = session.get('cod')

    if request.method == 'POST':
        if session.get('cad') == 'y':

            nome = session.get('n')
            nasc = session.get('nas')
            user = session.get('u')
            passw = session.get('p')


            if request.form.get('code_user') != "":
                print(request.form['code_user'])
                code_user = int(request.form['code_user'])
                print(code_user)
                if (code == code_user):

                    conn = sqlite3.connect('bd_dados.db')
                    c = conn.cursor()

                    c.execute('INSERT INTO login (email,password) VALUES (?,?)',
                                  (user, generate_password_hash(passw, method='sha256')))

                    u = c.execute('SELECT * FROM login WHERE email = ?', [user]).fetchone()

                    c.execute('INSERT INTO aluno (id_log,nome,data_nasc) VALUES (?,?,?)',
                                (u[0], nome.replace(" ", "").lower(), nasc))

                    session['logged'] = True
                    session["id"] = u[0]
                    session["user"] = nome

                    session.pop('cad',None)
                    session.pop('cod',None)

                    conn.commit()
                    conn.close()

                    return redirect(url_for("user_page"))

                else:
                    print('INCORRETO')

        else:
            mail = session.get('mail')
            if request.form.get('code_user') != "":
                print(request.form['code_user'])
                code_user = int(request.form['code_user'])
                print(code_user)
                if (code == code_user):
                    session.pop('cod',None)
                    return redirect(url_for('troca_senha'))
                else:
                    print('codigo incorreto')

    return render_template('conf_cad.html')

@app.route("/trocasenha",methods = ['GET','POST'])
def troca_senha():

    if request.method == 'POST':
        if request.form.get('password') and request.form.get('password2')!= "":
            b = sqlite3.connect('bd_dados.db')
            c = b.cursor()

            m = session.get('mail')
            p = request.form.get('password')

            print(session.get('mail'))

            c.execute("""
                        UPDATE login 
                        SET password = ? 
                        WHERE email = ?;
            """,(generate_password_hash(p,method='sha256'),m))


            u = c.execute('SELECT * FROM login WHERE email = ?', [m]).fetchone()
            n = c.execute('SELECT nome FROM aluno WHERE id_log = ?',[u[0]]).fetchall()
            session['logged'] = True
            session["id"] = u[0]
            session["user"] = n[0]

            session.pop('mail', None)
            b.commit()
            b.close()
            print('senha trocada')
            return redirect(url_for("user_page"))



    return render_template("troca_senha.html")

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
            monit = request.form.get('monitor')

            c.execute("""
                INSERT INTO form (data,nome_aluno,dez_min,vinte_min,trinta_min,quarenta_min,monitor) VALUES (?,?,?,?,?,?,?);
            """,(date,n,d_min,v_min,t_min,q_min,monit))


            print(n)
            print(date)

            b.commit()
            b.close()

        return render_template('pag_user.html',user = user)
    else:
        return redirect(url_for("home2"))

@app.route("/admin",methods = ['GET','POST'])
def pag_admin():
    if "mail" in session:
            if session['mail'] == 'professor@sistema.com':
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
                return redirect(url_for('home2'))
    else:
        return redirect(url_for("home2"))

@app.route("/logout" )
def logout():
    session.pop("logged",None)
    session.pop("id",None)
    session.pop("user",None)
    session.pop("mail",None)
    return redirect(url_for("home2"))

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

    b = sqlite3.connect("bd_dados.db")
    c = b.cursor()

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

@app.route("/termos", methods=['GET','POST'])
def termos():
    return render_template('termos.html')

@app.route("/teste",methods=['GET','POST'])
def teste():
    result = troca_senha('123123123','gike2519','kevinalvesk12@gmail.com')
    return render_template("admin_page.html",result = result)



if __name__ == "__main__":
    app.run(debug=True)

