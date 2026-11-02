// KATA UI icon renderer — rasterizes the real logo geometry (extracted from
// logo/favicon.svg) into the PNG/ICO set the site ships. Run: node render-icons.js
const { chromium } = require('playwright');
const net = require('net');
const fs = require('fs');
const path = require('path');

function startForwarder(upstreamHost, upstreamPort) {
  return new Promise(resolve => {
    const server = net.createServer(client => {
      client.once('data', first => {
        const line = first.toString('latin1').split('\r\n')[0];
        const m = line.match(/^CONNECT\s+(\S+)\s+HTTP/i);
        if (!m) { client.end('HTTP/1.1 405\r\n\r\n'); return; }
        const target = m[1];
        const upstream = net.connect(upstreamPort, upstreamHost, () => {
          upstream.write(`CONNECT ${target} HTTP/1.1\r\nHost: ${target}\r\n\r\n`);
        });
        let buf = Buffer.alloc(0);
        const onData = chunk => {
          buf = Buffer.concat([buf, chunk]);
          const idx = buf.indexOf('\r\n\r\n');
          if (idx === -1) return;
          upstream.off('data', onData);
          const header = buf.slice(0, idx).toString('latin1');
          const rest = buf.slice(idx + 4);
          if (/ 200 /.test(header.split('\r\n')[0] + ' ')) {
            client.write('HTTP/1.1 200 Connection Established\r\n\r\n');
            if (rest.length) client.write(rest);
            upstream.pipe(client); client.pipe(upstream);
          } else { client.end('HTTP/1.1 502\r\n\r\n'); upstream.end(); }
        };
        upstream.on('data', onData);
        upstream.on('error', () => client.destroy());
        client.on('error', () => upstream.destroy());
      });
    });
    server.listen(0, '127.0.0.1', () => resolve(server));
  });
}

async function main() {
  const here = __dirname;
  const fav = fs.readFileSync(path.join(here, 'favicon.svg'), 'utf8');
  const rects = (fav.match(/<rect[^>]*\/>/g) || []).filter(r => !/width="40"/.test(r)).join('');
  if (!rects) throw new Error('no mark rects found in favicon.svg');
  const centered = s => `<g transform="translate(24 24) scale(${s}) translate(-24 -24)">${rects}</g>`;
  const fullbleed = s => `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48"><rect width="48" height="48" fill="#18181b"/>${centered(s)}</svg>`;
  const variants = [
    { id: 'v512', svg: fullbleed(1.16), size: 512, out: 'icon-512.png' },
    { id: 'v192', svg: fullbleed(1.16), size: 192, out: 'icon-192.png' },
    { id: 'v180', svg: fullbleed(1.16), size: 180, out: 'apple-touch-icon.png' },
    { id: 'vmask', svg: fullbleed(0.86), size: 512, out: 'icon-maskable-512.png' },
    { id: 'r48', svg: fav, size: 48, out: '/tmp/fav48.png' },
    { id: 'r32', svg: fav, size: 32, out: '/tmp/fav32.png' },
    { id: 'r16', svg: fav, size: 16, out: '/tmp/fav16.png' },
  ];
  const cells = variants.map(v =>
    `<div class="cell" id="${v.id}" style="width:${v.size}px;height:${v.size}px">${v.svg.replace('<svg ', `<svg width="${v.size}" height="${v.size}" `)}</div>`).join('');
  const html = `<!doctype html><html><head><meta charset="utf-8"><style>*{margin:0;padding:0}body{background:transparent}.cell{margin:6px}svg{display:block}</style></head><body>${cells}</body></html>`;

  let fwd = null; const launchOpts = {};
  const proxyUrl = process.env.https_proxy || process.env.HTTPS_PROXY || process.env.http_proxy;
  if (proxyUrl) {
    const u = new URL(proxyUrl);
    fwd = await startForwarder(u.hostname, parseInt(u.port || '3128', 10));
    launchOpts.proxy = { server: `http://127.0.0.1:${fwd.address().port}` };
  }
  const browser = await chromium.launch(launchOpts);
  const page = await browser.newPage({ viewport: { width: 700, height: 1600 } });
  await page.setContent(html, { waitUntil: 'load' });
  await page.waitForTimeout(300);
  for (const v of variants) {
    const el = await page.$('#' + v.id);
    const dest = v.out.startsWith('/') ? v.out : path.join(here, v.out);
    await el.screenshot({ path: dest, omitBackground: true });
    console.log('wrote', dest);
  }
  // OGP card
  const ogpHtml = fs.readFileSync(path.join(here, 'ogp.html'), 'utf8');
  const p2 = await browser.newPage({ viewport: { width: 1200, height: 630 } });
  await p2.goto('file://' + path.join(here, 'ogp.html'), { waitUntil: 'networkidle', timeout: 45000 }).catch(() => {});
  await p2.waitForTimeout(1200);
  await p2.screenshot({ path: path.join(here, 'ogp.png') });
  console.log('wrote ogp.png');
  await browser.close();
  if (fwd) fwd.close();
}
main().catch(e => { console.error(e); process.exit(1); });
