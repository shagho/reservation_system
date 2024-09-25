from reservation.celery import app
from notifications import KavenegarSMS



@app.task
def send_inform(phone_number, status):
    sms = KavenegarSMS()
    sms.inform(phone_number, status)
    sms.send()
