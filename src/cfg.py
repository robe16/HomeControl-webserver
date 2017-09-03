import socket
from uuid import getnode as get_mac

def my_ip():
    return socket.gethostbyname(socket.gethostname())

def my_mac():
    return ':'.join(("%012X" % get_mac())[i:i + 2] for i in range(0, 12, 2))
