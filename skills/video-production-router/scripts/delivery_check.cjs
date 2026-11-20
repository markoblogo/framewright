#!/usr/bin/env node
// Reusable real-browser check. Requires an existing Playwright installation.
const fs = require('node:fs');
const crypto = require('node:crypto');
const path = require('node:path');
const {createRequire} = require('node:module');
const os = require('node:os');

async function main() {
  const [url, receiptPath, playwrightPath, ...options] = process.argv.slice(2);
  if (!url || !receiptPath || !playwrightPath) throw Error('Usage: delivery_check.cjs URL RECEIPT PLAYWRIGHT_PACKAGE_JSON');
  const target = new URL(url);
  if (!['127.0.0.1', 'localhost'].includes(target.hostname) || target.protocol !== 'http:')
    throw Error('Expected a loopback HTTP review URL');
  const baselineFlag = options.indexOf('--baseline');
  if (baselineFlag >= 0 && !options[baselineFlag + 1]) throw Error('--baseline needs a path');
  const cachePath = path.resolve(baselineFlag >= 0 ? options[baselineFlag + 1] :
    path.join(__dirname, '../../../../records/delivery-qa/player-baselines.json'));
  const forced = options.includes('--full-player');
  const {chromium} = createRequire(path.resolve(playwrightPath))('playwright');
  const previous = JSON.parse(fs.readFileSync(receiptPath, 'utf8'));
  const scope = {platforms: [...new Set(previous.files.filter(f => f.role === 'video').map(f => f.platform))],
    copy: /data-copy=/.test(fs.readFileSync(path.join(path.dirname(receiptPath), 'review.html'), 'utf8'))};
  const browserPaths = process.platform === 'darwin' ? ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'] :
    process.platform === 'win32' ? [path.join(process.env.PROGRAMFILES || '', 'Google/Chrome/Application/chrome.exe')] :
    ['/opt/google/chrome/chrome', '/usr/bin/google-chrome', '/usr/bin/google-chrome-stable'];
  const browserPath = browserPaths.find(p => fs.existsSync(p));
  const browserIdentity = browserPath ? (() => {const st=fs.statSync(browserPath);return {path: browserPath,size: st.size,mtime: st.mtimeMs};})() : null;
  const key = crypto.createHash('sha256').update(JSON.stringify({protocol: 1,
    template: previous.template_sha256, checker: hashFile(__filename),
    server: hashFile(path.join(__dirname, 'preview_server.py')),
    playwright: hashFile(path.resolve(playwrightPath)),browser: browserIdentity,
    node: process.version,platform: os.platform(),architecture: os.arch(),viewports: [[1440,1000],[390,844]]})).digest('hex');
  let cache = {schema_version: 1, entries: {}};
  try {const loaded=JSON.parse(fs.readFileSync(cachePath,'utf8'));if(loaded.schema_version===1 && loaded.entries && typeof loaded.entries==='object')cache=loaded;} catch {}
  const old = cache.entries[key];
  if (!forced && browserIdentity && reusable(old, key, scope)) {
    await cheapPackageCheck(target, receiptPath, previous);
    previous.browser_check = {state: 'reused', checked_at: new Date().toISOString(),
      baseline_key: key, baseline_checked_at: old.checked_at,
      scope: 'Current page/local file identity/HTTP HEAD/range/text checks;player seek/play/copy/layout regression reused,not rerun'};
    fs.writeFileSync(receiptPath, JSON.stringify(previous,null,2)+'\n');
    console.log('PASS: package checks;reused shared player baseline;no browser launched,seek/play/download/clipboard not repeated');
    return;
  }
  // A failed forced/new-scope regression must not leave a reusable passing claim.
  delete cache.entries[key];
  saveCache(cachePath,cache);
  previous.browser_check = 'pending';
  fs.writeFileSync(receiptPath, JSON.stringify(previous, null, 2) + '\n');
  const browser = await chromium.launch({headless: true, channel: 'chrome'});
  try {
    const page = await browser.newPage({viewport: {width: 1440, height: 1000}});
    const response = await page.goto(url);
    if (response.status() !== 200) throw Error('Review page unavailable');
    const receipt = JSON.parse(fs.readFileSync(receiptPath, 'utf8'));
    if (crypto.createHash('sha256').update(await response.body()).digest('hex') !== receipt.page_sha256)
      throw Error('Page changed since build');
    for (const file of receipt.files) {
      const asset = new URL(file.path.split('/').map(encodeURIComponent).join('/'), url);
      // Complete-film assets can exceed 600 MB; allow the verified local
      // download to finish instead of inheriting Playwright's 30 s default.
      const result = await page.request.get(asset.href, {timeout: 180000});
      if (!result.ok()) throw Error('Unavailable asset: ' + file.path);
      const bytes = await result.body();
      if (crypto.createHash('sha256').update(bytes).digest('hex') !== file.sha256)
        throw Error('HTTP bytes differ: ' + file.path);
      if (['copy', 'subtitles'].includes(file.role) && !/charset=utf-8/i.test(result.headers()['content-type']))
        throw Error('Missing UTF-8 response charset');
      await result.dispose();
    }
    const videos = page.locator('video');
    if (!await videos.count()) throw Error('No videos');
    for (let i = 0; i < await videos.count(); i++) {
      const v = videos.nth(i);
      await v.evaluate(el => el.load());
      await page.waitForFunction(index => {
        const el = document.querySelectorAll('video')[index];
        return Number.isFinite(el.duration) && el.duration > 0 && el.readyState >= 2;
      }, i);
      const duration = await v.evaluate(el => el.duration);
      for (const second of [duration * .7, duration * .2]) {
        await v.evaluate((el, t) => { el.currentTime = t; }, second);
        await page.waitForFunction(({index, second}) => {
          const el = document.querySelectorAll('video')[index];
          return !el.seeking && el.readyState >= 2 && Math.abs(el.currentTime - second) < .25;
        }, {index: i, second});
      }
      const start = await v.evaluate(el => { el.muted = true; return el.currentTime; });
      await v.evaluate(el => el.play());
      await page.waitForFunction(({index, start}) => document.querySelectorAll('video')[index].currentTime > start + .12, {index: i, start});
      await v.evaluate(el => el.pause());
    }
    for (const link of await page.locator('a[download]').all()) {
      const pending = page.waitForEvent('download');
      await link.click();
      const download = await pending;
      if (await download.failure()) throw Error('Browser download failed');
    }
    await page.context().grantPermissions(['clipboard-read', 'clipboard-write']);
    for (const button of await page.locator('[data-copy]').all()) {
      const id = await button.getAttribute('data-copy');
      await button.click();
      await page.waitForFunction(id => [...document.querySelectorAll('[data-copy]')]
        .some(button => button.dataset.copy === id && button.dataset.copied === 'true'), id);
      if (await button.getAttribute('data-copied') !== 'true' || !(await button.textContent()).includes('Copied'))
        throw Error('Copy confirmation missing');
      const expected = await page.locator('#' + id).textContent();
      const actual = await page.evaluate(() => navigator.clipboard.readText());
      if (expected !== actual) throw Error('Clipboard text mismatch');
    }
    const checkPortrait = async () => {
      const stage = page.locator('#tiktok .stage');
      if (await stage.count()) {
        const box = await stage.boundingBox();
        if (Math.abs(box.width / box.height - 9 / 16) > .02)
          throw Error('TikTok stage must itself be portrait');
      }
    };
    await checkPortrait();
    if(await page.locator('#youtube .stage').count() && await page.locator('#tiktok .stage').count()) {
      const y=await page.locator('#youtube .stage').boundingBox(),t=await page.locator('#tiktok .stage').boundingBox(),d=await page.locator('#download-links .files').boundingBox();
      if(Math.abs(y.height-t.height)>3 || Math.abs(y.height-d.height)>3 || !(y.x<t.x && t.x<d.x))throw Error('Desktop previews/download stack must align at equal heights');
      const youtubeCopy = page.locator('#youtube-copy');
      const tiktokCopy = page.locator('#tiktok-copy');
      if (await youtubeCopy.count() && await tiktokCopy.count()) {
        const yc = await youtubeCopy.boundingBox(), tc = await tiktokCopy.boundingBox();
        if (Math.abs(yc.x-y.x)>2 || Math.abs(tc.x-d.x)>2 || Math.abs((yc.x+yc.width)-(t.x+t.width))>3)
          throw Error('Publication columns must follow sketch alignment');
      }
    }
    await page.screenshot({path: path.join(path.dirname(receiptPath), 'review-desktop.png'), fullPage: true});
    await page.setViewportSize({width: 390, height: 844});
    await checkPortrait();
    if(await page.locator('#youtube-copy').count() && await page.locator('#tiktok-copy').count()) {
      const positions=[];
      for(const selector of ['#youtube','#tiktok','#download-links','#youtube-copy','#tiktok-copy'])positions.push((await page.locator(selector).boundingBox()).y);
      if(!positions.every((y,i)=>i===0 || y>positions[i-1]))throw Error('Mobile order must be YouTube,TikTok,downloads,YouTube copy,TikTok copy');
    }
    if (!await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth))
      throw Error('Mobile horizontal overflow');
    await page.screenshot({path: path.join(path.dirname(receiptPath), 'review-mobile.png'), fullPage: true});
    const lastDownload = page.locator('a[download]').last();
    const firstCopy = page.locator('[data-copy]').first();
    if (await lastDownload.count() && await firstCopy.count() && !await firstCopy.evaluate(el => {
      const last=[...document.querySelectorAll('a[download]')].at(-1);
      return Boolean(last.compareDocumentPosition(el) & Node.DOCUMENT_POSITION_FOLLOWING);
    })) throw Error('All downloads must precede publication copy');
    receipt.browser_check = {state: 'passed', checked_at: new Date().toISOString(),
      browser: await browser.version(), scope: 'HTTP bytes/UTF8, forward/backward seek, resumed playback, browser downloads, clipboard, desktop/mobile layout'};
    fs.writeFileSync(receiptPath, JSON.stringify(receipt, null, 2) + '\n');
    cache.entries[key] = {state: 'passed',key,checked_at: receipt.browser_check.checked_at,
      browser: receipt.browser_check.browser,
      platforms: [...new Set([...(Array.isArray(old?.platforms) ? old.platforms : []),...scope.platforms])],copy: Boolean(scope.copy || old?.copy),
      scope: 'Full seek/play/download/clipboard/desktop-mobile layout regression',receipt: path.resolve(receiptPath)};
    saveCache(cachePath,cache);
    console.log('PASS: full delivery browser regression;shared player baseline saved');
  } finally {
    await browser.close();
  }
}
function hashFile(file) {return crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');}
function reusable(entry,key,scope) {
  return Boolean(entry && entry.state==='passed' && entry.key===key && typeof entry.checked_at==='string' &&
    Array.isArray(entry.platforms) && scope.platforms.every(p=>entry.platforms.includes(p)) && (!scope.copy || entry.copy===true));
}
function saveCache(file,value) {
  fs.mkdirSync(path.dirname(file),{recursive:true});
  const tmp=file+'.'+process.pid+'.tmp';
  fs.writeFileSync(tmp,JSON.stringify(value,null,2)+'\n',{flag:'wx'});fs.renameSync(tmp,file);
}
async function cheapPackageCheck(target, receiptPath, receipt) {
  const response=await fetch(target,{signal:AbortSignal.timeout(30000)});
  if(!response.ok || crypto.createHash('sha256').update(Buffer.from(await response.arrayBuffer())).digest('hex')!==receipt.page_sha256)
    throw Error('Current review page differs from its receipt');
  const root=fs.realpathSync(path.dirname(receiptPath));
  for(const file of receipt.files) {
    const local=fs.realpathSync(path.resolve(root,file.path));
    const relative=path.relative(root,local);
    if(relative.startsWith('..') || path.isAbsolute(relative))throw Error('Asset escaped package');
    const st=fs.statSync(local,{bigint:true});
    const identity=file.identity;
    if(Number(st.size)!==file.bytes)throw Error('Local asset size changed: '+file.path);
    if(!identity || identity.mtime_ns!==st.mtimeNs.toString() || identity.inode!==st.ino.toString() || identity.device!==st.dev.toString()) {
      const hash=crypto.createHash('sha256');for await(const block of fs.createReadStream(local))hash.update(block);
      if(hash.digest('hex')!==file.sha256)throw Error('Local asset hash changed: '+file.path);
    }
    const asset=new URL(file.path.split('/').map(encodeURIComponent).join('/'),target);
    const head=await fetch(asset,{method:'HEAD',signal:AbortSignal.timeout(30000)});
    if(head.status!==200 || Number(head.headers.get('content-length'))!==file.bytes)throw Error('Asset HEAD failed: '+file.path);
    if(file.role==='video') {
      const end=Math.min(63,file.bytes-1);const range=await fetch(asset,{headers:{Range:'bytes=0-'+end},signal:AbortSignal.timeout(30000)});
      if(range.status!==206 || range.headers.get('content-range')!==`bytes 0-${end}/${file.bytes}`)throw Error('Video byte-range failed');
      const got=Buffer.from(await range.arrayBuffer());const expected=Buffer.alloc(end+1);const fd=fs.openSync(local,'r');
      try{fs.readSync(fd,expected,0,end+1,0);}finally{fs.closeSync(fd);}
      if(!got.equals(expected))throw Error('Served video range differs from local bytes');
    } else if(['copy','subtitles'].includes(file.role)) {
      const text=await fetch(asset,{signal:AbortSignal.timeout(30000)});
      if(!text.ok || !/charset=utf-8/i.test(text.headers.get('content-type')||'') ||
        crypto.createHash('sha256').update(Buffer.from(await text.arrayBuffer())).digest('hex')!==file.sha256)throw Error('Text asset differs or lacks UTF-8');
    }
  }
}
module.exports={reusable};
if(require.main===module)main().catch(e => {console.error(e); process.exitCode = 1});
