#!/usr/bin/env python
from setuptools import setup, find_packages

VERSION = __import__('notifier').get_version()

setup(
    name="django-notifier",
    version=VERSION,
    author='Siddharth Doshi',
    author_email='scdoshi@gmail.com',
    description=("User and Group Notifications for Django"),
    long_description=open('README.rst').read(),
    packages=find_packages(),
    url="http://github.com/scdoshi/django-notifier/",
    license='Simplified BSD',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    install_requires=[
        "Django >= 1.3.0",
        "django-bits",
    ],
)
