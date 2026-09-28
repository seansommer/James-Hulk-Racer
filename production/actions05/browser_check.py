"""Local self-contained action-viewer checks; no game or account connections."""
from pathlib import Path
import hashlib,json,shutil
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'art/01-characters/hulk/action-reviews/v01/review-export'
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
 ok(state()['imageCount']==14 and not state()['playing'],'Fourteen embedded images load; initially paused')
 page.click('#next');ok(state()['idx']==1,'Next steps forward')
 page.click('#previous');ok(state()['idx']==0,'Previous steps backward')
 page.click('#play');page.wait_for_timeout(220);page.click('#play');idx=state()['idx'];page.wait_for_timeout(150)
 ok(state()['idx']==idx and not state()['playing'],'Pause holds pose')
 page.select_option('#clip','smash');page.select_option('#speed','1.5');page.click('#play');page.wait_for_timeout(1100)
 ok(state()['idx']==7 and not state()['playing'],'Smash one-shot holds its last pose')
 page.click('#play');ok(state()['playing'] and state()['idx']==0,'Replay restarts from first pose');page.click('#play')
 page.select_option('#clip','thunderclap');ok(state()['total']==6 and state()['idx']==0,'Thunderclap selects six poses')
 page.click('#play');page.wait_for_timeout(850)
 ok(state()['idx']==5 and not state()['playing'],'Thunderclap one-shot holds its last pose')
 page.select_option('#clip','smash');ok(state()['total']==8 and state()['idx']==0,'Smash selects eight poses')
 page.select_option('#background','checker');ok(page.get_attribute('#stage','data-bg')=='checker','Checker background works')
 page.select_option('#size','160');ok(page.eval_on_selector('#canvas','c=>c.style.height')=='160px','Small gameplay-size display works')
 page.uncheck('#guide');ok(not page.is_checked('#guide'),'Provisional guide can be hidden')
 page.check('#show-strip');ok(page.locator('#strip button').count()==8 and page.is_visible('#strip'),'Strip displays current clip only')
 page.set_viewport_size({'width':390,'height':844});page.select_option('#clip','thunderclap');page.select_option('#size','240')
 ok(page.evaluate('document.documentElement.scrollWidth<=innerWidth'),'390px portrait has no horizontal page overflow')
 page.screenshot(path=str(OUT/'phone-review.png'),full_page=True)
 page.set_viewport_size({'width':844,'height':390})
 ok(page.evaluate('document.documentElement.scrollWidth<=innerWidth'),'844px landscape has no horizontal page overflow')
 ok(not errors and not [u for u in requests if not u.startswith('data:')],'No uncaught script errors or external requests')
 browser.close()
report=dict(result='PASS_LOCAL_REVIEWER',checkCount=len(checks),checks=checks,errors=errors,externalRequests=[],
 htmlSha256=hashlib.sha256(PAGE.read_bytes()).hexdigest(),
 scope='Local Chromium with supplied self-contained HTML; simulated viewports, not physical iPhone/Safari, art approval or live-game testing.')
(OUT/'browser-checks.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
