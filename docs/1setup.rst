Installation
============

Install via `pip`.

::

	$ pip install git+git://github.com/scdoshi/django-notifier.git


Coming to PyPI soon, after which it will be possible to install with

::

	$ pip install django-notifier


Setup
=====

1. Add 'notifier' to INSTALLED_APPS in your django settings file.

::

	INSTALLED_APPS = (
		...
		'notifier',
		...
	)

2. If you are going to use any custom backends to send notifications, add the setting NOTIFIER_BACKENDS to your settings file. By default (if the setting is not defined), only the inscluded EmailBackend is considered.

::

	NOTIFIER_BACKENDS = (
	    'notifier.backends.EmailBackend',
	    'path.to.custom.backend.CustomBackend',
	)


3. Run `syncdb` or `migrate` (if useing South) to create the necesarry tables in the database.

::

	$ python manage.py syndb

::

	$ python manage.py migrate


Terminology
===========

`Notification`:

`Backend`: