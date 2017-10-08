from log.log import log_general, log_error
import requests
import time


def create_cache(cache, server_url):
    while True:
        cache['setup'] = request_setup(server_url)
        cache['users'] = request_users(server_url)
        cache['tvchannels'] = request_tvchannels(server_url)
        #
        if not cache['setup'] or not cache['setup'] or not cache['setup']:
            time.sleep(60)  # 1 minute
        else:
            time.sleep(3600)  # 1 hour


def request_setup(server_url):
    url = '{url}/{uri}'.format(url=server_url, uri='cache/setup')
    r = requests.get(url)
    #
    if r.status_code == requests.codes.ok:
        log_general('Cache SETUP retrieved successfully - {status_code}'.format(status_code=r.status_code))
        return r.json()
    else:
        log_error('Cache SETUP failed to be retrieved - {status_code}'.format(status_code=r.status_code))
        return False


def request_users(server_url):
    url = '{url}/{uri}'.format(url=server_url, uri='cache/users')
    r = requests.get(url)
    #
    if r.status_code == requests.codes.ok:
        log_general('Cache USERS retrieved successfully - {status_code}'.format(status_code=r.status_code))
        return r.json()
    else:
        log_error('Cache USERS failed to be retrieved - {status_code}'.format(status_code=r.status_code))
        return False


def request_tvchannels(server_url):
    url = '{url}/{uri}'.format(url=server_url, uri='cache/tvchannels')
    r = requests.get(url)
    #
    if r.status_code == requests.codes.ok:
        log_general('Cache TVCHANNELS retrieved successfully - {status_code}'.format(status_code=r.status_code))
        return r.json()
    else:
        log_error('Cache TVCHANNELS failed to be retrieved - {status_code}'.format(status_code=r.status_code))
        return False