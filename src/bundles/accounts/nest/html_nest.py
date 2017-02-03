import datetime
import ast
from urllib import urlopen
import requests
from cfg import server_url
from log.console_messages import print_error
from lists.devices.list_devices import get_device_html_command, get_device_detail


_temp_unit = 'c'

def html_nest(account_id, query_dict):
    #
    body = _htmlbody(account_id)
    #
    script = ("\r\n<script>\r\n" +
              "setTimeout(function () {\r\n" +
              "updateNest('/web/account/" + account_id + "?body=true');\r\n" +
              "}, 30000);\r\n" +
              "</script>\r\n")
    #
    timestamp = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    #
    args_body = {'timestamp': timestamp,
                 'body_nest_therm': body['nest_therm'],
                 'body_nest_protect': body['nest_protect'],
                 'body_nest_cam': body['nest_cam']}
    #
    html_body = urlopen('web/html/html_devices/' + get_device_detail('nest_account', 'html_command_body')).read().encode('utf-8').format(**args_body)
    #
    if len(query_dict) > 0:
        if query_dict['body']:
            return html_body
    #
    args_html = {'script': script,
                 'nest_body': html_body}
    #
    return urlopen('web/html/html_devices/' + get_device_html_command('nest_account')).read().encode('utf-8').format(**args_html)


