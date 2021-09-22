from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def tt(code,mail):
    to=mail
    subject="確認メール"
    body=f"認証コード:___{code}"
    send_mail(to,subject,body)

def send_mail(to,subject,body):
    ID = "b.ou.sys20@morijyobi.ac.jp"
    PASS = "13144621680wwm00"
    HOST = "smtp.gmail.com"
    PORT = 587

    msg = MIMEMultipart()
    msg.attach(MIMEText(body, "html"))
    msg["Subject"] = subject
    msg["From"] = ID
    msg["To"] = to
    server=SMTP(HOST, PORT)
    server.starttls()   
    server.login(ID, PASS) 

    server.send_message(msg)    

    server.quit()
    print("送信完了")       
