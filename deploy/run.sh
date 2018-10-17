#!/bin/ash -e

cd /opt/backend

# Run upgrade in the background
./deploy/upgrade.sh &

# Start uwsgi
exec /usr/sbin/uwsgi \
	--master \
	--processes 2 \
	--plugins  python3 \
	--die-on-term \
	--uwsgi-socket 0.0.0.0:80 \
	--chdir /opt/my-web-app \
	--module mywebapp.wsgi:application
