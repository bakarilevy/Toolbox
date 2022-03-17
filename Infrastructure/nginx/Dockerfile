#file: ~/nginx/Dockerfile
# Base image with scripts for Nginx and Let's Encrypt
FROM staticfloat/nginx-certbot

# Copy a template Nginx configuration
COPY *.conf /etc/nginx/conf.d/

# Copy HTML webpages
COPY --chown=www-data:www-data html/* /var/www/html/

# Script to replace __DOMAIN__ with ENV domain value, also for IP
COPY init.sh /scripts/

ENV DOMAIN="www.somedomain.com"
ENV C2IP="192.168.1.29"
ENV CERTBOT_EMAIL="some.email@gmail.com"

CMD ["/bin/bash", "/scripts/init.sh"]