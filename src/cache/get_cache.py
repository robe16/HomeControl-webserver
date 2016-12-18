from src.cfg import server_url
from src.log.console_messages import print_msg, print_error
import requests


def create_cache(cache):
    cache['setup'] = request_setup()
    cache['users'] = request_users()
    cache['tvchannels'] = request_tvchannels()
    # cache['tvlistings'] = request_tvlistings()


def request_setup():
    url = server_url('cache/setup')
    r = requests.get(url)
    #
    if r.status_code == requests.codes.ok:
        print_msg('SETUP CACHE retrieved successfully - {status_code}'.format(status_code=r.status_code))
        return r.json()
    else:
        print_error('SETUP CACHE failed to be retrieved - {status_code}'.format(status_code=r.status_code))
        return False


def request_users():
    url = server_url('cache/users')
    r = requests.get(url)
    #
    if r.status_code == requests.codes.ok:
        print_msg('USERS CACHE retrieved successfully - {status_code}'.format(status_code=r.status_code))
        return r.json()
    else:
        print_error('USERS CACHE failed to be retrieved - {status_code}'.format(status_code=r.status_code))
        return False


def request_tvchannels():
    url = server_url('cache/tvchannels')
    r = requests.get(url)
    #
    if r.status_code == requests.codes.ok:
        print_msg('TVCHANNELS CACHE retrieved successfully - {status_code}'.format(status_code=r.status_code))
        return r.json()
    else:
        print_error('TVCHANNELS CACHE failed to be retrieved - {status_code}'.format(status_code=r.status_code))
        return False


# def request_tvlistings():
#     url = server_url('cache/tvlistings')
#     r = requests.get(url)
#     #
#     if r.status_code == requests.codes.ok:
#         print_msg('TVLISTINGS CACHE retrieved successfully - {status_code}'.format(status_code=r.status_code))
#         return r.json()
#     else:
#         print_error('TVLISTINGS CACHE failed to be retrieved - {status_code}'.format(status_code=r.status_code))
#         return False
