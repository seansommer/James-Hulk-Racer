"""Local viewer checks; does not connect to the game or approve the animation."""
from pathlib import Path
import hashlib,json,shutil
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'art/01-characters/hulk/jump-reviews/v01/review-export'
PAGE=OUT/'review.html'
checks=[];errors=[];requests=[]
def ok(condition,name):
 if not condition:raise AssertionError(name)
 checks.append(name)
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path=shutil.which('chromium'),args=['--no-sandbox'])
 page=browser.new_page(viewport={'width':1120,'height':900},device_scale_factor=1)
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.on('request',lambda r:requests.append(r.url))
 page.set_content(PAGE.read_text(),wait_until='load')
 page.wait_for_function('window.__reviewState && window.__reviewState().ready')
 state=lambda:page.evaluate('window.__reviewState()')
 ok(state()['imageCount']==9 and not state()['playing'],'Nine embedded images load; initially paused')
 page.click('#next');ok(state()['idx']==1,'Next selects the next source pose')
 page.click('#previous');ok(state()['idx']==0,'Previous returns to the preceding pose')
 page.click('#play');page.wait_for_timeout(220);page.click('#play');idx=state()['idx'];page.wait_for_timeout(150)
 ok(state()['idx']==idx and not state()['playing'],'Pause holds the current pose')
 page.select_option('#clip','full');page.select_option('#speed','1.5');page.click('#play');page.wait_for_timeout(1500)
 ok(state()['idx']==8 and not state()['playing'],'Combined one-shot holds its last pose')
 page.click('#play');ok(state()['playing'] and state()['idx']==0,'Replay restarts from first pose');page.click('#play')
 page.select_option('#clip','jump');ok(state()['total']==6 and state()['idx']==0,'Jump selects six frames')
 page.select_option('#clip','land');ok(state()['total']==3 and state()['idx']==0,'Landing selects three frames')
 page.select_option('#background','checker');ok(page.get_attribute('#stage','data-bg')=='checker','Checker background selected')
 page.select_option('#size','160');ok(page.eval_on_selector('#canvas','c=>c.style.height')=='160px','Gameplay-size display selected')
 page.uncheck('#guide');ok(not page.is_checked('#guide'),'Provisional anchor guide can be hidden')
 page.check('#show-strip');ok(page.locator('#strip button').count()==3 and page.is_visible('#strip'),'Pose strip contains the selected clip only')
 page.set_viewport_size({'width':390,'height':844});page.select_option('#clip','full');page.select_option('#size','240')
 ok(page.evaluate('document.documentElement.scrollWidth<=innerWidth'),'390px portrait has no horizontal page overflow')
 page.screenshot(path=str(OUT/'phone-review.png'),full_page=True)
 page.set_viewport_size({'width':844,'height':390})
 ok(page.evaluate('document.documentElement.scrollWidth<=innerWidth'),'844px landscape has no horizontal page overflow')
 ok(not errors and not [u for u in requests if not u.startswith('data:')],'No uncaught script errors or external requests')
 browser.close()
report=dict(result='PASS_LOCAL_REVIEWER',checkCount=len(checks),checks=checks,errors=errors,externalRequests=[],
 htmlSha256=hashlib.sha256(PAGE.read_bytes()).hexdigest(),
 scope='Local Chromium with supplied self-contained HTML; simulated portrait/landscape, not physical iPhone/Safari, motion approval or live-game testing.')
(OUT/'browser-checks.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
