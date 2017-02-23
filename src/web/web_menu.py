from urllib import urlopen

from cache.setup import get_cfg_group_name
from cache.setup import get_cfg_device_name, get_cfg_device_value
from cache.setup import get_cfg_info_enabled
from cache.users import get_userrole, get_userimage


def html_menu(user, _cache):
    return html_menu_lhs(_cache['setup']) +\
           _html_menu_rhs(_cache['users'], user) +\
           urlopen('web/html/cmd_alert.html').read().encode('utf-8')


def html_menu_lhs(_cache_setup):
    #
    html = ''
    add_divider = False
    #
    if get_cfg_info_enabled(_cache_setup, 'weather'):
        add_divider = True
        html += urlopen('web/html/html_menu/menu_sidebar_item.html').read().encode('utf-8').format(href='/web/info/weather',
                                                                                                   id='weather',
                                                                                                   cls='',
                                                                                                   name='Weather',
                                                                                                   img='/img/icon/ic_infoservice_weather.png')
    #
    if get_cfg_info_enabled(_cache_setup, 'news'):
        add_divider = True
        html += urlopen('web/html/html_menu/menu_sidebar_item.html').read().encode('utf-8').format(href='/web/info/news',
                                                                                                   id='news',
                                                                                                   cls='',
                                                                                                   name='News',
                                                                                                   img='/img/icon/ic_infoservice_news.png')
    #
    if get_cfg_info_enabled(_cache_setup, 'tvlistings'):
        add_divider = True
        html += urlopen('web/html/html_menu/menu_sidebar_item.html').read().encode('utf-8').format(href='/web/info/tvlistings',
                                                                                                   id='tvlistings',
                                                                                                   cls='',
                                                                                                   name='TV Listings',
                                                                                                   img='/img/icon/ic_infoservice_tvguide.png')
    #
    if add_divider:
        html += '<span class="sidebar_divider box-shadow"></span>'
    #
    for item_group in _cache_setup['bundles']['devices']['groups']:
        #
        html += urlopen('web/html/html_menu/menu_sidebar_title.html').read().encode('utf-8').format(name=get_cfg_group_name(_cache_setup, _cache_setup['bundles']['devices']['groups'][item_group]['group_id']))
        #
        for item_device in _cache_setup['bundles']['devices']['groups'][item_group]['devices']:
            #
            label = get_cfg_device_name(_cache_setup,
                                        _cache_setup['bundles']['devices']['groups'][item_group]['group_id'],
                                        _cache_setup['bundles']['devices']['groups'][item_group]['devices'][item_device]['device_id'])
            img = get_cfg_device_value(_cache_setup,
                                       _cache_setup['bundles']['devices']['groups'][item_group]['group_id'],
                                       _cache_setup['bundles']['devices']['groups'][item_group]['devices'][item_device]['device_id'], 'logo')
            #
            html += urlopen('web/html/html_menu/menu_sidebar_item.html').read().encode('utf-8').format(href=('/web/device/{group_id}/{device_id}').format(group_id=_cache_setup['bundles']['devices']['groups'][item_group]['group_id'],
                                                                                                                                                          device_id=_cache_setup['bundles']['devices']['groups'][item_group]['devices'][item_device]['device_id']),
                                                                                                  id='{group_id}_{device_id}'.format(group_id=_cache_setup['bundles']['devices']['groups'][item_group]['group_id'],
                                                                                                                                     device_id=_cache_setup['bundles']['devices']['groups'][item_group]['devices'][item_device]['device_id']),
                                                                                                  cls='',
                                                                                                  name=label,
                                                                                                  img='/img/logo/{img}'.format(img=img))
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