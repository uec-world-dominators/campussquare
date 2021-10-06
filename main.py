import os
import sys
from campussquare import CampusSquare
from campussquare.util import get_flow_execution_key
from campussquare.cli import get_parser, parse_args_with_handler, Authenticator


class UECCampusSquareAuthenticator(Authenticator):
    def __init__(self) -> None:
        self.campusweb_do_url = 'https://campusweb.office.uec.ac.jp/campusweb/campussquare.do'
        self.campusweb_url = 'https://campusweb.office.uec.ac.jp/campusweb/ssologin.do'

        # Shibboleth Login
        from uecauth.shibboleth import ShibbolethAuthenticator
        from uecauth.password import DefaultPasswordProvider
        from uecauth.mfa import AutoTOTPMFAuthCodeProvider
        self.shibboleth_host = 'shibboleth.cc.uec.ac.jp'
        self.shibboleth = ShibbolethAuthenticator(
            shibboleth_host=self.shibboleth_host,
            mfa_code_provider=AutoTOTPMFAuthCodeProvider(os.environ['UEC_MFA_SECRET']),
            password_provider=DefaultPasswordProvider(
                os.environ['UEC_USERNAME'],
                os.environ['UEC_PASSWORD']
            ),
            debug=False,
        )

    def login(self) -> CampusSquare:
        return CampusSquare(
            self.campusweb_do_url,
            None,
            self.shibboleth.get_cookies(),
            debug=False
        )

    def refresh(self) -> CampusSquare:
        print('refreshing...', file=sys.stderr)
        res = self.shibboleth.login(self.campusweb_url)
        return CampusSquare(
            self.campusweb_do_url,
            get_flow_execution_key(res.url),
            self.shibboleth.get_cookies(),
            debug=False
        )


if __name__ == '__main__':
    parser = get_parser(authenticator=UECCampusSquareAuthenticator())
    parse_args_with_handler(parser)
