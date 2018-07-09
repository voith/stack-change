#!/bin/bash

set -ex
export LC_ALL=C
export APP_NAME="stackXchange"

function wait_for_process(){
    while sudo fuser /var/lib/dpkg/lock >/dev/null 2>&1 || sudo fuser /var/lib/apt/lists/lock >/dev/null 2>&1; do
        echo "Waiting for a process to finish"
        sleep 10
    done
}

wait_for_process
wait_for_process && sudo apt-get -y update

cd /root/$APP_NAME

git pull origin master

sudo apt-get update
sudo apt-get install -y mysql-server
mysql_secure_installation

touch .env
sudo add-apt-repository ppa:jonathonf/python-3.6
sudo apt-get update
sudo apt-get install -y python3.6
update-alternatives --install /usr/bin/python python /usr/bin/python3.6 100
sudo apt-get install -y build-essential libssl-dev libffi-dev python3.6-dev
sudo apt-get install -y libmysqlclient-dev
sudo apt install -y python3-pip

sudo python -m pip install -r requirements.txt

mysql -u $DB_USER --password=$DB_PASSWORD -e "create database $DB_NAME";

python manage.py migrate

sudo apt-get install software-properties-common
sudo add-apt-repository ppa:certbot/certbot
sudo apt-get update
sudo apt-get install python-certbot-nginx
sudo certbot --nginx

sudo apt install -y gunicorn
sudo apt-get -y install supervisor

mkdir -p /root/logs
sudo rm -f /etc/supervisor/supervisord.conf
sudo cp -R /root/stackXchange/scripts/config/*  /etc/supervisor/conf.d/
