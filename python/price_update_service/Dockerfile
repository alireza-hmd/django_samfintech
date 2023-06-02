FROM python:3.10-bullseye

WORKDIR /app

COPY ./python/price_update_service/requirements.txt /app/requirements.txt

COPY ./price_data.csv /app/
RUN apt-get update \
    && apt-get install gcc -y \
    && apt-get clean

RUN pip install -r /app/requirements.txt \
    && rm -rf /root/.cache/pip

COPY ./python/price_update_service/ /app/

CMD ["python", "updater.py"]