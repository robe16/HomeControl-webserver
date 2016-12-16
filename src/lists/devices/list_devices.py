import json
import os


def read_list_devices():
    with open(os.path.join('lists', 'list_device_types.json'), 'r') as data_file:
        data = json.load(data_file)
        data_file.close()
    if isinstance(data, dict):
        return data
    else:
        return False


def _get_device_details(type):
    data = read_list_devices()
    try:
        return data[type]
    except:
        return False


def get_device_name(type):
    item = _get_device_details(type)
    if item:
        return item['name']
    return False


def get_device_html_command(type):
    item = _get_device_details(type)
    if item:
        return item['html_command']
    return False


def get_device_detail(type, key):
    item = _get_device_details(type)
    if item:
        return item[key]
    return False