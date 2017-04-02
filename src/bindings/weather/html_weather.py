import datetime
import requests
import ast
from urllib import urlopen
from cfg import server_url
from cache.setup import cfg_urlencode, get_cfg_info_name
from log.console_messages import print_msg, print_error
from weather_lists import *

def weather_body(_cache, info_seq):
    #
    forecast = request_weather(_cache, info_seq)
    #
    if not str(forecast)=='False':
        args = {'timestamp': datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
                'town': forecast['location']['name'],
                'county': forecast['location']['unitaryAuthArea'],
                'body_weather_days': _create_html(forecast)}
    else:
        args = {'timestamp': datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
                'town': '-',
                'county': '-',
                'body_weather_days': ''}
    #
    return urlopen('bindings/weather/weather_main.html').read().encode('utf-8').format(**args)


def request_weather(_cache, info_seq):
    url = server_url('data/info/{info}/forecast'.format(info=cfg_urlencode(get_cfg_info_name(_cache, info_seq))))
    r = requests.get(url)
    #
    if r.status_code == requests.codes.ok:
        print_msg('Weather info retrieved successfully - {status_code}'.format(status_code=r.status_code))
        data = r.content
        return ast.literal_eval(data)
    else:
        print_error('Weather info failed to be retrieved - {status_code}'.format(status_code=r.status_code))
        return False

def _create_html(forecast):
    #
    html = ''
    #
    days_count = 0
    #
    while days_count < len(forecast['days']):
        #
        day_item = forecast['days'][str(days_count)]
        daytime = day_item['daytime']
        nighttime = day_item['nighttime']
        hourly = day_item['3hourly']
        #
        date = datetime.datetime.strptime(day_item['date'], "%Y-%m-%d")
        #
        date_name = date.strftime('%A')
        date_label = date.strftime('%d/%m')
        #
        time_sunrise = datetime.datetime.strptime(day_item['sunRiseSet']['sunrise'], "%Y-%m-%d %H:%M:%S").strftime('%H:%M')
        time_sunset = datetime.datetime.strptime(day_item['sunRiseSet']['sunset'], "%Y-%m-%d %H:%M:%S").strftime('%H:%M')
        #
        if date_label == datetime.date.today().strftime('%d/%m'):
            date_label = 'Today'
        elif date_label == (datetime.date.today() + datetime.timedelta(days=1)).strftime('%d/%m'):
            date_label = 'Tomorrow'
        #
        html_hrs = ''
        hours_count = 0
        #
        while hours_count < len(hourly):
            #
            hour_item = hourly[str(hours_count)]
            #
            args_hours = {'time': hour_item['time'],
                          'weather_type_glyph': getWeatherType_glyph(hour_item['weather_type']),
                          'temp': hour_item['temp'],
                          'temp_unit': forecast['units']['3hourly']['temp'],
                          'precipitation_prob': hour_item['precipitation_prob']}
            #
            html_hrs += urlopen('bindings/weather/weather_hour_item.html').read().encode('utf-8').format(
                **args_hours)
            #
            hours_count += 1
        #
        args_item = {'date_day': date_name,
                     'date': date_label,
                     'time_sunrise': time_sunrise,
                     'time_sunset': time_sunset,
                     'd_weather_type_glyph': getWeatherType_glyph(daytime['weather_type']),
                     'd_temp': daytime['temp'],
                     'd_temp_unit': forecast['units']['daily']['temp'],
                     'd_weather_direction_glyph': getWind_glyphCardinalFrom(daytime['wind_direction']),
                     'd_wind_direction': daytime['wind_direction'],
                     'd_wind_speed': daytime['wind_speed'],
                     'd_wind_speed_unit': forecast['units']['daily']['wind_speed'],
                     'd_visibility': daytime['visibility'],
                     'd_precipitation_prob': daytime['precipitation_prob'],
                     'd_uv_index': daytime['uv_index'],
                     'n_weather_type_glyph': getWeatherType_glyph(nighttime['weather_type']),
                     'n_temp': nighttime['temp'],
                     'n_temp_unit': forecast['units']['daily']['temp'],
                     'n_weather_direction_glyph': getWind_glyphCardinalFrom(nighttime['wind_direction']),
                     'n_wind_direction': nighttime['wind_direction'],
                     'n_wind_speed': nighttime['wind_speed'],
                     'n_wind_speed_unit': forecast['units']['daily']['wind_speed'],
                     'n_visibility': nighttime['visibility'],
                     'n_precipitation_prob': nighttime['precipitation_prob'],
                     'hour_weather': html_hrs}
        #
        days_count += 1
        #
        html += urlopen('bindings/weather/weather_day_item.html').read().encode('utf-8').format(
            **args_item)
        #
    return html


# def convert_TempToHue(self, temp):
#     # temp_colour is the 'h' in hsl based colour
#     return 30 + 240 * (30 - int(temp)) / 60