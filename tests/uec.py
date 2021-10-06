import subprocess
import unittest
import hashlib


class Test(unittest.TestCase):
    def test_syllabus_search(self):
        output = subprocess.check_output("python3 main.py syllabus search --year 2021 -s 'コンピュータサイエンス'", shell=True)
        self.assertEqual(hashlib.sha256(output).hexdigest(), '796cced98290616484dc08ce7d187e17d1b0fbb4c98ed83c220158e895abf724')

    def test_syllabus_detail(self):
        output = subprocess.check_output("python3 main.py syllabus get --year 2021 -t 31 -c 21124235", shell=True)
        self.assertEqual(hashlib.sha256(output).hexdigest(), '7f492093d01f9d6de4f984f72ea359799fb30b80866f4dcd37a00075a64d74fe')

    def test_syllabus_detail_markdown(self):
        output = subprocess.check_output("python3 main.py --markdown syllabus get --year 2021 -t 31 -c 21124229", shell=True)
        self.assertEqual(hashlib.sha256(output).hexdigest(), 'a021711c18b1902ef2a96f0e300c3e37864805398e7c4807e07f51cdae311319')


if __name__ == '__main__':
    unittest.main()
