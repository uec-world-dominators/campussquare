import datetime
import subprocess
import unittest
import hashlib

import sys
import os.path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from campussquare import util


class Test(unittest.TestCase):
    def test_syllabus_search(self):
        output = subprocess.check_output(
            "python3 main.py syllabus search --year 2021 -s 'コンピュータサイエンス'", shell=True)
        self.assertEqual(hashlib.sha256(output).hexdigest(
        ), '796cced98290616484dc08ce7d187e17d1b0fbb4c98ed83c220158e895abf724')

    def test_syllabus_detail(self):
        output = subprocess.check_output(
            "python3 main.py syllabus get 2021:31:21124235", shell=True)
        self.assertEqual(hashlib.sha256(output).hexdigest(
        ), '7f492093d01f9d6de4f984f72ea359799fb30b80866f4dcd37a00075a64d74fe')

    def test_syllabus_detail_multiple(self):
        output = subprocess.check_output(
            "python3 main.py syllabus get 2021:31:21124235 2021:31:21124208 --interval 1", shell=True)
        self.assertEqual(hashlib.sha256(output).hexdigest(
        ), 'ccaf6ade7a4177e257e434ae7713d147ad9000b9159fe0810501cc314185b8c3')

    def test_syllabus_detail_markdown(self):
        output = subprocess.check_output(
            "python3 main.py --markdown syllabus get 2021:31:21124229", shell=True)
        self.assertEqual(hashlib.sha256(output).hexdigest(
        ), 'a021711c18b1902ef2a96f0e300c3e37864805398e7c4807e07f51cdae311319')


class UtilTest(unittest.TestCase):
    def test_get_school_year1(self):
        year = util.get_school_year(datetime.datetime(2021, 4, 1))
        self.assertEqual(year, 2021)

    def test_get_school_year2(self):
        year = util.get_school_year(datetime.datetime(2021, 3, 31))
        self.assertEqual(year, 2020)


if __name__ == '__main__':
    unittest.main()
