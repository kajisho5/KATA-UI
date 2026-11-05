#!/usr/bin/env node
// kataui — install KATA UI parts from the registry into your project.
// Zero dependencies; Node 18+. Existing files are protected by default.
import {
  mkdir, writeFile, readFile, lstat, rename, copyFile, rm, chmod
} from 'node:fs/promises';
import { dirname, isAbsolute, relative, resolve, sep, join } from 'node:path';
import { randomUUID } from 'node:crypto';
import { constants } from 'node:fs';

const argv = process.argv.slice(2);
let DIR = 'kata';
let BASE = (process.env.KATA_BASE || 'https://kata-ui.dev').replace(/\/$/, '');
let FORCE = false;
let DRY_RUN = false;
let BACKUP = false;
const rest = [];
try {
for (let i = 0; i < argv.length; i++) {
  if (argv[i] === '--dir') {
    if (!argv[i + 1] || argv[i + 1].startsWith('--')) throw new Error('--dir requires a path');
    DIR = argv[++i];
  } else if (argv[i] === '--base') {
    if (!argv[i + 1] || argv[i + 1].startsWith('--')) throw new Error('--base requires a URL');
    BASE = String(argv[++i]).replace(/\/$/, '');
  } else if (argv[i] === '--force') FORCE = true;
  else if (argv[i] === '--dry-run') DRY_RUN = true;
  else if (argv[i] === '--backup') BACKUP = true;
  else if (argv[i].startsWith('--') && !['--help','--version'].includes(argv[i])) throw new Error('unknown option: '+argv[i]);
  else rest.push(argv[i]);
}
if (BACKUP && !FORCE) throw new Error('--backup requires --force');
if (!/^https?:$/.test(new URL(BASE).protocol)) throw new Error('--base must use http or https');
} catch (error) { console.error('error: '+error.message); process.exit(1); }
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
  return data;
}
async function exists(p) {
  try { await lstat(p); return true; } catch (e) {
    if (e.code === 'ENOENT') return false;
    throw e;
  }
}
// Treat registry paths as untrusted, including Windows spellings on Unix.
function safeDestination(relPath) {
  if (typeof relPath !== 'string' || !relPath || relPath.includes('\0') || relPath.includes('\\') || /^[a-z]:/i.test(relPath) || isAbsolute(relPath) || relPath.split('/').some(part => !part || part === '.' || part === '..')) throw new Error('unsafe registry path: '+String(relPath));
  const dest = resolve(ROOT, relPath), rel = relative(ROOT, dest);
  if (!rel || rel.startsWith('..'+sep) || rel==='..' || isAbsolute(rel)) throw new Error('path escapes --dir: '+relPath);
  return dest;
}
async function assertNoSymlinkPath(dest) {
  // Inspect existing ancestors too: a missing install directory may sit below a link.
  const chain=[];
  for(let cursor=dest;;cursor=dirname(cursor)) { chain.unshift(cursor); if(dirname(cursor)===cursor)break; }
  for(const cursor of chain) {
    if(!await exists(cursor))continue;
    const stat=await lstat(cursor);
    if(stat.isSymbolicLink())throw new Error('refusing symlink: '+cursor);
    if(cursor!==dest&&!stat.isDirectory())throw new Error('not a directory: '+cursor);
    if(cursor===dest&&!stat.isFile())throw new Error('destination is not a file: '+cursor);
  }
}
function moldVersion(text) {
  const first=text.replace(/^\uFEFF/,'').split(/\r?\n/,1)[0];
  if(!first.includes('KATA mold'))return 1;
  const match=first.match(/^\/\*\s*KATA mold v([1-9]\d*)(?=\s|\*)/);
  if(!match||!first.includes('*/')||!Number.isSafeInteger(+match[1]))throw new Error('invalid mold header; version cannot be determined');
  return +match[1];
}
function requiredVersion(value,fallback=1) {
  if(value===undefined)return fallback;
  if(!Number.isSafeInteger(value)||value<1)throw new Error('invalid requiresMold/moldVersion metadata');
  return value;
}
function warnMold(installed,required) {
  if(installed<required)console.error(`warning: Installed mold v${installed}; selected parts require mold >= ${required}. Review https://kata-ui.dev/docs/update-mold/ before updating tokens.css.`);
}
async function savedMold() {
  const dest=safeDestination('tokens.css');await assertNoSymlinkPath(dest);
  if(!await exists(dest))return null;
  // EACCES and other read errors propagate; never infer a version from them.
  return moldVersion(await readFile(dest,'utf8'));
}
async function backupOriginal(dest) {
  for(let index=0;;index++) {
    const backup=dest+'.bak'+(index?'.'+index:'');
    try { await copyFile(dest,backup,constants.COPYFILE_EXCL);return backup; }
    catch(error){if(error.code!=='EEXIST')throw error;}
  }
}
async function collectFiles(registry, names) {
  const items=registry.items;
  const fallback=requiredVersion(registry.moldVersion);
  let requiresMold=1;
  const seen = new Set();
  const files = new Map();
  async function addOne(name) {
    if (seen.has(name)) return;
    const item = items.find(i => i.name === name) || items.find(i => i.name === 'theme-' + name);
    if (!item) throw new Error('unknown part: ' + name + ' (run "kataui list")');
    if (!Array.isArray(item.files)) throw new Error('invalid registry item (missing files): ' + name);
    seen.add(name);
    requiresMold=Math.max(requiresMold,requiredVersion(item.requiresMold,fallback));
    for (const dep of item.dependencies || []) await addOne(dep);
    const html = item.files.filter(f => typeof f.path === 'string' && f.path.endsWith('.html')).map(f => f.content || '').join('\n');
    for (const m of html.matchAll(/\/components\/([a-z0-9-]+)\/\1\.css/g)) {
      if (m[1] !== name) await addOne(m[1]);
    }
    for (const f of item.files) {
      if (typeof f.content !== 'string') throw new Error('invalid file content in registry item: ' + name);
      if(f.path==='tokens.css')throw new Error('registry part cannot replace tokens.css');
      const dest = safeDestination(f.path);
      if(files.has(dest)&&files.get(dest).content!==f.content)throw new Error('conflicting registry files: '+f.path);
      files.set(dest, { path: f.path, content: f.content });
    }
  }
  for (const name of names) await addOne(name);
  return {files,requiresMold};
}
async function addTokens(files,requiresMold) {
  const installed=await savedMold();
  if(installed!==null){warnMold(installed,requiresMold);return;}
  const content=await getText(BASE+'/tokens.css');
  if(moldVersion(content)<requiresMold)throw new Error('downloaded tokens.css is older than selected parts require');
  files.set(safeDestination('tokens.css'),{path:'tokens.css',content});
}
async function commitFiles(files) {
  const conflicts = [];
  for (const [dest, file] of files) {
    await assertNoSymlinkPath(dest);
    if (await exists(dest)) conflicts.push(file.path);
  }
  if (conflicts.length && !FORCE && !DRY_RUN) {
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
        const mode=(await lstat(entry.dest)).mode & 0o777;
        originals.set(entry.dest, {content:previous,mode});
        await chmod(entry.temp,mode);
        if (BACKUP) await backupOriginal(entry.dest);
      } else {
        originals.set(entry.dest, null);
      }
    }
    for (const entry of staged) {
      await assertNoSymlinkPath(entry.dest);
      if(!FORCE&&await exists(entry.dest))throw new Error('file appeared during install: '+entry.dest);
      await rename(entry.temp, entry.dest);
      committed.push(entry.dest);
    }
  } catch (e) {
    // Roll back destinations already replaced so a failed batch does not leave a partial install.
    const rollbackErrors=[];
    for (const dest of committed.reverse()) {
      try {
        await assertNoSymlinkPath(dest);
        const previous=originals.get(dest);
        if(previous===null)await rm(dest,{force:true});
        else {
          const restore=dest+'.restore-'+randomUUID();
          await writeFile(restore,previous.content,{flag:'wx',mode:previous.mode});
          await chmod(restore,previous.mode);
          await rename(restore,dest);
        }
      } catch(error) {rollbackErrors.push(dest+': '+error.message);}
    }
    await Promise.all(staged.map(x => rm(x.temp, { force: true }).catch(() => {})));
    if(rollbackErrors.length)e.message+='; rollback errors: '+rollbackErrors.join('; ');
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
    '--force overwrites selected files; --backup keeps unique .bak copies. add never replaces an existing tokens.css.',
    '--dry-run prints the plan without writing files.',
    'Docs: https://kata-ui.dev/docs/cli/',
  ].join('\n'));
}

try {
  if (cmd === 'version' || cmd === '--version' || cmd === '-v') {
    console.log('kataui ' + VERSION);
  } else if (cmd === 'init') {
    const content=await getText(BASE+'/tokens.css');
    const required=moldVersion(content), installed=await savedMold();
    if(installed!==null)warnMold(installed,required);
    const files=new Map([[safeDestination('tokens.css'),{path:'tokens.css',content}]]);
    await commitFiles(files);
  } else if (cmd === 'add') {
    if (!positional.length) throw new Error('add needs at least one name');
    const registry = await loadRegistry();
    const {files,requiresMold} = await collectFiles(registry, positional);
    await addTokens(files,requiresMold);
    await commitFiles(files);
  } else if (cmd === 'list') {
    const {items} = await loadRegistry();
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
