// Reuse an installed Playwright: set PLAYWRIGHT_MODULE to its package directory.
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const fs=require('fs'),path=require('path'),assert=require('assert/strict');
(async()=>{
 const root=path.resolve(__dirname,'..'),output=path.join(root,'.local');fs.mkdirSync(output,{recursive:true});
 const data=JSON.parse(fs.readFileSync(path.join(root,'data/catalog.json'),'utf8'));
 const base=(process.env.TEST_URL||'http://127.0.0.1:3410').replace(/\/$/,'');
 const browser=await chromium.launch({headless:true});
 const ctx=await browser.newContext({viewport:{width:1440,height:1050}}),page=await ctx.newPage(),errors=[],checks=[];
 page.on('pageerror',e=>errors.push(String(e)));
 const test=name=>checks.push(name),total=async n=>assert.equal(await page.locator('#count').innerText(),String(n));
 try{
 await page.goto(base,{waitUntil:'networkidle'});await total(300);assert.equal(await page.locator('.card:visible').count(),24);test('300 entries / first 24 rendered');
 await page.screenshot({path:path.join(output,'desktop.png'),fullPage:false});
 const first=await page.locator('.card:visible h2').first().innerText();await page.locator('#next').click();assert.notEqual(await page.locator('.card:visible h2').first().innerText(),first);assert.ok(page.url().includes('page=2'));
 await page.reload();assert.equal(await page.locator('#page-label').innerText(),'2 / 13');await page.locator('#previous').click();assert.equal(await page.locator('.card:visible h2').first().innerText(),first);test('pagination and reload state');
 await page.locator('[data-kind="Skill"]').click();await total(287);await page.locator('[data-kind="插件"]').click();await total(13);assert.equal(await page.locator('.card:visible').count(),13);test('individual skills / plugins toggle');
 for(const source of ['panrui','anthropic','l0cka','thu']){await page.locator('#clear-filters').click();await page.locator('#source').selectOption(source);await total(data.filter(x=>x.sourceId===source).length);}test('four source filters');
 await page.locator('#clear-filters').click();await page.locator('#query').fill('NDA');assert.ok((await page.locator('.card:visible').count())>0);test('NDA keyword search');
 await page.locator('#publisher').selectOption('协会');await total(0);assert.equal(await page.locator('#empty').isVisible(),true);test('combined filters / empty state');
 await page.locator('#clear-filters').click();await total(300);test('reset');
 await page.locator('#query').fill('争议焦点');assert.ok((await page.locator('.card:visible').count())>0);test('Chinese task search');
 await page.locator('#clear-filters').click();await page.locator('#material').selectOption('司法解释');assert.ok((await page.locator('.card:visible').count())>0);
 await page.reload();assert.equal(await page.locator('#material').inputValue(),'司法解释');test('material filter / URL restoration');
 await page.locator('#clear-filters').click();await page.locator('#access').selectOption('仓库快照');await total(262);test('262 entries with licensed full archives');
 await page.locator('#clear-filters').click();await page.locator('#query').fill('<img src=x onerror=alert(1)>');await total(0);test('query handled as text');
 await page.goto(base+'/US/index.html');assert.equal(await page.locator('html').getAttribute('lang'),'en');await total(58);test('58 US entries / English page');
 await page.goto(base+'/publishers.html');assert.equal(await page.locator('.sources-group').count(),5);assert.equal(await page.locator('.source-row').count(),19);test('publisher groups / one row per source');
 await page.goto(base+'/references.html');assert.equal(await page.locator('.source-row').count(),15);test('15 references separate from skill counts');
 const nda=data.find(x=>x.sourceId==='anthropic'&&x.kind==='Skill'&&x.originalName==='nda-review');assert.ok(nda);
 await page.goto(base+'/resources/'+nda.id+'.html');const text=await page.locator('body').innerText();assert.ok(text.includes('Apache-2.0')&&text.includes(nda.sourceCommit));test('skill provenance / pinned file / license');
 const plugin=data.find(x=>x.id===nda.pluginId);assert.ok(plugin);await page.goto(base+'/resources/'+plugin.id+'.html');assert.equal(await page.locator('.member-list li').count(),plugin.members.length);test('plugin members directly linked');
 await page.setViewportSize({width:390,height:844});await page.goto(base);assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);await page.screenshot({path:path.join(output,'mobile.png'),fullPage:false});test('mobile viewport no overflow');
 await page.locator('#task').selectOption('合规');assert.ok((await page.locator('.card:visible').count())>0);test('mobile filters');
 const nojs=await browser.newContext({javaScriptEnabled:false}),p=await nojs.newPage();await p.goto(base);assert.equal(await p.locator('.card').count(),300);assert.equal(await p.locator('.card h2 a').count(),300);test('300 static entries crawlable without JavaScript');await nojs.close();
 assert.deepEqual(errors,[]);test('no browser runtime errors');
 const result={date:'2026-11-02',base,status:'passed',checks};fs.writeFileSync(path.join(output,'browser-check.json'),JSON.stringify(result,null,2));console.log(JSON.stringify(result));
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exit(1)});
