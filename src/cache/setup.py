################################################################################################
# Return count of groups and devices
################################################################################################


def get_cfg_count_groups(data):
    return len(data['groups'])


def get_cfg_count_devices(data, group_id):
    return len(data['groups'][group_id]['devices'])

################################################################################################
# Return list of group and device ids
################################################################################################


def get_cfg_idlist_groups(data):
    #
    r_list = []
    #
    for key, value in data['groups'].iteritems():
        r_list.append(key)
    #
    return r_list


def get_cfg_idlist_devices(data, group_id):
    #
    d_list = []
    #
    for key, value in data['groups'][group_id]['devices'].iteritems():
        d_list.append(key)
    #
    return d_list

################################################################################################
# Return number/index for group and device
################################################################################################


def get_cfg_group_index(data, group_id):
    #
    count = 0
    #
    for key, value in data['groups'].iteritems():
        if key == group_id:
            return count
        count += 1
    #
    return -1


def get_cfg_device_index(data, group_id, device_id):
    #
    count = 0
    #
    for key, value in data['groups'][group_id]['devices'].iteritems():
        if key == device_id:
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
# Return name of group and device
################################################################################################


def get_cfg_group_name(data, group_id):
    #
    return get_cfg_group_value(data, group_id, 'group_name')


def get_cfg_device_name(data, group_id, device_id):
    #
    return get_cfg_device_value(data, group_id, device_id, 'device_name')

################################################################################################
# Return type of device
################################################################################################


def get_cfg_device_type(data, group_id, device_id):
    #
    return get_cfg_device_value(data, group_id, device_id, 'device_type')

################################################################################################
# Return private detail value of device
################################################################################################


def get_cfg_device_detail(data, group_id, device_id, detail):
    #
    details = get_cfg_device_value(data, group_id, device_id, 'details')
    #
    return details[detail]

################################################################################################
# Return public detail value of device
################################################################################################


def get_cfg_device_detail_public(data, group_id, device_id, detail):
    #
    details = get_cfg_device_value(data, group_id, device_id, 'details_public')
    #
    return details[detail]

################################################################################################
# Return value for structure group and device
# (used as 'master' code for returning name, type, etc. in above defs)
################################################################################################


def get_cfg_structure_value(data, key):
    #
    return data['structure'][key]


def get_cfg_group_value(data, group_id, key):
    #
    return data['groups'][group_id][key]


def get_cfg_device_value(data, group_id, device_id, key):
    #
    return data['groups'][group_id]['devices'][device_id][key]

################################################################################################
################################################################################################