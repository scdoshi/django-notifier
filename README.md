django-notifier
===============

Django app to manage notification preferences and permissions per user or group.

To register a notification:
notifier.create_notification('test-notification')

To send notifications:
notifier.send('test-notification', [user1, user2, ..])
