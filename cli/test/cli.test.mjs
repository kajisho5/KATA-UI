import test from 'node:test';
import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {mkdtemp,mkdir,readFile,writeFile,rm,access,chmod,symlink,readdir,stat} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {fileURLToPath} from 'node:url';
import {spawn} from 'node:child_process';
const CLI=fileURLToPath(new URL('../kata-ui.mjs',import.meta.url));
const MOLD='/* KATA mold v2 — 2026-11-05 — kata-ui.dev/docs/mold-changelog */\n:root{--k-mold:2}\n';
const initial=()=>({moldVersion:2,items:[
 {name:'dep',type:'registry:component',requiresMold:2,files:[{path:'components/dep/dep.css',content:'dependency'}]},
 {name:'demo',type:'registry:component',requiresMold:1,dependencies:['dep'],files:[{path:'components/demo/demo.css',content:'component'}]}
]});
const missing=async path=>{try{await access(path);return false;}catch(e){if(e.code==='ENOENT')return true;throw e;}};
function exec(args,options={}){return new Promise((resolve,reject)=>{const child=spawn(process.execPath,[CLI,...args],options);let stdout='',stderr='';child.stdout.on('data',d=>stdout+=d);child.stderr.on('data',d=>stderr+=d);child.on('error',reject);child.on('close',code=>resolve({code,stdout,stderr}));});}

