# Frontend asset builder
FROM node:8-stretch as frontend

ENV NPM_CONFIG_LOGLEVEL=warn \
	YARN_MODULES_PATH=/app/node_modules

RUN mkdir -p /app/frontend/
WORKDIR /app/frontend/
COPY dev42/frontend/package.json dev42/frontend/yarn.lock /app/frontend/

# `yarn install` has a bug where the .bin folder does not respect
# --modules-folder. By installing normally, moving node_modules, and then
# adding .bin/ to $PATH manually, this issue is worked around.
# See https://github.com/yarnpkg/yarn/issues/3724
RUN yarn install \
	&& yarn cache clean \
	&& echo "--*.modules-folder ${YARN_MODULES_PATH}" > ~/.yarnrc \
	&& mv node_modules "${YARN_MODULES_PATH}" \
	&& true

COPY ./dev42/frontend/ /app/frontend/

ENV PATH="${PATH}:${YARN_MODULES_PATH}/.bin"
RUN yarn run build
CMD ["yarn", "run", "watch"]

# Backend application
FROM alpine as backend

RUN mkdir /app/
WORKDIR /app/

RUN apk add --no-cache \
		tini \
		python3 python3-dev py3-pillow \
		postgresql-dev gcc musl-dev \
		uwsgi uwsgi-python3 \
	&& true

RUN pip3 install --no-cache-dir --upgrade \
		pip setuptools wheel \
	&& true

COPY requirements.txt /app/
RUN pip3 install --no-cache-dir \
		-r requirements.txt \
	&& true

COPY ./dev42/ /app/dev42/
COPY ./deploy/ /app/deploy/
COPY ./manage.py /app/manage.py
COPY --from=frontend /app/static/ /app/dev42/static/
RUN ln -fs /app/deploy/settings.py /app/settings.py

ENV PYTHONUNBUFFERED=1 \
	PYTHONIOENCODING=UTF-8 \
	PYTHONDONTWRITEBYTECODE=1 \
	PYTHONPATH=/app/ \
	DJANGO_SETTINGS_MODULE=settings \
	LC_ALL=C.UTF-8 \
	LANG=C.UTF-8

EXPOSE 80
ENTRYPOINT ["/sbin/tini", "--"]
CMD ["/app/deploy/run.sh"]
