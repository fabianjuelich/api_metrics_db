#!/bin/sh
echo "Hello From Container $(date)" >> /var/log/cron.log 2>&1
