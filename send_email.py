from email.mime.text import MIMEText
import smtplib

def send_email(content):
    from_email = "1000dadaytest@gmail.com"
    from_password = "dadaytest1000"
    to_email = "EretzZavatHalavUmas@gmail.com"

    subject = "New comment on your website!"
    message = content

    msg = MIMEText(message, 'html')
    msg['subject'] = subject
    msg['To'] = to_email
    msg['From'] = from_email

    gmail = smtplib.SMTP('smtp.gmail.com', 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(from_email, from_password)
    gmail.send_message(msg)
