import requests
import ast
from urllib import urlopen
from src.cfg import server_url
from src.lists.devices.list_devices import get_device_html_command
from src.log.console_messages import print_error


def html_tv_lg_netcast(room_id, device_id):
    #
    args = {'room_id': room_id,
            'device_id': device_id,
            'apps': _html_apps(room_id, device_id)}
    #
    return urlopen('web/html/html_devices/' + get_device_html_command('tv_lg_netcast')).read().encode('utf-8').format(**args)


def _html_apps(room_id, device_id):
    #
    try:
        json_applist = _get_applist(room_id, device_id)
        #
        html = '<table style="width:100%">' +\
               '<tr style="height:80px; padding-bottom:2px; padding-top:2px">'
        #
        count = 1
        for app in json_applist:
            try:
                #
                html += ('<td class="grid_item" style="width: 20%; cursor: pointer; vertical-align: top;" align="center" onclick="sendHttp(\'/command/{room_id}/{device_id}?command=app&auid={auid}&name={app_name}\', null, \'GET\', false, true)">' +
                         '<img src="/command/device/{room_id}/{device_id}?command=image&auid={auid}&name={app_name}" style="height:50px;"/>' +
                         '<p style="text-align:center; font-size: 13px;">{name}</p>' +
                         '</td>').format(room_id=room_id,
                                         device_id=device_id,
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


def _get_applist(room_id, device_id):
    data = _getData(room_id, device_id, 'applist')
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
        print_error('LG TV - Attempted to request {data} from server - {status}'.format(data=datarequest,
                                                                                        status=r.status_code))
        return False