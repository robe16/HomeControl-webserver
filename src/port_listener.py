import os

from bottle import error, HTTPError
from bottle import get, post
from bottle import request, run, static_file, HTTPResponse, redirect, response

import requests as requests

import cfg
from cfg import server_url
from src.cache.setup import get_cfg_room_name, get_cfg_device_name, get_cfg_account_name
from src.cache.setup import get_cfg_device_type, get_cfg_account_type
from src.cache.users import check_user
from src.web.web_create_error import create_error
from web.web_create_pages import create_login, create_home, create_about, create_tvguide, create_weather, create_device

from src.bundles.devices.tv_lg_netcast.html_tv_lg_netcast import html_tv_lg_netcast
from src.bundles.devices.tivo.html_tivo import html_tivo
from src.bundles.accounts.nest.html_nest import html_nest


################################################################################################

_cache = False

################################################################################################

def start_bottle(cache):
    #
    global _cache
    _cache = cache
    #
    run_bottle()

################################################################################################
# Web UI
################################################################################################

@get('/')
def web_redirect():
    redirect('/web/')


@get('/web/login')
def web_login():
    global _cache
    user = request.query.user
    if not user:
        return HTTPResponse(body=create_login(_cache), status=200)
    else:
        response.set_cookie('user', user, path='/', secret=None)
        return redirect('/web/')


@get('/web/logout')
def web_logout():
    response.delete_cookie('user')
    return redirect('/web/login')


@get('/web/')
@get('/web/home/')
def web_home():
    global _cache
    # Get and check user
    user = _check_user(request.get_cookie('user'))
    if not user:
        redirect('/web/login')
    #
    return HTTPResponse(body=create_home(user, _cache), status=200)


@get('/web/about/')
def web_about():
    # Get and check user
    user = _check_user(request.get_cookie('user'))
    if not user:
        redirect('/web/login')
    #
    return HTTPResponse(body=create_about(user, _cache), status=200)


@get('/web/info/<service>')
def web_info(service=False):
    global _cache
    # Get and check user
    user = _check_user(request.get_cookie('user'))
    if not user:
        redirect('/web/login')
    #
    if service == 'tvguide':
        return HTTPResponse(body=create_tvguide(user, _cache), status=200)
    elif service == 'weather':
        return HTTPResponse(body=create_weather(user, _cache), status=200)
    else:
        raise HTTPError(404)


@get('/web/device/<room_id>/<device_id>')
def web_devices(room_id=False, device_id=False):
    global _cache
    #
    try:
        if (not room_id) or (not device_id):
            raise HTTPError(404)
        #
        # Get and check user
        user = _check_user(request.get_cookie('user'))
        if not user:
            redirect('/web/login')
        #
        device_type = get_cfg_device_type(_cache['setup'], room_id, device_id)
        #
        if device_type == 'tv_lg_netcast':
            html_body = html_tv_lg_netcast(room_id,
                                           device_id)
        elif device_type == 'tivo':
            html_body = html_tivo(user,
                                  _cache,
                                  room_id,
                                  device_id)
        else:
            return HTTPError(404)
        #
        body = create_device(user,
                             _cache,
                             html_body,
                             '{room}: {device}'.format(room=get_cfg_room_name(_cache['setup'], room_id),
                                                       device=get_cfg_device_name(_cache['setup'], room_id, device_id)),
                             '{room}: {device}'.format(room=get_cfg_room_name(_cache['setup'], room_id),
                                                       device=get_cfg_device_name(_cache['setup'], room_id, device_id)))
        #
        return HTTPResponse(body=body, status=200)
    except:
        raise HTTPError(500)


@get('/web/account/<account_id>')
def web_accounts(account_id=False):
    global _cache
    #
    try:
        if not account_id:
            raise HTTPError(404)
        #
        # Get and check user
        user = _check_user(request.get_cookie('user'))
        if not user:
            redirect('/web/login')
        #
        account_type = get_cfg_account_type(_cache['setup'], account_id)
        #
        if account_type == 'nest_account':
            html_body = html_nest(account_id)
        else:
            return HTTPError(404)
        #
        body = create_device(user,
                             _cache,
                             html_body,
                             get_cfg_account_name(_cache['setup'], account_id),
                             get_cfg_account_name(_cache['setup'], account_id))
        #
        return HTTPResponse(body=body, status=200)
    except:
        raise HTTPError(500)


@get('/web/static/<folder>/<filename>')
def get_resource(folder, filename):
    return static_file(filename, root=os.path.join(os.path.dirname(__file__),('web/html/static/{folder}'.format(folder=folder))))


