"""Local, offline reviewer checks; does not connect to the game or accounts."""
from pathlib import Path
import hashlib,json,shutil
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'art/01-characters/hulk/state-reviews/v01/review-export'
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
 page.wait_for_function('() => window.__reviewState && window.__reviewState().ready')
 state=lambda:page.evaluate('window.__reviewState()')
 ok(state()['imageCount']==13 and not state()['playing'],'Thirteen embedded images load; initially paused')
 page.click('#next');ok(state()['idx']==1,'Next steps forward')
 page.click('#previous');ok(state()['idx']==0,'Previous steps backward')
 page.click('#play');page.wait_for_timeout(140);page.click('#play');idx=state()['idx'];page.wait_for_timeout(200)
 ok(state()['idx']==idx and not state()['playing'],'Pause holds the current pose')
 page.select_option('#clip','power_up');page.select_option('#speed','1.5');page.click('#play')
 page.wait_for_function('() => !window.__reviewState().playing')
 ok(state()['idx']==5,'Power-up one-shot holds the final pose')
 page.click('#play');ok(state()['playing'] and state()['idx']==0,'Replay restarts from the first pose');page.click('#play')
 page.select_option('#clip','hurt');ok(state()['total']==3 and state()['idx']==0,'Bump recovery selects three poses')
 page.click('#play');page.wait_for_function('() => !window.__reviewState().playing')
 ok(state()['idx']==2,'Bump recovery one-shot holds the final pose')
 page.select_option('#clip','menu_idle');ok(state()['total']==4 and state()['idx']==0,'Menu idle selects four front-view poses')
 page.click('#next');page.click('#next');page.click('#next')
 page.select_option('#speed','0.5');page.click('#play');page.wait_for_function('() => window.__reviewState().idx===3')
 page.wait_for_function('() => window.__reviewState().idx===0')
 ok(state()['playing'],'Menu idle wraps rather than stopping');page.click('#play')
 ok('front three quarter' in page.get_attribute('#canvas','aria-label'),'Accessible pose description matches the front camera')
 page.select_option('#background','checker');ok(page.get_attribute('#stage','data-bg')=='checker','Checker background works')
 page.select_option('#background','light');ok(page.get_attribute('#stage','data-bg')=='light','Light background works')
 page.select_option('#background','dark');ok(page.get_attribute('#stage','data-bg')=='dark','Dark background works')
 page.select_option('#size','160');ok(page.eval_on_selector('#canvas','c=>c.style.height')=='160px','Small display size works')
 page.uncheck('#guide');ok(not page.is_checked('#guide'),'Provisional root guide can be hidden')
 page.check('#show-strip');ok(page.locator('#strip button').count()==4 and page.is_visible('#strip'),'Strip shows only the selected clip')
 page.locator('#strip button').nth(2).click();ok(state()['idx']==2 and not state()['playing'],'Pose-strip selection is precise and paused')
 page.set_viewport_size({'width':390,'height':844});page.select_option('#size','240')
 ok(page.evaluate('document.documentElement.scrollWidth<=innerWidth'),'390px portrait has no horizontal page overflow')
 page.screenshot(path=str(OUT/'phone-review.png'),full_page=True)
 page.set_viewport_size({'width':844,'height':390})
 ok(page.evaluate('document.documentElement.scrollWidth<=innerWidth'),'844px landscape has no horizontal page overflow')
 ok(not errors and not [u for u in requests if not u.startswith('data:')],'No uncaught script errors or external requests')
 browser.close()
report=dict(result='PASS_LOCAL_REVIEWER',checkCount=len(checks),checks=checks,errors=errors,externalRequests=[],
 htmlSha256=hashlib.sha256(PAGE.read_bytes()).hexdigest(),
 scope='Executed local Chromium checks against the self-contained reviewer. Simulated viewports, not physical Safari testing, visual approval or live-game validation.')
(OUT/'browser-checks.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
