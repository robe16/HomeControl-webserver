import os
import requests as requests
from bottle import error, HTTPError
from bottle import get, post
from bottle import request, run, static_file, HTTPResponse, redirect, response
#
from bindings.tivo.html_tivo import html_tivo
from bindings.tv_lg_netcast.html_tv_lg_netcast import html_tv_lg_netcast
from bindings.nest.html_nest import html_nest
from bindings.news.html_news import news_body
from bindings.tvlistings.html_tvlisting import tvlisting_body
from bindings.weather.html_weather import weather_body
#
from cache.setup import get_cfg_group_seq, get_cfg_thing_seq, get_cfg_info_seq
from cache.setup import get_cfg_thing_type, get_cfg_info_type
from cache.setup import cfg_urldecode
#
from cache.users import check_user
from web.web_create_error import create_error
from web.web_create_pages import create_login, create_home, create_about, create_page_body
#
from log.log import log_general, log_error
from lists.resources.english import *


################################################################################################

_cache = False
_server_url = ""

################################################################################################
# Create log message
################################################################################################

def log_msg(request, resource):
    #
    ip = request['REMOTE_ADDR']
    msg = '{ip} - {resource}'.format(ip=ip, resource=resource)
    #
    return msg

################################################################################################


def start_bottle(cache, self_port, server_url):
    #
    global _cache
    _cache = cache
    #
    global _server_url
    _server_url = server_url
    #
    run_bottle(self_port)

################################################################################################
# Web UI
################################################################################################

@get(uri_null)
def web_redirect():
    log = log_msg(request, uri_web_login)
    log_general('{log} - client redirected to "{redirect}"'.format(log=log, redirect=uri_web))
    redirect(uri_web)


@get(uri_web_login)
def web_login():
    global _cache
    log = log_msg(request, uri_web_login)
    #
    user = request.query.user
    if not user:
        log_general(log)
        return HTTPResponse(body=create_login(_cache), status=200)
    else:
        response.set_cookie('user', user, path='/', secret=None)
        log_general('{log} - client redirected to "{redirect}"'.format(log=log, redirect=uri_web))
        return redirect(uri_web)


@get(uri_web_logout)
def web_logout():
    log = log_msg(request, uri_web_logout)
    #
    response.delete_cookie('user')
    #
    log_general(log)
    return redirect(uri_web_login)


@get(uri_web)
@get(uri_web_home)
def web_home():
    global _cache
    log = log_msg(request, uri_web_home)
    #
    # Get and check user
    user = _check_user(request.get_cookie('user'))
    if not user:
        log_general('{log} - client redirected to "{redirect}"'.format(log=log, redirect=uri_web_login))
        redirect(uri_web_login)
    #
    log_general(log)
    return HTTPResponse(body=create_home(user, _cache), status=200)


@get(uri_web_about)
def web_about():
    log = log_msg(request, uri_web_about)
    #
    # Get and check user
    user = _check_user(request.get_cookie('user'))
    if not user:
        log_general('{log} - client redirected to "{redirect}"'.format(log=log, redirect=uri_web_login))
        redirect(uri_web_login)
    #
    log_general(log)
    return HTTPResponse(body=create_about(user, _cache), status=200)


@get(uri_web_infoservice)
def web_info(info=False):
    global _cache
    global _server_url
    log = log_msg(request, uri_web_infoservice)
    #
    try:
        if not info:
            log_error('{log} - {error}'.format(log=log, error='URI invalid'))
            raise HTTPError(404)
        #
        # Get and check user
        user = _check_user(request.get_cookie('user'))
        if not user:
            log_general('{log} - client redirected to "{redirect}"'.format(log=log, redirect=uri_web_login))
            redirect(uri_web_login)
        #
        info = cfg_urldecode(info)
        #
        info_seq = get_cfg_info_seq(_cache['setup'], info)
        #
        type = get_cfg_info_type(_cache['setup'], info_seq)
        #
        if type == 'news':
            html_body = news_body(user,
                                  _cache,
                                  _server_url,
                                  info_seq)
        elif type == 'tvlistings':
            html_body = tvlisting_body(user,
                                       _cache,
                                       _server_url,
                                       info_seq)
        elif type == 'weather':
            html_body = weather_body(_cache['setup'],
                                     _server_url,
                                     info_seq)
        else:
            return HTTPError(404)
        #
        body = create_page_body(user,
                                _cache,
                                html_body,
                                '{info}'.format(info=info),
                                '{info}'.format(info=info))
        #
        log_general(log)
        return HTTPResponse(body=body, status=200)
    except Exception as e:
        log_error('{log} - {error}'.format(log=log, error=e))
        raise HTTPError(500)


