import datetime
import requests
import ast
from urllib import urlopen
from cfg import server_url
from log.console_messages import print_msg, print_error
from cache.users import get_usernews

def news_body(user, _cache):
    #
    news = request_news(user, _cache)
    #
    if not str(news)=='False':
        args = {'timestamp': datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
                'body_news_articles': _create_html(news)}
    else:
        args = {'timestamp': datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
                'body_news_articles': ''}
    #
    return urlopen('web/html/html_info_services/news_main.html').read().encode('utf-8').format(**args)


def request_news(user, _cache):
    #
    if user:
        cache_users = _cache['users']
        tmp_user_sources = get_usernews(cache_users, user)
    else:
        tmp_user_sources = ''
    #
    user_sources = ''
    for user_src in tmp_user_sources:
        if not user_sources == '':
            user_sources += ' '
        user_sources += user_src
    #
    url = server_url('data/info/news/articles?sources={sources}&sortby={sortby}'.format(sources=user_sources,
                                                                                        sortby='latest'))
    r = requests.get(url)
    #
    if r.status_code == requests.codes.ok:
        print_msg('News articles retrieved successfully - {status_code}'.format(status_code=r.status_code))
        data = r.content
        return ast.literal_eval(data)
    else:
        print_error('News articles failed to be retrieved - {status_code}'.format(status_code=r.status_code))
        return False


def _create_html(news):
    #
    html = ''
    #
    for k, v in news['news_articles'].items():
        #
        for article in news['news_articles'][k]['articles']:
            #TODO: put in chronoclogical order first then re-run through temp created list and build html
            args_item = {'source_name': news['news_articles'][k]['source_details']['name'],
                         'source_logo': news['news_articles'][k]['source_details']['logos']['small'],
                         'article_link': article['url'],
                         'article_title': removeUnicodeChars(article['title']),
                         'article_description': removeUnicodeChars(article['description'])}
            #
            html += urlopen('web/html/html_info_services/news_article_item.html').read().encode('utf-8').format(**args_item)
        #
    return html


def removeUnicodeChars(text):
    text = text.replace('\u2019', '\'')
    return text