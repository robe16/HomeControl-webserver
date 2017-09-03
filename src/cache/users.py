import requests

def check_user(data, user):
    if data != None:
        for id in data['users']:
            if data['users'][id]['name']==user:
                return True
    return False


def check_userpin(server_url, user, pin):
    #
    try:
        #
        payload = {'user': user,
                   'pin': pin}
        #
        r = requests.post('{url}/{uri}'.format(url=server_url, uri='user/pin'), data=payload)
        #
        if r.status_code == requests.codes.ok:
            return True
        else:
            return False
            #
    except:
        return False


def get_usernames(data):
    if data != None:
        LSTnames = []
        for id in data['users']:
            LSTnames.append(data["users"][id]["name"])
        return LSTnames
    return None


def get_userchannels(data, user):
    if data != None:
        for id in data['users']:
            if data['users'][id]['name']==user:
                return data['users'][id]['tvchannels']
    return None


def get_usernews(data, user):
    if data != None:
        for id in data['users']:
            if data['users'][id]['name']==user:
                return data['users'][id]['news_sources']
    return None


def get_userrole(data, user):
    if data != None:
        for id in data['users']:
            if data['users'][id]['name']==user:
                return data['users'][id]['role']
    return None


def get_userimage(data, user):
    if data != None:
        for id in data['users']:
            if data['users'][id]['name']==user:
                if data['users'][id]['image'] != "":
                    return data['users'][id]['image']
    return "default.png"