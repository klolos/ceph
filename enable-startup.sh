#!/usr/bin/env bash

sudo mv supervisor.conf /etc/supervisor/conf.d/ceph.conf && \
     ln -s /etc/supervisor/conf.d/ceph.conf supervisor.conf

sudo ln -s /etc/nginx/sites-available/ceph.conf /etc/nginx/sites-enabled/
sudo update-rc.d -f nginx enable

