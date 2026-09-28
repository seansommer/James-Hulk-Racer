"""Synthetic export tests, not approval of Jamesy artwork or motion."""
import unittest
from PIL import Image,ImageDraw
from pathlib import Path
from movement03_export import matte,register,pack,art_path,clear_floor_plate,FRAMES,SCALES,CLIPS
class MovementTests(unittest.TestCase):
    def test_exterior_removed_interior_white_retained(self):
        im=Image.new('RGB',(60,80),'white');d=ImageDraw.Draw(im);d.rectangle((10,10,50,70),fill='#168045');d.rectangle((25,25,35,40),fill='white')
        result=matte(im);self.assertEqual(result.getpixel((0,0))[3],0);self.assertEqual(result.getpixel((30,30)),(255,255,255,255))
    def test_explicit_negative_space(self):
        im=Image.new('RGB',(60,80),'white');d=ImageDraw.Draw(im);d.rectangle((10,10,50,70),fill='#168045');d.rectangle((25,25,35,40),fill='white')
        self.assertEqual(matte(im,[(30,30)]).getpixel((30,30))[3],0)
    def test_root_and_canvas(self):
        im=Image.new('RGBA',(60,80));ImageDraw.Draw(im).rectangle((10,10,50,70),fill=(20,100,40,255))
        result,offset=register(im,1,[30,70]);self.assertEqual(offset,[226,506]);self.assertEqual(result.size,(512,640));self.assertEqual(result.getbbox(),(236,516,277,577))
    def test_blank_rejected(self):
        with self.assertRaises(ValueError):register(Image.new('RGBA',(60,80)),1,[30,70])
    def test_clipping_rejected(self):
        with self.assertRaises(ValueError):register(Image.new('RGBA',(1000,1000),(1,2,3,255)),1,[500,900])
    def test_path_boundary(self):
        with self.assertRaises(ValueError):art_path(Path('/tmp'),'../../credentials.txt')
    def test_atlas_alpha_copy(self):
        im=Image.new('RGBA',(256,320));im.putpixel((10,10),(70,120,40,128));a,r=pack([im]*12)
        self.assertEqual(a.size,(1056,984));self.assertEqual(r[-1],[796,660,256,320]);self.assertEqual(a.getpixel((806,670)),(70,120,40,128))
    def test_invalid_atlas_count(self):
        with self.assertRaises(ValueError):pack([Image.new('RGBA',(256,320))]*4)
    def test_source_plan(self):
        self.assertEqual(len(FRAMES),12);self.assertEqual(len({f[0] for f in FRAMES}),12)
        self.assertEqual(sorted(i for c in CLIPS.values() for i in c['frames']),list(range(12)))
        self.assertTrue(all(f[1] in SCALES for f in FRAMES))
    def test_floor_shadow_not_colored_sole(self):
        im=Image.new('RGBA',(20,20));im.putpixel((10,18),(180,180,180,255));im.putpixel((11,18),(10,120,20,255))
        out=clear_floor_plate(im,18);self.assertEqual(out.getpixel((10,18))[3],0);self.assertEqual(out.getpixel((11,18))[3],255)
if __name__=='__main__':unittest.main()
