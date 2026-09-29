"""Small synthetic tests of masking and packing, not artwork approval."""
import unittest
from pathlib import Path
from PIL import Image, ImageDraw
from character_sprites import remove_white_matte, frame_export, pack_runtime, safe_art_path

class SpriteTests(unittest.TestCase):
    def test_preserves_enclosed_white_emblem(self):
        image=Image.new('RGB',(80,80),'white');d=ImageDraw.Draw(image)
        d.rectangle((10,10,70,70),fill=(30,110,45));d.rectangle((30,30,45,45),fill='white')
        out=remove_white_matte(image,[])
        self.assertEqual(out.getpixel((0,0))[3],0)
        self.assertEqual(out.getpixel((37,37)),(255,255,255,255))
    def test_negative_space_seed(self):
        image=Image.new('RGB',(80,80),'white');d=ImageDraw.Draw(image)
        d.rectangle((10,10,70,70),fill=(30,110,45));d.rectangle((30,30,45,45),fill='white')
        out=remove_white_matte(image,[[37,37]])
        self.assertEqual(out.getpixel((37,37))[3],0)
    def test_bad_seed_rejected(self):
        with self.assertRaises(ValueError):remove_white_matte(Image.new('RGB',(20,20),'green'),[])
    def test_path_escape_rejected(self):
        with self.assertRaises(ValueError):safe_art_path(Path('/tmp'),'../credentials.json')
    def test_frame_canvas_and_anchor(self):
        sheet=Image.new('RGBA',(80,80));ImageDraw.Draw(sheet).rectangle((25,20,55,70),fill=(70,200,100,255))
        frame=frame_export(sheet,[0,0,80,80],[40,70],1)
        self.assertEqual(frame.size,(512,640));self.assertEqual(frame.getchannel('A').getbbox(),(241,526,272,577))
    def test_frame_clipping_rejected(self):
        with self.assertRaises(ValueError):frame_export(Image.new('RGBA',(800,800),(1,2,3,255)),[0,0,800,800],[400,800],1)
    def test_atlas_preserves_straight_alpha(self):
        frame=Image.new('RGBA',(256,320));frame.putpixel((10,10),(80,140,200,128))
        image,rects=pack_runtime([frame]*8)
        self.assertEqual(image.size,(1056,656));self.assertEqual(rects[4],[4,332,256,320])
        self.assertEqual(image.getpixel((14,14)),(80,140,200,128))
    def test_wrong_runtime_size_rejected(self):
        with self.assertRaises(ValueError):pack_runtime([Image.new('RGBA',(20,20))])

if __name__=='__main__':unittest.main()
