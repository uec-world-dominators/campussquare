import http.cookiejar
import requests
import bs4

from campussquare.util import debug_response, get_flow_execution_key


class CampusSquareSession():
    def __init__(self,
                 campussquare_url: str,
                 initial_flow_execution_key: str,
                 cookies: http.cookiejar.CookieJar,
                 debug: bool = False) -> None:
        self.flow_execution_key = initial_flow_execution_key
        self.session = requests.Session()
        self.session.cookies = cookies
        self.url = campussquare_url
        self.debug = debug

    def do(self, data={}):
        res = self.session.post(self.url, data=data, headers={
            'Referer': f'{self.url}?_flowExecutionKey={self.flow_execution_key}'
        })

        # update flowExecutionKey
        self.flow_execution_key = get_flow_execution_key(res.url) or self.flow_execution_key

        # error check
        doc = bs4.BeautifulSoup(res.text, 'html.parser')
        if doc.select_one('title').text == 'SYSTEM ERROR':
            raise RuntimeError('CampusSquare Flow Error')

        self.debug and debug_response(res)

        return res
