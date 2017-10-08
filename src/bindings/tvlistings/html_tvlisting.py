import datetime
import requests
import ast
from urllib import urlopen
from cache.setup import cfg_urlencode, get_cfg_info_name
from log.log import log_general, log_error
from cache.users import get_userchannels


hourly_width_px = 400
max_hours = 6
isoformat = '%Y-%m-%d %H:%M:%S'
time_format = '%H:%M'


def tvlisting_body(user, _cache, server_url, info_seq):
    #
    try:
        listings = request_tvlistings(_cache, server_url, info_seq)
        #
        if not str(listings)=='False':
            args = {'timestamp': datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
                    'body_tvlistings': _create_html(user, _cache, listings)}
        else:
            args = {'timestamp': datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
                    'body_tvlistings': 'ERROR'}
        #
        return urlopen('bindings/tvlistings/tvlistings_main.html').read().encode('utf-8').format(**args)
        #
    except Exception as e:
        raise Exception


def request_tvlistings(_cache, server_url, info_seq):
    url = '{url}/{uri}'.format(url=server_url, uri='data/info/{info}/alllistings'.format(info=cfg_urlencode(get_cfg_info_name(_cache['setup'], info_seq))))
    r = requests.get(url)
    #
    if r.status_code == requests.codes.ok:
        log_general('TV Listing info retrieved successfully - {status_code}'.format(status_code=r.status_code))
        return ast.literal_eval(r.content)
    else:
        log_error('TV Listing info failed to be retrieved - {status_code}'.format(status_code=r.status_code))
        return False


