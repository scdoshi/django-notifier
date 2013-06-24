###############################################################################
## Imports
###############################################################################
from django.conf import settings
from django.template.loader import render_to_string
from notifier.backends import BaseBackend
from twilio.rest import TwilioRestClient


###############################################################################
## Backends
###############################################################################
TWILIO_ACCOUNT_SID = getattr(settings, 'TWILIO_ACCOUNT_SID', None)
TWILIO_AUTH_TOKEN = getattr(settings, 'TWILIO_AUTH_TOKEN', None)
TWILIO_FROM_NUMBER = getattr(settings, 'TWILIO_FROM_NUMBER', None)
client = TwilioRestClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


class TwilioBackend(BaseBackend):
    name = 'sms-twilio'
    display_name = 'SMS'
    description = 'Send via SMS using Twilio'

    def send(self, user, context=None):
        super(TwilioBackend, self).send(user, context)

        message = render_to_string(self.template, self.context)

        sms = client.sms.messages.create(
            to=user.phone,
            from_=TWILIO_FROM_NUMBER,
            body=message
        )
        return True


###############################################################################
## Notifications
###############################################################################
