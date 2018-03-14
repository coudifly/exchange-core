from urllib.parse import urlparse


def pairs(value):   
    pairs = [v.split(':') for v in value.split(',')]
    try:
        return {pair[0]: pair[1] for pair in pairs}
    except IndexError:
        return {}


def redis_url(value):
	url = urlparse(value)

	if not url.path[1:]:
		return

	database = int(url.path[1:].split('?', 2)[0] or 0)
	return {
	    'host': url.hostname, 'port': url.port, 'db': database,
	    'password': url.password, 'prefix': 'session', 'socket_timeout': 1
	}