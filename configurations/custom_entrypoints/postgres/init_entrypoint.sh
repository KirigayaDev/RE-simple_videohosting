#!/bin/bash
chown -R postgres:postgres /var/lib/postgresql/
chmod 600 /var/lib/postgresql/ssl/*.key
chmod 644 /var/lib/postgresql/ssl/*.crt

exec docker-entrypoint.sh postgres -c config_file=/etc/postgresql/postgresql.conf
