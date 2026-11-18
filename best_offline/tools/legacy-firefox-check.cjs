/* Test a portable Firefox 78 ESR via its matching WebDriver; no system install. */
const fs = require("fs");
const path = require("path");
const assert = require("assert");
const {spawn} = require("child_process");
const {pathToFileURL} = require("url");
const root = path.resolve(__dirname, "..");
const legacy = path.join(root, "build/legacy-firefox");
const site = path.resolve(process.argv[2] || path.join(root, "build/rhel7/offline-site"));
const output = path.resolve(process.argv[3] || path.join(root, "build/qa/firefox78"));
const expectedLanguages = JSON.parse(fs.readFileSync(path.join(site,"js/highlight-languages.json"),"utf8"));
fs.mkdirSync(output, {recursive:true});
const driver = spawn(path.join(legacy,"driver/geckodriver.exe"), ["--host","127.0.0.1","--port","4447","--log","error"], {windowsHide:true});
const logs = [];
driver.stdout.on("data", data => logs.push(data.toString()));
driver.stderr.on("data", data => logs.push(data.toString()));
let session;
async function request(method, route, body) {
  const response = await fetch("http://127.0.0.1:4447" + route, {method, headers:{"Content-Type":"application/json"}, body:body ? JSON.stringify(body) : undefined});
  const data = await response.json();
  if (!response.ok) { throw new Error(JSON.stringify(data)); }
  return data.value;
}
async function command(route, body) { return request("POST","/session/"+session+route,body); }
async function execute(script) { return command("/execute/sync",{script,args:[]}); }
async function waitFor(script, label) {
  for (let i=0;i<100;i++) {
    if (await execute("return document.readyState === 'complete' && !!("+script+");")) { return; }
    await new Promise(resolve=>setTimeout(resolve,100));
  }
  throw new Error("Timed out: " + label);
}
async function run() {
  const report = {browser:"Firefox 78 ESR",site,pages:[],externalResources:[],checks:[]};
  try {
    for (let i=0;i<60;i++) {
      try { await request("GET","/status"); break; } catch (error) { await new Promise(resolve=>setTimeout(resolve,100)); }
    }
    const created = await request("POST","/session",{capabilities:{alwaysMatch:{
      browserName:"firefox",
      "moz:firefoxOptions":{
        binary:path.join(legacy,"firefox78/core/firefox.exe"),
        args:["-headless"],
        prefs:{"app.update.auto":false,"app.update.enabled":false,
          "network.proxy.type":1,"network.proxy.http":"127.0.0.1","network.proxy.http_port":9,
          "network.proxy.ssl":"127.0.0.1","network.proxy.ssl_port":9,
          "network.proxy.no_proxies_on":"localhost, 127.0.0.1"}
      }
    }}});
    session = created.sessionId;
    report.version = created.capabilities.browserVersion;
    await command("/window/rect",{width:1440,height:1000});
    for (const file of ["index.html","guide/installation.html","guide/authoring.html","guide/configuration.html",
      "guide/links.html","guide/code-highlighting.html","guide/styled-content.html","guide/cheat-sheets.html","reference/cheat-sheet.html",
      "guide/workflow.html","guide/troubleshooting.html",
      "reference/languages.html","reference/math.html","reference/components.html","reference/offline.html","404.html"]) {
      await command("/url",{url:pathToFileURL(path.join(site,file)).href});
      await waitFor("window.hljs && window.MathJax && MathJax.startup && MathJax.startup.document",file);
      if (file === "reference/math.html") {
        await waitFor("document.querySelectorAll('mjx-container').length >= 22","math");
        assert.strictEqual(await execute("return document.querySelectorAll('[data-mml-node=\"merror\"]').length;"),0);
      }
      if (file === "guide/styled-content.html") {
        assert.strictEqual(await execute("return document.querySelectorAll('.feature-grid .feature-card').length;"),2);
        assert.strictEqual(await execute("return document.querySelectorAll('.feature-card a[href=\"authoring.html\"]').length;"),1);
        await execute("document.querySelector('details.disclosure summary').click();");
        assert.strictEqual(await execute("return document.querySelector('details.disclosure').open;"),true);
      }
      if (file === "guide/cheat-sheets.html") {
        assert.strictEqual(await execute("return document.querySelectorAll('pre.linked-code a').length;"),4);
        assert.strictEqual(await execute("return document.querySelector('pre.linked-code code.language-cpp').textContent;"),
          "std::vector<float> ReadSamples(int count);\nbool Ready(const Buffer& buffer);");
        await execute("document.querySelector('pre.linked-code code.language-cpp a').click();");
        assert.strictEqual(await execute("return location.hash;"),"#sample-buffer");
      }
      if (file === "reference/cheat-sheet.html") {
        assert.strictEqual(await execute("return document.querySelectorAll('.api-group pre a').length;"),12);
        await execute("document.querySelector('.linked-code a[href=\"#mean\"]').click();");
        assert.strictEqual(await execute("return location.hash;"),"#mean");
        await execute("scrollTo(0,0);");
        const overview = await request("GET","/session/"+session+"/screenshot");
        fs.writeFileSync(path.join(output,"firefox78-cheatsheet.png"),Buffer.from(overview,"base64"));
      }
      assert.strictEqual(await execute("return document.querySelectorAll('.offline-label,.header-caption,.page-footer').length;"),0);
      if (file === "reference/languages.html") {
        assert.deepStrictEqual(await execute("return hljs.listLanguages().sort();"),expectedLanguages);
        const counts = await execute("return ['python','lua','c','cpp','java','fortran','bash'].map(function(x){return {language:x,count:document.querySelectorAll('code.language-'+x+' span').length};});");
        counts.forEach(item=>assert(item.count>0,"No syntax tokens for "+item.language));
        report.highlighting = counts;
      }
      const resources = await execute("return performance.getEntriesByType('resource').map(function(x){return x.name;}).filter(function(x){return /^https?:/.test(x);});");
      report.externalResources.push(...resources);
      assert.strictEqual(await execute("return document.documentElement.scrollWidth > innerWidth;"),false,"Overflow: "+file);
      report.pages.push(file);
    }
    await command("/url",{url:pathToFileURL(path.join(site,"reference/math.html")).href});
    await waitFor("window.BEST_OFFLINE_SEARCH && window.lunr","search dependencies");
    await execute("document.querySelector('.search-open').click();var i=document.getElementById('search-input');i.value='factorial';i.dispatchEvent(new Event('input'));");
    await waitFor("document.querySelector('#search-results a')","search result");
    const href = await execute("return document.querySelector('#search-results a').href;");
    assert(href.endsWith("reference/languages.html#lua"));
    await execute("document.querySelector('#search-results a').click();");
    await waitFor("location.hash === '#lua' && window.hljs","search navigation");
    await execute("document.documentElement.setAttribute('data-theme','light');document.getElementById('theme-toggle').click();");
    assert.strictEqual(await execute("return document.documentElement.getAttribute('data-theme');"),"dark");
    const screenshot = await request("GET","/session/"+session+"/screenshot");
    fs.writeFileSync(path.join(output,"firefox78-languages-dark.png"),Buffer.from(screenshot,"base64"));
    assert.deepStrictEqual(report.externalResources,[]);
    report.checks = ["direct-file pages","required language syntax tokens",expectedLanguages.length + " registered languages","math SVG",
      "clickable highlighted signatures","escaped C++ text preserved","wide cheat sheet","removed labels",
      "equation rendering without errors","nested direct-file search navigation","dark mode","no horizontal overflow",
      "no HTTP(S) resources in resource timing","outbound proxy disabled"];
    report.passed = true;
    fs.writeFileSync(path.join(output,"browser-report.json"),JSON.stringify(report,null,2)+"\n");
    console.log("PASS Firefox "+report.version+": local files, languages, math, search, dark mode");
  } finally {
    if (session) { await request("DELETE","/session/"+session).catch(()=>{}); }
    driver.kill();
    fs.writeFileSync(path.join(output,"driver.log"),logs.join(""));
  }
}
run().catch(error=>{console.error(error);process.exitCode=1;});
