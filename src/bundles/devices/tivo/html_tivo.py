import requests
import ast
from urllib import urlopen
from cfg import server_url
from cache.setup import get_cfg_device_detail_public
from lists.devices.list_devices import get_device_html_command
from log.console_messages import print_error, print_msg
from web.web_tvchannels import html_channels_user_and_all


def html_tivo(user, _cache, room_id, device_id):
    #
    json_recordings = _get_recordings(room_id, device_id)
    #
    chan_current = _get_current_chan(room_id, device_id)
    if chan_current:
        currentChan_name = chan_current['channel']['name']
        currentChan_number = chan_current['channel']['number']
        currentChan_logo = chan_current['channel']['logo']
    else:
        currentChan_name = '-'
        currentChan_number = ''
        currentChan_logo = 'ic_blank.png'
    #
    _device_details = {}
    _device_details['type'] = 'tivo'
    _device_details['room_id'] = room_id
    _device_details['device_id'] = device_id
    _device_details['package'] = ["virginmedia_package", get_cfg_device_detail_public(_cache['setup'], room_id, device_id, 'package')]
    _device_details['current_chan'] = currentChan_number
    #
    try:
        html_channels = html_channels_user_and_all(_cache=_cache,
                                                   user=user,
                                                   _device_details=_device_details)
    except Exception as e:
        print_error('Could not create TV channel HTML - {error}'.format(error=e))
        html_channels = ''
    #
    args = {'room_id': room_id,
            'device_id': device_id,
            'html_recordings': _html_recordings(json_recordings),
            'timestamp_recordings': json_recordings['timestamp'],
            'now_viewing_logo': currentChan_logo,
            'now_viewing': currentChan_name,
            'html_channels': html_channels}
    #
    return urlopen('web/html/html_devices/' + get_device_html_command('tivo')).read().encode('utf-8').format(**args)


def _html_recordings(json_recordings):
    #
    html_recordings = ''
    #
    try:
        #
        if not json_recordings:
            raise Exception
        #
        html_recordings += '<div class="row">'
        html_recordings += '<div class="col-xs-10"><h5>Title</h5></div>'
        html_recordings += '<div class="col-xs-2" style="text-align: right;"><h5>#</h5></div>'
        html_recordings += '</div>'
        #
        folderCount = 0
        while folderCount < len(json_recordings['recordings']):
            #
            iFolder = json_recordings['recordings'][str(folderCount)]
            seriesdrop_html = ''
            #
            itemCount = 0
            while itemCount < len(iFolder['items']):
                #
                iFile = iFolder['items'][str(itemCount)]
                #
                if not iFile['episodeNumber']['series'] == '' and not iFile['episodeNumber']['episode'] == '':
                    episodenumber = 'Series {se} Episode {ep}'.format(se=iFile['episodeNumber']['series'],
                                                                      ep=iFile['episodeNumber']['episode'])
                else:
                    episodenumber = ''
                #
                img = '<img style="height: 25px;" src="/img/channel/{imgFile}"/>'.format(imgFile=iFile['channel']['image'])
                #
                seriesdrop_html += '<div class="row">'
                seriesdrop_html += '<div class="col-xs-9"><h5>{ep_title}</h5></div>'.format(ep_title=iFile['episodeTitle'])
                seriesdrop_html += '<div class="col-xs-3" style="text-align: right;">{img}</div>'.format(img=img)
                seriesdrop_html += '</div>'
                seriesdrop_html += '<div class="row"><div class="col-xs-12"><p>{desc}</p></div></div>'.format(desc=iFile['description'])
                seriesdrop_html += '<div class="row" style="margin-bottom: 20px">'
                seriesdrop_html += '<div class="col-xs-6"><p>{episodenumber}</p></div>'.format(episodenumber=episodenumber)
                seriesdrop_html += '<div class="col-xs-6" align="right"><p>{date}</p></div>'.format(date=iFile['recordingDate'])
                seriesdrop_html += '</div>'
                #
                itemCount += 1
            #
            html_recordings += '<div class="row btn-col-grey btn_pointer" style="margin-bottom: 5px;" data-toggle="collapse" data-target="#collapse_series{count}">'.format(count=folderCount)
            #
            # Based Bootstrap's Scaffolding (12-column grid)
            # | (9) Title | (2) Number of episodes | (1) Movie/TV Image |
            # | (9) Episode title | (3) Channel logo |
            # | (12) Description |
            # | (6) Series & Episode number | (6) Recording date |
            #
            html_recordings += '<div class="col-xs-9"><h5>{title}</h5></div>'.format(title=iFolder['folderName'])
            #
            if iFolder['type']=='tv':
                html_recordings += '<div class="col-xs-2" style="text-align: right;"><h6>{count}</h6></div>'.format(count=len(iFolder['items']))
            else:
                html_recordings += '<div class="col-xs-2" style="text-align: right;"></div>'
            #
            if iFolder['type']=='tv' or iFolder['type']=='movie':
                html_recordings += '<div class="col-xs-1" style="text-align: right; padding: 5px;"><img style="height: 25px;" src="/img/icon/ic_{type}.png"/></div>'.format(type=iFolder['type'])
            else:
                html_recordings += '<div class="col-xs-1" style="text-align: right;"></div>'
            #
            html_recordings += '</div>'
            html_recordings += '<div class="row collapse out" id="collapse_series{count}"><div class="container-fluid">{drop}</div></div>'.format(count=folderCount,
                                                                                                                                                  drop=seriesdrop_html)
            #
            folderCount += 1
            #
        return html_recordings
    except Exception as e:
        print_error('Attempted to create recordings html - {error}'.format(error=e))
        return '<p>Error</p>'


def _get_recordings(room_id, device_id):
    data = _getData(room_id, device_id, 'recordings')
    if data:
        return ast.literal_eval(data)
    else:
        return False


def _get_current_chan(room_id, device_id):
    data = _getData(room_id, device_id, 'channel')
    if data:
        return ast.literal_eval(data)
    else:
        return False


def _getData(room_id, device_id, datarequest):
    r = requests.get(server_url('data/device/{room_id}/{device_id}/{datarequest}'.format(room_id=room_id,
                                                                                         device_id=device_id,
                                                                                         datarequest=datarequest)))
    if r.status_code == requests.codes.ok:
        return r.content
    else:
        print_error('TIVO - Attempted to request {data} from server - {status}'.format(data=datarequest,
                                                                                       status=r.status_code))
        return False