FROM python:3.10-bullseye

WORKDIR /app

COPY ./python/kafka_updater_service/requirements.txt /app/requirements.txt

COPY ./price_data.csv /app/
RUN apt-get update \
    && apt-get install gcc -y \
    && apt-get clean

RUN pip install -r /app/requirements.txt \
    && rm -rf /root/.cache/pip

COPY ./python/kafka_updater_service/ /app/
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]