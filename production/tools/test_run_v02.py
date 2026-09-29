"""Synthetic export tests. Passing these is not artistic approval."""
import unittest
from pathlib import Path
from PIL import Image,ImageDraw
from run_v02 import remove_white,pack,safe_path,SOURCE_ORDER
class RunRevisionTests(unittest.TestCase):
    def test_cycle_uses_each_source_once(self):self.assertEqual(sorted(SOURCE_ORDER),list(range(8)))
    def test_no_path_escape(self):
        with self.assertRaises(ValueError):safe_path(Path('/tmp/art-test'),'../outside.png')
    def test_alpha_is_copied_once(self):
        f=Image.new('RGBA',(256,320));f.putpixel((10,10),(40,150,80,128))
        atlas,rects=pack([f]*8)
        self.assertEqual(atlas.getpixel((14,14)),(40,150,80,128));self.assertEqual(rects[4],[4,332,256,320])
    def test_wrong_size_rejected(self):
        with self.assertRaises(ValueError):pack([Image.new('RGBA',(250,320))]*8)
    def test_wrong_count_rejected(self):
        with self.assertRaises(ValueError):pack([Image.new('RGBA',(256,320))]*7)
    def test_enclosed_white_is_not_silently_erased(self):
        im=Image.new('RGB',(80,80),'white');d=ImageDraw.Draw(im);d.rectangle((10,10,70,70),fill='green');d.rectangle((30,30,45,45),fill='white')
        out=remove_white(im);self.assertEqual(out.getpixel((0,0))[3],0);self.assertEqual(out.getpixel((35,35)),(255,255,255,255))
    def test_explicit_negative_space_seed(self):
        im=Image.new('RGB',(80,80),'white');d=ImageDraw.Draw(im);d.rectangle((10,10,70,70),fill='green');d.rectangle((30,30,45,45),fill='white')
        self.assertEqual(remove_white(im,[(35,35)]).getpixel((35,35))[3],0)
if __name__=='__main__':unittest.main()
