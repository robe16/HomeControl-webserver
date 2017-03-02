import cfg
from bottle import request, run, post, HTTPResponse

_cache = False

@post('/cache/<category>')
def post_cache(category):
    global _cache
    #
    try:
        #
        data = request.json
        #
        if category == 'setup' and data['category'] == 'setup':
            _cache['setup'] = data['cache']
        elif category == 'users' and data['category'] == 'users':
            _cache['users'] = data['cache']
        elif category == 'tvchannels' and data['category'] == 'tvchannels':
            _cache['tvchannels'] = data['cache']
        else:
            raise Exception
        #
        return HTTPResponse(status=200)
        #
    except Exception as e:
        return HTTPResponse(status=400)


def start_port_listener(cache):
    global _cache
    _cache = cache
    #
    run(host='0.0.0.0', port=cfg.self_port_cache, debug=True)