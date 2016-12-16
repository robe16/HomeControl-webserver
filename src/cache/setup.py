################################################################################################
# Return count of rooms, devices and accounts
################################################################################################


def get_cfg_count_rooms(data):
    return len(data['structure']['rooms'])


def get_cfg_count_devices(data, room_id):
    return len(data['structure']['rooms'][room_id]['devices'])


def get_cfg_count_accounts(data):
    return len(data['structure']['accounts'])

################################################################################################
# Return list of room, device and account ids
################################################################################################


def get_cfg_idlist_rooms(data):
    #
    r_list = []
    #
    for key, value in data['structure']['rooms'].iteritems():
        r_list.append(key)
    #
    return r_list


def get_cfg_idlist_devices(data, room_id):
    #
    d_list = []
    #
    for key, value in data['structure']['rooms'][room_id]['devices'].iteritems():
        d_list.append(key)
    #
    return d_list


def get_cfg_idlist_accounts(data):
    #
    a_list = []
    #
    for key, value in data['structure']['accounts'].iteritems():
        a_list.append(key)
    #
    return a_list

################################################################################################
# Return number/index for room, device and account
################################################################################################


def get_cfg_room_index(data, room_id):
    #
    count = 0
    #
    for key, value in data['structure']['rooms'].iteritems():
        if key == room_id:
            return count
        count += 1
    #
    return -1


def get_cfg_device_index(data, room_id, device_id):
    #
    count = 0
    #
    for key, value in data['structure']['rooms'][room_id]['devices'].iteritems():
        if key == device_id:
            return count
        count += 1
    #
    return -1


def get_cfg_account_index(data, account_id):
    #
    count = 0
    #
    for key, value in data['structure']['accounts'].iteritems():
        if key == account_id:
            return count
        count += 1
    #
    return -1

################################################################################################
# Return structure properties
################################################################################################


def get_cfg_structure_postcode(data):
    #
    return get_cfg_structure_value(data, 'structure_postcode')


def get_cfg_structure_town(data):
    #
    return get_cfg_structure_value(data, 'structure_town')

################################################################################################
# Return name of room, device and account
################################################################################################


def get_cfg_room_name(data, room_id):
    #
    return get_cfg_room_value(data, room_id, 'room_name')


def get_cfg_device_name(data, room_id, device_id):
    #
    return get_cfg_device_value(data, room_id, device_id, 'device_name')


def get_cfg_account_name(data, account_id):
    #
    return get_cfg_account_value(data, account_id, 'account_name')

################################################################################################
# Return type of device and account
################################################################################################


def get_cfg_device_type(data, room_id, device_id):
    #
    return get_cfg_device_value(data, room_id, device_id, 'device_type')


def get_cfg_account_type(data, account_id):
    #
    return get_cfg_account_value(data, account_id, 'account_type')

################################################################################################
# Return private detail value of device and account
################################################################################################


def get_cfg_device_detail(data, room_id, device_id, detail):
    #
    details = get_cfg_device_value(data, room_id, device_id, 'details')
    #
    return details[detail]


def get_cfg_account_detail(data, account_id, detail):
    #
    details = get_cfg_account_value(data, account_id, 'details')
    #
    return details[detail]

################################################################################################
# Return public detail value of device and account
################################################################################################


def get_cfg_device_detail_public(data, room_id, device_id, detail):
    #
    details = get_cfg_device_value(data, room_id, device_id, 'details_public')
    #
    return details[detail]


def get_cfg_account_detail_public(data, account_id, detail):
    #
    details = get_cfg_account_value(data, account_id, 'details_public')
    #
    return details[detail]

################################################################################################
# Return value for structure room, device and account
# (used as 'master' code for returning name, type, etc. in above defs)
################################################################################################


def get_cfg_structure_value(data, key):
    #
    return data['structure'][key]


def get_cfg_room_value(data, room_id, key):
    #
    return data['structure']['rooms'][room_id][key]


def get_cfg_device_value(data, room_id, device_id, key):
    #
    return data['structure']['rooms'][room_id]['devices'][device_id][key]


def get_cfg_account_value(data, account_id, key):
    #
    return data['structure']['accounts'][account_id][key]

################################################################################################
################################################################################################