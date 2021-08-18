# syntax=docker/dockerfile:experimental
FROM python:3.6

RUN apt-get update -y && apt-get install -y \
    git \
    gcc \
    procps \
    vim \
    nginx \
    sendmail \
    supervisor
RUN mkdir ~/.ssh && echo "Host git*\n\tStrictHostKeyChecking no\n" >> ~/.ssh/config

ARG IFXURLS_COMMIT=bc85aaee65db8e63b37762804cb57f8b8f22cd4e
ARG NANITES_CLIENT_COMMIT=e4099cb6c9edadf2f722e8c26c413caf7e2c1c51
ARG IFXUSER_COMMIT=bcc84807bde34f8277a4d2def0503151ab89d174
ARG IFXAUTH_COMMIT=afcaad2b05f5dd90e86e53b2de864bef04c91898

WORKDIR /app
COPY requirements.txt .
RUN --mount=type=ssh pip install --upgrade pip && \
    pip install gunicorn && \
    pip install 'Django>2.2,<3' && \
    pip install git+ssh://git@github.com/harvardinformatics/ifxurls.git@${IFXURLS_COMMIT} && \
    pip install git+ssh://git@github.com/harvardinformatics/nanites.client.git@${NANITES_CLIENT_COMMIT} && \
    pip install git+ssh://git@github.com/harvardinformatics/ifxuser.git@${IFXUSER_COMMIT} && \
    pip install git+ssh://git@github.com/harvardinformatics/ifxauth.git@${IFXAUTH_COMMIT} && \
    pip install -r requirements.txt

RUN echo "daemon off;" >> /etc/nginx/nginx.conf
COPY etc/nginx.conf /etc/nginx/sites-available/default
COPY etc/supervisor.conf /etc/supervisor/conf.d/app.conf

COPY . /app

ENV DJANGO_SETTINGS_FILE=settings
ENV PYTHONPATH=/app

CMD ["/usr/bin/supervisord","-n"]
