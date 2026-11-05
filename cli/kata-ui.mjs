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
// or $KATA_BASE), --force, --dry-run. Zero dependencies; Node 18+.
import { mkdir, writeFile, access, lstat } from 'node:fs/promises';
import { dirname, join, resolve, relative, isAbsolute, sep } from 'node:path';

const argv = process.argv.slice(2);
let DIR = 'kata';
let BASE = (process.env.KATA_BASE || 'https://kata-ui.dev').replace(/\/$/, '');
let FORCE = false;
let DRY_RUN = false;
const rest = [];
for (let i = 0; i < argv.length; i++) {
  if (argv[i] === '--dir') DIR = argv[++i];
  else if (argv[i] === '--base') BASE = String(argv[++i]).replace(/\/$/, '');
  else if (argv[i] === '--force') FORCE = true;
  else if (argv[i] === '--dry-run') DRY_RUN = true;
  else rest.push(argv[i]);
}
const ROOT = resolve(DIR);
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

// Registry paths are untrusted input. Keep every write inside --dir and
// reject symlinks so an existing project cannot redirect an install elsewhere.
function safeDestination(relPath) {
  if (typeof relPath !== 'string' || !relPath || relPath.includes('\0') || isAbsolute(relPath)) {
    throw new Error('unsafe registry path: ' + String(relPath));
  }
  const parts = relPath.split(/[\\/]+/);
  if (parts.some((part) => !part || part === '.' || part === '..')) {
    throw new Error('unsafe registry path: ' + relPath);
  }
  const dest = resolve(ROOT, ...parts);
  const fromRoot = relative(ROOT, dest);
  if (!fromRoot || fromRoot === '..' || fromRoot.startsWith('..' + sep) || isAbsolute(fromRoot)) {
    throw new Error('registry path escapes --dir: ' + relPath);
  }
  return { dest, parts };
}

async function ensureSafeParents(parts) {
  if (DRY_RUN) return;
  await mkdir(ROOT, { recursive: true });
  const rootStat = await lstat(ROOT);
  if (rootStat.isSymbolicLink() || !rootStat.isDirectory()) {
    throw new Error('install root must be a real directory, not a symlink or file: ' + ROOT);
  }
  let current = ROOT;
  for (const part of parts.slice(0, -1)) {
    current = join(current, part);
    try {
      const st = await lstat(current);
      if (st.isSymbolicLink()) throw new Error('refusing to follow symlink: ' + current);
      if (!st.isDirectory()) throw new Error('not a directory: ' + current);
    } catch (e) {
      if (e.code !== 'ENOENT') throw e;
      await mkdir(current);
    }
  }
}

async function put(relPath, content) {
  const { dest, parts } = safeDestination(relPath);
  await ensureSafeParents(parts);
  try {
    const st = await lstat(dest);
    if (st.isSymbolicLink()) throw new Error('refusing to replace symlink: ' + dest);
    if (!st.isFile()) throw new Error('refusing to replace non-file: ' + dest);
    if (!FORCE) {
      console.error('  ! exists (not overwritten): ' + dest + ' — use --force to replace');
      process.exitCode = 1;
      return;
    }
  } catch (e) {
    if (e.code !== 'ENOENT') throw e;
  }
  if (DRY_RUN) {
    console.log('  ' + (await exists(dest) ? '~ ' : '+ ') + dest);
    return;
  }
  await writeFile(dest, content);
  console.log('  ' + (FORCE ? '~ ' : '+ ') + dest);
}
async function ensureTokens() {
  if (await exists(join(ROOT, 'tokens.css'))) return;
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
    'Options: --dir <folder> (default kata), --base <url>, --force, --dry-run',
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
