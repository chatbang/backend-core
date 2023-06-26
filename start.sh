#!/usr/bin/env bash
PID=`sudo ps -ef |grep '0.0.0.0:10020'|grep -v grep |awk '{print $2}'`
if [ -n '$PID' ];then
    sudo kill -9 $PID
fi
sudo /usr/bin/nohup /mnt/python3.8/bin/gunicorn -w 2 -b 0.0.0.0:10020 app:app &
