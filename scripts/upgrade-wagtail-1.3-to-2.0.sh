#!/bin/bash
# Upgrade the WD42 database from the old export running Wagtail 1.3 to running
# Wagtail 2.1, performing all Wagtail and Django migrations along the way

set -e
ARGS=( $@ )

PROG="${0}"
HERE=$( cd -P -- "$( dirname -- "${PROG}" )" && pwd -P )
REPO=$( basename -- "$HERE" )
PROG="${HERE}/$( basename -- "${PROG}" )"

function main() {
	local in_file=${0}

	cd -- "$REPO"
	init_db $in_file
	upgrade
	finalise
}

function init_db() {
	local in_file=${1}

	echo "Recreating database..."
	docker-compose start database
	sleep 1
	docker-compose exec -T database dropdb -U postgres postgres
	docker-compose exec -T database createdb -U postgres postgres
	docker-compose exec -T database psql -U postgres postgres < wd42.sql
}

function upgrade() {
	echo "Upgrading all the things..."
	mkdir -p './pip'

	get_upgrade_script \
	| docker-compose run \
		-T --rm \
		-v './pip:/root/.cache' \
		backend \
		/bin/ash
}

function finalise() {
	docker-compose rm -f backend
}

function get_upgrade_script() {
	awk 'x==1 {print} /^START_UPGRADE_SCRIPT$/ {x=1}' < "${PROG}"
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]] ; then
	main "${ARGS[@]}"
	exit $?
else
	return
fi

START_UPGRADE_SCRIPT
#!/bin/ash
export SETTINGS_FILE="upgrade_settings.py"

function install() {
	local version="$1"
	echo "Installing Wagtail ~= ${version}"
	pip3 install "wagtail~=${version}"
	env DJANGO_SETTINGS_MODULE='upgrade_settings' \
		./manage.py migrate --no-input
}

cat > urls.py <<'URLS'
urlpatterns = []
URLS

cat > "${SETTINGS_FILE}" <<'SETTINGS'
INSTALLED_APPS = [
    'wagtail.wagtailadmin',
    'wagtail.wagtailcore',
    'wagtail.wagtaildocs',
    'wagtail.wagtailembeds',
    'wagtail.wagtailimages',
    'wagtail.wagtailsites',
    'wagtail.wagtailsnippets',
    'wagtail.wagtailusers',
    'wagtail.contrib.settings',
    'modelcluster',
    'taggit',
    'django.forms',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
]

from dj_database_url import parse
DATABASES = {'default': parse('postgres://postgres@database/postgres')}

SECRET_KEY = 'naspw'
ROOT_URLCONF = 'urls'
SETTINGS

for version in 1.4.0 1.5.0 1.6.0 1.7.0 1.8.0 1.9.0 1.10.0 1.11.0 1.12.0 1.13.0 ; do
	install "${version}"
done

cat > "${SETTINGS_FILE}" <<'SETTINGS'
INSTALLED_APPS = [
    'wagtail.admin',
    'wagtail.core',
    'wagtail.documents',
    'wagtail.embeds',
    'wagtail.images',
    'wagtail.sites',
    'wagtail.snippets',
    'wagtail.users',
    'wagtail.contrib.settings',
    'modelcluster',
    'taggit',
    'django.forms',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
]

from dj_database_url import parse
DATABASES = {'default': parse('postgres://postgres@database/postgres')}

SECRET_KEY = 'naspw'
ROOT_URLCONF = 'urls'
SETTINGS

for version in 2.0.0 ; do
	install "${version}"
done

pip install -r requirements.txt
./manage.py migrate
./manage.py shell <<'PYTHON'
from django.contrib.auth.models import User
User.objects.create_superuser('admin', 'admin@example.com', 'p')
PYTHON
