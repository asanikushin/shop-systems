FROM python:3.8.2-alpine

COPY requirements.txt requirements.txt
RUN python -m pip install -r requirements.txt

COPY app app
COPY migrations migrations
ENV FLASK_APP runner.py
COPY config.py runner.py ./

COPY run.sh ./
RUN chmod +x run.sh runner.py

ENTRYPOINT ["./run.sh"]
