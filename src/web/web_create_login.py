from urllib import urlopen


def html_users(users):
    return urlopen('web/html/html_login/login.html').read().encode('utf-8').format(users=_useritems(users))


def _useritems(data):
    STRhtml = ""
    STRhtml += '<div class="col-md-10 col-md-offset-1">'
    if data is None:
        STRhtml += '<p>No users are available on the server. Please continue as guest</p>'
        STRhtml += '<p>Users can be added within the settings pages</p>'
    else:
        STRhtml += '<form action="html_login">'
        x=0
        while x < len(data['users']):
            username = data['users'][str(x)]['name']
            STRhtml += urlopen('web/html/html_login/login_items.html').read().encode('utf-8').format(name=username)
            x += 1
        STRhtml += '<button class="btn btn-success btn-block" type="submit">Continue</button>'
        STRhtml += '</form>'
    STRhtml += '<button class="btn btn-default btn-block" onclick="window.location.href={guest}">Continue as guest</button>'.format(guest="'/web/login?user=Guest'")
    STRhtml += '</div>'
    return STRhtml