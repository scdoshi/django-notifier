.. django-notifier documentation master file, created by
   sphinx-quickstart on Sun May 26 15:04:16 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


django-notifier
===============

*django-notifier* is a django app to send notifications and manage preferences and permissions per user and group.

It can support multiple methods of sending notifications and provides methods to manage user preferences as well as group settings for notifications. `email` notifications are supported out of the box using django's email settings, additional methods of sending notification (Backends) can be added as required to support `SMS`, `phone` or even `snail mail`.

The general idea is to reduce the overhead of setting up notifications for different actions (payment processed, new membership, daily update) and making it easy to use the same backend for all kinds of notifications.


Contents
========

.. toctree::
   :maxdepth: 2

   1setup
   2use
   3backends
   4methods
   5forms


Contribute / Report Errors
==========================

To contribute to the code or docs, please visit the github repository at
	
	https://github.com/scdoshi/django-notifier

To report errors, please create a new issue at

	https://github.com/scdoshi/django-notifier/issues


To Do
=====

* Add notification support for non-user addresses (emails, phones etc.)
* Functions to output all email addresses for particular notification
* Ways to send a notification to everyone in a notification list


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
