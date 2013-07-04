==========
Quickstart
==========

A quick primer on how to start sending notifications.

Create Notification
===================

1. Use the ``create_notification`` shortcut method to create a new type of notification.

    Convention is to declare all notifications for an app in ``notifications.py`` in the app directory.

    ::

        from notifier.shortcuts import create_notification
        create_notification('card-declined')

    This will create a notification called 'card-declined'.

2. Create templates for notifications you want to be sent.

    For the ``email`` backend, the required templates for the 'card-declined' notification will be:

    * ``notifier/card-declined_email_message.txt``
    * ``notifier/card-declined_email_subject.txt``

    These can be placed in the app's templates directory.

    The ``Site`` and ``User`` models are available as context for the templates. Different backends may use a different number and format of templates, but the convention is:

    ::

        <notification-name>_<backend>_<optional_descriptor>.txt
        card-declined_email_subject.txt


Send Notification
=================

::

    from notifier.shortcuts import send_notification
    send_notification('card-declined', [user1, user2])

