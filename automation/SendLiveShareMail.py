import pyperclip
import smtplib, os, datetime
from email.message import EmailMessage

to = username = 'capthestone@gmail.com'
password = 'mvjt lzvg gfyn pgoa'
logfile = 'smtpLogin.txt'

clipboard_content = pyperclip.paste()
msg = EmailMessage()
msg.set_content(clipboard_content)
msg['Subject'] = 'Connect to my VSCode!'
msg['From'] = username
msg['To'] = to

# Send the email
try:
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()  # Upgrade to a secure connection
        server.login(username, password)
        server.sendmail(username, to, msg.as_string())
    print("Email sent successfully!")
except Exception as e:
    print(f"Error: {e}")
    if not os.path.isfile(logfile):
        with open(logfile, 'w') as f:
            pass
        
    with open(logfile, 'r+') as f:
        f.readlines()
        f.write(f'{datetime.datetime.today()} ({username=},{to=})[{clipboard_content=}]: {e=}\n')
        pass
