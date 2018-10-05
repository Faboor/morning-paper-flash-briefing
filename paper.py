#!/homes/pk3115/virtualEnvs/py3/bin/python

import requests
import re
import html
from datetime import datetime
import json

URL = 'https://blog.acolyer.org/feed/'
ITEM_PARSE_PATTERN = re.compile(r'<item>.+?<title>(?P<titleText>.+?)</title>.+?<link>(?P<redirectionUrl>.+?)</link>.+?<pubDate>(?P<updateDate>.+?)</pubDate>.+?<guid.+?>(?P<uid>.+?)</guid>.+?<content.+?</p>.+?<p>(?P<mainText>.+?)<h3>', re.DOTALL)
FEED_DATETIME_FORMAT = '%a, %d %b %Y %H:%M:%S %z'
OUTPUT_DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S.0Z'

def get_rss_feed():
    request = requests.get(URL)
    if request.ok:
        return request.text
    raise ConnectionError('Feed response not OK')

def get_latest_paper_info(xml):
    match = ITEM_PARSE_PATTERN.search(xml[:100000])
    if not match:
        raise ValueError('No feed items found')
    latest = match.groupdict()
    update_date = datetime.strptime(latest['updateDate'], FEED_DATETIME_FORMAT)
    latest['updateDate'] = datetime.strftime(update_date, OUTPUT_DATETIME_FORMAT)
    latest['mainText'] = latest['titleText'] + '. ' + html.unescape(re.sub(r'<.+?>|\n|\t', '', latest['mainText']))
    return latest

if __name__ == '__main__':
    print('Content-Type: application/json')
    print()
    print(json.dumps(get_latest_paper_info(get_rss_feed())))
