#!/usr/bin/env node
// KATA UI MCP server — the catalog, served to AI tools over stdio.
// Zero dependencies (Node 18+). Speaks JSON-RPC 2.0, one message per line.
//
//   node kata-ui-mcp.mjs [--registry <url-or-path>]
//
// The registry defaults to https://kata-ui.dev/registry.json and can be
// a local file instead (a mirror, or a pinned version). $KATA_BASE works
// too. Logs go to stderr; stdout is the protocol, kept clean.

import { readFile } from 'node:fs/promises';
import readline from 'node:readline';

const args = process.argv.slice(2);
let registryArg = process.env.KATA_REGISTRY || '';
for (let i = 0; i < args.length; i++) {
  if (args[i] === '--registry') registryArg = args[++i] || '';
}
const base = (process.env.KATA_BASE || 'https://kata-ui.dev').replace(/\/$/, '');

let registry = null;
async function loadRegistry() {
  if (registry) return registry;
  const src = registryArg || base + '/registry.json';
  let text;
  if (/^https?:\/\//.test(src)) {
    const res = await fetch(src);
    if (!res.ok) throw new Error('registry fetch failed: ' + res.status);
    text = await res.text();
  } else {
    text = await readFile(src, 'utf8');
  }
  registry = JSON.parse(text);
  return registry;
}

async function localAudit() {
  if (registryArg && !/^https?:\/\//.test(registryArg)) return (await loadRegistry()).audit;
  if (registryArg) return null;
  try {
    const report = JSON.parse(await readFile(new URL('../mold-results.json', import.meta.url), 'utf8'));
    const x = report.summary, p = x.by_profile;
    return { label: `Mold Verified ${x.passed} / ${x.total} · UI ${p.ui.passed} / ${p.ui.total} · Lab ${p.lab.passed} / ${p.lab.total}`, url: 'https://kata-ui.dev/audit/', updated_at: report.updated_at, summary: x };
  } catch { return null; }
}

async function localMold() {
  if (registryArg) {
    const reg = await loadRegistry();
    return { moldVersion: reg.moldVersion || 1, instruction: reg.moldInstruction || 'Before copying a part, check tokens.css against requiresMold.' };
  }
  try { return JSON.parse(await readFile(new URL('./mold.json', import.meta.url), 'utf8')); }
  catch { const reg = await loadRegistry(); return {moldVersion: reg.moldVersion || 1, instruction: reg.moldInstruction || 'Before copying a part, check tokens.css against requiresMold.'}; }
}

const TOOLS = [
  {
    name: 'get_audit',
    description: 'Read the catalog static-check summary, profiles and update date. Browser behavior requires separate testing.',
    inputSchema: { type: 'object', properties: {} }
  },
  {
    name: 'list_components',
    description: 'List the KATA UI catalog: parts (registry:component), blocks (registry:block), templates (registry:page) and themes (registry:theme). Optionally filter by type.',
    inputSchema: {
      type: 'object',
      properties: {
        type: { type: 'string', enum: ['registry:component', 'registry:block', 'registry:page', 'registry:theme'], description: 'Only return items of this type.' }
      }
    }
  },
  {
    name: 'search_components',
    description: 'Search the catalog by name, title, description and tags. Use this to find the right part before fetching it.',
    inputSchema: {
      type: 'object',
      properties: { query: { type: 'string', description: 'Words to search for, e.g. "date picker" or "sidebar".' } },
      required: ['query']
    }
  },
  {
    name: 'get_component',
    description: 'Fetch one catalog item by name, with the full contents of its files (HTML preview, CSS, JS) and its dependencies. This is everything needed to install the part into a project.',
    inputSchema: {
      type: 'object',
      properties: { name: { type: 'string', description: 'The item name, e.g. "sidebar", "login" or "indigo".' } },
      required: ['name']
    }
  }
];

function brief(it) {
  return { name: it.name, type: it.type, title: it.title, description: it.description, requiresMold: it.requiresMold, dependencies: it.dependencies || [] };
}

async function callTool(name, a) {
  const reg = await loadRegistry();
  if (name === 'get_audit') return JSON.stringify({...reg.audit, moldVersion: reg.moldVersion || 1, moldInstruction: reg.moldInstruction});
  const items = reg.items || [];
  if (name === 'list_components') {
    const out = items.filter(it => !a.type || it.type === a.type).map(brief);
    return out.length + ' items\n' + JSON.stringify(out, null, 1);
  }
  if (name === 'search_components') {
    const q = String(a.query || '').toLowerCase();
    const hits = items.filter(it => JSON.stringify([it.name, it.title, it.description, (it.categories || []).join(' ')]).toLowerCase().includes(q)).map(brief);
    return hits.length ? JSON.stringify(hits, null, 1) : 'No matches for "' + a.query + '". Try list_components for the whole catalog.';
  }
  if (name === 'get_component') {
    const it = items.find(x => x.name === a.name);
    if (!it) return 'No catalog item named "' + a.name + '". Try search_components.';
    return JSON.stringify({moldVersion: reg.moldVersion || 1, moldInstruction: reg.moldInstruction, tokens: reg.tokens, ...it}, null, 1);
  }
  throw new Error('unknown tool: ' + name);
}

function send(obj) { process.stdout.write(JSON.stringify(obj) + '\n'); }
function reply(id, result) { send({ jsonrpc: '2.0', id, result }); }
function replyError(id, code, message) { send({ jsonrpc: '2.0', id, error: { code, message } }); }

const rl = readline.createInterface({ input: process.stdin, crlfDelay: Infinity });
rl.on('line', async line => {
  line = line.trim();
  if (!line) return;
  let msg;
  try { msg = JSON.parse(line); } catch { return; }
  const { id, method, params } = msg;
  try {
    if (method === 'initialize') {
      const audit = await localAudit();
      const mold = await localMold();
      reply(id, {
        instructions: `moldVersion: ${mold.moldVersion}. ${mold.instruction} ` + (audit ? `${audit.label}. ${audit.url}. Updated ${audit.updated_at}. Static checks only.` : 'Use get_audit to read current registry audit metadata.'),
        _meta: {'kata-ui/moldVersion': mold.moldVersion},
        protocolVersion: (params && params.protocolVersion) || '2024-11-05',
        capabilities: { tools: {} },
        serverInfo: { name: 'kata-ui', version: '1.0.0' }
      });
    } else if (method === 'ping') {
      reply(id, {});
    } else if (method === 'tools/list') {
      reply(id, { tools: TOOLS });
    } else if (method === 'tools/call') {
      const text = await callTool(params.name, params.arguments || {});
      reply(id, { content: [{ type: 'text', text }] });
    } else if (id !== undefined && id !== null) {
      replyError(id, -32601, 'method not found: ' + method);
    }
    // notifications (no id) need no answer
  } catch (e) {
    if (id !== undefined && id !== null) replyError(id, -32603, String(e && e.message || e));
  }
});

process.stderr.write('kata-ui MCP server ready (stdio)\n');
