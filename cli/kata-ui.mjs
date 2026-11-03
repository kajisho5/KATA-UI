#!/usr/bin/env node
// kataui — install KATA UI parts from the registry into your project.
//
//   node kata-ui.mjs init                 write the design tokens (kata/tokens.css)
//   node kata-ui.mjs add button select    write parts + what they depend on
//   node kata-ui.mjs add login            blocks and templates install the same way
//   node kata-ui.mjs add indigo           theme presets too
//   node kata-ui.mjs list                 every part in the registry
//
// Options: --dir <folder> (default: kata)  --base <url> (default: https://kata-ui.dev,
// or $KATA_BASE). Zero dependencies; Node 18+. The files are yours — nothing
// phones home and nothing updates itself.
import { mkdir, writeFile, access } from 'node:fs/promises';
import { dirname, join } from 'node:path';

const argv = process.argv.slice(2);
let DIR = 'kata';
let BASE = (process.env.KATA_BASE || 'https://kata-ui.dev').replace(/\/$/, '');
const rest = [];
for (let i = 0; i < argv.length; i++) {
  if (argv[i] === '--dir') DIR = argv[++i];
  else if (argv[i] === '--base') BASE = String(argv[++i]).replace(/\/$/, '');
  else rest.push(argv[i]);
}
const VERSION = '1.0.0';
const cmd = rest[0];
if (cmd === 'version' || cmd === '--version' || cmd === '-v') { console.log('kataui ' + VERSION); process.exit(0); }
const positional = rest.slice(1);

const KIND = {
  'registry:component': 'component',
  'registry:block': 'block',
  'registry:page': 'template',
  'registry:theme': 'theme',
};

async function getText(url) {
  const r = await fetch(url);
  if (!r.ok) throw new Error('fetch failed: ' + r.status + ' ' + url);
  return r.text();
}
async function loadRegistry() {
  const data = JSON.parse(await getText(BASE + '/registry.json'));
  return data.items || [];
}
async function exists(p) {
  try { await access(p); return true; } catch { return false; }
}
async function put(relPath, content) {
  const dest = join(DIR, relPath);
  await mkdir(dirname(dest), { recursive: true });
  await writeFile(dest, content);
  console.log('  + ' + dest);
}
async function ensureTokens() {
  if (await exists(join(DIR, 'tokens.css'))) return;
  await put('tokens.css', await getText(BASE + '/tokens.css'));
}

async function addOne(items, name, seen) {
  if (seen.has(name)) return;
  const item = items.find((i) => i.name === name) || items.find((i) => i.name === 'theme-' + name);
  if (!item) {
    console.error('  ! unknown part: ' + name + '  (run "kataui list")');
    process.exitCode = 1;
    return;
  }
  seen.add(name);
  for (const dep of item.dependencies || []) await addOne(items, dep, seen);
  // A part can also build on another part's CSS through its example HTML.
  const html = (item.files || []).filter((f) => f.path.endsWith('.html')).map((f) => f.content).join('\n');
  for (const m of html.matchAll(/\/components\/([a-z0-9-]+)\/\1\.css/g)) {
    if (m[1] !== name) await addOne(items, m[1], seen);
  }
  for (const f of item.files || []) await put(f.path, f.content);
  console.log('added ' + name + ' (' + (KIND[item.type] || item.type) + ')');
}

function usage() {
  console.log([
    'kataui — install KATA UI parts from the registry',
    '',
    '  kataui init              write the design tokens',
    '  kataui add <name...>     add parts (components, blocks, templates, themes)',
    '  kataui list              list every part',
    '',
    'Options: --dir <folder> (default kata), --base <url>',
    'Docs: https://kata-ui.dev/docs/cli/',
  ].join('\n'));
}

try {
  if (cmd === 'init') {
    await ensureTokens();
    console.log('ready. Load kata/tokens.css first, then add parts:  kataui add button');
  } else if (cmd === 'add') {
    if (!positional.length) { console.error('add needs at least one name'); process.exit(1); }
    const items = await loadRegistry();
    await ensureTokens();
    const seen = new Set();
    for (const name of positional) await addOne(items, name, seen);
  } else if (cmd === 'list') {
    const items = await loadRegistry();
    const groups = {};
    for (const i of items) (groups[KIND[i.type] || i.type] ||= []).push(i);
    for (const [kind, list] of Object.entries(groups)) {
      console.log('\n' + kind + 's (' + list.length + ')');
      for (const i of list) console.log('  ' + i.name.padEnd(18) + (i.title || ''));
    }
  } else {
    usage();
    if (cmd && cmd !== 'help' && cmd !== '--help') process.exitCode = 1;
  }
} catch (e) {
  console.error('error: ' + e.message);
  process.exit(1);
}
