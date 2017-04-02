import requests
import ast
from urllib import urlopen
from cfg import server_url
from cache.setup import cfg_urlencode, get_cfg_group_name, get_cfg_thing_name
from log.console_messages import print_error


def html_tv_lg_netcast(_cache, group_seq, thing_seq):
    #
    args = {'group': cfg_urlencode(get_cfg_group_name(_cache, group_seq)),
            'thing': cfg_urlencode(get_cfg_thing_name(_cache, group_seq, thing_seq)),
            'apps': _html_apps(_cache, group_seq, thing_seq)}
    #
    return urlopen('bindings/tv_lg_netcast/object_device_tv_lg_netcast.html').read().encode('utf-8').format(**args)


def _html_apps(_cache, group_seq, thing_seq):
    #
    try:
        json_applist = _get_applist(_cache, group_seq, thing_seq)
        #
        html = '<table style="width:100%">' +\
               '<tr style="height:80px; padding-bottom:2px; padding-top:2px">'
        #
        count = 1
        for app in json_applist:
            try:
                #
                html += ('<td class="grid_item" style="width: 20%; cursor: pointer; vertical-align: top;" align="center" onclick="sendHttp(\'/command/{group}/{thing}?command=app&auid={auid}&name={app_name}\', null, \'GET\', false, true)">' +
                         '<img src="/command/{group}/{thing}?command=image&auid={auid}&name={app_name}" style="height:50px;"/>' +
                         '<p style="text-align:center; font-size: 13px;">{name}</p>' +
                         '</td>').format(group=cfg_urlencode(get_cfg_group_name(_cache, group_seq)),
                                         thing=cfg_urlencode(get_cfg_thing_name(_cache, group_seq, thing_seq)),
                                         auid = json_applist[app]['auid'],
                                         app_name = json_applist[app]['name'].replace(' ', '%20'),
                                         name = json_applist[app]['name'])
                #
                if count % 4 == 0:
                    html += '</tr><tr style="height:35px; padding-bottom:2px; padding-top:2px">'
                count += 1
                #
            except Exception as e:
                html += ''
            #
        #
        html += '</table></div>'
        return html
    except:
        return '<p style="text-align:center">App list could has not been retrieved from the device.</p>' +\
               '<p style="text-align:center">Please check the TV is turned on and then try again.</p>'


def _get_applist(_cache, group_seq, thing_seq):
    data = _getData(_cache, group_seq, thing_seq, 'applist')
    if data:
        return ast.literal_eval(data)
    else:
        return False


def _getData(_cache, group_seq, thing_seq, datarequest):
    r = requests.get(server_url('data/{group}/{thing}/{datarequest}'.format(group=cfg_urlencode(get_cfg_group_name(_cache, group_seq)),
                                                                            thing=cfg_urlencode(get_cfg_thing_name(_cache, group_seq, thing_seq)),
                                                                            datarequest=datarequest)))
    if r.status_code == requests.codes.ok:
        return r.content
    else:
        print_error('LG TV - Attempted to request {data} from server - {status}'.format(data=datarequest,
                                                                                        status=r.status_code))
        return False