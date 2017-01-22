from urllib import urlopen

from cache.setup import get_cfg_room_name
from cache.setup import get_cfg_device_name, get_cfg_device_value
from cache.setup import get_cfg_account_name, get_cfg_account_value
from cache.users import get_userrole, get_userimage


def html_menu(user, _cache):
    return html_menu_lhs(_cache['setup']) +\
           _html_menu_rhs(_cache['users'], user) +\
           urlopen('web/html/cmd_alert.html').read().encode('utf-8')


def html_menu_lhs(_cache_setup):
    #
    html = ''
    html += '<span class="sidebar_divider box-shadow"></span>'
    #
    for item_account in _cache_setup['accounts']:
        #
        label = get_cfg_account_name(_cache_setup, _cache_setup['accounts'][item_account]['account_id'])
        img = get_cfg_account_value(_cache_setup, _cache_setup['accounts'][item_account]['account_id'], 'logo')
        #
        html += urlopen('web/html/html_menu/menu_sidebar_item.html').read().encode('utf-8').format(href=('/web/account/{account_id}').format(account_id=_cache_setup['accounts'][item_account]['account_id']),
                                                                                              id='{account_id}'.format(account_id=_cache_setup['accounts'][item_account]['account_id']),
                                                                                              cls='',
                                                                                              name=label,
                                                                                              img=img)
    #
    for item_room in _cache_setup['rooms']:
        #
        html += '<span class="sidebar_divider box-shadow"></span>'
        #
        html += urlopen('web/html/html_menu/menu_sidebar_title.html').read().encode('utf-8').format(name=get_cfg_room_name(_cache_setup, _cache_setup['rooms'][item_room]['room_id']))
        #
        for item_device in _cache_setup['rooms'][item_room]['devices']:
            #
            label = get_cfg_device_name(_cache_setup,
                                        _cache_setup['rooms'][item_room]['room_id'],
                                        _cache_setup['rooms'][item_room]['devices'][item_device]['device_id'])
            img = get_cfg_device_value(_cache_setup,
                                       _cache_setup['rooms'][item_room]['room_id'],
                                       _cache_setup['rooms'][item_room]['devices'][item_device]['device_id'], 'logo')
            #
            html += urlopen('web/html/html_menu/menu_sidebar_item.html').read().encode('utf-8').format(href=('/web/device/{room_id}/{device_id}').format(room_id=_cache_setup['rooms'][item_room]['room_id'],
                                                                                                                                                    device_id=_cache_setup['rooms'][item_room]['devices'][item_device]['device_id']),
                                                                                                  id='{room_id}_{device_id}'.format(room_id=_cache_setup['rooms'][item_room]['room_id'],
                                                                                                                                    device_id=_cache_setup['rooms'][item_room]['devices'][item_device]['device_id']),
                                                                                                  cls='',
                                                                                                  name=label,
                                                                                                  img=img)
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