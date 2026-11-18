/* Real-browser checks with network request interception, using fresh profiles. */
const assert = require("assert");
const fs = require("fs");
const path = require("path");
const http = require("http");
const {pathToFileURL} = require("url");
const {chromium, firefox} = require("playwright");
const root = path.resolve(__dirname, "..");
const site = path.resolve(process.argv[2] || path.join(root, "build/rhel7/site"));
const output = path.resolve(process.argv[3] || path.join(root, "build/qa/rhel7"));
fs.mkdirSync(output, {recursive: true});
const report = {site, browsers: [], externalRequests: [], errors: []};
const expectedLanguages = JSON.parse(fs.readFileSync(path.join(site,"js/highlight-languages.json"),"utf8"));
const pages = ["index.html", "guide/installation.html", "guide/authoring.html", "guide/configuration.html",
  "guide/links.html", "guide/code-highlighting.html", "guide/styled-content.html", "guide/cheat-sheets.html", "reference/cheat-sheet.html",
  "guide/workflow.html", "guide/troubleshooting.html",
  "reference/languages.html", "reference/math.html", "reference/components.html", "reference/offline.html", "404.html"];
const mime = {".html":"text/html", ".css":"text/css", ".js":"application/javascript", ".svg":"image/svg+xml", ".woff2":"font/woff2", ".json":"application/json"};
const server = http.createServer(function (request, response) {
  const pathname = decodeURIComponent(new URL(request.url, "http://localhost").pathname);
  const file = path.resolve(site, "." + (pathname.endsWith("/") ? pathname + "index.html" : pathname));
  if (!file.startsWith(site + path.sep) || !fs.existsSync(file) || !fs.statSync(file).isFile()) {
    response.writeHead(404); response.end(); return;
  }
  response.writeHead(200, {"Content-Type": mime[path.extname(file)] || "application/octet-stream"});
  fs.createReadStream(file).pipe(response);
});
async function ready(page) {
  await page.waitForFunction(function () { return window.hljs && window.MathJax && MathJax.startup && MathJax.startup.promise; });
  await page.evaluate(function () { return MathJax.startup.promise; });
  await page.evaluate(function () { return document.fonts.ready; });
}
async function run() {
  await new Promise(resolve => server.listen(0, "127.0.0.1", resolve));
  const origin = "http://127.0.0.1:" + server.address().port;
  try {
    for (const name of ["edge", "firefox"]) {
      const browser = await (name === "edge" ? chromium.launch({channel:"msedge", headless:true}) : firefox.launch({headless:true}));
      const result = {name, version:browser.version(), protocols:[], checks:[]};
      try {
        for (const protocol of ["file", "http"]) {
          const context = await browser.newContext({viewport:{width:1440,height:960}, colorScheme:"light", serviceWorkers:"block"});
          await context.route("**/*", async route => {
            const url = route.request().url();
            if (/^https?:/.test(url) && !url.startsWith(origin + "/")) { report.externalRequests.push(url); await route.abort(); }
            else { await route.continue(); }
          });
          const page = await context.newPage();
          page.on("pageerror", error => report.errors.push(name + ": " + error.message));
          page.on("console", message => { if (message.type() === "error") { report.errors.push(name + ": " + message.text()); } });
          page.on("requestfailed", request => report.errors.push(name + ": failed " + request.url()));
          page.on("response", response => { if (response.status() >= 400) { report.errors.push(name + ": HTTP " + response.status() + " " + response.url()); } });
          const url = file => protocol === "file" ? pathToFileURL(path.join(site, file)).href : origin + "/" + file;
          for (const file of pages) {
            await page.goto(url(file));
            await ready(page);
            assert(await page.locator("main h1").count(), file + " has no heading");
            assert.strictEqual(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth), false, file + " overflows");
            assert.strictEqual(await page.locator(".offline-label, .header-caption, .page-footer").count(), 0);
          }
          await page.goto(url("guide/styled-content.html")); await ready(page);
          assert.strictEqual(await page.locator(".feature-grid .feature-card").count(), 2);
          assert.strictEqual(await page.locator('.feature-card a[href="authoring.html"]').count(), 1);
          await page.locator("details.disclosure summary").click();
          assert(await page.locator("details.disclosure").getAttribute("open") !== null);
          assert.strictEqual(await page.locator("details.disclosure strong").innerText(), "styles, scripts, fonts, and search data");
          await page.goto(url("guide/cheat-sheets.html")); await ready(page);
          assert.strictEqual(await page.locator("pre.linked-code a").count(), 4);
          const cpp = page.locator("pre.linked-code code.language-cpp");
          const cppText = "std::vector<float> ReadSamples(int count);\nbool Ready(const Buffer& buffer);";
          assert.strictEqual(await cpp.textContent(), cppText);
          assert((await cpp.locator("a").first().locator("span").count()) > 1, "Link lost syntax spans");
          await cpp.locator("a").first().focus();
          await page.keyboard.press("Enter");
          assert(page.url().endsWith("#sample-buffer"), "Keyboard code link navigation");
          // Observe the clipboard payload through either browser API without
          // replacing the user's system clipboard during the verification.
          await page.evaluate(() => {
            if (navigator.clipboard) {
              navigator.clipboard.writeText = function (value) { window.testCopiedCode = value; return Promise.resolve(); };
            }
            document.execCommand = function (command) {
              if (command === "copy") { window.testCopiedCode = document.querySelector("textarea").value; return true; }
              return false;
            };
          });
          await page.locator(".code-toolbar").filter({has:page.locator("span", {hasText:/^cpp$/})}).locator("button").click();
          assert.strictEqual(await page.evaluate(() => window.testCopiedCode), cppText, "Copy must preserve plain code");
          await page.goto(url("reference/cheat-sheet.html")); await ready(page);
          assert.strictEqual(await page.locator("body.page-wide").count(), 1);
          assert.strictEqual(await page.locator(".api-group").count(), 6);
          assert.strictEqual(await page.locator(".api-group pre a").count(), 12);
          assert(await page.locator(".page-toc").isHidden());
          assert(await page.evaluate(() => Array.from(document.querySelectorAll(".linked-code a")).every(a => document.getElementById(a.hash.slice(1)))));
          await page.locator('.linked-code a[href="#mean"]').click();
          assert(page.url().endsWith("#mean"));
          await page.setViewportSize({width:1920,height:1080});
          for (const appearance of ["light", "dark"]) {
            if (await page.locator("html").getAttribute("data-theme") !== appearance) { await page.locator("#theme-toggle").click(); }
            if (protocol === "file") {
              await page.evaluate(() => scrollTo(0,0));
              await page.screenshot({path:path.join(output,name+"-cheatsheet-"+appearance+".png")});
            }
          }
          await page.setViewportSize({width:390,height:844});
          assert.strictEqual(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth), false, "Cheat sheet mobile overflow");
          await page.setViewportSize({width:1440,height:960});
          if (await page.locator("html").getAttribute("data-theme") !== "light") { await page.locator("#theme-toggle").click(); }
          await page.goto(url("reference/languages.html"));
          await ready(page);
          for (const language of ["python","lua","c","cpp","java","fortran","bash","powershell","yaml","json","sql"]) {
            const blocks = page.locator("code.language-" + language);
            for (let i = 0; i < await blocks.count(); i++) {
              assert(await blocks.nth(i).locator("span").count() > 0, "Unhighlighted " + language);
            }
            assert(await blocks.count() > 0, "Missing " + language);
          }
          assert.deepStrictEqual(await page.evaluate(() => hljs.listLanguages().sort()), expectedLanguages);
          await page.locator("#theme-toggle").click();
          assert.strictEqual(await page.locator("html").getAttribute("data-theme"), "dark");
          await page.reload(); await ready(page);
          assert.strictEqual(await page.locator("html").getAttribute("data-theme"), "dark");
          if (protocol === "file") { await page.screenshot({path:path.join(output,name+"-languages-dark.png"),fullPage:true}); }
          await page.goto(url("reference/math.html")); await ready(page);
          assert(await page.locator("mjx-container").count() >= 22, "Math not rendered");
          assert.strictEqual(await page.locator('[data-mml-node="merror"]').count(), 0, "Math error");
          assert(!(await page.locator("main").innerText()).includes("???"), "Unresolved equation reference");
          await page.locator(".search-open").click();
          await page.locator("#search-input").fill("factorial");
          await page.waitForSelector("#search-results a");
          const link = page.locator("#search-results a").first();
          assert((await link.getAttribute("href")).includes("reference/languages.html#lua"));
          await link.click(); await ready(page);
          assert(page.url().endsWith("reference/languages.html#lua"), "Search navigation failed");
          await page.locator(".search-open").click();
          for (const query of ["installation","equations","C++","fact"]) {
            await page.locator("#search-input").fill(query);
            await page.waitForTimeout(180);
            assert(await page.locator("#search-results a").count() > 0, "No results for " + query);
            if (query === "C++") { assert((await page.locator("#search-results").innerText()).includes("C++")); }
          }
          await page.locator("#search-input").fill("zzznothingmatches987");
          await page.waitForFunction(() => document.getElementById("search-status").textContent.indexOf("No results") === 0);
          await page.keyboard.press("Escape");
          assert(await page.locator("#search-dialog").isHidden());
          await page.goto(url("index.html")); await ready(page);
          if (protocol === "file") {
            if (await page.locator("html").getAttribute("data-theme") !== "dark") { await page.locator("#theme-toggle").click(); }
            await page.screenshot({path:path.join(output,name+"-home-dark.png"),fullPage:true});
            await page.locator("#theme-toggle").click();
            await page.screenshot({path:path.join(output,name+"-home-light.png"),fullPage:true});
          }
          await page.setViewportSize({width:390,height:844});
          assert.strictEqual(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth), false, "Mobile overflow");
          await page.locator("#menu-toggle").click();
          assert.strictEqual(await page.locator("#menu-toggle").getAttribute("aria-expanded"),"true");
          await page.keyboard.press("Escape");
          if (protocol === "file") { await page.screenshot({path:path.join(output,name+"-mobile.png"),fullPage:true}); }
          await context.close();
          result.protocols.push(protocol);
          console.log("PASS " + name + " " + protocol + ": pages, math, languages, search, appearance, mobile");
        }
        const plain = await browser.newContext({javaScriptEnabled:false});
        const plainPage = await plain.newPage();
        await plainPage.goto(pathToFileURL(path.join(site,"reference/cheat-sheet.html")).href);
        await plainPage.locator('.linked-code a[href="#mean"]').click();
        assert(plainPage.url().endsWith("#mean"), "Links must work without JavaScript");
        await plain.close();
        result.checks = [pages.length + " pages","required language samples",expectedLanguages.length + " bundled languages","22 rendered math expressions",
          "cards and Markdown inside HTML","disclosures","removed labels","highlighted code links and keyboard navigation",
          "multi-token links and escaped C++","plain-text copy","wide cheat sheet and mobile layout","code links without JavaScript",
          "equation reference","direct-file search result navigation","empty search","theme toggle and reload",
          "mobile layout","no external requests","no browser errors"];
        report.browsers.push(result);
      } finally { await browser.close(); }
    }
    assert.deepStrictEqual(report.externalRequests, [], "External requests attempted");
    assert.deepStrictEqual(report.errors, [], "Browser errors");
    report.passed = true;
  } finally {
    server.close();
    fs.writeFileSync(path.join(output,"browser-report.json"),JSON.stringify(report,null,2)+"\n");
  }
}
run().catch(error => { console.error(error); process.exitCode=1; });
