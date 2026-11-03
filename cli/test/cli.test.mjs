import { after, before, test } from 'node:test';
import assert from 'node:assert/strict';
import { createServer } from 'node:http';
import { mkdtemp, mkdir, readFile, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
const execFileAsync = promisify(execFile);

const CLI = new URL('../kata-ui.mjs', import.meta.url).pathname;
let server, base, root;
const registry = {
  items: [{
    name: 'sample',
    type: 'registry:component',
    files: [{ path: 'components/sample/sample.css', content: '.sample{color:var(--k-ink)}' }]
  }, {
    name: 'escape',
    type: 'registry:component',
    files: [{ path: '../outside.txt', content: 'unsafe' }]
  }]
};

before(async () => {
  server = createServer((req, res) => {
    if (req.url === '/registry.json') {
      res.writeHead(200, { 'content-type': 'application/json' });
      res.end(JSON.stringify(registry));
    } else if (req.url === '/tokens.css') {
      res.writeHead(200, { 'content-type': 'text/css' });
      res.end(':root{--k-ink:#18181b}');
    } else {
      res.writeHead(404); res.end('not found');
    }
  });
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  base = 'http://127.0.0.1:' + server.address().port;
});

after(async () => {
  if (server) await new Promise(resolve => server.close(resolve));
});

async function setup() {
  root = await mkdtemp(join(tmpdir(), 'kataui-cli-'));
  return root;
}
async function run(dir, ...args) {
  try {
    const r = await execFileAsync(process.execPath, [CLI, '--dir', dir, '--base', base, ...args], { encoding: 'utf8' });
    return { status: 0, stdout: r.stdout, stderr: r.stderr };
  } catch (e) {
    return { status: typeof e.code === 'number' ? e.code : 1, stdout: e.stdout || '', stderr: e.stderr || e.message };
  }
}

test('default install refuses to overwrite and preserves existing content', async () => {
  const dir = await setup();
  const target = join(dir, 'components/sample/sample.css');
  await mkdir(join(dir, 'components/sample'), { recursive: true });
  await writeFile(target, 'keep me');
  const r = await run(dir, 'add', 'sample');
  assert.notEqual(r.status, 0);
  assert.match(r.stderr, /existing files were not changed/);
  assert.equal(await readFile(target, 'utf8'), 'keep me');
  await rm(dir, { recursive: true, force: true });
});

test('--dry-run reports files without creating them', async () => {
  const dir = await setup();
  const r = await run(dir, '--dry-run', 'add', 'sample');
  assert.equal(r.status, 0, r.stderr);
  assert.match(r.stdout, /dry-run: no files written/);
  await assert.rejects(readFile(join(dir, 'tokens.css')));
  await rm(dir, { recursive: true, force: true });
});

test('--force overwrites and --backup preserves the previous file', async () => {
  const dir = await setup();
  const target = join(dir, 'components/sample/sample.css');
  await mkdir(join(dir, 'components/sample'), { recursive: true });
  await writeFile(target, 'old content');
  const r = await run(dir, '--force', '--backup', 'add', 'sample');
  assert.equal(r.status, 0, r.stderr);
  assert.equal(await readFile(target, 'utf8'), '.sample{color:var(--k-ink)}');
  assert.equal(await readFile(target + '.bak', 'utf8'), 'old content');
  await rm(dir, { recursive: true, force: true });
});

test('registry paths cannot escape the output directory', async () => {
  const dir = await setup();
  const r = await run(dir, 'add', 'escape');
  assert.notEqual(r.status, 0);
  assert.match(r.stderr, /unsafe registry path|escapes output directory/);
  await assert.rejects(readFile(join(dir, '..', 'outside.txt')));
  await rm(dir, { recursive: true, force: true });
});
