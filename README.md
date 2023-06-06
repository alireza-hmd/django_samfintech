
# Python Django Test
A sample microservice project with Django, Redis and Kafka to test your familiarities with these tools.

## Project Set Up
first you need to create a docker network for containers to communicate with the following command:
```
docker network create --driver=bridge sam_net
```
then you should run redis server and kafka with docker compose in seprate terminal windows:
```
cd redis
docker-compose up --build
```
```
cd kafka
docker-compose up --build
```

## Task 1
price updater service files are in `python/price_updater_service` directory but because of `price_data.csv` file that is in the main directory you should run this service from main directory with this commands:
```
docker build -t python_updater -f python/price_update_service/Dockerfile .
docker run -it --rm --network=redis_default --name updater python_updater 
```

## Task 2
performance calculation service files are in `python/performance_calculation_service`.   
run the service with this commands:
```
cd python/performance_calculation_service
docker build -t python_performance . 
docker run -it --rm --network=sam_net --name performance python_performance
```

## Task 3
price updater using kafka service files are in `python/kafka_updater_service` directory but beacause of `price_data.csv` file you should run this service from main directory with this commands:
```
docker build -t kafka_updater -f python/kafka_updater_service/Dockerfile .
docker run -it --rm --network=sam_net --name kafka_updater kafka_updater 
```

## Task 4
api service files are in `python/api_service` directory and you can run this service with this commands:
```
cd python/api_service
docker-compose up --build
```
service will be running on port `8000` 

## Task 5
request inception service files are in `python/request_inception` directory and you can run this service with this commands:
```
cd python/request_inception_service
docker-compose up --build
```
service will be running on port `8001` 