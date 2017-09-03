FROM resin/rpi-raspbian:latest
MAINTAINER robe16

# Port number to listen on
ARG portApplication
# IP address that the core server runs on
ARG serverIp
# Port number the core server listens on
ARG serverPort

# Update
RUN apt-get update && apt-get install -y python python-pip

WORKDIR /HomeControl/webserver

# Bundle app source
COPY src /HomeControl/webserver

# Copy app dependencies
COPY req.txt requirements.txt

# Install app dependencies
RUN pip install -r requirements.txt

# Expose the application port and run application
EXPOSE ${portApplication}
CMD python start.py ${portApplication} ${serverIp} ${serverPort}
