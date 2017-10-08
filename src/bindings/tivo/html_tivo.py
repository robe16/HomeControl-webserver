import requests
import ast
from urllib import urlopen
from cache.setup import cfg_urlencode, get_cfg_group_name, get_cfg_thing_name
from cache.setup import get_cfg_thing_detail_public
from log.log import log_error
from web.web_tvchannels import html_channels_user_and_all


def html_tivo(user, _cache, server_url, group_seq, thing_seq):
    #
    json_recordings = _get_recordings(_cache['setup'], server_url, group_seq, thing_seq)
    #
    chan_current = _get_current_chan(_cache['setup'], server_url, group_seq, thing_seq)
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
    _device_details['group_seq'] = group_seq
    _device_details['thing_seq'] = thing_seq
    _device_details['package'] = ["virginmedia_package", get_cfg_thing_detail_public(_cache['setup'], group_seq, thing_seq, 'package')]
    _device_details['current_chan'] = currentChan_number
    #
    try:
        html_channels = html_channels_user_and_all(_cache=_cache,
                                                   user=user,
                                                   _device_details=_device_details)
    except Exception as e:
        log_error('Could not create TV channel HTML - {error}'.format(error=e))
        html_channels = ''
    #
    try:
        recordings_timestamp = json_recordings['timestamp']
    except:
        recordings_timestamp = 'n/a'
    #
    args = {'group': cfg_urlencode(get_cfg_group_name(_cache['setup'], group_seq)),
            'thing': cfg_urlencode(get_cfg_thing_name(_cache['setup'], group_seq, thing_seq)),
            'html_recordings': _html_recordings(json_recordings),
            'timestamp_recordings': recordings_timestamp,
            'now_viewing_logo': currentChan_logo,
            'now_viewing': currentChan_name,
            'html_channels': html_channels}
    #
    return urlopen('bindings/tivo/object_device_tivo.html').read().encode('utf-8').format(**args)


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
                seriesdrop_html += '<div class="row"><div class="col-xs-12"><p>{desc}</p></div></div>'.format(desc=iFile['description'].encode('utf-8'))
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
        log_error('Attempted to create recordings html - {error}'.format(error=e))
        return '<p>Error</p>'


def _get_recordings(_cache, server_url, group_seq, thing_seq):
    data = _getData(_cache, server_url, group_seq, thing_seq, 'recordings')
    if data:
        return ast.literal_eval(data)
    else:
        return False


def _get_current_chan(_cache, server_url, group_seq, thing_seq):
    data = _getData(_cache, server_url, group_seq, thing_seq, 'channel')
    if data:
        return ast.literal_eval(data)
    else:
        return False


def _getData(_cache, server_url, group_seq, thing_seq, datarequest):
    r = requests.get('{url}/{uri}'.format(url=server_url, uri='data/{group}/{thing}/{datarequest}'.format(group=cfg_urlencode(get_cfg_group_name(_cache, group_seq)),
                                                                                                          thing=cfg_urlencode(get_cfg_thing_name(_cache, group_seq, thing_seq)),
                                                                                                          datarequest=datarequest)))
    if r.status_code == requests.codes.ok:
        return r.content
    else:
        log_error('TIVO - Attempted to request {data} from server - {status}'.format(data=datarequest,
                                                                                     status=r.status_code))
        return False