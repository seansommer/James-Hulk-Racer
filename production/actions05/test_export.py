"""Synthetic tests cover contracts and image handling, not animation approval."""
from pathlib import Path
import unittest
from PIL import Image,ImageDraw
import export
class ExportTests(unittest.TestCase):
 def test_disjoint_clip_counts(self):
  a=export.CLIPS['smash']['frames'];b=export.CLIPS['thunderclap']['frames']
  self.assertEqual((len(a),len(b)),(8,6));self.assertEqual(a+b,list(range(14)))
 def test_one_shot_clips(self):
  self.assertTrue(all(not c['loop'] for c in export.CLIPS.values()))
 def test_contact_marker_in_bounds(self):
  for c in export.CLIPS.values():self.assertTrue(0<=c['contactFrame']<len(c['frames']))
 def test_source_and_root_counts(self):
  self.assertEqual([len(s['roots']) for s in export.SOURCES.values()],[8,6])
 def test_atlas_alpha_not_multiplied(self):
  im=Image.new('RGBA',(256,320));im.putpixel((9,10),(100,70,210,128))
  a,r=export.pack([im]*14)
  self.assertEqual(a.size,(1056,1312));self.assertEqual(a.getpixel((13,14)),(100,70,210,128));self.assertEqual(r[13],[268,988,256,320])
 def test_atlas_wrong_count(self):
  with self.assertRaises(ValueError):export.pack([Image.new('RGBA',(256,320))]*13)
 def test_atlas_wrong_size(self):
  with self.assertRaises(ValueError):export.pack([Image.new('RGBA',(16,20))]*14)
 def test_enclosed_white_preserved(self):
  im=Image.new('RGB',(80,80),'white');d=ImageDraw.Draw(im);d.rectangle((10,10,70,70),fill='green');d.rectangle((30,30,42,42),fill='white')
  rgba=export.matte(im);self.assertEqual(rgba.getpixel((35,35)),(255,255,255,255));self.assertEqual(rgba.getpixel((0,0))[3],0)
 def test_negative_space_annotation(self):
  im=Image.new('RGB',(80,80),'white');d=ImageDraw.Draw(im);d.rectangle((10,10,70,70),fill='green');d.rectangle((30,30,42,42),fill='white')
  self.assertEqual(export.matte(im,[[35,35]]).getpixel((35,35))[3],0)
 def test_path_scope(self):
  with self.assertRaises(ValueError):export.art_path(Path('/tmp'),'../outside.png')
 def test_fixed_registration(self):
  im=Image.new('RGBA',(60,80));ImageDraw.Draw(im).rectangle((20,20,40,70),fill=(0,170,90,255))
  f,p=export.register(im,1,[30,70]);self.assertEqual(f.size,(512,640));self.assertEqual(p,[226,506])
 def test_clipping_rejected(self):
  with self.assertRaises(ValueError):export.register(Image.new('RGBA',(900,900),(0,170,90,255)),1,[450,900])
if __name__=='__main__':unittest.main()
