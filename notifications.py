from kavenegar import *

from django.conf import settings



class KavenegarSMS:

    def __init__(self):
        self.api = KavenegarAPI(settings.KAVENEGAR_API_KEY)

    def register(self, receptor=None, code=None, password=None):
        self.params = {
            'receptor': receptor,
            'template': 'otp-code-res',
            'token': code,
            'type': 'sms'
        }
    
    def inform(self, receptor=None, status=None, password=None):
        self.params = {
            'receptor': receptor,
            'template': 'res-inform',
            'token': status,
            'type': 'sms'
        }

    def send(self):
        flag = True
        for i, j in self.params.items():
            if j is None:
                flag = False
        if flag:
            try:
                return self.api.verify_lookup(self.params)
            except APIException as e:
                return e
            except HTTPException as e:
                return e
        else:
            raise APIException