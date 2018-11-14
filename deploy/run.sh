#!/bin/ash -e

cd /opt/backend

# Run upgrade in the background
./deploy/upgrade.sh &

# Start uwsgi
exec /usr/sbin/uwsgi \
	--master \
	--plugins  python3 \
	--die-on-term \
	--chdir /opt/backend \
	--uwsgi-socket 0.0.0.0:80 \
	--module dev42.wsgi:application
