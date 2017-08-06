FROM resin/rpi-raspbian:latest
MAINTAINER robe16

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
EXPOSE 1610
CMD python ”start.py”
