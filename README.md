# CampusSquare

```py
import http.cookiejar
from campussquare import CampusSquare

# 事前に取得しておく
cookies: http.cookiejar # 認証情報
flow_execution_key: str

# Campus Square
campussquare = CampusSquare(
    'https://campusweb.office.uec.ac.jp/campusweb/campussquare.do',
    cookies,
    flow_execution_key,
    debug=True
)

campussquare.goto_syllabus_search()
campussquare.search_syllabus(year=2021, subject='コンピュータサイエンス')
campussquare.syllabus_detail(2021, 31, 21124124)
```
