==========
Quickstart
==========

A quick primer on how to start sending notifications.

Create Notification
===================

1. Use the ``create_notification`` shortcut method to create a new type of notification.

    ::

        from notifier.shortcuts import create_notification
        create_notification('card-declined')

    This will create a notification called 'card-declined'.

2. Create templates for notifications you want to be sent.

    For the ``email`` backend, the templates required are:

    * notifier/card-declined_email_message.txt
    * notifier/card-declined_email_subject.txt

    The ``Site`` and ``User`` models are available as context for the templates. Different backends may use a different number of templates, but the convention is 

    ::

        <notification-name>_<backend>.txt


Send Notification
=================

::

    from notifier.shortcuts import send_notification
    send_notification('card-declined', [user1, user2])

