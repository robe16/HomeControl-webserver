FROM resin/rpi-raspbian:latest
MAINTAINER robe16

# Update
RUN apt-get update && apt-get install -y python python-pip

RUN ls

# Install app dependencies
RUN pip install -r -req.txt

# Bundle app source
COPY src /usr/local/src

# Expose the application port and run application
EXPOSE 1610
CMD [“python”, ”/usr/local/src/start.py”]