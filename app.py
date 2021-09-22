from flask import Flask,render_template,request,redirect,url_for,session
import random
import string
import hashlib
import db
from datetime import timedelta
import items


app = Flask(__name__)

app.secret_key = "".join(random.choices(string.ascii_letters,k=256))

# ログイン画面
@app.route("/login")  
def login():
    return render_template("login.html")

# トップページ
@app.route("/top_page",methods=["POST"])
def top_page():
    mail = request.form.get("mail")
    pw = request.form.get("pw")

    reuslt = db.login(mail,pw)
    if reuslt != None :
        session["user"] = True
        session["mail"] = mail
        session.permanent = True # セッションの有効期限有効化
        app.permanent_session_lifetime = timedelta(minutes=30) # 有効期限の値の設定
        return render_template("top_page.html")
    else :
        error = "メール又はパスワードが間違いました"
        return render_template("login.html",error=error)

# アカウント作成
@app.route("/new_account")
def new_account():
    session["new_account"] = True
    session.permanent = True # セッションの有効期限有効化
    app.permanent_session_lifetime = timedelta(minutes=30)
    if "new_account" in session:
        return render_template("new_account.html")
    else :
        error="セッションエラー"
        return render_template("login.html",error=error)

@app.route("/new_account_all",methods=["POST"])
def new_account_all():

    name = request.form.get("name")
    pw =request.form.get("pw")
    mail = request.form.get("mail")
    birth = request.form.get("birth")
    class_name = request.form.get("class_name")
    pow =request.form.get("gen")

    list = db.select_mail()
    flg = True
    for i in list:
        if mail in i:
            flg = False
            break
    session["new_account_data"] = [name,pw,mail,birth,class_name,pow]
    if pow == "0":
        p = "男"
    elif pow == "1":
        p = "女"
    if class_name == "1":
        c = "情報システム科"
    elif class_name == "2":
        c = "ネットワークセキュリティ科"
    elif class_name == "3":
        c = "高度情報工学科"

    if "new_account" in session:
        if flg:
            return render_template("new_account_all.html",name=name,birth=birth,class_name=c,p=p,mail=mail)
        else :
            s = "メールアドレスは重複しています"
            return render_template("new_account.html",s=s)
    else :
        error="セッションエラー"
        return render_template("login.html",error=error)

@app.route("/mail")
def mail():

    code = ''.join(random.choices(string.ascii_letters,k=7))
    session["code"] = code
    mail = session["new_account_data"][2]
    t = items.tt(code,mail)
    if "new_account" in session:
        return render_template("mail.html",code=code)
    else :
        error="セッションエラー"
        return render_template("login.html",error=error)

@app.route("/true")
def code_true():

    c = request.args.get("code")

    code = session["code"]
    pw = session["new_account_data"][1]
    name = session["new_account_data"][0]
    birth = session["new_account_data"][3]
    pow = session["new_account_data"][5]
    class_name = session["new_account_data"][4]
    mail = session["new_account_data"][2]

    if "new_account" in session:
        if c == code:
            salt = db.get_salt()
            b_pw = bytes(pw, "utf-8")
            b_salt = bytes(salt, "utf-8")
            hashed_pw = hashlib.pbkdf2_hmac("sha256", b_pw, b_salt, 2560).hex()
            print(len(hashed_pw))
            print(hashed_pw)


            db.insert(name,hashed_pw,salt,mail,birth,pow,class_name)
            s = "登録成功しました。"
            session.pop("new_account_data",None)
            session.pop("code",None)
            return render_template('login.html',s=s)

        else:
            mail_error = "codeが間違いました"
            return render_template("mail.html",mail_error=mail_error)
    else :
        error="セッションエラー"
        return render_template("login.html",error=error)

@app.route("/student")
def student():
    if "user" in session:
        return render_template("top_page.html")
    else :
        error="セッションエラー"
        return render_template("login.html",error=error)

@app.route("/search_student")
def search_student():
    id = request.args.get("id")
    student = db.select_student(id)
    if "user" in session:
        if student :
            return render_template("search_student.html",student=student)
        else :
            s="検索失敗"
            return render_template("top_page.html",s=s)
    else :
        error="セッションエラー"
        return render_template("login.html",error=error)

@app.route("/insert_student")
def insert_student():
    name = request.args.get("name")
    kana = request.args.get("kana")
    gen = request.args.get("gen")
    class_name = request.args.get("class_name")
    g = int(gen)
    if class_name == "1":
        c = 1
    elif class_name == "2":
        c = 2
    else :
        c = 3
    result = db.insert_student(name,kana,g,c)


    if "user" in session:
        if result:
            s = "登録成功"
        else :
            s = "登録失敗"
        return render_template("insert_student.html",s=s)
    else :
        error="セッションエラー"
        return render_template("login.html",error=error)

@app.route("/student_all")
def student_all():
    list = db.select_all()
    if "user" in session:
        return render_template("student_all.html",list=list)
    else :
        error="セッションエラー"
        return render_template("login.html",error=error)

@app.route("/teacher_student")
def teacher_student():
    mail = session["mail"]
    class_name = db.select_student_2(mail)
    print(class_name[0])
    print(type(class_name[0]))

    student_2 = db.select_student_3(class_name)
    if "user" in session:
        return render_template("teacher_student.html",student_2=student_2)
    else :
        error="セッションエラー"
        return render_template("login.html",error=error)


@app.route("/delete_student")
def delete_student():
    if "user" in session:
        return render_template("delete_student.html")
    else :
        error="セッションエラー"
        return render_template("login.html",error=error)


@app.route("/delete_end")
def delete_end():
    id = request.args.get("id")
    result = db.delete_student(id)
    if "user" in session:
        if result:
            s = "削除完了"
        else :
            s = "削除失敗"
        return render_template("delete_end.html",s=s)
    else :
        error="セッションエラー"
        return render_template("login.html",error=error)

@app.route("/logout")
def logout():
    session.pop("user",None)
    session.pop("mail",None)

    return render_template("login.html")

if __name__ == '__main__':
    app.run(debug=True)