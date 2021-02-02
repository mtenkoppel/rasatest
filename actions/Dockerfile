FROM rasa/rasa-sdk:2.2.0

USER root

WORKDIR /app

COPY requirements.txt /app

COPY actions.py /app

RUN pip3 install -r requirements.txt

CMD ["START","--actions","actions"]

USER 1001