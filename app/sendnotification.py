# import smtplib

# def sendmail(recipient, content,title):
#     sender = 'victormaina1962@gmail.com'
#     receivers = [recipient]
#     message = content
#     # try:
#     smtpObj = smtplib.SMTP('localhost')
#     smtpObj.sendmail(sender, receivers, message)         
#     # except SMTPException:
#     #     print ("Error: unable to send email")
#     # finally:
#     #    print ("Successfully sent email")  
# recipient='mugechivictor@students.must.ac.ke'
# content='Hello there brother'
# title='Greetings'
# sendmail(recipient, content,title)
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
def sendmail(from_address,to_address, content):
    from_address = 'johndoe@gmail.com'
    to_address = 'johndoe@gmail.com'
    message = MIMEMultipart('Foobar')
    message['From'] = from_address
    message['To'] = to_address
    content = MIMEText(content, 'plain')
    message.attach(content)
    mail = smtplib.SMTP('smtp.gmail.com', 587)
    mail.ehlo()
    mail.starttls()
    mail.login(from_address, 'password')
    mail.sendmail(from_address,to_address, message.as_string())
    mail.close()

