import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from termcolor import colored

def rainbow_text(text):
    colors = ['red', 'yellow', 'green', 'cyan', 'blue', 'magenta']
    return ''.join(colored(char, colors[i % len(colors)]) for i, char in enumerate(text))

banner = r"""
  _________                     _____  _____         .__.__                
 /   _____/_____   ____   _____/ ____\/     \ _____  |__|  |   ___________ 
 \_____  \\____ \ /  _ \ /  _ \   __\/  \ /  \\__  \ |  |  | _/ __ \_  __ \
 /        \  |_> >  <_> |  <_> )  | /    Y    \/ __ \|  |  |_\  ___/|  | \/
/_______  /   __/ \____/ \____/|__| \____|__  (____  /__|____/\___  >__|   
        \/|__|                              \/     \/             \/       
"""

print(rainbow_text(banner))
print(colored("                    SMTP Mailer Tool", 'cyan'))
print(colored("                    Version: 1.0", 'cyan'))
print(colored("                    Author: G4UR4V007", 'cyan'))
print(colored("Disclaimer: Please use this tool responsibly. Do not send unsolicited emails. The author is not responsible for any misuse.", 'yellow'))

SMTP_HOST = 'your_host'
SMTP_PORT = 587
SMTP_USER = 'your_userid'
SMTP_PASS = 'your_pass'

from_address = input(colored("From (email): ", 'white'))
from_name = input(colored("From (name): ", 'white'))

to_address = input(colored("To: ", 'white'))
subject = input(colored("Subject: ", 'white'))

priority = input(colored("Flag this message as high priority? [yes|no]: ", 'white')).strip().lower()

body = []
print(colored("Enter the body of the email (type 'END' to finish):", 'white'))
while True:
    line = input()
    if line.strip().upper() == 'END':
        break
    body.append(line)
body_text = "\n".join(body)

attachment_path = input(colored("Enter path to attachment (leave blank for none): ", 'white')).strip()

msg = MIMEMultipart()
msg['From'] = f"{from_name} <{from_address}>"
msg['To'] = to_address
msg['Subject'] = subject

if priority == 'yes':
    msg['X-Priority'] = '1'  # High priority
    msg['Priority'] = 'urgent'
    msg['Importance'] = 'high'

msg.attach(MIMEText(body_text, 'plain'))

if attachment_path and os.path.isfile(attachment_path):
    with open(attachment_path, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header(
        'Content-Disposition',
        f'attachment; filename={os.path.basename(attachment_path)}',
    )
    msg.attach(part)

try:
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)
    print(colored("Email sent successfully!", 'green'))
except Exception as e:
    print(colored(f"Failed to send email: {str(e)}", 'red'))
