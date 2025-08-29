import logging
import azure.functions as func
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import json

SENDGRID_KEY = os.getenv('SENDGRID_API_KEY')
FROM_EMAIL = os.getenv('FROM_EMAIL', 'noreply@langunana.com')

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        data = req.get_json()
    except Exception:
        data = req.params
    email = data.get('email')
    username = data.get('username', '')
    t = data.get('type', 'signup')
    if not email:
        return func.HttpResponse("Missing email", status_code=400)

    subject = "Welcome to Langunana" if t=='signup' else "Welcome back to Langunana"
    content = f"Hi {username},\n\nThanks for {('registering' if t=='signup' else 'logging in')} to Langunana!\n\n— Langunana Team"

    message = Mail(from_email=FROM_EMAIL, to_emails=email, subject=subject, plain_text_content=content)
    try:
        sg = SendGridAPIClient(SENDGRID_KEY)
        resp = sg.send(message)
        return func.HttpResponse(json.dumps({'status':'sent','code':resp.status_code}), status_code=200, mimetype='application/json')
    except Exception as e:
        logging.exception(e)
        return func.HttpResponse("Error sending email", status_code=500)
