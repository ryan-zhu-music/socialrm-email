from flask import Flask, request
import base64
from email.message import EmailMessage
import json

import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

app = Flask(__name__)

@app.route('/')
def index():
  return "Hello, World!"

# adapted significantly from google quickstart guides
@app.route('/sendmail', methods=['POST'])
def sendmail():
  f_headers = request.headers
  
  if app.debug: print(f_headers)
  
  if not ('msg' in f_headers and 'from' in f_headers and 'to' in f_headers and 'token' in f_headers):
    if app.debug: print("some headers missing")
    return 'invalid input', 400
  
  u_from = f_headers['from']
  u_to = f_headers['to']
  msg_text = f_headers['msg']
  mail_token = json.loads(f_headers['token'])
  if app.debug: print("From: {} To: {}\r\nMessage:\r\n{}\r\nToken:\r\n{}".format(u_from, u_to, msg_text, mail_token))
  
  creds = Credentials.from_authorized_user_info(mail_token, SCOPES)
  if creds and creds.expired and creds.refresh_token: creds.refresh(Request())
  
  
  try:
    service = build('gmail', 'v1', credentials=creds)
    message = EmailMessage()
    message.set_content(msg_text)
    message['To'] = u_to
    message['From'] = u_from
    message['Subject'] = "Whats up?" ## TODO: add optional header in request
    
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    
    create_message = {
      'raw': encoded_message
    }
    send_message = (service.users().messages().send(userId="me", body=create_message).execute())
    return 'Email sent. Message ID: {}'.format(send_message), 200
  except HttpError as error:
    return 'An error has occured: {}'.format(error), 500

if __name__ == '__main__':
    app.run(threaded=True)