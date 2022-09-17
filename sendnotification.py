import smtplib

def sendmail(recipient, content,title):
    sender = 'victormaina1962@gmail.com'
    receivers = [recipient]
    message = content
    try:
        smtpObj = smtplib.SMTP('localhost')
        smtpObj.sendmail(sender, receivers, message)         
    except SMTPException:
        print ("Error: unable to send email")
    finally:
       print ("Successfully sent email")  
