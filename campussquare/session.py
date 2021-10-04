import http.cookiejar
import requests
import bs4
import re
import threading
import time

from campussquare.util import debug_response, get_flow_execution_key


class CampusSquareSession():
    def __init__(self,
                 campussquare_url: str,
                 initial_flow_execution_key: str,
                 cookies: http.cookiejar.CookieJar,
                 debug: bool = False,
                 refresh_interval_sec: int = 600) -> None:
        self.flow_execution_keys = {}
        self.flow_execution_keys['default'] = initial_flow_execution_key

        self.session = requests.Session()
        self.session.cookies = cookies

        self.url = campussquare_url
        self.debug = debug

        # key refreshing
        topmenu_flow_execution_key = self._get_topmenu_flow_execution_key()
        self.flow_execution_keys['topmenu'] = topmenu_flow_execution_key

        def _refresh():
            while True:
                time.sleep(refresh_interval_sec)
                self._refresh()
        threading.Thread(target=_refresh, daemon=True).start()

    def get_flow_execution_key(self, namespace='default'):
        return self.flow_execution_keys.get(namespace)

    def do(self, data={}, namespace='default'):
        res = self.session.post(self.url, data=data, headers={
            'Referer': f'{self.url}?_flowExecutionKey={self.get_flow_execution_key(namespace)}'
        })

        # update flowExecutionKey
        self.flow_execution_keys[namespace] = get_flow_execution_key(res.url) or self.get_flow_execution_key(namespace)

        # error check
        doc = bs4.BeautifulSoup(res.text, 'html.parser')
        if doc.select_one('title').text == 'SYSTEM ERROR':
            raise RuntimeError('CampusSquare Flow Error')

        self.debug and debug_response(res)

        return res

    def _refresh(self):
        print('refreshing key...')
        res = self.do({
            '_eventId': 'extendSession',
            '_flowExecutionKey': self.get_flow_execution_key('topmenu'),
        }, namespace='topmenu')

    def _get_topmenu_flow_execution_key(self):
        url = f'{self.url}?_flowId=USW0009210-flow'
        res = self.session.get(url)
        regex = re.compile('document\.TopForm\._flowExecutionKey\.value = "([^"]+)";')
        topmenu_flow_execution_key = regex.findall(res.text)[0]
        return topmenu_flow_execution_key
