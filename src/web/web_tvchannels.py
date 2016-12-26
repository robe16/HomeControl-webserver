from urllib import urlopen

from cache.users import get_userchannels
from cache.tvchannels import *


def html_channels_user_and_all (_cache, user=False, _device_details=False):
    #
    cache_channels = _cache['tvchannels']
    cache_devices = _cache['setup']
    cache_users = _cache['users']
    #
    if not cache_channels:
        return _html_no_channels()
    #
    if _device_details:
        type = _device_details['type']
        room_id = _device_details['room_id']
        device_id = _device_details['device_id']
        package = _device_details['package']
        current_chan = _device_details['current_chan']
    else:
        type = False
        room_id = False
        device_id = False
        package = False
        current_chan = False
    #
    html_channels = ''
    #
    if room_id and device_id:
        html_channels += '<script>setTimeout(function () {getChannel(\'/data/device/' + str(room_id) + \
                         '/' + str(device_id) + \
                         '/channel\', true);}, 10000);</script>'
    #
    first_tab = True
    html_nav_user = ''
    html_nav_all = ''
    html_content = ''
    #
    user_channels = get_userchannels(cache_users, user)
    #
    # If user_channels has a value, then create a
    # tab and contents for user favourite channels
    if user_channels:
        #
        if first_tab:
            active = 'active'
            first_tab = False
        else:
            active = ''
        #
        userCount = 0
        user_channels_temp = {}
        user_channels_temp['category'] = user
        user_channels_temp['channels'] = {}
        #
        catCount = 0
        while catCount < len(cache_channels['channels']):
            chanCount = 0
            while chanCount < len(cache_channels['channels'][str(catCount)]['channels']):
                #
                if cache_channels['channels'][str(catCount)]['channels'][str(chanCount)]['name'] in user_channels:
                    #
                    user_channels_temp['channels'][str(userCount)] = cache_channels['channels'][str(catCount)]['channels'][str(chanCount)]
                    userCount += 1
                    #
                #
                chanCount += 1
            catCount += 1
        #
        # Pill header
        html_nav_user += urlopen('web/html/pills_nav.html').read().encode('utf-8').format(active=active,
                                                                                    category=str(user).lower(),
                                                                                    title=str(user)+'\'s favourites')
        #
        body = _html_channels_container(user_channels_temp,
                                        user=user,
                                        _device_details=_device_details)
        # Pill contents
        html_content += urlopen('web/html/pills_contents.html').read().encode('utf-8').format(active=active,
                                                                                         category=str(user).lower(),
                                                                                         body=body)
    #
    #
    catCount = 0
    while catCount < len(cache_channels['channels']):
        #
        if first_tab:
            active = 'active'
            first_tab = False
        else:
            active = ''
        #
        category = cache_channels['channels'][str(catCount)]['category']
        #
        html_nav_all += urlopen('web/html/pills_nav.html').read().encode('utf-8').format(active=active,
                                                                                         category=category.lower(),
                                                                                         title=category)
        #
        body = _html_channels_container(cache_channels['channels'][str(catCount)],
                                        _device_details=_device_details)
        #
        html_content += urlopen('web/html/pills_contents.html').read().encode('utf-8').format(active=active,
                                                                                              category=category.lower(),
                                                                                              body=body)
        #
        catCount += 1
    #
    # If user channels available, change categories into dropdown menu
    if user_channels:
        html_nav_all = urlopen('web/html/pills_nav_dropdown.html').read().encode('utf-8').format(title='All Channels',
                                                                                            dropdowns=html_nav_all)
    #
    # Combine pills for 'user' and 'all' channel listings
    html_nav = html_nav_user + html_nav_all
    #
    html_channels += urlopen('web/html/pills_parent.html').read().encode('utf-8').format(nav=html_nav,
                                                                                   content=html_content)
    #
    return html_channels


def _html_channels_container(channels_items, user=False, _device_details=False):
    #
    header = '{user}\'s favourites'.format(user=user) if user else channels_items['category']
    #
    html_chans = _channels_contents(channels_items,
                                    user=user,
                                    _device_details=_device_details)
    #
    return urlopen('web/html/html_tvguide/tvguide-grid.html').read().encode('utf-8').format(header=header,
                                                                                            html_chans=html_chans)


def _channels_contents(channel_items, user=False, _device_details=False):
    #
    if _device_details:
        type = _device_details['type']
        room_id = _device_details['room_id']
        device_id = _device_details['device_id']
        package = _device_details['package']
        current_chan = _device_details['current_chan']
    else:
        type = False
        room_id = False
        device_id = False
        package = False
        current_chan = False
    #
    html = ''
    #
    chanCount = 0
    while chanCount < len(channel_items['channels']):
        #
        if chanCount > 1 and chanCount % 6 == 0:
            html += '</div><div class="row">'
        #
        res = _get_res(channel_items['channels'][str(chanCount)], package)
        #
        channo = channel_items['channels'][str(chanCount)][res]['devicekeys'][type]
        #
        # Create element id, including user name if required (user name prevents duplication of id names within page)
        chan_id = str(user).lower()+'_' if user else ''
        chan_id += channel_items['category'].replace(' ', '').lower()
        chan_id += channel_items['channels'][str(chanCount)]['name'].replace(' ', '').lower()
        #
        # If current channel, create element class text for highlighting
        if current_chan and channo == current_chan:
            chan_highlight = 'chan-highlight'
        else:
            chan_highlight = ''
        #
        html += urlopen('web/html/html_tvguide/tvguide-grid_item.html').read().encode('utf-8').format(id=('chan' + str(channo)),
                                                                                                 chan_id=chan_id,
                                                                                                 cls_highlight=chan_highlight,
                                                                                                 imgchan=channel_items['channels'][str(chanCount)][res]['logo'],
                                                                                                 channame=channel_items['channels'][str(chanCount)]['name'],
                                                                                                 room_id=room_id,
                                                                                                 device_id=device_id,
                                                                                                 channo=channo)

        #
        chanCount += 1
    #
    return html


def _get_res(_channelitem, package):
    if bool(package):
        use = False
        if package[0]=='freeview':
            if _channelitem['hd']['freeview']:
                return 'hd'
            elif _channelitem['sd']['freeview']:
                return 'sd'
        else:
            device_package_name = package[0]
            device_package_level = package[1]
            #
            try:
                hd_package = _channelitem['hd'][device_package_name]
            except:
                hd_package = False
            #
            if bool(hd_package):
                for p in device_package_level:
                    if p in hd_package:
                        return 'hd'
            #
            try:
                sd_package = _channelitem['sd'][device_package_name]
            except:
                sd_package = False
            #
            if bool(sd_package):
                for p in device_package_level:
                    if p in sd_package:
                        return 'sd'
    return False


def _html_no_channels():
    #
    body = '<strong>An error has occurred!!</strong> The list of channels on the server is empty. Please check server setup.'
    #
    return urlopen('web/html/comp_alert.html').read().encode('utf-8').format(type='alert-danger',
                                                                        body=body)