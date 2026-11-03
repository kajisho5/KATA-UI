#!/usr/bin/env node
// kataui — install KATA UI parts from the registry into your project.
// Zero dependencies; Node 18+. Existing files are protected by default.
import {
  mkdir, writeFile, access, readFile, lstat, rename, copyFile, rm
} from 'node:fs/promises';
import { dirname, isAbsolute, relative, resolve, sep, join } from 'node:path';
import { randomUUID } from 'node:crypto';

const argv = process.argv.slice(2);
let DIR = 'kata';
let BASE = (process.env.KATA_BASE || 'https://kata-ui.dev').replace(/\/$/, '');
let FORCE = false;
let DRY_RUN = false;
let BACKUP = false;
const rest = [];
for (let i = 0; i < argv.length; i++) {
  if (argv[i] === '--dir') {
    if (!argv[i + 1]) throw new Error('--dir requires a path');
    DIR = argv[++i];
  } else if (argv[i] === '--base') {
    if (!argv[i + 1]) throw new Error('--base requires a URL');
    BASE = String(argv[++i]).replace(/\/$/, '');
  } else if (argv[i] === '--force') FORCE = true;
  else if (argv[i] === '--dry-run') DRY_RUN = true;
  else if (argv[i] === '--backup') BACKUP = true;
  else rest.push(argv[i]);
}
const VERSION = '1.1.0';
const cmd = rest[0];
const positional = rest.slice(1);
const ROOT = resolve(DIR);

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
  if (!data || !Array.isArray(data.items)) throw new Error('invalid registry: expected an items array');
  return data.items;
}
async function exists(p) {
  try { await lstat(p); return true; } catch (e) {
    if (e.code === 'ENOENT') return false;
    throw e;
  }
}
function safeDestination(relPath) {
  if (typeof relPath !== 'string' || !relPath || relPath.includes('\\0') || isAbsolute(relPath)) {
    throw new Error('unsafe registry path: ' + String(relPath));
  }
  const dest = resolve(ROOT, relPath);
  const rel = relative(ROOT, dest);
  if (!rel || rel === '..' || rel.startsWith('..' + sep) || isAbsolute(rel)) {
    throw new Error('registry path escapes output directory: ' + relPath);
  }
  return dest;
}
async function assertNoSymlinkPath(dest) {
  const rel = relative(ROOT, dest);
  let cursor = ROOT;
  for (const part of rel.split(sep)) {
    cursor = join(cursor, part);
    if (!(await exists(cursor))) continue;
    const st = await lstat(cursor);
    if (st.isSymbolicLink()) throw new Error('refusing to write through symlink: ' + cursor);
  }
}
async function collectFiles(items, names) {
  const seen = new Set();
  const files = new Map();
  async function addOne(name) {
    if (seen.has(name)) return;
    const item = items.find(i => i.name === name) || items.find(i => i.name === 'theme-' + name);
    if (!item) throw new Error('unknown part: ' + name + ' (run "kataui list")');
    if (!Array.isArray(item.files)) throw new Error('invalid registry item (missing files): ' + name);
    seen.add(name);
    for (const dep of item.dependencies || []) await addOne(dep);
    const html = item.files.filter(f => typeof f.path === 'string' && f.path.endsWith('.html')).map(f => f.content || '').join('\n');
    for (const m of html.matchAll(/\/components\/([a-z0-9-]+)\/\1\.css/g)) {
      if (m[1] !== name) await addOne(m[1]);
    }
    for (const f of item.files) {
      if (typeof f.content !== 'string') throw new Error('invalid file content in registry item: ' + name);
      const dest = safeDestination(f.path);
      files.set(dest, { path: f.path, content: f.content });
    }
  }
  for (const name of names) await addOne(name);
  return files;
}
async function addTokens(files) {
  const dest = safeDestination('tokens.css');
  if (files.has(dest)) return;
  files.set(dest, { path: 'tokens.css', content: await getText(BASE + '/tokens.css') });
}
async function commitFiles(files) {
  const conflicts = [];
  for (const [dest, file] of files) {
    await assertNoSymlinkPath(dest);
    if (await exists(dest)) conflicts.push(file.path);
  }
  if (conflicts.length && !FORCE) {
    throw new Error('existing files were not changed:\n' + conflicts.map(p => '  - ' + p).join('\n') +
      '\nUse --force to overwrite, or --dry-run to preview the plan.');
  }
  for (const file of files.values()) {
    const dest = safeDestination(file.path);
    console.log((await exists(dest) ? (FORCE ? '~ ' : '= ') : '+ ') + dest);
  }
  if (DRY_RUN) {
    console.log('dry-run: no files written');
    return;
  }
  // Stage every output first. A failed download or staging write cannot leave a partial install.
  const staged = [];
  const originals = new Map();
  const committed = [];
  try {
    for (const file of files.values()) {
      const dest = safeDestination(file.path);
      await mkdir(dirname(dest), { recursive: true });
      await assertNoSymlinkPath(dest);
      const temp = dest + '.kataui-' + randomUUID() + '.tmp';
      await writeFile(temp, file.content, { flag: 'wx' });
      staged.push({ dest, temp });
    }
    // Recheck and snapshot every destination before the first replacement.
    for (const entry of staged) {
      await assertNoSymlinkPath(entry.dest);
      if (await exists(entry.dest)) {
        if (!FORCE) throw new Error('file appeared during install: ' + entry.dest);
        const previous = await readFile(entry.dest);
        originals.set(entry.dest, previous);
        if (BACKUP) await copyFile(entry.dest, entry.dest + '.bak');
      } else {
        originals.set(entry.dest, null);
      }
    }
    for (const entry of staged) {
      await rename(entry.temp, entry.dest);
      committed.push(entry.dest);
    }
  } catch (e) {
    // Roll back destinations already replaced so a failed batch does not leave a partial install.
    for (const dest of committed.reverse()) {
      const previous = originals.get(dest);
      if (previous === null) await rm(dest, { force: true }).catch(() => {});
      else await writeFile(dest, previous).catch(() => {});
    }
    await Promise.all(staged.map(x => rm(x.temp, { force: true }).catch(() => {})));
    throw e;
  }
  console.log('written ' + staged.length + ' file(s)');
}
function usage() {
  console.log([
    'kataui — install KATA UI parts from the registry',
    '',
    '  kataui init              write the design tokens',
    '  kataui add <name...>     add parts (components, blocks, templates, themes)',
    '  kataui list              list every part',
    '',
    'Options: --dir <folder>, --base <url>, --dry-run, --force, --backup',
    '--force overwrites existing files; --backup saves overwritten files as .bak.',
    '--dry-run prints the plan without writing files.',
    'Docs: https://kata-ui.dev/docs/cli/',
  ].join('\n'));
}

try {
  if (cmd === 'version' || cmd === '--version' || cmd === '-v') {
    console.log('kataui ' + VERSION);
  } else if (cmd === 'init') {
    const files = new Map([[safeDestination('tokens.css'), {
      path: 'tokens.css', content: await getText(BASE + '/tokens.css')
    }]]);
    await commitFiles(files);
  } else if (cmd === 'add') {
    if (!positional.length) throw new Error('add needs at least one name');
    const items = await loadRegistry();
    const files = await collectFiles(items, positional);
    await addTokens(files);
    await commitFiles(files);
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
