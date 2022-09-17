# Import smtplib for the actual sending function
import smtplib
from flask import Flask,request

# Import the email modules we'll need
from email.mime.text import MIMEText
app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/sendmail', methods='GET')
def sendmail():
  from_user = request.args.get('from');
  to_user = request.args.get('to');
  msg = MIMEText(request.args.get('msg'));

  # me == the sender's email address
  # you == the recipient's email address
  msg['Subject'] = "Hello"
  msg['From'] = from_user
  msg['To'] = to_user

  s = smtplib.SMTP('localhost')
  s.sendmail(from_user, [to_user], msg.as_string())
  s.quit()