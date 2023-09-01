FROM debian:bookworm

RUN ln -sf /usr/share/zoneinfo/Europe/Berlin /etc/localtime
RUN apt update && apt install cron python3 python3-elasticsearch -y
# RUN pip install elasticsearch --break-system-packages

ADD ./crontab /etc/cron.d/crontab
ADD ./cronjob.py /home/cronjob.py

RUN chmod +x /etc/cron.d/crontab
RUN chmod +x /home/cronjob.py

RUN touch /var/log/cron.log
CMD cron && tail -f /var/log/cron.log
