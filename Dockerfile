#
# Dockerfile for the ifx.rc portal application
#
# Use a volume to deploy code to /app

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
    supervisor 


WORKDIR /app

ADD requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt && \
    pip install git+https://gitlab-int.rc.fas.harvard.edu/common/rcpy.git && \
    pip install gunicorn

RUN echo "daemon off;" >> /etc/nginx/nginx.conf 
COPY etc/nginx.conf /etc/nginx/sites-available/default
COPY etc/supervisor.conf /etc/supervisor/conf.d/app.conf
ENV DJANGO_SETTINGS_FILE=settings

ENV PYTHONPATH=/app

# Set Django setting DEBUG to False
ENV DJANGO_DEBUG=FALSE
ENV DJANGO_LOGLEVEL=INFO

CMD ["/usr/bin/supervisord","-n"]
