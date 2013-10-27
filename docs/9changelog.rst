==========
Change Log
==========

0.7
===

- BREAKING - NotificationManager.update_user_prefs() removed.
- Notification.update_group_prefs() on added to allow setting group preferences.
- shortcuts.update_prefrences() is a shotcut to set both user and group preferences.
- 'read' field for SentNotifications.

	If your notification method supports read reciepts, you can use this field to keep track of it. Not used anywhere right now, but we could add webhook support to mark messages as read.
