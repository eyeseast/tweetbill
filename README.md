Tweetbill
==========

Tweetbill is an attempt to create a Congressional alert system, something that tells you when it's time to call your congressman, write to your senator or make some noise on the internet.

It's built in Django and uses the New York Times Congress API and Sunlight Congress API.

Quickstart
-----------

If you want to run this code at home, grab a copy from Github:

    $ git clone git://github.com/tweetbill/tweetbill.git

I recommend doing this in a virtual environment. Otherwise, you'll have conflicting dependencies all over. No one likes that. Next, install requirements.

    $ cd tweetbill
    $ pip install -r requirements.txt

Sync your database. This defaults to SQLite for local development. Change it in production.

    $ cd tweetbill
    $ python manage.py syncdb # create a superuser if you like
    $ python manage.py load_congress # get all members in the database

Run the dev server:

    $ python manage.py runserver

