#!/usr/bin/env bash

sudo mv /etc/supervisor/conf.d/ceph.conf supervisor.conf

sudo rm /etc/nginx/sites-enabled/ceph.conf
sudo update-rc.d nginx disable

