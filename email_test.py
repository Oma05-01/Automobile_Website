import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

sender_email = 'oesigbone@gmail.com'
sender_password = 'mgtj dweb qvqb zsgf'  # or app-specific password

try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    print("Successfully authenticated!")
    server.quit()
except smtplib.SMTPAuthenticationError as e:
    print(f"SMTP Authentication error: {e.smtp_error.decode('utf-8')}")
except smtplib.SMTPException as e:
    print(f"SMTP error occurred: {str(e)}")
except Exception as e:
    print(f"Unexpected error occurred: {str(e)}")