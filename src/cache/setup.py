import sys
import urllib

################################################################################################
# Return count of groups, Things and info_services
################################################################################################


def get_cfg_count_groups(data):
    #
    return len(data['bindings']['groups'])


def get_cfg_count_things(data, group_seq):
    #
    for group in data['bindings']['groups']:
        if group['sequence'] == group_seq:
            return len(group['things'])
    #
    return False


def get_cfg_count_info(data):
    #
    return len(data['bindings']['info_services'])


# ----------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------
# STRUCTURE
# ----------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------


################################################################################################
# Return structure properties
################################################################################################


def get_cfg_structure_postcode(data):
    #
    return get_cfg_structure_value(data, 'structure_postcode')


def get_cfg_structure_town(data):
    #
    return get_cfg_structure_value(data, 'structure_town')


# ----------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------
# THINGS
# ----------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------


################################################################################################
# Return sequence for group and Thing from name
################################################################################################


def get_cfg_group_seq(data, group_name):
    #
    for group in data['bindings']['groups']:
        if group['name'].lower() == group_name.lower():
            return group['sequence']
    #
    raise Exception


def get_cfg_thing_seq(data, group_name, thing_name):
    #
    for group in data['bindings']['groups']:
        if group['name'].lower() == group_name.lower():
            for thing in group['things']:
                if thing['name'].lower() == thing_name.lower():
                    return thing['sequence']
    #
    raise Exception


################################################################################################
# Return name of group and Thing
################################################################################################


def get_cfg_group_name(data, group_seq):
    return get_cfg_group_value(data, group_seq, 'name')


def get_cfg_thing_name(data, group_seq, thing_seq):
    return get_cfg_thing_value(data, group_seq, thing_seq, 'name')

################################################################################################
# Return type of Thing
################################################################################################

def get_cfg_thing_type(data, group_seq, thing_seq):
    return get_cfg_thing_value(data, group_seq, thing_seq, 'type')

################################################################################################
# Return public detail value of Thing
################################################################################################


def get_cfg_thing_detail_public(data, group_seq, thing_seq, detail):
    return get_cfg_thing_detail(data, group_seq, thing_seq, 'details_public', detail)


def get_cfg_thing_detail(data, group_seq, thing_seq, privpub, detail):
    #
    details = get_cfg_thing_value(data, group_seq, thing_seq, privpub)
    #
    return details[detail]


# ----------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------
# INFO_SERVICE
# ----------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------


################################################################################################
# Return sequence for info_service from name
################################################################################################


def get_cfg_info_seq(data, info_name):
    #
    for info in data['bindings']['info_services']:
        if info['name'].lower() == info_name.lower():
            return info['sequence']
    #
    raise Exception


################################################################################################
# Return name and type of info_service
################################################################################################


def get_cfg_info_name(data, info_seq):
    return get_cfg_info_value(data, info_seq, 'name')


def get_cfg_info_type(data, info_seq):
    return get_cfg_info_value(data, info_seq, 'type')

################################################################################################
# Return private/public detail info_service of info_service
################################################################################################


def get_cfg_info_detail_public(data, info_seq, detail):
    return get_cfg_info_detail(data, info_seq, 'details_public', detail)


def get_cfg_info_detail(data, info_seq, privpub, detail):
    #
    details = get_cfg_info_value(data, info_seq, privpub)
    #
    return details[detail]


# ----------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------


################################################################################################
# Return value for structure, group, Thing and info_service
# (used as 'master' code for returning name, type, details etc. in above defs)
################################################################################################


def get_cfg_structure_value(data, key):
    #
    return data['structure'][key]


def get_cfg_group_value(data, group_seq, key):
    #
    for group in data['bindings']['groups']:
        if group['sequence'] == group_seq:
            return group[key]
    #
    raise Exception('Requested group not found in config file')


def get_cfg_thing_value(data, group_seq, thing_seq, key):
    #
    for group in data['bindings']['groups']:
        if group['sequence'] == group_seq:
            for thing in group['things']:
                if thing['sequence'] == thing_seq:
                    return thing[key]
    #
    raise Exception('Requested thing not found in config file')


def get_cfg_info_value(data, info_seq, key):
    #
    for info in data['bindings']['info_services']:
        if info['sequence'] == info_seq:
            return info[key]
    #
    raise Exception('Requested info_service not found in config file')

################################################################################################
################################################################################################

def cfg_urlencode(text):
    try:
        if (sys.version_info > (3, 0)):
            # Python 3 code in this block
            return urllib.parse.quote(text).lower()
        else:
            # Python 2 code in this block
            return urllib.quote(text).lower()
    except Exception as e:
        return text.replace(' ', '').lower()


def cfg_urldecode(text):
    try:
        if (sys.version_info > (3, 0)):
            # Python 3 code in this block
            return urllib.parse.unquote(text)
        else:
            # Python 2 code in this block
            return urllib.unquote(text)
    except Exception as e:
        raise Exception