test('CLI safety and mold integration',async t=>{
 let registry=initial(),tokens=MOLD;
 const server=createServer((req,res)=>{if(req.url==='/registry.json'){res.setHeader('content-type','application/json');res.end(JSON.stringify(registry));}else if(req.url==='/tokens.css')res.end(tokens);else {res.statusCode=404;res.end('missing');}});
 await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));const base='http://127.0.0.1:'+server.address().port;
 async function scenario(name,fn){await t.test(name,async st=>{registry=initial();tokens=MOLD;const folder=await mkdtemp(join(tmpdir(),'kata-cli-'));const dir=join(folder,'install');const run=(...args)=>exec(['--dir',dir,'--base',base,...args]);const put=async(content,path='tokens.css')=>{await mkdir(dir,{recursive:true});await writeFile(join(dir,path),content);};try{await fn({st,folder,dir,run,put});}finally{await rm(folder,{recursive:true,force:true});}});}
 try {
  await scenario('missing mold installs current file and dependencies',async({dir,run})=>{const r=await run('add','demo');assert.equal(r.code,0,r.stderr);assert.equal(await readFile(join(dir,'tokens.css'),'utf8'),MOLD);assert.equal(await readFile(join(dir,'components/dep/dep.css'),'utf8'),'dependency');});
  for(const [name,content] of [['unversioned','/* local theme */\n:root{--custom:red}'],['v1','/* KATA mold v1 */\noriginal'],['hand-edited','/* hand-edited theme */\n:root{--accent:purple}']]){
   await scenario(name+' warns once using dependency maximum and preserves bytes',async({dir,run,put})=>{await put(content);const r=await run('add','demo','--force');assert.equal(r.code,0,r.stderr);assert.equal(r.stderr.trim().split('\n').length,1);assert.match(r.stderr,/Installed mold v1.*require mold >= 2.*\/docs\/update-mold\//);assert.equal(await readFile(join(dir,'tokens.css'),'utf8'),content);});
  }
  await scenario('v2 customizations are preserved without a warning',async({dir,run,put})=>{const content=MOLD+'/* personal edits */';await put(content);const r=await run('add','demo','--force','--backup');assert.equal(r.code,0,r.stderr);assert.equal(r.stderr,'');assert.equal(await readFile(join(dir,'tokens.css'),'utf8'),content);assert.equal(await missing(join(dir,'tokens.css.bak')),true);});
  await scenario('uses selected/dependency requirements, not whole catalog version',async({run,put})=>{registry.moldVersion=3;await put(MOLD);const r=await run('add','demo');assert.equal(r.code,0,r.stderr);assert.equal(r.stderr,'');});
  for(const content of ['/* KATA mold vx */','/* KATA mold v0 */','/* KATA mold v2.1 */','/* KATA mold v2']){
   await scenario('malformed header: '+content,async({dir,run,put})=>{await put(content);const r=await run('add','demo');assert.equal(r.code,1);assert.match(r.stderr,/invalid mold header/);assert.doesNotMatch(r.stderr,/Installed mold v1/);assert.equal(await missing(join(dir,'components')),true);assert.equal(await readFile(join(dir,'tokens.css'),'utf8'),content);});
  }
  await scenario('unreadable mold is an error, not guessed legacy',async({st,folder,dir,run,put})=>{await put(MOLD);const path=join(dir,'tokens.css');await chmod(path,0);try{let r;if(process.getuid?.()===0){await chmod(folder,0o755);await chmod(dir,0o755);r=await exec(['--dir',dir,'--base',base,'add','demo'],{uid:65534,gid:65534});}else r=await run('add','demo');assert.equal(r.code,1);assert.match(r.stderr,/EACCES|permission denied/);assert.doesNotMatch(r.stderr,/Installed mold/);assert.equal(await missing(join(dir,'components')),true);}finally{await chmod(path,0o600);}});
  for(const kind of ['root','ancestor','tokens','parent','target']){
   await scenario('rejects '+kind+' symlink even with force',async({folder,dir,run})=>{const outside=join(folder,'outside');await mkdir(outside);await writeFile(join(outside,'keep'),'preserve');
    if(kind==='root')await symlink(outside,dir,'dir');
    if(kind==='ancestor'){await symlink(outside,dir,'dir');const r=await exec(['--dir',join(dir,'nested'),'--base',base,'add','demo','--force']);assert.equal(r.code,1);assert.match(r.stderr,/symlink/);assert.deepEqual(await readdir(outside),['keep']);return;}
    if(kind==='tokens'){await mkdir(dir);await symlink(join(outside,'keep'),join(dir,'tokens.css'));}
    if(kind==='parent'){await mkdir(dir);await symlink(outside,join(dir,'components'),'dir');}
    if(kind==='target'){await mkdir(join(dir,'components/demo'),{recursive:true});await symlink(join(outside,'keep'),join(dir,'components/demo/demo.css'));}
    const r=await run('add','demo','--force','--backup');assert.equal(r.code,1);assert.match(r.stderr,/symlink/);assert.equal(await readFile(join(outside,'keep'),'utf8'),'preserve');assert.deepEqual(await readdir(outside),['keep']);});
  }
  for(const path of ['../escape.css','/tmp/kata-escape.css','..\\escape.css','C:\\escape.css','components/../escape.css','components/evil\0.css']){
   await scenario('rejects registry path '+JSON.stringify(path),async({dir,run})=>{registry.items[1].files[0].path=path;const r=await run('add','demo');assert.equal(r.code,1);assert.match(r.stderr,/unsafe|escapes/);assert.equal(await missing(dir),true);});
  }
  await scenario('unknown part aborts the whole plan before writes',async({dir,run})=>{const r=await run('add','demo','missing');assert.equal(r.code,1);assert.equal(await missing(dir),true);});
  await scenario('malformed registry is rejected',async({dir,run})=>{registry={};const r=await run('add','demo');assert.equal(r.code,1);assert.match(r.stderr,/invalid registry/);assert.equal(await missing(dir),true);});
  await scenario('existing part is protected and no dependencies partially install',async({dir,run,put})=>{await put(MOLD);await mkdir(join(dir,'components/demo'),{recursive:true});await writeFile(join(dir,'components/demo/demo.css'),'custom');const r=await run('add','demo');assert.equal(r.code,1);assert.equal(await readFile(join(dir,'components/demo/demo.css'),'utf8'),'custom');assert.equal(await missing(join(dir,'components/dep')),true);});
  await scenario('dry-run creates no installation directory',async({dir,run})=>{const r=await run('add','demo','--dry-run');assert.equal(r.code,0,r.stderr);assert.equal(await missing(dir),true);});
  await scenario('dry-run can preview conflicts without changing files',async({dir,run,put})=>{await put(MOLD);await mkdir(join(dir,'components/demo'),{recursive:true});await writeFile(join(dir,'components/demo/demo.css'),'custom');const r=await run('add','demo','--dry-run');assert.equal(r.code,0,r.stderr);assert.match(r.stdout,/dry-run/);assert.equal(await readFile(join(dir,'components/demo/demo.css'),'utf8'),'custom');assert.equal(await missing(join(dir,'components/dep')),true);});
  await scenario('force backup never overwrites a prior backup or existing mold',async({dir,run,put})=>{await put(MOLD+'custom');await mkdir(join(dir,'components/demo'),{recursive:true});const path=join(dir,'components/demo/demo.css');await writeFile(path,'old');await writeFile(path+'.bak','older');const r=await run('add','demo','--force','--backup');assert.equal(r.code,0,r.stderr);assert.equal(await readFile(path,'utf8'),'component');assert.equal(await readFile(path+'.bak','utf8'),'older');assert.equal(await readFile(path+'.bak.1','utf8'),'old');assert.equal(await readFile(join(dir,'tokens.css'),'utf8'),MOLD+'custom');});
  await scenario('explicit init force backup updates a legacy mold',async({dir,run,put})=>{await put('/* KATA mold v1 */\ncustom');const blocked=await run('init');assert.equal(blocked.code,1);const r=await run('init','--force','--backup');assert.equal(r.code,0,r.stderr);assert.equal(await readFile(join(dir,'tokens.css'),'utf8'),MOLD);assert.equal(await readFile(join(dir,'tokens.css.bak'),'utf8'),'/* KATA mold v1 */\ncustom');});
  await scenario('init dry-run does not create backup',async({dir,run,put})=>{await put('custom');const r=await run('init','--force','--backup','--dry-run');assert.equal(r.code,0,r.stderr);assert.equal(await readFile(join(dir,'tokens.css'),'utf8'),'custom');assert.equal(await missing(join(dir,'tokens.css.bak')),true);});
  await scenario('rejects insufficient downloaded mold before installation',async({dir,run})=>{tokens='/* KATA mold v1 */';const r=await run('add','demo');assert.equal(r.code,1);assert.match(r.stderr,/older than/);assert.equal(await missing(dir),true);});
  await scenario('registry item cannot smuggle tokens.css into force plan',async({dir,run,put})=>{await put(MOLD+'custom');registry.items[1].files[0].path='tokens.css';const r=await run('add','demo','--force');assert.equal(r.code,1);assert.equal(await readFile(join(dir,'tokens.css'),'utf8'),MOLD+'custom');});
  await scenario('conflicting duplicate outputs abort before writes',async({dir,run})=>{registry.items[1].files[0].path=registry.items[0].files[0].path;const r=await run('add','demo');assert.equal(r.code,1);assert.match(r.stderr,/conflicting/);assert.equal(await missing(dir),true);});
  await scenario('force preserves existing destination mode',async({dir,run,put})=>{await put(MOLD);await mkdir(join(dir,'components/demo'),{recursive:true});const path=join(dir,'components/demo/demo.css');await writeFile(path,'private');await chmod(path,0o600);const r=await run('add','demo','--force');assert.equal(r.code,0,r.stderr);assert.equal((await stat(path)).mode&0o777,0o600);});
  await scenario('staging permission failure does not partially replace targets',async({st,dir,run,put})=>{if(process.getuid?.()===0){st.skip('permission boundary requires a non-root process');return;}await put(MOLD);await mkdir(join(dir,'components/demo'),{recursive:true});await mkdir(join(dir,'components/dep'),{recursive:true});const path=join(dir,'components/dep/dep.css');await writeFile(path,'keep');await chmod(join(dir,'components/demo'),0o555);try{const r=await run('add','demo','--force');assert.equal(r.code,1);assert.equal(await readFile(path,'utf8'),'keep');assert.deepEqual(await readdir(join(dir,'components/dep')),['dep.css']);assert.equal(await missing(join(dir,'components/demo/demo.css')),true);}finally{await chmod(join(dir,'components/demo'),0o755);}});
  await scenario('help distinguishes component overwrite from mold updates',async({run})=>{const r=await run('--help');assert.equal(r.code,0);assert.match(r.stdout,/add --force overwrites component files but never overwrites an existing tokens\.css/);assert.match(r.stdout,/To update tokens\.css, follow https:\/\/kata-ui\.dev\/docs\/update-mold\//);});
  await scenario('version matches package and missing options fail cleanly',async({run})=>{const pkg=JSON.parse(await readFile(new URL('../package.json',import.meta.url),'utf8'));const r=await run('--version');assert.equal(r.code,0);assert.match(r.stdout,new RegExp(pkg.version.replaceAll('.','\\.')));for(const args of [['add','demo','--dir'],['add','demo','--dir','--force'],['add','demo','--backup']]){const bad=await run(...args);assert.equal(bad.code,1);assert.doesNotMatch(bad.stderr,/at file:/);}});
 } finally {await new Promise(resolve=>{server.close(resolve);server.closeAllConnections?.();});}
});
