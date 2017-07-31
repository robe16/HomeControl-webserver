FROM resin/rpi-raspbian:latest
MAINTAINER robe16

# Update
RUN apk add --update -y python
RUN apk add --update -y py-pip

# Install app dependencies
RUN pip install -r -y req.txt

# Bundle app source
COPY src /usr/local/src

# Expose the application port and run application
EXPOSE 1610
CMD [“python”, ”/usr/local/src/start.py”]