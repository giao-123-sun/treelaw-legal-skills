// Reuse an installed Playwright: set PLAYWRIGHT_MODULE to its package directory.
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const fs=require('fs');const path=require('path');const assert=require('assert/strict');
(async()=>{
 const root=path.resolve(__dirname,'..'), output=path.join(root,'.local');fs.mkdirSync(output,{recursive:true});
 const base=process.env.TEST_URL||'http://127.0.0.1:3410';
 const browser=await chromium.launch({headless:true});
 const ctx=await browser.newContext({viewport:{width:1440,height:1050}});const page=await ctx.newPage();const errors=[];page.on('pageerror',e=>errors.push(String(e)));
 const checks=[];const test=(name)=>checks.push(name);
 try{
 await page.goto(base,{waitUntil:'networkidle'});assert.equal(await page.locator('.card:visible').count(),24);test('24 resources rendered');
 await page.screenshot({path:path.join(output,'desktop.png'),fullPage:false});
 await page.locator('#query').fill('NDA');assert.ok((await page.locator('.card:visible').count())>0);test('NDA keyword search');
 await page.locator('#publisher').selectOption('协会');assert.equal(await page.locator('.card:visible').count(),0);assert.equal(await page.locator('#empty').isVisible(),true);test('combined filters / empty state');
 await page.locator('#clear-filters').click();assert.equal(await page.locator('.card:visible').count(),24);test('reset');
 await page.locator('#material').selectOption('司法解释');assert.ok((await page.locator('.card:visible').count())>0);test('judicial interpretation material filter');
 await page.reload();assert.equal(await page.locator('#material').inputValue(),'司法解释');test('URL state restoration');
 await page.locator('#clear-filters').click();await page.locator('#access').selectOption('仓库快照');assert.equal(await page.locator('.card:visible').count(),9);test('three archives and six shared subskills');
 await page.locator('#clear-filters').click();await page.locator('#query').fill('<img src=x onerror=alert(1)>');assert.equal(await page.locator('.card:visible').count(),0);test('query handled as text');
 await page.goto(base+'/US/index.html');assert.equal(await page.locator('html').getAttribute('lang'),'en');assert.equal(await page.locator('.card:visible').count(),14);test('US English page');
 await page.goto(base+'/publishers.html');assert.equal(await page.locator('.sources-group').count(),5);assert.equal(await page.locator('.source-row').count(),18);test('publisher groups deduplicate subskills');
 await page.goto(base+'/resources/anthropic-nda-review.html');assert.ok(await page.locator('body').innerText().then(t=>t.includes('Apache-2.0')));test('resource provenance and license');
 await page.setViewportSize({width:390,height:844});await page.goto(base);assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);await page.screenshot({path:path.join(output,'mobile.png'),fullPage:false});test('mobile viewport no overflow');
 await page.locator('#task').selectOption('合规');assert.ok((await page.locator('.card:visible').count())>0);test('mobile filters');
 const nojs=await browser.newContext({javaScriptEnabled:false});const p=await nojs.newPage();await p.goto(base);assert.equal(await p.locator('.card').count(),24);assert.equal(await p.locator('.card h2 a').count(),24);test('no-JavaScript crawlable content');await nojs.close();
 assert.deepEqual(errors,[]);test('no browser runtime errors');
 fs.writeFileSync(path.join(output,'browser-check.json'),JSON.stringify({date:'2026-11-02',base,status:'passed',checks},null,2));console.log(JSON.stringify({status:'passed',checks}));
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exit(1)});
