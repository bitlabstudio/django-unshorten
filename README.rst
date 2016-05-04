Django Unshorten
================

A Django application for un-shortening URLs that have been shortened by
URL shorteners like bit.ly.


Installation
------------

You need to install the following prerequisites in order to use this app::

    pip install Django

If you want to install the latest stable release from PyPi::

    $ pip install django-unshorten

If you feel adventurous and want to install the latest commit from GitHub::

    $ pip install -e git://github.com/bitmazk/django-unshorten.git#egg=unshorten

Add ``unshorten`` to your ``INSTALLED_APPS``::

    INSTALLED_APPS = (
        ...,
        'unshorten',
    )

Hook this app into your ``urls.py``::

    urlpatterns = [
        url(r'^unshorten/$', include('unshorten.urls')),
    ]

You need to set the class that does the rate limiting.
For Default set this to: ::

    UNSHORTEN_RATE_LIMIT_CLASS = 'unshorten.rate_limit.SimpleRateLimit'

This will simply limit the daily api calls to the following setting, you must
also provide::

    UNSHORTEN_DAILY_LIMIT = 5000


Also you need to provide the setting for ``UNSHORTEN_API_AUTH_CLASS``.
Default is: ::

    UNSHORTEN_API_AUTH_CLASS = 'unshorten.authentication.SimpleAuthentication'

This provides simple http authentification as well as login authentication.

On your server, if you are using ``mod_wsgi`` you need to add this to your
``httpd.conf``: ::

    WSGIPassAuthorization On


Usage
-----

After installation a user should be able to call the api using basic http
authentication and a query. A requested URL could look like this: ::

    https://example.com/unshorten/api/v1/unshorten/?url=http%3A%2F%2Fbitmazk.com

And here's an example of a request with basic http authentication using curl:::

    curl --user user@example.com:password123 "https://example.com/unshorten/api/v1/unshorten/?url=bit.ly%2FUn9Gns"


Contribute
----------

If you want to contribute to this project, please perform the following steps

.. code-block:: bash

    # Fork this repository
    # Clone your fork
    mkvirtualenv django-unshorten
    make develop

    git co -b feature_branch master
    # Implement your feature and tests
    git add . && git commit
    git push -u origin feature_branch
    # Send us a pull request for your feature branch

In order to run the tests, simply execute ``tox``. This will install two new
environments (for Django 1.8 and Django 1.9) and run the tests against both
environments.
