FROM openmatchmaking/docker-base-python-image:3.7
RUN apt-get update && apt-get -y install make

COPY ./ /app
WORKDIR /app
