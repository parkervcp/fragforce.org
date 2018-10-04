""" DonorDrive API Base Class """
from .log import root_logger
import requests
from collections import namedtuple
import re
from urllib.parse import urljoin

mod_logger = root_logger.getChild('base')
FetchResponse = namedtuple('FetchResponse', ['data', 'headers', 'urls'])


class DonorDriveBase(object):
    DEFAULT_BASE_URL = 'http://www.extra-life.org/api/'
    RE_MATCH_LINK = re.compile(r'^\<(.*)\>;rel="(.*)"')

    def __init__(self, base_url=DEFAULT_BASE_URL, log_parent=mod_logger):
        self.base_url = base_url
        self.log_parent = log_parent
        self.log = self.log_parent.getChild(self.__class__.__name__)
        self.session = requests.Session()

    @classmethod
    def _parse_link_header(cls, link):
        if link is None:
            return {}
        n = {}
        for a in link.split(','):
            r = cls.RE_MATCH_LINK.match(a).groups()
            n[r[1].lower()] = r[0]
        return n

    def fetch_json(self, url, **kwargs):
        """ Fetch the given URL with the given data. Returns data structure from JSON or raises an error. """
        e = dict(url=url, data=kwargs)
        try:
            self.log.debug(f'Going to fetch {url}', extra=e)
            r = self.session.get(url, data=kwargs)
            e['result'] = r
            self.log.log(5, f'Got result from {url}', extra=e)
            r.raise_for_status()
            self.log.log(5, f"Status of {url} is ok", extra=e)
            j = r.json()
            e['data_len'] = len(j)
            e['data'] = j
            self.log.debug(f"Got JSON data from {url}", extra=e)
            return FetchResponse(j, r.headers, self._parse_link_header(r.headers.get('Link', None)))
        finally:
            self.log.log(5, f"Done fetching {url}", extra=e)

    def fetch(self, sub_url, **kwargs):
        """ Fetch all records """
        url = urljoin(self.DEFAULT_BASE_URL, sub_url)
        e = dict(url=url, data=kwargs)

        fresp = self.fetch_json(url=url, **kwargs)
        ret = fresp.data
        while 'next' in fresp.urls:
            assert isinstance(ret, list), "Expected a list not %r" % ret
            fresp = self.fetch_json(url=fresp.urls['next'])
            ret.extend(fresp.data)
        return ret
