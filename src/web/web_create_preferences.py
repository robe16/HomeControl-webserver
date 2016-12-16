from urllib import urlopen
from web_menu import html_menu
from web_preferences import _preference_tvguide


def create_preference_tvguide(user):
    body = _preference_tvguide(user)
    #
    return urlopen('web/html/header.html').read().encode('utf-8').format(title='User Preferences: TV Guide') +\
           html_menu(user) +\
           urlopen('web/html/body.html').read().encode('utf-8').format(header='User Preferences: TV Guide', body=body) +\
           urlopen('web/html/message_popup.html').read().encode('utf-8') +\
           urlopen('web/html/footer.html').read().encode('utf-8')