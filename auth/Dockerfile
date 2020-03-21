FROM python:3.8.2-alpine

COPY requirements.txt requirements.txt
RUN python -m pip install -r requirements.txt

ENV FLASK_APP runner.py
COPY auth/config.py auth/runner.py ./

COPY auth/run.sh ./
RUN chmod +x run.sh runner.py

COPY auth/migrations migrations
COPY swagger.yaml ./
COPY utils utils
COPY constants constants
COPY auth auth
ENTRYPOINT ["./run.sh"]
