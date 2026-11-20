#!/usr/bin/env node
// Render an HTML design to PNG.
// Usage: node tools/render.js <file.html> [width=1080] [height=1350] [out.png] [--transparent]
// --transparent keeps the page background see-through (for video text overlays).
const path = require('path');
const { chromium } = require('playwright');

(async () => {
  const args = process.argv.slice(2);
  const transparent = args.includes('--transparent');
  const [file, w = '1080', h = '1350', outArg] = args.filter(a => a !== '--transparent');
  if (!file) {
    console.error('Usage: node tools/render.js <file.html> [width] [height] [out.png] [--transparent]');
    process.exit(1);
  }
  const width = parseInt(w, 10), height = parseInt(h, 10);
  const abs = path.resolve(file);
  const out = outArg ? path.resolve(outArg) : abs.replace(/\.html?$/i, `-${width}x${height}.png`);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width, height }, deviceScaleFactor: 1 });
  await page.goto('file://' + abs, { waitUntil: 'networkidle', timeout: 15000 }).catch(() => {});
  await page.evaluate(() => document.fonts && document.fonts.ready);
  await page.screenshot({ path: out, clip: { x: 0, y: 0, width, height }, omitBackground: transparent });
  await browser.close();
  console.log(out);
})();
