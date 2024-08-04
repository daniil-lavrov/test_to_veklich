#!/bin/bash

mkdir -p /etc/ssl/mycerts

openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/ssl/mycerts/selfsigned.key \
  -out /etc/ssl/mycerts/selfsigned.crt \
  -subj "/C=US/ST=State/L=City/O=Organization/OU=Unit/CN=$HOSTNAME"
