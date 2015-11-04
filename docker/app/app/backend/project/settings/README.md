<a href="http://www.djangoproject.com/" ><img src="https://www.djangoproject.com/m/img/badges/djangoproject120x25.gif" border="0" alt="A Django project." title="A Django project." style="float: right;" /></a>

## 'settings' Directory 

### Introduction
This is the settings directory containing Django project configuration.

### How to Use

`from django.conf import settings`

It can be useful to have a link to the Django Global Settings (it's location could vary depending on or version of Django)

e.g. 
`ln -s /usr/local/lib/python2.7/site-packages/Django-1.7.1-py2.7.egg/django/conf/global_settings.py global.py`

### Files
The settings files are split for better separate of roles:

* README.md - this file
* base.py   - this is your core settings
* dev.py    - this is your local development settings
* test.py   - this is your settings for unit tests

*(__global.py__ - worth a link to the global Django settings for reference. See comments above.)*

### Main Settings file - base.py
This is your core settings file.

### Local Settings file - dev.py
Your development settings file may have to differ for various reasons.

This is the settings file that you use when you're working on the project locally. 
Change this file when testing new settings / third party apps.

Local development-specific settings could include DEBUG mode, log level, and activation of developer tools like django-debug-toolbar may be used. 
Developers sometimes name this file local.py

### Test Settings file - test.py
Settings for running tests including test runners, in-memory database definitions, and log settings.

### Considerations / Future
In the future or for production/deployment purposes consider the use of extra files:

*(We will leave this to you when the time comes...)*

* staging.py    - specific settings for a staging environment
* production.py - specific settings for the production environment