def _create_html(user, _cache, listings):
    #
    channels = _cache['tvchannels']
    if user:
        cache_users = _cache['users']
        user_channels = get_userchannels(cache_users, user)
    else:
        user_channels = False
    #
    current_hour = datetime.datetime.now().hour
    current_hourly_time = datetime.datetime.combine(datetime.date.today(),
                                                    datetime.time(current_hour))
    #
    html_hours_title = ''
    for x in range(0, (2 * max_hours) + 1, 1):
        hr = int(float(x)/2)
        mn = int((float(x)/2 - hr) * 60)
        t = current_hourly_time + datetime.timedelta(hours=hr, minutes=mn)
        args_time = {'width': hourly_width_px/2,
                     'hour': t.strftime(time_format)}
        html_hours_title += urlopen('bindings/tvlistings/tvlistings_listing_row_listings_title_item.html').read().encode('utf-8').format(**args_time)
    #
    # vertical line for now() time
    left_dist = _calc_item_width(current_hourly_time, datetime.datetime.now())
    #
    first_tab = True
    html_pill_contents = ''
    #
    # User specific channels
    #
    html_pill_nav_user = ''
    if user_channels:
        #
        if first_tab:
            active = 'active'
            first_tab = False
        else:
            active = ''
        #
        html_channels = urlopen('bindings/tvlistings/tvlistings_listing_row_channel_title.html').read().encode('utf-8')
        html_listings = urlopen('bindings/tvlistings/tvlistings_listing_row_listings.html').read().encode('utf-8').format(listings=html_hours_title)
        cat = 0
        while cat < len(channels['channels']):
            chan = 0
            while chan < len(channels['channels'][str(cat)]['channels']):
                #
                if channels['channels'][str(cat)]['channels'][str(chan)]['name'] in user_channels:
                    #
                    try:
                        logo = channels['channels'][str(cat)]['channels'][str(chan)]['hd']['logo']
                    except:
                        logo = channels['channels'][str(cat)]['channels'][str(chan)]['sd']['logo']
                    #
                    args_channels = {'imgchan': logo}
                    html_channels += urlopen('bindings/tvlistings/tvlistings_listing_row_channel.html').read().encode('utf-8').format(**args_channels)
                    #
                    temp_html = ''
                    #
                    try:
                        if len(listings[str(cat)][str(chan)]) > 0:
                            #
                            item_keys = sorted(listings[str(cat)][str(chan)].keys())
                            #
                            for item in item_keys:
                                #
                                start = datetime.datetime.strptime(listings[str(cat)][str(chan)][item]['start'],
                                                                   isoformat)
                                end = datetime.datetime.strptime(listings[str(cat)][str(chan)][item]['end'], isoformat)
                                #
                                if (start > current_hourly_time or end > current_hourly_time) and start < (
                                    current_hourly_time + datetime.timedelta(hours=max_hours)):
                                    #
                                    if start < current_hourly_time:
                                        width_s = current_hourly_time
                                    else:
                                        width_s = start
                                    #
                                    if end > current_hourly_time + datetime.timedelta(hours=max_hours):
                                        width_e = current_hourly_time + datetime.timedelta(hours=max_hours)
                                    else:
                                        width_e = end
                                    #
                                    item_width = _calc_item_width(width_s, width_e)
                                    #
                                    subtitle = ''
                                    try:
                                        if listings[str(cat)][str(chan)][item]['subtitle'] != '':
                                            subtitle = '{subtitle}: '.format(
                                                subtitle=listings[str(cat)][str(chan)][item]['subtitle'])
                                    except Exception as e:
                                        pass
                                    #
                                    args_item = {'width': item_width - 2,
                                                 'start': start.strftime(time_format),
                                                 'end': end.strftime(time_format),
                                                 'title': listings[str(cat)][str(chan)][item]['title'],
                                                 'subtitle': subtitle,
                                                 'desc': listings[str(cat)][str(chan)][item]['desc']}
                                    temp_html += urlopen('bindings/tvlistings/tvlistings_listing_row_listings_item.html').read().encode('utf-8').format(**args_item)
                        else:
                            raise Exception
                        #
                        args_listings = {'listings': temp_html}
                        html_listings += urlopen('bindings/tvlistings/tvlistings_listing_row_listings.html').read().encode('utf-8').format(**args_listings)
                    except Exception as e:
                        args_listings = {'listings': '<div style="padding: 5px;">No listings available</div>'}
                        html_listings += urlopen('bindings/tvlistings/tvlistings_listing_row_listings.html').read().encode('utf-8').format(**args_listings)
                        #
                chan += 1
            cat += 1
        #
        #
        html_pill_nav_user = urlopen('web/html/html_pills/pills_nav.html').read().encode('utf-8').format(active=active,
                                                                                              category=str(user).lower(),
                                                                                              title=str(user)+'\'s favourites')
        #
        html_cat_pill_body = urlopen('bindings/tvlistings/tvlistings_listing.html').read().encode('utf-8').format(left_dist=left_dist,
                                                                                                                          rows_channel_images=html_channels,
                                                                                                                          rows_listings=html_listings)
        #
        html_pill_contents += urlopen('web/html/html_pills/pills_contents.html').read().encode('utf-8').format(active=active,
                                                                                                    category=str(user).lower(),
                                                                                                    body=html_cat_pill_body)
    #
    # All channels grouped into categories
    #
    html_pill_nav_cat = ''
    cat = 0
    while cat < len(channels['channels']):
        #
        if first_tab:
            active = 'active'
            first_tab = False
        else:
            active = ''
        #
        category = channels['channels'][str(cat)]['category']
        #
        html_pill_nav_cat += urlopen('web/html/html_pills/pills_nav.html').read().encode('utf-8').format(active=active,
                                                                                              category=category.lower(),
                                                                                              title=category)
        #
        html_channels = urlopen('bindings/tvlistings/tvlistings_listing_row_channel_title.html').read().encode('utf-8')
        html_listings = urlopen('bindings/tvlistings/tvlistings_listing_row_listings.html').read().encode('utf-8').format(listings=html_hours_title)
        #
        chan = 0
        while chan < len(channels['channels'][str(cat)]['channels']):
            #
            try:
                logo = channels['channels'][str(cat)]['channels'][str(chan)]['hd']['logo']
            except:
                logo = channels['channels'][str(cat)]['channels'][str(chan)]['sd']['logo']
            #
            args_channels = {'imgchan': logo}
            html_channels += urlopen('bindings/tvlistings/tvlistings_listing_row_channel.html').read().encode('utf-8').format(**args_channels)
            #
            temp_html = ''
            #
            try:
                if len(listings[str(cat)][str(chan)]) > 0:
                    #
                    item_keys = sorted(listings[str(cat)][str(chan)].keys())
                    #
                    for item in item_keys:
                        #
                        start = datetime.datetime.strptime(listings[str(cat)][str(chan)][item]['start'], isoformat)
                        end = datetime.datetime.strptime(listings[str(cat)][str(chan)][item]['end'], isoformat)
                        #
                        if (start > current_hourly_time or end > current_hourly_time) and start < (current_hourly_time + datetime.timedelta(hours=max_hours)):
                            #
                            if start < current_hourly_time:
                                width_s = current_hourly_time
                            else:
                                width_s = start
                            #
                            if end > current_hourly_time + datetime.timedelta(hours=max_hours):
                                width_e = current_hourly_time + datetime.timedelta(hours=max_hours)
                            else:
                                width_e = end
                            #
                            item_width = _calc_item_width(width_s, width_e)
                            #
                            subtitle = ''
                            try:
                                if listings[str(cat)][str(chan)][item]['subtitle'] != '':
                                    subtitle = '{subtitle}: '.format(subtitle=listings[str(cat)][str(chan)][item]['subtitle'])
                            except Exception as e:
                                pass
                            #
                            args_item = {'width': item_width - 2,
                                         'start': start.strftime(time_format),
                                         'end': end.strftime(time_format),
                                         'title': listings[str(cat)][str(chan)][item]['title'],
                                         'subtitle': subtitle,
                                         'desc': listings[str(cat)][str(chan)][item]['desc']}
                            temp_html += urlopen('bindings/tvlistings/tvlistings_listing_row_listings_item.html').read().encode('utf-8').format(**args_item)
                else:
                    raise Exception
                #
                args_listings = {'listings': temp_html}
                html_listings += urlopen('bindings/tvlistings/tvlistings_listing_row_listings.html').read().encode('utf-8').format(**args_listings)
            except Exception as e:
                args_listings = {'listings': '<div style="padding: 5px;">No listings available</div>'}
                html_listings += urlopen('bindings/tvlistings/tvlistings_listing_row_listings.html').read().encode('utf-8').format(**args_listings)
            #
            chan += 1
            #
        #
        html_cat_pill_body = urlopen('bindings/tvlistings/tvlistings_listing.html').read().encode('utf-8').format(left_dist=left_dist,
                                                                                                                          rows_channel_images=html_channels,
                                                                                                                          rows_listings=html_listings)
        #
        html_pill_contents += urlopen('web/html/html_pills/pills_contents.html').read().encode('utf-8').format(active=active,
                                                                                                    category=category.lower(),
                                                                                                    body=html_cat_pill_body)
        #
        cat += 1
        #
    #
    if user_channels:
        html_pill_nav_cat = urlopen('web/html/html_pills/pills_nav_dropdown.html').read().encode('utf-8').format(title='Categories',
                                                                                                      dropdowns=html_pill_nav_cat)
    #
    html_pill_nav = html_pill_nav_user + html_pill_nav_cat
    #
    return urlopen('web/html/html_pills/pills_parent.html').read().encode('utf-8').format(nav=html_pill_nav,
                                                                               content=html_pill_contents)


def _calc_item_width(start, end):
    hours_diff = (end - start).total_seconds()/3600
    return hourly_width_px * hours_diff
