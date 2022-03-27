def send_email(text):
    import smtplib

    #getting the email username and password
    gmail_user = 'eretzzavathalavumas@gmail.com'
    gmail_password = 'gcrmsvqzowfumrot'

    #declaring the sent-from, send-to, subject and the email
    sent_from = 'User'
    to = ['eretzzavathalavumas@gmail.com']
    subject = 'New Message from TaxCalculatorIsrael'
    message = 'Subject: {}\n\n{}'.format(subject, text)

    #trying to send the email and return True, if it fails return False
    try:
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.ehlo()
        smtp_server.login(gmail_user, gmail_password)
        smtp_server.sendmail(sent_from, to, message.encode('utf-8'))
        smtp_server.close()
        return True
    except Exception as ex:
        print("Something went wrong…", ex)
        return False
