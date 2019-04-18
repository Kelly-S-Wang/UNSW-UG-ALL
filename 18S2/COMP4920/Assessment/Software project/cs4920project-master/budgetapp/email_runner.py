import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
 
def send_email(recepient, subject, text_body):

    msg = MIMEMultipart()
    msg['From'] = "Lorem Ipsum 4920"
    msg['To'] = recepient
    msg['Subject'] = subject
    body = text_body

    msg.attach(MIMEText(body, 'html'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    fromaddr = "loremipsum4920@gmail.com"
    server.login(fromaddr, "thisRocks")
    text = msg.as_string()
    server.sendmail(fromaddr, recepient, text)
    server.quit()