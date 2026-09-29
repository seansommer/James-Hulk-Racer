import unittest, io, hashlib
from PIL import Image
from archive_art import validate_url, validate_bytes, target_path

class ArchiveTests(unittest.TestCase):
    def test_host_allowlist(self):
        self.assertTrue(validate_url('https://d2jqrm6oza8nb6.cloudfront.net/datasets/example.png'))
    def test_other_host_denied(self):
        with self.assertRaises(ValueError):validate_url('https://example.com/art.png')
    def test_insecure_scheme_denied(self):
        with self.assertRaises(ValueError):validate_url('http://d2jqrm6oza8nb6.cloudfront.net/example.png')
    def test_escape_denied(self):
        with self.assertRaises(ValueError):target_path('art/../src/app.js')
    def test_application_path_denied(self):
        with self.assertRaises(ValueError):target_path('src/hero.png')
    def test_correct_checksum(self):
        b=io.BytesIO();Image.new('RGBA',(32,40),(10,20,30,128)).save(b,format='PNG');data=b.getvalue()
        self.assertEqual(validate_bytes(data,hashlib.sha256(data).hexdigest())['height'],40)
    def test_bad_checksum_denied(self):
        with self.assertRaises(ValueError):validate_bytes(b'not-art','0'*64)
if __name__=='__main__':unittest.main()
