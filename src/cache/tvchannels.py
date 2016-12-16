def get_channels_in_category(data, category):
    try:
        for cat in data['channels']:
            if data['channels'][cat] == category:
                return data['channels'][cat]['channels']
    except Exception as e:
        print('ERROR - ' + str(e))
        pass
    return False


def get_channel_item(data, category, channel):
    try:
        channels = get_channels_in_category(data, category)
        if bool(channels):
            for chan in channels:
                if channels[chan]['name'] == channel:
                    return channels[chan]
    except Exception as e:
        print('ERROR - ' + str(e))
        pass
    return False


def get_channel_item_detail(data, category, channel, detail):
    try:
        item = get_channel_item(data, category, channel)
        if bool(item):
            return item[detail]
        return False
    except Exception as e:
        print('ERROR - ' + str(e))
        return False


def get_channel_item_type(data, category, channel):
    try:
        item = get_channel_item(data, category, channel)
        if bool(item):
            return item['type']
        return False
    except Exception as e:
        print('ERROR - ' + str(e))
        return False


def get_channel_item_listingsrc(data, category, channel, src):
    try:
        item = get_channel_item(data, category, channel)
        if bool(item):
            return item['listingsrc'][src]
        return False
    except Exception as e:
        print('ERROR - ' + str(e))
        return False


def get_channel_item_res_detail(data, category, channel, res, detail):
    try:
        item = get_channel_item(data, category, channel)
        if bool(item):
            return item[res][detail]
        return False
    except Exception as e:
        print('ERROR - ' + str(e))
        return False


def get_channel_item_res_logo(data, category, channel, res):
    try:
        item = get_channel_item(data, category, channel)
        if bool(item):
            return item[res]['logo']
        return False
    except Exception as e:
        print('ERROR - ' + str(e))
        return False


def get_channel_item_res_devicekey(data, category, channel, res, device_type):
    try:
        item = get_channel_item(data, category, channel)
        if bool(item):
            return item[res]['devicekeys'][device_type]
        return False
    except Exception as e:
        print('ERROR - ' + str(e))
        return False


def get_channel_item_res_freeview(data, category, channel, res):
    try:
        item = get_channel_item(data, category, channel)
        if bool(item):
            return item[res]['freeview']
        return False
    except Exception as e:
        print('ERROR - ' + str(e))
        return False


def get_channel_item_res_package(data, category, channel, res, package_name):
    try:
        item = get_channel_item(data, category, channel)
        if bool(item):
            return item[res][package_name]
        return False
    except Exception as e:
        print('ERROR - ' + str(e))
        return False


def get_channel_detail_from_devicekey(data, device_type, channo, detail=''):
    #
    res_list = ['sd', 'hd']
    #
    catCount = 0
    while catCount < len(data['channels']):
        #
        chanCount = 0
        while chanCount < len(data['channels'][str(catCount)]['channels']):
            #
            for res in res_list:
                #
                try:
                    if data['channels'][str(catCount)]['channels'][str(chanCount)][res]['devicekeys'][device_type] == channo:
                        #
                        if detail == 'name' or detail == 'type':
                            return data['channels'][str(catCount)]['channels'][str(chanCount)][detail]
                        elif detail=='logo' or detail == 'freeview' or detail == 'virginmedia_package':
                            return data['channels'][str(catCount)]['channels'][str(chanCount)][res][detail]
                        else:
                            return data['channels'][str(catCount)]['channels'][str(chanCount)]
                        #
                except Exception as e:
                    pass
                #
            #
            chanCount += 1
        #
        catCount += 1
    #
    return False


def get_channel_name_from_devicekey(data, device_type, channo):
    try:
        #
        return  get_channel_detail_from_devicekey(data, device_type, channo, detail='name')
    except Exception as e:
        return ''


def get_channel_logo_from_devicekey(data, device_type, channo):
    try:
        #
        return get_channel_detail_from_devicekey(data, device_type, channo, detail='logo')
    except Exception as e:
        return ''
