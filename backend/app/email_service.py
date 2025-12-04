import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()
SMTP_HOST = os.getenv('SMTP_HOST')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
SMTP_USER = os.getenv('SMTP_USER')
SMTP_PASS = os.getenv('SMTP_PASS')
FROM_ADDRESS = os.getenv('FROM_ADDRESS', SMTP_USER)

def send_email(to_address: str, subject: str, body: str):
    if not SMTP_HOST or not SMTP_USER or not SMTP_PASS:
        return False, "SMTP not configured (set SMTP_HOST, SMTP_USER, SMTP_PASS in .env)"
    msg = EmailMessage()
    msg['From'] = FROM_ADDRESS
    msg['To'] = to_address
    msg['Subject'] = subject
    msg.set_content(body)
    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=20) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
        return True, None
    except Exception as e:
        return False, str(e)
