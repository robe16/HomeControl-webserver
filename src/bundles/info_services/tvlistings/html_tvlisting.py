import datetime
import requests
import ast
from urllib import urlopen
from src.cfg import server_url
from src.log.console_messages import print_msg, print_error


hourly_width_px = 400
isoformat = '%Y-%m-%d %H:%M:%S'
time_format = '%H:%M'


def tvlisting_body(_cache_channels):
    #
    listings = request_tvlistings()
    #
    if not str(listings)=='False':
        args = {'timestamp': datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
                'body_tvlistings': _create_html(_cache_channels, listings)}
    else:
        args = {'timestamp': datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
                'body_tvlistings': 'ERROR'}
    #
    return urlopen('web/html/html_info_services/tvlistings_main.html').read().encode('utf-8').format(**args)


def request_tvlistings():
    url = server_url('data/info/tvlistings/alllistings')
    r = requests.get(url)
    #
    if r.status_code == requests.codes.ok:
        print_msg('TV Listing info retrieved successfully - {status_code}'.format(status_code=r.status_code))
        return ast.literal_eval(r.content)
    else:
        print_error('TV Listing info failed to be retrieved - {status_code}'.format(status_code=r.status_code))
        return False


def _create_html(channels, listings):
    #
    current_hour = datetime.datetime.now().hour
    current_hourly_time = datetime.datetime.combine(datetime.date.today(),
                                                    datetime.time(current_hour))
    #
    html_hours_title = ''
    for x in range(0, 6, 1):
        hr = int(float(x)/2)
        mn = int((float(x)/2 - hr) * 60)
        t = datetime.time(current_hour + hr, mn).strftime(time_format)
        args_time = {'width': hourly_width_px/2,
                     'hour': t}
        html_hours_title += urlopen('web/html/html_info_services/tvlistings_listing_row_listings_title_item.html').read().encode('utf-8').format(**args_time)
    #
    html_channels = urlopen('web/html/html_info_services/tvlistings_listing_row_channel_title.html').read().encode('utf-8')
    html_listings = urlopen('web/html/html_info_services/tvlistings_listing_row_listings_title.html').read().encode('utf-8').format(hour_titles=html_hours_title)
    #
    cat = 0
    while cat < len(channels['channels']):
        chan = 0
        while chan < len(channels['channels'][str(cat)]['channels']):
            #
            try:
                logo = channels['channels'][str(cat)]['channels'][str(chan)]['hd']['logo']
            except:
                logo = channels['channels'][str(cat)]['channels'][str(chan)]['sd']['logo']
            #
            args_channels = {'imgchan': logo}
            html_channels += urlopen('web/html/html_info_services/tvlistings_listing_row_channel.html').read().encode('utf-8').format(**args_channels)
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
                        if start > current_hourly_time or end > current_hourly_time:
                            #
                            if start < current_hourly_time:
                                item_width = _calc_item_width(current_hourly_time, end)
                            else:
                                item_width = _calc_item_width(start, end)
                            #
                            args_item = {'width': item_width - 2,
                                         'start': start.strftime(time_format),
                                         'end': end.strftime(time_format),
                                         'title': listings[str(cat)][str(chan)][item]['title'],
                                         'desc': listings[str(cat)][str(chan)][item]['desc']}
                            temp_html += urlopen('web/html/html_info_services/tvlistings_listing_row_listings_item.html').read().encode('utf-8').format(**args_item)
                else:
                    raise Exception
                #
                args_listings = {'listings': temp_html}
                html_listings += urlopen('web/html/html_info_services/tvlistings_listing_row_listings.html').read().encode('utf-8').format(**args_listings)
            except Exception as e:
                # print_error('Failed to create html listings for channel - {error}'.format(error=e))
                args_listings = {'listings': '<div style="padding: 5px;">No listings available</div>'}
                html_listings += urlopen('web/html/html_info_services/tvlistings_listing_row_listings.html').read().encode('utf-8').format(**args_listings)
            #
            chan += 1
        cat += 1
    #
    return urlopen('web/html/html_info_services/tvlistings_listing.html').read().encode('utf-8').format(rows_channel_images=html_channels,
                                                                                                        rows_listings=html_listings)

def _calc_item_width(start, end):
    hours_diff = (end - start).total_seconds()/3600
    return hourly_width_px * hours_diff
