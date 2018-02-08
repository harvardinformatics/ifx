#
# Dockerfile for the ifx.rc portal application
#
# COPYs code to /apps
# db.sqlite3 must come from the host (e.g. -v /var/www/html/db.sqlite3:/app/db.sqlite3)
# If migrations must be applied, pull the latest container and run manage.py migrate as the entrypoint
#

FROM debian

EXPOSE 80
RUN apt-get update -y && apt-get install -y \
    git \
    gcc \
    procps \
    vim \
    mariadb-client-10.1 \
    libmariadbclient-dev-compat \
    python \
    python-dev \
    python-pip \
    python-ldap \
    python-mysqldb \
    nginx \
    sendmail \
    supervisor 


WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt && \
    pip install git+https://gitlab-int.rc.fas.harvard.edu/common/rcpy.git && \
    pip install gunicorn

RUN echo "daemon off;" >> /etc/nginx/nginx.conf 
COPY etc/nginx.conf /etc/nginx/sites-available/default
COPY etc/supervisor.conf /etc/supervisor/conf.d/app.conf

COPY . /app

ENV DJANGO_SETTINGS_FILE=settings
ENV PYTHONPATH=/app

CMD ["/usr/bin/supervisord","-n"]
