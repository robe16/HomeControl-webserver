FROM resin/rpi-raspbian:latest
MAINTAINER robe16

# Port number to listen on - default 8080
ARG portApplication=8080
# Port number the core server listens on - default 1600
ARG portServer=1600

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
CMD python start.py ${portApplication} ${portServer}
