"""Local-only review-page tests; browser dependency is not part of the game."""
import json,hashlib,shutil
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'art/01-characters/hulk/movement-reviews/v01/review-export'
checks=[];errors=[];network=[]
def check(condition,label):
    if not condition:raise AssertionError(label)
    checks.append(label)
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,executable_path=shutil.which('chromium'),args=['--no-sandbox'])
    context=browser.new_context(viewport={'width':1280,'height':850},device_scale_factor=1)
    page=context.new_page()
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.on('request',lambda r:network.append(r.url) if r.url.startswith(('http:','https:')) else None)
    page.set_content((OUT/'review.html').read_text(),wait_until='load')
    page.wait_for_function('window.__movement03?.().loaded')
    state=page.evaluate('window.__movement03()')
    check(state['images']==12 and not state['playing'],'12 embedded frames load; starts paused')
    page.locator('#next').click();check(page.evaluate('window.__movement03().index')==1,'Next steps one frame')
    page.locator('#prev').click();check(page.evaluate('window.__movement03().index')==0,'Previous steps back')
    page.locator('#play').click();page.wait_for_timeout(240)
    check(page.evaluate('window.__movement03().index')!=0,'Playback advances')
    page.locator('#play').click();i=page.evaluate('window.__movement03().index');page.wait_for_timeout(240)
    check(not page.evaluate('window.__movement03().playing') and page.evaluate('window.__movement03().index')==i,'Pause holds the frame')
    for value in ['lean_left','lean_right','rear_idle']:
        page.locator('#clip').select_option(value)
        check(page.evaluate('window.__movement03().clip')==value and page.evaluate('window.__movement03().index')==0,'Select '+value+' and reset frame')
    page.locator('#background').select_option('checker');page.locator('#size').select_option('180');page.locator('#strip').check()
    check(page.locator('#stage').get_attribute('class')=='stage checker','Background, small size and strip controls')
    page.locator('#strip').uncheck();page.locator('#clip').select_option('lean_left');page.locator('#background').select_option('dark');page.locator('#size').select_option('320')
    page.screenshot(path=str(OUT/'desktop-review.png'))
    page.set_viewport_size({'width':390,'height':844})
    check(page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),'390px portrait has no horizontal overflow')
    page.screenshot(path=str(OUT/'phone-review.png'),full_page=True)
    page.set_viewport_size({'width':844,'height':390})
    check(page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),'844px landscape has no horizontal overflow')
    check(not errors,'No uncaught JavaScript errors')
    check(not network,'No external asset or account requests')
    browser.close()
report=dict(result='PASS_REVIEW_PAGE_ONLY',checkCount=len(checks),checks=checks,errors=errors,externalRequests=network,
    browser='Local headless Chromium; supplied self-contained HTML; simulated viewports, not physical iPhone/Safari',
    reviewerSha256=hashlib.sha256((OUT/'review.html').read_bytes()).hexdigest(),
    scope='Viewer loading, controls, layout and network isolation. Not a natural-motion or game-performance approval.')
(OUT/'browser-checks.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