def _htmlbody(account_id):
    #
    devices_therm_html = ''
    devices_protect_html = ''
    devices_cam_html = ''
    #
    try:
        json_devices = _get_nest_data(account_id)
        json_devices = json_devices['devices']
        #
        if not json_devices:
            print_error('Nest devices could not retrieved from Nest server', dvc_or_acc_id=account_id)
            return False
        #
        # Thermostats
        #
        devices_therm_html = '<div class="row">'
        #
        html_therm = get_device_detail('nest_account', 'html_therm')
        #
        if html_therm:
            #
            try:
                therm_ids = json_devices['thermostats'].keys()
            except Exception as e:
                therm_ids = False
            #
            if bool(therm_ids):
                count = 0
                for therm in therm_ids:
                    if count> 0 and count % 4 == 0:
                        devices_therm_html += '</div><div class="row">'
                    #
                    colwidth = '3'
                    rem = len(therm_ids) - count
                    if rem == 1:
                        colwidth = '12'
                    elif rem == 2:
                        colwidth = '6'
                    elif rem == 3:
                        colwidth = '4'
                    #
                    nest_device_id = json_devices['thermostats'][therm]['device_id']
                    therm_name = json_devices['thermostats'][therm]['name']
                    #
                    if json_devices['thermostats'][therm]['is_online']:
                        #
                        is_online = 'online'
                        #
                        therm_hvac_state = json_devices['thermostats'][therm]['hvac_state']
                        if therm_hvac_state == 'heating':
                            temp_hvac_statement = 'Heating to'
                        elif therm_hvac_state =='cooling':
                            temp_hvac_statement = 'Cooling to'
                        else:
                            temp_hvac_statement = 'Heat set to'
                        #
                        temp_unit_html = '&#8451;' if _temp_unit == 'c' else '&#8457'
                        therm_temp_target = json_devices['thermostats'][therm]['target_temperature_{unit}'.format(unit=_temp_unit)]
                        therm_temp_ambient = json_devices['thermostats'][therm]['ambient_temperature_{unit}'.format(unit=_temp_unit)]
                        #
                        therm_label = 'Current: '
                        #
                        new_temp_up = therm_temp_target + 0.5
                        new_temp_down = therm_temp_target - 0.5
                        #
                        therm_leaf = json_devices['thermostats'][therm]['has_leaf']
                        #
                    else:
                        #
                        is_online = 'offline'
                        therm_hvac_state = 'offline'
                        temp_hvac_statement = ''
                        temp_unit_html = ''
                        therm_label = 'Offline'
                        therm_temp_target = ''
                        therm_temp_ambient = ''
                        therm_leaf = 'false'
                        new_temp_up = ''
                        new_temp_down = ''
                        #
                    #
                    temp_therm_html = urlopen('web/html/html_devices/{html_therm}'.format(html_therm=html_therm))\
                        .read().encode('utf-8').format(colwidth=colwidth,
                                                       account_id=account_id,
                                                       nest_device_id=nest_device_id,
                                                       name=therm_name,
                                                       therm_label=therm_label,
                                                       is_online=is_online,
                                                       temp_hvac=temp_hvac_statement,
                                                       temp_target=therm_temp_target,
                                                       temp_ambient=therm_temp_ambient,
                                                       temp_unit=temp_unit_html,
                                                       has_leaf=str(therm_leaf).lower(),
                                                       hvac=therm_hvac_state,
                                                       new_temp_up=new_temp_up,
                                                       new_temp_down=new_temp_down)
                    #
                    if _temp_unit == 'c':
                        #
                        _str_to_replace = 'tick-target temp-tick-c-{temp}'.format(temp=therm_temp_target)
                        temp_therm_html = temp_therm_html.replace(_str_to_replace,
                                                                  'tick-target tick-target-active')
                        #
                        if therm_hvac_state == 'heating' or therm_hvac_state =='cooling':
                            _str_to_replace = 'tick-ambient temp-tick-c-{temp}'.format(temp=therm_temp_ambient)
                            if therm_temp_ambient < therm_temp_target:
                                _col = 'blue'
                            else:
                                _col = 'red'
                            temp_therm_html = temp_therm_html.replace(_str_to_replace,
                                                                      'tick-ambient tick-ambient-active tick-ambient-active-{col}'.format(col=_col))
                    #
                    devices_therm_html += temp_therm_html
                    #
                    count += 1
                    #
        #
        devices_therm_html += '</div>'
        #
        # Smoke and CO detectors
        #
        devices_protect_html = '<div class="row">'
        #
        html_smoke = get_device_detail('nest_account', 'html_smoke')
        #
        if html_smoke:
            #
            try:
                smoke_ids = json_devices['smoke_co_alarms'].keys()
            except Exception as e:
                smoke_ids = False
            #
            if bool(smoke_ids):
                count = 0
                for smoke in smoke_ids:
                    if count> 0 and count % 4 == 0:
                        devices_protect_html += '</div><div class="row">'
                    #
                    colwidth = '3'
                    rem = len(smoke_ids) - count
                    if rem == 1:
                        colwidth = '12'
                    elif rem == 2:
                        colwidth = '6'
                    elif rem == 3:
                        colwidth = '4'
                    #
                    nest_device_id = json_devices['smoke_co_alarms'][smoke]['device_id']
                    smoke_name = json_devices['smoke_co_alarms'][smoke]['name']
                    #
                    if json_devices['smoke_co_alarms'][smoke]['is_online']:
                        #
                        smoke_online = 'online'
                        #
                        battery_health = json_devices['smoke_co_alarms'][smoke]['battery_health']
                        # ok / replace
                        #
                        co_alarm_state = json_devices['smoke_co_alarms'][smoke]['co_alarm_state']
                        # ok / warning / emergency
                        #
                        smoke_alarm_state = json_devices['smoke_co_alarms'][smoke]['smoke_alarm_state']
                        # ok / warning / emergency
                        #
                        ui_color_state = json_devices['smoke_co_alarms'][smoke]['ui_color_state']
                        # gray / green / yellow / red
                        #
                    else:
                        #
                        smoke_online = 'offline'
                        battery_health = ''
                        co_alarm_state = ''
                        smoke_alarm_state = ''
                        ui_color_state = ''
                        #
                    #
                    devices_protect_html += urlopen('web/html/html_devices/{html_smoke}'.format(html_smoke=html_smoke))\
                        .read().encode('utf-8').format(colwidth=colwidth,
                                                       account_id=account_id,
                                                       nest_device_id=nest_device_id,
                                                       name=smoke_name,
                                                       online=smoke_online,
                                                       ui_color_state=ui_color_state,
                                                       battery_health=battery_health,
                                                       co_alarm_state=co_alarm_state,
                                                       smoke_alarm_state=smoke_alarm_state)
                    #
                    count += 1
                    #
        #
        devices_protect_html += '</div>'
        #
        # Cameras
        #
        devices_cam_html = '<div class="row">'
        #
        html_cam = get_device_detail('nest_account', 'html_cam')
        #
        if html_cam:
            #
            try:
                cam_ids = json_devices['cameras'].keys()
            except Exception as e:
                cam_ids = False
            #
            if bool(cam_ids):
                count = 0
                for cam in cam_ids:
                    if count> 0 and count % 4 == 0:
                        devices_cam_html += '</div><div class="row">'
                    #
                    colwidth = '3'
                    rem = len(cam_ids) - count
                    if rem == 1:
                        colwidth = '12'
                    elif rem == 2:
                        colwidth = '6'
                    elif rem == 3:
                        colwidth = '4'
                    #
                    nest_device_id = json_devices['cameras'][cam]['device_id']
                    cam_name = json_devices['cameras'][cam]['name']
                    #
                    if json_devices['cameras'][cam]['is_online']:
                        #
                        cam_online = 'Online'
                        img_color = 'blue'
                        #
                        cam_streaming = json_devices['cameras'][cam]['is_streaming']
                        #
                    else:
                        #
                        cam_online = 'Offline'
                        img_color = 'gray'
                        cam_streaming = ''
                        #
                    #
                    devices_cam_html += urlopen('web/html/html_devices/{html_cam}'.format(html_cam=html_cam))\
                        .read().encode('utf-8').format(colwidth=colwidth,
                                                       account_id=account_id,
                                                       nest_device_id=nest_device_id,
                                                       name=cam_name,
                                                       color=img_color,
                                                       online=cam_online)
                    #
                    count += 1
                    #
        #
        devices_cam_html += '</div>'
        #
    except Exception as e:
        print_error('Nest devices could not be compiled into html - ' + str(e), dvc_or_acc_id=account_id)
    #
    return {'nest_therm': devices_therm_html,
            'nest_protect': devices_protect_html,
            'nest_cam': devices_cam_html}


def _get_nest_data(account_id):
    data = _getData(account_id, 'data')
    if data:
        return ast.literal_eval(data)
    else:
        return False


def _getData(account_id, datarequest):
    r = requests.get(server_url('data/account/{account_id}/{datarequest}'.format(account_id=account_id,
                                                                                 datarequest=datarequest)))
    if r.status_code == requests.codes.ok:
        return r.content
    else:
        print_error('Nest Account - Attempted to request {data} from server - {status}'.format(data=datarequest,
                                                                                               status=r.status_code))
        return False