import os
from django.conf import settings
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

client = Client(os.environ['TWILIO_ACCOUNT_SID'], os.environ['TWILIO_AUTH_TOKEN'])
verify = client.verify.services(os.environ['TWILIO_VERIFY_SERVICE_SID'])


def send(phone):
    verify.verifications.create(to=str('+91')+phone, channel='sms')


def check(phone, code):
    try:
        result = verify.verification_checks.create(to=str('+91')+phone, code=code)
    except TwilioRestException:
        print('no')
        return False
    return result.status == 'approved'
