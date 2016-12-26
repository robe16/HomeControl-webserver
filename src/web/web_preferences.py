import json
import os
from urllib import urlopen

from cache.users import get_userchannels


def _preference_tvguide(user):
    #
    color_usr = 'warning'
    #
    user_channels = get_userchannels(user)
    #
    usr_header = '<span class="label label-{color_usr}" style="font-weight: bold">{user}\'s favourites</span>'.format(user = user, color_usr = color_usr)
    #
    return urlopen('web/html/html_preferences/preferences_tvguide.html').read().encode('utf-8').format(usr_header = usr_header,
                                                                                                  listings = _preference_tvguide_items(user_channels, color_usr))

def _preference_tvguide_items(user_channels, color_usr):
    #
    with open(os.path.join('lists', 'list_channels.json'), 'r') as data_file:
        data = json.load(data_file)
    data_channels = data["channels"]
    html = ''
    rowcolor = '#ffffff'
    #
    for chan in data_channels:
        #
        chan_id = chan['name'].replace(' ', '').lower()
        glyphicon = 'glyphicon-ok' if chan['enabled'] else 'glyphicon-remove'
        color_gen = 'green' if chan['enabled'] else 'red'
        # Create alternating row colours
        rowcolor = '#e8e8e8' if rowcolor == '#ffffff' else '#ffffff'
        #
        # Get if item is in user's preferences
        chkd_usr = ''
        for n in user_channels:
            if chan['name'].lower() == n.lower():
                chkd_usr = 'checked'
                break
        #
        html_usr_tgle = urlopen('web/html/html_preferences/preferences_tvguide_toggle.html').read().encode('utf-8').format(chan_name = chan['name'],
                                                                                                                      color_usr = color_usr,
                                                                                                                      chkd_usr = chkd_usr)
        #
        html += urlopen('web/html/html_preferences/preferences_tvguide_item.html').read().encode('utf-8').format(chan_id = chan_id,
                                                                                                            rowcolor = rowcolor,
                                                                                                            color_gen = color_gen,
                                                                                                            glyphicon_gen = glyphicon,
                                                                                                            channame = chan['name'],
                                                                                                            imgtype = chan['type'],
                                                                                                            imgchan = chan['logo'],
                                                                                                            user_chan_toggle = html_usr_tgle)
    #
    return html