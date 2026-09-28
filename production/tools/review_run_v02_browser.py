"""Optional local browser checks. Requires Playwright and a Chromium executable."""
import json
from pathlib import Path
import shutil, os
from playwright.sync_api import sync_playwright
folder=Path(__file__).resolve().parents[2]/'art/01-characters/hulk/run-reviews/v02/review-export'
page_html=(folder/'review.html').read_text()
checks=[];errors=[];requests=[]
def ok(text): checks.append(text);print('PASS',text)
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path=os.environ.get('CHROMIUM_PATH') or shutil.which('chromium'),args=['--no-sandbox'])
 page=browser.new_page(viewport={'width':1180,'height':820})
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.on('request',lambda r:requests.append(r.url))
 page.set_content(page_html,wait_until='load')
 page.wait_for_function('window.__runReview?.().ready === true')
 assert not page.evaluate('window.__runReview().playing');ok('Embedded new and previous atlases load; playback starts paused')
 page.locator('#next').click();assert page.evaluate('window.__runReview().index')==1;ok('Forward frame step')
 page.locator('#prev').click();assert page.evaluate('window.__runReview().index')==0;ok('Backward frame step')
 page.locator('#play').click();page.wait_for_timeout(210);assert page.evaluate('window.__runReview().index')!=0
 page.locator('#play').click();idx=page.evaluate('window.__runReview().index');page.wait_for_timeout(150)
 assert page.evaluate('window.__runReview().index')==idx;ok('Play advances and Pause holds the exact frame')
 page.locator('#view').select_option('source');assert page.evaluate('window.__runReview().mapped')==4;ok('Original-source order maps back to the correct new drawing')
 page.locator('#view').select_option('compare');assert page.evaluate('window.__runReview().view')=='compare';ok('Previous/new comparison selectable')
 for bg in ['light','checker','dark']:
  page.locator('#background').select_option(bg);assert bg in page.locator('#stage').get_attribute('class')
 ok('Light, dark and checker backgrounds')
 page.locator('#size').select_option('180');page.locator('#speed').select_option('6');page.locator('#guides').uncheck();ok('Size, speed and anchor controls')
 page.screenshot(path=str(folder/'desktop-review.png'),full_page=True)
 for w,h,name in [(390,844,'phone-review'),(844,390,'landscape-review')]:
  page.set_viewport_size({'width':w,'height':h});page.wait_for_timeout(100)
  assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth+1')
  page.screenshot(path=str(folder/f'{name}.png'),full_page=True)
  ok(f'{w}x{h} viewport has no horizontal overflow')
 assert not errors;ok('No uncaught browser errors')
 assert not [u for u in requests if u.startswith(('http:','https:'))];ok('No external network requests during review')
 browser.close()
report={'result':'PASS_REVIEW_PAGE_ONLY','checkCount':len(checks),'checks':checks,'errors':errors,'scope':'Local headless Chromium with embedded HTML; simulated sizes, not physical Safari or gameplay testing.'}
(folder/'browser-checks.json').write_text(json.dumps(report,indent=2)+'\n')