################################################################################################
# Handle requests for resource data
################################################################################################

@get('/data/device/<room_id>/<device_id>/<resource_requested>')
def get_data_device(room_id=False, device_id=False, resource_requested=False):
    #
    if (not room_id) or (not device_id) or (not resource_requested):
        raise HTTPError(404)
    #
    try:
        r = requests.get(server_url('data/device/{room_id}/{device_id}/{resource_requested}'.format(room_id=room_id,
                                                                                                    device_id=device_id,
                                                                                                    resource_requested=resource_requested)))
        #
        if r.status_code == requests.codes.ok:
            if r.content:
                return HTTPResponse(body=r.content, status=200)
            else:
                return HTTPResponse(status=200)
        else:
            return HTTPResponse(status=400)
            #
    except:
        raise HTTPError(500)


@get('/data/account/<account_id>/<resource_requested>')
def get_data_account(account_id=False, resource_requested=False):
    #
    if (not account_id) or (not resource_requested):
        raise HTTPError(404)
    #
    try:
        r = requests.get(server_url('data/account/{account_id}/{resource_requested}'.format(account_id=account_id,
                                                                                            resource_requested=resource_requested)))
        #
        if r.status_code == requests.codes.ok:
            if r.content:
                return HTTPResponse(body=r.content, status=200)
            else:
                return HTTPResponse(status=200)
        else:
            return HTTPResponse(status=400)
            #
    except:
        raise HTTPError(500)


################################################################################################
# Handle commands
################################################################################################


@get('/command/device/<room_id>/<device_id>')
@post('/command/device/<room_id>/<device_id>')
def send_command_device(room_id=False, device_id=False):
    #
    if (not room_id) or (not device_id):
        raise HTTPError(404)
    #
    cmd_dict = dict(request.query)
    #
    try:
        r = requests.post(server_url('command/device/{room_id}/{device_id}'.format(room_id=room_id, device_id=device_id)),
                          json=cmd_dict)
        #
        if r.status_code == requests.codes.ok:
            if r.content:
                return HTTPResponse(body=r.content, status=200)
            else:
                return HTTPResponse(status=200)
        else:
            return HTTPResponse(status=400)
            #
    except:
        raise HTTPError(500)


@get('/command/account/<account_id>')
def send_command_account(account_id=False):
    #
    if not account_id:
        raise HTTPError(404)
    #
    cmd_dict = dict(request.query)
    #
    try:
        r = requests.post(server_url('command/account/{account_id}'.format(account_id=account_id)),
                          json=cmd_dict)
        #
        if r.status_code == requests.codes.ok:
            return HTTPResponse(status=200)
        else:
            return HTTPResponse(status=400)
        #
    except:
        raise HTTPError(500)


################################################################################################
# Update user preferences
################################################################################################

# @post('/preferences/<category>')
# def save_preferences(category='-'):
#     if _check_user(request.get_cookie('user')):
#         if category == 'tvguide':
#             user = request.get_cookie('user')
#             data = request.body
#             if update_user_channels(user, data):
#                 return HTTPResponse(status=200)
#     else:
#         raise HTTPError(404)


################################################################################################
# Image files
################################################################################################

@get('/favicon.ico')
def get_favicon():
    try:
        r = requests.get(server_url('favicon.ico'))
        #
        if r.status_code == requests.codes.ok:
            return HTTPResponse(status=200, body=r.content)
        else:
            return HTTPResponse(status=400)
        #
    except:
        raise HTTPError(500)


@get('/img/<category>/<filename>')
def get_image(category, filename):
    try:
        r = requests.get(server_url('img/{category}/{filename}'.format(category=category,
                                                                       filename=filename)))
        #
        if r.status_code == requests.codes.ok:
            response = HTTPResponse(status=200, body=r.content)
            response.set_header("Cache-Control", "public, max-age=604800")
            return response
        else:
            return HTTPResponse(status=400)
        #
    except:
        raise HTTPError(500)


################################################################################################
# Error pages/responses
################################################################################################

@error(404)
def error404(error):
    return HTTPResponse(body=create_error(404), status=404)


@error(500)
def error500(error):
    return HTTPResponse(body=create_error(500), status=500)


################################################################################################


def _check_user(user_cookie):
    global _cache
    if not user_cookie:
        return False
    else:
        if check_user(_cache['users'], user_cookie):
            return user_cookie
        else:
            return 'Guest'

def run_bottle():
    # '0.0.0.0' - all interfaces including the external one
    # 'localhost' - internal interfaces only
    run(host='0.0.0.0', port=cfg.self_port, debug=True)
