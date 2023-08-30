FROM debian:bookworm

RUN ln -sf /usr/share/zoneinfo/Europe/Berlin /etc/localtime
RUN apt update && apt install cron -y

ADD ./crontab /etc/cron.d/crontab
ADD ./cronjob.sh /home/cronjob.sh

RUN chmod +x /etc/cron.d/crontab
RUN chmod +x /home/cronjob.sh

RUN touch /var/log/cron.log
CMD cron && tail -f /var/log/cron.log
