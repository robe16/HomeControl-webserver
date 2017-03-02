import socket
from uuid import getnode as get_mac

def my_ip():
    return socket.gethostbyname(socket.gethostname())

def my_mac():
    return ':'.join(("%012X" % get_mac())[i:i + 2] for i in range(0, 12, 2))

server_ip = 'http://0.0.0.0'
self_ip = 'http://0.0.0.0'
server_port = 1600
self_port = 1610
self_port_cache = 1611

def server_url(uri):
    return '{ip}:{port}/{uri}'.format(ip=server_ip,
                                      port=server_port,
                                      uri=uri)
