#!/bin/sh
flask db upgrade
exec python runner.py runserver -h 0.0.0.0 -p 8080
