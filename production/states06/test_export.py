"""Synthetic contract checks; not approval of generated poses or animation."""
from pathlib import Path
import unittest
from PIL import Image,ImageDraw
import export
class ExportTests(unittest.TestCase):
 def test_disjoint_clip_counts(self):
  groups=[c['frames'] for c in export.CLIPS.values()]
  self.assertEqual([len(g) for g in groups],[6,3,4]);self.assertEqual(sum(groups,[]),list(range(13)))
 def test_loop_flags(self):
  self.assertFalse(export.CLIPS['power_up']['loop']);self.assertFalse(export.CLIPS['hurt']['loop']);self.assertTrue(export.CLIPS['menu_idle']['loop'])
 def test_phase_and_source_counts(self):
  self.assertEqual(len(export.PHASES),13);self.assertEqual([len(s['roots']) for s in export.SOURCES.values()],[6,3,4])
 def test_source_grid_contract(self):
  for s in export.SOURCES.values():self.assertEqual(s['cols']*s['rows'],len(s['roots']))
 def test_root_coordinates_inside_source(self):
  for s in export.SOURCES.values():
   w,h=s['size']
   for x,y in s['roots']:self.assertTrue(0<x<w and 0<y<h)
 def test_hash_contract(self):
  for s in export.SOURCES.values():self.assertRegex(s['sha256'],r'^[a-f0-9]{64}$')
 def test_atlas_alpha_not_multiplied(self):
  im=Image.new('RGBA',(256,320));im.putpixel((9,10),(100,70,210,128))
  a,r=export.pack([im]*13)
  self.assertEqual(a.size,(1056,1312));self.assertEqual(a.getpixel((13,14)),(100,70,210,128));self.assertEqual(r[12],[4,988,256,320])
 def test_atlas_wrong_count(self):
  with self.assertRaises(ValueError):export.pack([Image.new('RGBA',(256,320))]*12)
 def test_atlas_wrong_size(self):
  with self.assertRaises(ValueError):export.pack([Image.new('RGBA',(16,20))]*13)
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
 def test_no_game_contact_events(self):
  self.assertTrue(all('contactFrame' not in c and 'events' not in c for c in export.CLIPS.values()))
if __name__=='__main__':unittest.main()
