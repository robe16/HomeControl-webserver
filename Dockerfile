FROM resin/rpi-raspbian:latest
MAINTAINER robe16

# Update
RUN apt-get update && apt-get install -y python python-pip

# Bundle app source
WORKDIR /HomeControl
COPY src /webserver

# Install app dependencies
WORKDIR /HomeControl/webserver
COPY req.txt requirements.txt
RUN pip install -r requirements.txt

CMD ls

# Expose the application port and run application
EXPOSE 1610
CMD [“python”, ”start.py”]