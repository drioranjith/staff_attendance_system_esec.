import smtplib
import random
import json
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def generate_otp():
    return random.randint(100000, 999999)

def send_otp_email(receiver_email, otp):
    sender_email = "esecaidsattendance@gmail.com"
    sender_password = "relv ebpz xnpj aain"  # Use Gmail App Password
    subject = "Your OTP Code"
    body = f"Your OTP code is: {otp}"
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
