FROM python:3.8.2-alpine

COPY requirements.txt requirements.txt
RUN python -m pip install -r requirements.txt

COPY utils utils
COPY constants constants
COPY notifications notifications
COPY notifications/notifications.py ./
RUN chmod +x notifications.py

ENTRYPOINT ["./notifications.py"]
