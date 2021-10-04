import http.cookiejar
from .session import CampusSquareSession
from .util import create_form_data, debug_response


class CampusSquare():
    def __init__(self,
                 campussquare_url: str,
                 initial_flow_execution_key: str,
                 cookies: http.cookiejar.CookieJar,
                 debug: bool = False
                 ) -> None:
        self.session = CampusSquareSession(campussquare_url,
                                           initial_flow_execution_key,
                                           cookies,
                                           debug=debug)

    def goto_syllabus_search(self):
        res = self.session.do({
            '_flowId': 'SYW0001000-flow'
        })
        return res

    def search_syllabus(self,
                        year: int = '',
                        subject: str = '',
                        display_count: int = 100,
                        ):
        data = {
            's_no': '0',
            '_flowExecutionKey': self.session.get_flow_execution_key(),
            '_eventId': 'search',
            'nendo': year,
            'jikanwariShozokuCode': '',
            'gakkiKubunCode': '',
            'kyokannm': '',
            'kaikoKamokunm': subject,
            'numberingcd': '',
            'keyword': '',
            'nenji': '',
            'yobi': '',
            'jigen': '',
            'jitsumuKbn': '',
            '_displayCount': display_count,
        }
        res = self.session.do(data=data)
        return res

    def syllabus_detail(self,
                        year: int,
                        affiliation_code: int,
                        timetable_code: int,
                        locale: str = 'ja_JP'):
        data = {
            '_flowExecutionKey': self.session.get_flow_execution_key(),
            '_eventId': 'input',
            'nendo': year,
            'jikanwariShozokuCode': affiliation_code,
            'jikanwaricd': timetable_code,
            'locale': locale,
            'secchikbncd': '',
            'dispCount': '100',
        }
        res = self.session.do(data=data)
        return res
