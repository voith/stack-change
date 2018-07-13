import re
from urllib.parse import urlparse, urlunparse


def get_site_url(url):
    scheme, netloc, _, _, _, _ = urlparse(url)
    return urlunparse([scheme, netloc, '', '', '', ''])


def get_url_part(url, regex):
    _, _, url, _, _, _ = urlparse(url)
    return re.match(regex, url).group(1)

