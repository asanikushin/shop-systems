FROM python:3.8.2-alpine

COPY requirements.txt requirements.txt
RUN python -m pip install -r requirements.txt

COPY notifications notifications
RUN chmod +x notifications/notifications.py

ENTRYPOINT ["notifications/notifications.py"]
