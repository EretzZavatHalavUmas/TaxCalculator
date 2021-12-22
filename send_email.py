from email.mime.text import MIMEText
import smtplib

def send_email(email, height, average_height, count):
    from_email = "1000dadaytest@gmail.com"
    from_password = "dadaytest1000"
    to_email = email

    subject = "height data"
    message = "hey there your height is <strong>%s</strong> [cm]" \
              " average is <strong>%s</strong> [cm] out of <strong>%s</strong> peoples" % (height, average_height, count)

    msg = MIMEText(message, 'html')
    msg['subject'] = subject
    msg['To'] = to_email
    msg['From'] = from_email

    gmail = smtplib.SMTP('smtp.gmail.com', 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(from_email, from_password)
    gmail.send_message(msg)