@get(uri_web_devices)
def web_devices(group=False, thing=False):
    global _cache
    global _server_url
    log = log_msg(request, uri_web_devices)
    #
    try:
        if (not group) or (not thing):
            log_error('{log} - {error}'.format(log=log, error='URI invalid'))
            raise HTTPError(404)
        #
        # Get and check user
        user = _check_user(request.get_cookie('user'))
        if not user:
            log_general('{log} - client redirected to "{redirect}"'.format(log=log, redirect=uri_web_login))
            redirect(uri_web_login)
        #
        group = cfg_urldecode(group)
        thing = cfg_urldecode(thing)
        #
        group_seq = get_cfg_group_seq(_cache['setup'], group)
        thing_seq = get_cfg_thing_seq(_cache['setup'], group, thing)
        #
        query_dict = dict(request.query)
        #
        type = get_cfg_thing_type(_cache['setup'], group_seq, thing_seq)
        #
        if type == 'tv_lg_netcast':
            html_body = html_tv_lg_netcast(_cache['setup'],
                                           _server_url,
                                           group_seq,
                                           thing_seq)
        elif type == 'tivo':
            html_body = html_tivo(user,
                                  _cache,
                                  _server_url,
                                  group_seq,
                                  thing_seq)
        elif type == 'nest_account':
            html_body = html_nest(_cache['setup'],
                                  _server_url,
                                  group_seq,
                                  thing_seq,
                                  query_dict)
            try:
                if query_dict['body']:
                    return html_body
            except Exception as e:
                pass
        else:
            return HTTPError(404)
        #
        body = create_page_body(user,
                                _cache,
                                html_body,
                                '{group}: {thing}'.format(group=group, thing=thing),
                                '{group}: {thing}'.format(group=group, thing=thing))
        #
        log_general(log)
        return HTTPResponse(body=body, status=200)
    except Exception as e:
        log_error('{log} - {error}'.format(log=log, error=e))
        raise HTTPError(500)


@get(uri_web_static_resources)
def get_resource(folder, filename):
    return static_file(filename, root=os.path.join(os.path.dirname(__file__),('web/html/static/{folder}'.format(folder=folder))))


################################################################################################
# Handle requests for resource data
################################################################################################

@get(uri_data_device)
def get_data_device(group=False, thing=False, resource_requested=False):
    global _server_url
    log = log_msg(request, uri_data_device)
    #
    if (not group) or (not thing) or (not resource_requested):
        log_error('{log} - {error}'.format(log=log, error='URI invalid'))
        raise HTTPError(404)
    #
    try:
        #
        r = requests.get('{url}/{uri}'.format(url=_server_url, uri='data/{group}/{thing}/{resource_requested}'.format(group=group,
                                                                                                                      thing=thing,
                                                                                                                      resource_requested=resource_requested)))
        #
        log_general(log)
        if r.status_code == requests.codes.ok:
            if r.content:
                return HTTPResponse(body=r.content, status=200)
            else:
                return HTTPResponse(status=200)
        else:
            return HTTPResponse(status=400)
            #
    except Exception as e:
        log_error('{log} - {error}'.format(log=log, error=e))
        raise HTTPError(500)


################################################################################################
# Handle commands
################################################################################################


@get(uri_command)
@post(uri_command)
def send_command_device(group=False, thing=False):
    global _server_url
    log = log_msg(request, uri_command)
    #
    if (not group) or (not thing):
        log_error('{log} - {error}'.format(log=log, error='URI invalid'))
        raise HTTPError(404)
    #
    cmd_dict = dict(request.query)
    #
    try:
        #
        r = requests.post('{url}/{uri}'.format(url=_server_url, uri='command/{group}/{thing}'.format(group=group, thing=thing)),
                          json=cmd_dict)
        #
        log_general(log)
        if r.status_code == requests.codes.ok:
            if r.content:
                return HTTPResponse(body=r.content, status=200)
            else:
                return HTTPResponse(status=200)
        else:
            return HTTPResponse(status=400)
            #
    except Exception as e:
        log_error('{log} - {error}'.format(log=log, error=e))
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

@get(uri_favicon)
def get_favicon():
    global _server_url
    log = log_msg(request, uri_favicon)
    #
    try:
        r = requests.get('{url}/{uri}'.format(url=_server_url, uri='favicon.ico'))
        #
        log_general(log)
        if r.status_code == requests.codes.ok:
            return HTTPResponse(status=200, body=r.content)
        else:
            return HTTPResponse(status=400)
        #
    except Exception as e:
        log_error('{log} - {error}'.format(log=log, error=e))
        raise HTTPError(500)


@get(uri_image)
def get_image(category, filename):
    global _server_url
    log = log_msg(request, uri_image)
    #
    try:
        r = requests.get('{url}/{uri}'.format(url=_server_url, uri='img/{category}/{filename}'.format(category=category,
                                                                                                      filename=filename)))
        #
        log_general(log)
        if r.status_code == requests.codes.ok:
            response = HTTPResponse(status=200, body=r.content)
            response.set_header("Cache-Control", "public, max-age=604800")
            return response
        else:
            return HTTPResponse(status=400)
        #
    except Exception as e:
        log_error('{log} - {error}'.format(log=log, error=e))
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

def run_bottle(self_port):
    host='0.0.0.0'
    log_general('Bottle started: listening on {host}:{port}'.format(host=host, port=self_port))
    run(host=host, port=self_port, debug=True)
