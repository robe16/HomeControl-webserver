from cfg import server_url, self_ip, self_port_cache
from log.console_messages import print_msg, print_error
from cache_port_listener import start_port_listener
import requests
import time


def create_cache(cache):
    while True:
        cache['setup'] = request_setup()
        cache['users'] = request_users()
        cache['tvchannels'] = request_tvchannels()
        #
        subscription = False
        while not subscription:
            subscription = send_cache_subscription()
            if not subscription:
                time.sleep(60)
        #
        start_cache_port_listener(cache)
        #
        #time.sleep(3600)


def send_cache_subscription():
    details = {'categories': ['setup', 'users', 'tvchannels'],
               'ipaddress': self_ip,
               'port': self_port_cache}
    url = server_url('cache/subscribe')
    r = requests.post(url, json=details)
    #
    if r.status_code == requests.codes.ok:
        print_msg('Subscription for cache updates successful - {status_code}'.format(status_code=r.status_code))
        return True
    else:
        print_error('Subscription for cache updates failed - {status_code}'.format(status_code=r.status_code))
        return False


def start_cache_port_listener(cache):
    start_port_listener(cache)


def request_setup():
    url = server_url('cache/setup')
    r = requests.get(url)
    #
    if r.status_code == requests.codes.ok:
        print_msg('Cache SETUP retrieved successfully - {status_code}'.format(status_code=r.status_code))
        return r.json()
    else:
        print_error('Cache SETUP failed to be retrieved - {status_code}'.format(status_code=r.status_code))
        return False


def request_users():
    url = server_url('cache/users')
    r = requests.get(url)
    #
    if r.status_code == requests.codes.ok:
        print_msg('Cache USERS retrieved successfully - {status_code}'.format(status_code=r.status_code))
        return r.json()
    else:
        print_error('Cache USERS failed to be retrieved - {status_code}'.format(status_code=r.status_code))
        return False


def request_tvchannels():
    url = server_url('cache/tvchannels')
    r = requests.get(url)
    #
    if r.status_code == requests.codes.ok:
        print_msg('Cache TVCHANNELS retrieved successfully - {status_code}'.format(status_code=r.status_code))
        return r.json()
    else:
        print_error('Cache TVCHANNELS failed to be retrieved - {status_code}'.format(status_code=r.status_code))
        return False


# def request_tvlistings():
#     url = server_url('cache/tvlistings')
#     r = requests.get(url)
#     #
#     if r.status_code == requests.codes.ok:
#         print_msg('TCache VLISTINGS retrieved successfully - {status_code}'.format(status_code=r.status_code))
#         return r.json()
#     else:
#         print_error('Cache TVLISTINGS failed to be retrieved - {status_code}'.format(status_code=r.status_code))
#         return False
