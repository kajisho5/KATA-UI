// Run after build.py. Requires playwright and axe-core (see tools/CHECKING.md).
const fs = require('node:fs');
const path = require('node:path');
const http = require('node:http');
const { chromium } = require('playwright');
const root = path.resolve(__dirname, '..');
const registry = JSON.parse(fs.readFileSync(path.join(root, 'dist/registry.json')));
const axe = fs.readFileSync(require.resolve('axe-core/axe.min.js'), 'utf8');
const selected = process.argv.slice(2);
const items = registry.items.filter(x => x.type !== 'registry:theme' && (!selected.length || selected.includes(x.name)));
if (!items.length) throw new Error('No matching parts');
const server = http.createServer((req, res) => {
  if (req.url === '/__audit__') { res.writeHead(200, {'Content-Type':'text/html'}); return res.end('<!doctype html><title>Audit</title>'); }
  const file = path.resolve(root, '.' + decodeURIComponent(req.url.split('?')[0]));
  if (!file.startsWith(root + path.sep)) { res.writeHead(403); return res.end(); }
  fs.readFile(file, (err, data) => { res.writeHead(err ? 404 : 200, {'Content-Type': file.endsWith('.css') ? 'text/css' : file.endsWith('.js') ? 'text/javascript' : 'text/html'}); res.end(err ? '' : data); });
});
(async () => {
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  const browser = await chromium.launch(process.env.CHROMIUM_PATH ? {executablePath:process.env.CHROMIUM_PATH} : {});
  const results = [];
  try {
    fs.writeFileSync(path.join(root,'mold-browser-results.json'), JSON.stringify({complete:false, items:[]}));
    for (const item of items) {
      const page = await browser.newPage(); const errors = [];
      page.on('pageerror', error => errors.push(error.message));
      const deps = []; const seen = new Set();
      function visit(it) { if (seen.has(it.name)) return; seen.add(it.name); for (const name of it.dependencies || []) { const dep=registry.items.find(x=>x.name===name); if(dep) visit(dep); } deps.push(it); }
      visit(item);
      const files = deps.flatMap(x=>x.files);
      const html = item.files.find(x=>x.path.endsWith('.html')).content;
      await page.goto(`http://127.0.0.1:${server.address().port}/__audit__`);
      await page.setContent('<!doctype html><html lang="en"><head><title>Two-instance mold audit</title><link rel="stylesheet" href="/tokens.css">'+files.filter(x=>x.path.endsWith('.css')).map(x=>`<link rel="stylesheet" href="/${x.path}">`).join('')+'</head><body><main><h1>Two-instance audit</h1><section>'+html+'</section><section>'+html+'</section></main></body></html>');
      for (const f of files.filter(x=>x.path.endsWith('.js'))) await page.addScriptTag({content:f.content}).catch(e=>errors.push(e.message));
      await page.addScriptTag({content:axe});
      const audit = await page.evaluate(async()=>await axe.run(document, {runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa','best-practice']}}));
      const duplicateIds = await page.evaluate(()=>{const seen=new Set();return [...document.querySelectorAll('[id]')].map(e=>e.id).filter(id=>seen.has(id)||!seen.add(id));});
      results.push({id:item.name, errors, duplicateIds, violations:audit.violations, incomplete:audit.incomplete});
      fs.writeFileSync(path.join(root,'mold-browser-results.json'),JSON.stringify({complete:false,items:results},null,2)+'\n');
      console.log(item.name + ': ' + audit.violations.length + ' axe violations, ' + errors.length + ' JS errors');
      await page.close();
    }
    fs.writeFileSync(path.join(root,'mold-browser-results.json'),JSON.stringify({complete:true,items:results},null,2)+'\n');
    process.exitCode = results.some(x=>x.errors.length||x.duplicateIds.length||x.violations.length) ? 1 : 0;
  } finally { await browser.close(); server.close(); }
})().catch(error=>{console.error(error); server.close(); process.exitCode=2;});
