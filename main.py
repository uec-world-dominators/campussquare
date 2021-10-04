import os
from uecauth.shibboleth import ShibbolethAuthenticator
from uecauth.password import DefaultPasswordProvider
from uecauth.mfa import AutoTOTPMFAuthCodeProvider
from campussquare import CampusSquare
from campussquare.util import get_flow_execution_key


# Shibboleth Login
campusweb_url = 'https://campusweb.office.uec.ac.jp/campusweb/ssologin.do'
shibboleth_host = 'shibboleth.cc.uec.ac.jp'

shibboleth = ShibbolethAuthenticator(
    original_url=campusweb_url,
    shibboleth_host=shibboleth_host,
    mfa_code_provider=AutoTOTPMFAuthCodeProvider(os.environ['UEC_MFA_SECRET']),
    password_provider=DefaultPasswordProvider(
        os.environ['UEC_USERNAME'],
        os.environ['UEC_PASSWORD']
    ),
    debug=False,
)

res = shibboleth.login(campusweb_url)
print(res.url)


# Campus Square
campussquare = CampusSquare(
    'https://campusweb.office.uec.ac.jp/campusweb/campussquare.do',
    get_flow_execution_key(res.url),
    shibboleth.lwp,
    debug=True
)

campussquare.goto_syllabus_search()
campussquare.search_syllabus(year=2021, subject='コンピュータサイエンス')
campussquare.syllabus_detail(2021, 31, 21124124)
