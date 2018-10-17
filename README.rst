#wd42 & #pd42 website
=====================

Setting up for development
--------------------------

Get the code, then run ``docker-compose up``.
Once the containers are up and running for the first time,
you need to run the migrations:

.. code-block:: shell

    $ docker-compose exec backend ./manage.py migrate
