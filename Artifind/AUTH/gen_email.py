from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import ssl
from typing import List
from dotenv import dotenv_values
from typing import List
import smtplib



config_credentials = dotenv_values(".env")


async def send_emaill(subject: str, recipients: List[str], body: str) -> None:

    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "Smart.Reservoir@gmail.com"
    password = "hackerman31"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = ", ".join(recipients)
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, recipients, message.as_string())
 
    
