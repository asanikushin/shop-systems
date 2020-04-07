#!/bin/sh
while true; do
    echo Migrating database
    flask db upgrade
    if [[ "$?" == "0" ]]; then
        break
    fi
    echo Deploy command failed, retrying in 5 secs...
    sleep 5
done

exec gunicorn -b :8080 -w 4 runner:app