// usage: node shoot.cjs <path> <outprefix> [width] [height] [actions-json]
const { chromium } = require("/Users/z.christensen/environment/node_modules/playwright");
(async () => {
  const [, , path, out, w = "1440", h = "900", acts = "[]"] = process.argv;
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: +w, height: +h } });
  const errs = [];
  page.on("pageerror", e => errs.push("pageerror: " + e.message));
  page.on("requestfailed", r => { if (!/\.mp4/.test(r.url())) errs.push("reqfail: " + r.url().slice(0, 140) + " " + (r.failure() || {}).errorText); });
  page.on("console", m => { if (m.type() === "error") errs.push("console: " + m.text()); });
  await page.goto("http://127.0.0.1:8765/" + path, { waitUntil: "load", timeout: 60000 }).catch(e => errs.push("goto: " + e.message));
  await page.waitForTimeout(1500);
  let n = 0;
  for (const a of JSON.parse(acts)) {
    if (a.scroll !== undefined) { await page.evaluate(y => window.scrollTo(0, y), a.scroll); await page.waitForTimeout(a.wait || 900); }
    if (a.hover) { await page.hover(a.hover).catch(e => errs.push("hover: " + e.message)); await page.waitForTimeout(a.wait || 900); }
    if (a.click) { await page.click(a.click).catch(e => errs.push("click: " + e.message)); await page.waitForTimeout(a.wait || 1000); }
    if (a.eval) { const r = await page.evaluate(a.eval).catch(e => "evalerr " + e.message); console.log("eval:", JSON.stringify(r)); }
    if (a.shot) { await page.screenshot({ path: `${out}-${a.shot}.png` }); n++; }
  }
  if (!n) await page.screenshot({ path: `${out}.png` });
  console.log(errs.length ? errs.join("\n") : "no errors");
  await browser.close();
})();
