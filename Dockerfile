FROM python:3.9 as base

ENV PYTHONUNBUFFERED 1 \
    PYTHONFAULTHANDLER=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

WORKDIR /src

###
# Builder image. Install poetry, create and populate venv
###
FROM base as builder

RUN pip install "poetry==1.1.4"

COPY pyproject.toml poetry.lock /src/

RUN python -m venv /venv

RUN . /venv/bin/activate && poetry install --no-root

ENV DEBUG 1
ENV SECRET_KEY Build
ENV ALLOWED_HOSTS *

###
# Final image that will contain only venv and app
###
FROM base as final

COPY --from=builder /venv /venv
COPY . .
COPY docker-entrypoint.sh manage.py ./

RUN chmod +x docker-entrypoint.sh

EXPOSE 8001

CMD ["./docker-entrypoint.sh"]