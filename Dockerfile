FROM python:3.8.2-slim

MAINTAINER grodriguezra@gmail.com
ENV TZ=Europe/Madrid

# install system dependencies
RUN apt-get update \
    && apt-get install -y cron \
    && apt-get autoremove -y


COPY . /app
WORKDIR /app

# change privileges
RUN chmod 777 /app/app.py

# install python dependencies
run pip install -r requirements.txt

# Configure CRON
# Add crontab file in the cron directory
ADD crontab /etc/cron.d/cg-cron

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/cg-cron

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# Run the command on container startup
CMD cron && tail -f /var/log/cron.log


