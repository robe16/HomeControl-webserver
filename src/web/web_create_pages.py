from urllib import urlopen

from web_create_login import html_users
from web_menu import html_menu
# from web_tvlistings import html_listings_user_and_all


def create_login(_cache):
    return urlopen('web/html/header.html').read().encode('utf-8').format(title='Login') +\
           html_users(_cache['users']) +\
           urlopen('web/html/footer.html').read().encode('utf-8')


def create_page(user, _cache, page_body, browser_title, page_title):
    return urlopen('web/html/header.html').read().encode('utf-8').format(title=browser_title) +\
           html_menu(user, _cache) +\
           urlopen('web/html/body.html').read().encode('utf-8').format(header=page_title, body=page_body) +\
           urlopen('web/html/footer.html').read().encode('utf-8')


def create_home(user, _cache):
    return create_page(user,
                       _cache,
                       urlopen('web/html/index.html').read().encode('utf-8'),
                       'Home',
                       '')


def create_about(user, _cache):
    return create_page(user,
                       _cache,
                       urlopen('web/html/about.html').read().encode('utf-8'),
                       'About',
                       'About')


def create_page_body(user, _cache, body_html, browser_title, page_title):
    return create_page(user,
                       _cache,
                       body_html,
                       browser_title,
                       page_title)