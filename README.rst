#wd42 & #pd42 website
=====================

Setting up for development
--------------------------

Get the code, then run ``docker-compose up``.
Once the containers are up and running for the first time,
you need to run the migrations:

.. code-block:: shell

    $ docker-compose exec backend ./manage.py migrate

Once the database is up to date, make yourself a superuser:

.. code-block:: shell

    $ docker-compose exec backend ./manage.py createsuperuser

Log in to the admin at http://localhost/admin/ and create a new home page.
Update the sites entry at http://localhost/admin/sites/1/ to point to the new home page.

You're now good to go!
