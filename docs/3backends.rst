========
Backends
========

Backends are classes that define how a notification will be sent via a particular method. The ``email`` backend works out of the box using the django email settings. Other custom backends can be written to support other methods of sending notifications.


Email Backend
=============

The email backend sends email notifications using Django's default email settings. The backend uses 2 templates for every notification:

    * Email Subject: 
        notify/<notification-name>_email_subject.txt
    * Email Message: 
        notify/<notification-name>_email_message.txt

The templates already have the User and the Site objects passed in as context variables, additional context variables can be passed in using the send method for the notification. For e.g.

::

    extra_context = {
        'var1': value1,
        'var2': value2
    }

    send_notification('notification-name', [user1, user2], extra_context)

The EmailBackend can be extended if required to change behaviour.

::

    from notifier.backends import EmailBackend


Custom Backend
==============

Custom backends should be extended from the ``BaseBackend`` class. The ``send`` method in a backend class deals with how the actual message is sent.

The template used by default will be ``notify/<notification-name>_<backend-name>.txt``


BaseBackend
-----------

::

    class BaseBackend(object):
        # Name of backend method associated with this class
        name = None
        display_name = None
        description = None

        def __init__(self, notification, *args, **kwargs):
            # self.notifier = Notifier.objects.get(name=self.name)
            self.notification = notification
            self.template = ('/notifier/%s_%s.txt' % (notification.name, self.name))

        # Define how to send the notification
        def send(self, user, context=None):
            if not context:
                self.context = {}
            else:
                self.context = context

            self.context.update({
                'user': user,
                'site': Site.objects.get_current()
            })


Example
-------

An example of a custom backend to send SMS messages via Twilio.

::

    from django.conf import settings
    from django.template.loader import render_to_string
    from notifier.backends import BaseBackend
    from twilio.rest import TwilioRestClient

    TWILIO_ACCOUNT_SID = getattr(settings, 'TWILIO_ACCOUNT_SID', None)
    TWILIO_AUTH_TOKEN = getattr(settings, 'TWILIO_AUTH_TOKEN', None)
    TWILIO_FROM_NUMBER = getattr(settings, 'TWILIO_FROM_NUMBER', None)
    client = TwilioRestClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    # self.template = 'notify/<notification-name>_sms-twilio.txt'

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
