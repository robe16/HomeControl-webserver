import datetime
import requests
import ast
from urllib import urlopen
from cfg import server_url
from log.console_messages import print_msg, print_error
from cache.users import get_usernews
from cache.setup import cfg_urlencode, get_cfg_info_name

def news_body(user, _cache, info_seq):
    #
    try:
        news = request_news(user, _cache, info_seq)
        args = {'timestamp': datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
                'body_news_articles': _create_html(news)}
    except Exception as e:
        args = {'timestamp': datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
                'body_news_articles': ''}
    #
    return urlopen('bindings/news/news_main.html').read().encode('utf-8').format(**args)


def request_news(user, _cache, info_seq):
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
    url = server_url('data/info/{info}/articles?sources={sources}&sortby={sortby}'.format(info=cfg_urlencode(get_cfg_info_name(_cache['setup'], info_seq)),
                                                                                          sources=user_sources,
                                                                                          sortby='latest'))
    r = requests.get(url)
    #
    if r.status_code == requests.codes.ok:
        print_msg('News articles retrieved successfully - {status_code}'.format(status_code=r.status_code))
        return r.json()
    else:
        print_error('News articles failed to be retrieved - {status_code}'.format(status_code=r.status_code))
        raise Exception


def _create_html(news):
    #
    html = ''
    dict_html = {}
    #
    for k, v in news['news_articles'].items():
        #
        for article in news['news_articles'][k]['articles']:
            #
            try:
                #
                if article['description'] is None or article['description'] is None:
                    raise Exception
                #
                if not article['publishedAt'] is None:
                    #
                    try:
                        publish_datetime = datetime.datetime.strptime(article['publishedAt'], "%Y-%m-%dT%H:%M:%Sz")
                    except:
                         pass
                    #
                    try:
                        publish_datetime = datetime.datetime.strptime(article['publishedAt'], "%Y-%m-%dT%H:%M:%Sz.%f")
                    except:
                         pass
                    #
                    try:
                        publish_string = publish_datetime.strftime('%d-%m-%Y %H:%M')
                    except:
                        publish_datetime = datetime.datetime.now()
                        publish_string = '-'
                    #
                else:
                    publish_datetime = datetime.datetime.now()
                    publish_string = '-'
                #
                if article['urlToImage']:
                    image_url = article['urlToImage'].encode('utf-8')
                else:
                    image_url = ''
                #
                args_item = {'source_name': news['news_articles'][k]['source_details']['name'],
                             'source_logo': news['news_articles'][k]['source_details']['logos']['small'],
                             'article_link': article['url'].encode('utf-8'),
                             'article_title': article['title'].encode('utf-8'),
                             'article_description': article['description'].encode('utf-8'),
                             'article_date': publish_string,
                             'article_image': image_url}
                #
                dict_html[publish_datetime] = urlopen('bindings/news/news_article_item.html').read().encode('utf-8').format(**args_item)
            except Exception as e:
                pass
    #
    for html_key in sorted(dict_html.keys(), reverse=True):
        html += dict_html[html_key]
    #
    return html


def removeUnicodeChars(text):
    text = text.replace('\\u2019', '\'')
    text = text.replace('\u2019', '\'')
    return text