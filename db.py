import MySQLdb
import hashlib
import random
import string

def login(mail,pw):
    salt = search_salt(mail)

    if salt == None:
        return None

    b_pw = bytes(pw,"utf-8")
    b_salt = bytes(salt,"utf-8")
    hashed_pw = hashlib.pbkdf2_hmac("sha256",b_pw,b_salt,2560).hex()

    result = search_account(mail,hashed_pw) 

    return result

def get_salt():
    salt = ''.join(random.choices(string.ascii_letters,k=64))
    return salt

def search_salt(mail):
    conn = get_connection()
    cur = conn.cursor()

    sql = "SELECT salt FROM user WHERE mail = %s"

    try:
        cur.execute(sql, (mail,))
    except Exception as e:
        print("SQL実行に失敗：" , e)

    result = cur.fetchone()

    cur.close()
    conn.close()

    if result:
        return result[0]

    return None

def search_account(mail,hashed_pw):
    conn = get_connection()
    cur = conn.cursor()

    sql = "SELECT name FROM user WHERE mail = %s AND pw = %s"

    try:
        cur.execute(sql, (mail,hashed_pw))
    except Exception as e:
        print("SQL実行に失敗：" , e)

    result = cur.fetchone()

    cur.close()
    conn.close()

    return result




def get_connection():
    return MySQLdb.connect(user='root',passwd="13144621680wwm00",host='localhost',db='flask',charset="utf8")


def select_all():
    conn = get_connection()
    cur = conn.cursor()

    sql = "select * from student"

    try:
        cur.execute(sql, ())
    except Exception as e:
        print("SQL実行に失敗：" , e)

    result = cur.fetchall()

    cur.close()
    conn.close()

    return result

def select_student(id):
    conn = get_connection()
    cur = conn.cursor()

    sql = "SELECT * FROM student WHERE student_id = %s"

    try :
        cur.execute(sql, (id,))
    except Exception as e:
        print("SQL実行に失敗：" , e)

    result = cur.fetchone()

    cur.close()
    conn.close()

    return result

def insert_student(name,kana,g,c):
    conn = get_connection()
    cur = conn.cursor()

    sql = "insert into student(name_kan,name_kana,gender,class) values(%s,%s,%s,%s)"

    try :
        cur.execute(sql, (name,kana,g,c,))
    except Exception as e:
        print("SQL実行に失敗：" , e)


    conn.commit()
    cur.close()
    conn.close()
    
    return True

def select_mail():
    conn = get_connection()
    cur = conn.cursor()

    sql = "SELECT mail FROM user"

    try :
        cur.execute(sql, ())
    except Exception as e:
        print("SQL実行に失敗：" , e)

    result = cur.fetchall()

    cur.close()
    conn.close()

    return result

def select_student_2(mail):
    conn = get_connection()
    cur = conn.cursor()

    sql = "SELECT class_name FROM user WHERE mail = %s"

    try :
        cur.execute(sql, (mail,))
    except Exception as e:
        print("SQL実行に失敗：" , e)

    result = cur.fetchone()

    cur.close()
    conn.close()

    return result

def select_student_3(class_name):
    conn = get_connection()
    cur = conn.cursor()

    sql = "SELECT * FROM student WHERE class = %s"

    try :
        cur.execute(sql, (class_name,))
    except Exception as e:
        print("SQL実行に失敗：" , e)

    result = cur.fetchall()

    cur.close()
    conn.close()

    return result

def delete_student(id):
    conn = get_connection()
    cur = conn.cursor()

    sql = 'DELETE FROM student WHERE student_id = %s'

    try :
        cur.execute(sql, (id,))
    except Exception as e:
        print("SQL実行に失敗：" , e)


    conn.commit()
    cur.close()
    conn.close()
    return True

def insert(name,pw,salt,mail,birth,pow,class_name):
    conn = get_connection()
    cur = conn.cursor()

    sql = "insert into user(name,pw,salt,mail,birth,pow,class_name) VALUES (%s,%s,%s,%s,%s,%s,%s)"

    try:
        cur.execute(sql, (name,pw,salt,mail,birth,pow,class_name,))
    except Exception as e:
        print("SQL実行に失敗：" , e)


    conn.commit()
    cur.close()
    conn.close()

def get_connection():
    return MySQLdb.connect(user='root',passwd="password",host='localhost',db='flask',charset="utf8")
