FROM resin/rpi-raspbian:latest
MAINTAINER robe16

# Update
RUN apk add --update python py-pip

# Install app dependencies
RUN pip install -r req.txt

# Bundle app source
COPY simpleapp.py /src/simpleapp.py

# Expose the application port and run application
EXPOSE 1610
CMD [“python”, ”/src/start.py”]