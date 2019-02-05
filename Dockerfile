#
# Dockerfile for the ifx.rc portal application
#
# COPYs code to /apps
# db.sqlite3 must come from the host (e.g. -v /var/www/html/db.sqlite3:/app/db.sqlite3)
# If migrations must be applied, pull the latest container and run manage.py migrate as the entrypoint
#

FROM python:3.6

RUN apt-get update -y && apt-get install -y \
    git \
    gcc \
    procps \
    vim \
    nginx \
    sendmail \
    supervisor


WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install gunicorn && \
    pip install git+https://github.com/harvardinformatics/ifxurls.git && \
    pip install git+https://github.com/harvardinformatics/ifxauth.git && \
    pip install git+https://github.com/harvardinformatics/ifxuser.git && \
    pip install -r requirements.txt

RUN echo "daemon off;" >> /etc/nginx/nginx.conf
COPY etc/nginx.conf /etc/nginx/sites-available/default
COPY etc/supervisor.conf /etc/supervisor/conf.d/app.conf

COPY . /app

ENV DJANGO_SETTINGS_FILE=settings
ENV PYTHONPATH=/app

CMD ["/usr/bin/supervisord","-n"]
