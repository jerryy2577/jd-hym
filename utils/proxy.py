from conf import config


def get_proxies():
    """
    :return:
    """
    if config.JY_PROXY_POOL_URL:
        proxies = {'all://': config.JY_PROXY_POOL_URL}
    else:
        proxies = {'all://': None}
    return proxies


def get_no_proxies():
    """
    :return:
    """
    return {'all://': None}


if __name__ == '__main__':
    print(get_proxies())