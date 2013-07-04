========
Backends
========

Backends are classes that define how a notification will be sent via a particular method. The ``email`` backend works out of the box using the django email settings. Other custom backends can be written to support other methods of sending notifications.


Email Backend
=============

The email backend sends email notifications using Django's default email settings. Two templates are required per notification to form the email:

    * Subject: ``notifier/<notification-name>_email_subject.txt``

    * Message: ``notifier/<notification-name>_email_message.txt``

The templates already have the User and the Site objects passed in as context variables, additional context variables can be passed in using the send method for the notification. For e.g.

::

    extra_context = {
        'var1': value1,
        'var2': value2
    }

    send_notification('notification-name', [user1, user2], extra_context)

Customization
-------------

The EmailBackend can be extended if the standard backend does not meet the requirements. For example, to add a users current membership status or some other such custom object to the context for all notifications:

::

    from notifier.backends import EmailBackend
    class CustomEmailBackend(EmailBackend):
        def send(self, user, context=None):
            if not context:
                context = {}
            context.update({
                'membership': user.membership_set.latest()
            })
            return super(CustomEmailBackend, self).send(user, context)


Custom Backend
==============

A completely custom backend can be written to support any method of sending a notification. 

Custom backends should be extended from the ``BaseBackend`` class. The ``send`` method in a backend class deals with how the actual message is sent.

The template used by default will be ``notifier/<notification-name>_<backend-name>.txt``.


BaseBackend
-----------

.. autoclass:: notifier.backends.BaseBackend


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

    # self.template = 'notifier/<notification-name>_sms-twilio.txt'

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
