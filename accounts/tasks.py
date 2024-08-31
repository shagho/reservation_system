from reservation.celery import app
from accounts.models import PhoneCode


@app.task
def send_code(phone_number):
    PhoneCode.objects.get(phone_number=phone_number).send_code()
