import datetime
import re


def match_value_from_cookie(cookie, key='pt_pin'):
    pattern = re.compile(f'{key}=([^;]+)')
    match = pattern.search(cookie)
    return match.group(1) if match else None


def timestamp_to_local_time_string(ms_timestamp):
    # 将毫秒时间戳转换为秒时间戳
    seconds_timestamp = ms_timestamp / 1000.0
    # 将秒时间戳转换为本地时间对象
    local_time = datetime.datetime.fromtimestamp(seconds_timestamp)
    # 将本地时间对象格式化为字符串
    local_time_string = local_time.strftime('%Y-%m-%d %H:%M:%S')
    return local_time_string


def get_timestamp_n_days_ago(n):
    # 获取当前时间
    now = datetime.datetime.now()
    # 计算N天前的时间
    n_days_ago = now - datetime.timedelta(days=n)
    # 将时间转换为秒时间戳
    seconds_timestamp = n_days_ago.timestamp()
    # 将秒时间戳转换为毫秒时间戳
    ms_timestamp = int(seconds_timestamp * 1000)
    return ms_timestamp
