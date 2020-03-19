FROM python:3.8.2-alpine

COPY requirements.txt requirements.txt
RUN python -m pip install -r requirements.txt

ENV FLASK_APP runner.py
COPY shop/config.py shop/runner.py ./

COPY shop/run.sh ./
RUN chmod +x run.sh runner.py

COPY shop/migrations migrations
COPY swagger.yaml ./
COPY utils utils
COPY constants constants
COPY shop shop
ENTRYPOINT ["./run.sh"]
