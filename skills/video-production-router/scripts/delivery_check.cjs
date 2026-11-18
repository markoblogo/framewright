#!/usr/bin/env node
// Reusable real-browser check. Requires an existing Playwright installation.
const fs = require('node:fs');
const crypto = require('node:crypto');
const path = require('node:path');
const {createRequire} = require('node:module');

async function main() {
  const [url, receiptPath, playwrightPath] = process.argv.slice(2);
  if (!url || !receiptPath || !playwrightPath) throw Error('Usage: delivery_check.cjs URL RECEIPT PLAYWRIGHT_PACKAGE_JSON');
  const target = new URL(url);
  if (!['127.0.0.1', 'localhost'].includes(target.hostname) || target.protocol !== 'http:')
    throw Error('Expected a loopback HTTP review URL');
  const {chromium} = createRequire(path.resolve(playwrightPath))('playwright');
  const previous = JSON.parse(fs.readFileSync(receiptPath, 'utf8'));
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
      if (await button.getAttribute('data-copied') !== 'true' || !(await button.textContent()).includes('Скопировано'))
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
    await page.screenshot({path: path.join(path.dirname(receiptPath), 'review-desktop.png'), fullPage: true});
    await page.setViewportSize({width: 390, height: 844});
    await checkPortrait();
    if (!await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth))
      throw Error('Mobile horizontal overflow');
    await page.screenshot({path: path.join(path.dirname(receiptPath), 'review-mobile.png'), fullPage: true});
    receipt.browser_check = {state: 'passed', checked_at: new Date().toISOString(),
      browser: await browser.version(), scope: 'HTTP bytes/UTF8, forward/backward seek, resumed playback, browser downloads, clipboard, desktop/mobile layout'};
    fs.writeFileSync(receiptPath, JSON.stringify(receipt, null, 2) + '\n');
    console.log('PASS: delivery browser checks');
  } finally {
    await browser.close();
  }
}
main().catch(e => {console.error(e); process.exitCode = 1});
