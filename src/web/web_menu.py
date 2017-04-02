from urllib import urlopen
from cache.setup import cfg_urlencode
from cache.users import get_userrole, get_userimage


def html_menu(user, _cache):
    return html_menu_lhs(_cache['setup']) +\
           _html_menu_rhs(_cache['users'], user) +\
           urlopen('web/html/cmd_alert.html').read().encode('utf-8')


def html_menu_lhs(_cache_setup):
    #
    html = ''
    #
    if len(_cache_setup['bindings']['info_services']) > 0:
        add_divider = True
    else:
        add_divider = False
    #
    for info in _cache_setup['bindings']['info_services']:
        #
        html += urlopen('web/html/html_menu/menu_sidebar_item.html').read().encode('utf-8').format(href=('/web/info/{info}').format(info=cfg_urlencode(info['name'])),
                                                                                                   id='{info}'.format(info=info['sequence']),
                                                                                                   cls='',
                                                                                                   name=info['name'],
                                                                                                   img='/img/logo/{img}'.format(img=info['logo']))
    #
    if add_divider:
        html += '<span class="sidebar_divider box-shadow"></span>'
    #
    add_divider = False
    #
    for group in _cache_setup['bindings']['groups']:
        #
        if add_divider:
            html += '<span class="sidebar_divider box-shadow"></span>'
        #
        html += urlopen('web/html/html_menu/menu_sidebar_title.html').read().encode('utf-8').format(name=group['name'])
        #
        for thing in group['things']:
            #
            html += urlopen('web/html/html_menu/menu_sidebar_item.html').read().encode('utf-8').format(href=('/web/{group}/{thing}').format(group=cfg_urlencode(group['name']),
                                                                                                                                            thing=cfg_urlencode(thing['name'])),
                                                                                                       id='{group}_{thing}'.format(group=group['sequence'],
                                                                                                                                   thing=thing['sequence']),
                                                                                                       cls='',
                                                                                                       name=thing['name'],
                                                                                                       img='/img/logo/{img}'.format(img=thing['logo']))
        #
        add_divider = True
        #
    #
    return urlopen('web/html/html_menu/menu_lhs.html').read().encode('utf-8').format(menu=html)


def _html_menu_rhs(_cache, user):
    #user = user if user != False else 'Guest'
    user_image = _user_image(_cache, user)
    html_settings = _user_settings(_cache, user)
    return urlopen('web/html/html_menu/menu_rhs.html').read().encode('utf-8').format(settings=html_settings,
                                                                                user=user,
                                                                                user_image=user_image)


def _user_settings(_cache_users, user):
    if get_userrole(_cache_users, user) == "admin":
        return urlopen('web/html/html_menu/menu_settings.html').read().encode('utf-8')
    else:
        return ""


def _user_image(_cache_users, user):
    return get_userimage(_cache_users, user)