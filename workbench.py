"""
A local page for running the CareSets pipeline and reviewing mappings.

  python workbench.py          start it and open a browser
  python workbench.py --port 8800 --no-browser

Everything an analyst does here is otherwise a command line and a CSV opened in
Excel. Two things live on the page:

  Pipeline    the steps, in order, each with what it will do and its live output
  Mappings    the proposed model-to-glossary mappings, grouped by concept, with
              each model's own wording beside them, and accept / reject buttons

Standard library only, and no network listener beyond localhost. The project is
delivered into a government environment where adding a dependency or opening a
port is a question somebody has to answer; neither is worth it for a tool that
runs on one analyst's machine while they work.

The page calls back into the same scripts the command line uses. There is no
second implementation of anything: a step here runs `python <script>` and shows
what it printed, so what an analyst sees and what a developer sees are the same
run.
"""

import argparse
import csv
import io
import json
import os
import subprocess
import sys
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.abspath(__file__))
MAPPINGS = os.path.join(ROOT, "input", "glossary_mappings.csv")
FIELDS = ["Model", "ElementSuffix", "GlossaryCode", "GlossaryStatus", "Status",
          "Confidence", "Rationale", "ElementDescription"]

# Every step the page can run. `args` is passed to python <script>; `why` is
# shown to the analyst, because "Merge mappings" means nothing on its own.
# key, label, script, fixed args, explanation, takes --model, takes --include-draft
STEPS = [
    ("fetch", "Fetch published models", "fetch_ehealth_models.py", ["--apply"],
     "Downloads the logical models eHealth publishes. Run every few weeks, or "
     "when you are told a new model is out.", False, False),
    ("export", "Models to workbooks", "export_logical_model_xlsx.py",
     ["--overwrite"],
     "Rewrites models/xls/*.xlsx from the published models. Overwrites the "
     "workbooks, so do not run it with unsaved work in them.", True, True),
    ("propose", "Propose mappings", "propose_model_mappings.py", ["--report"],
     "Suggests a glossary concept for elements that have none, into the "
     "mappings CSV. Nothing is applied - they arrive as proposed, for the "
     "Mappings tab.", False, False),
    ("merge", "Merge confirmed mappings", "merge_mappings_to_xlsx.py", [],
     "Writes the confirmed mappings into the model workbooks' Code column.",
     False, False),
    ("import", "Workbooks to models", "import_logical_model_xlsx.py", [],
     "Rebuilds models/generated/*.json from the workbooks. Run after merging. "
     "Selecting models here skips rewriting the mappings CSV, which is "
     "regenerated whole and would lose the models left out.", True, False),
    ("content", "Rebuild site content", "build_content.py", [],
     "Glossary workbook to CSV, models synced, CodeSystems and the ConceptMap "
     "rebuilt. Run after any change to input/.", False, False),
    ("diagrams", "Diagrams and Word documents", "generate_model_diagrams.py", [],
     "One .docx, .svg and .png per model per language, into exports/diagrams/. "
     "Slow over all 41 - pick the ones you need.", True, True),
    ("site", "Build the site", "build_package.py", ["--ghpages"],
     "Builds the public site into _site_ghpages/ without publishing it.",
     False, False),
]


def list_models():
    """Every logical model, with whether it is a draft.

    Read from the model folders rather than from a hardcoded list, so a model
    published upstream this morning is in the picker this afternoon.
    """
    import glob as _glob
    import json as _json
    out = {}
    for folder, draft in ((os.path.join(ROOT, "input", "models"), False),
                          (os.path.join(ROOT, "input", "models", "draft"), True)):
        for path in sorted(_glob.glob(os.path.join(folder, "*.json"))):
            try:
                doc = _json.load(io.open(path, encoding="utf-8"))
            except ValueError:
                continue
            if doc.get("resourceType") != "StructureDefinition":
                continue
            if doc.get("kind") != "logical":
                continue
            name = doc.get("name") or doc.get("id")
            if name and name not in out:
                out[name] = {"name": name, "draft": draft,
                             "title": doc.get("title") or ""}
    return [out[k] for k in sorted(out)]


def read_rows():
    if not os.path.exists(MAPPINGS):
        return []
    with io.open(MAPPINGS, encoding="utf-8-sig", newline="") as fh:
        return [{k: (r.get(k) or "").strip() for k in FIELDS}
                for r in csv.DictReader(fh, delimiter=";")
                if (r.get("Model") or "").strip()]


def write_rows(rows):
    with io.open(MAPPINGS, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS, delimiter=";",
                           extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)


def grouped():
    """Proposed rows, grouped by the concept they point at.

    Grouping is the whole point: `status` is proposed for 22 models and
    `identifier` for 20, and those are one judgement each, not forty-two. The
    per-model wording is kept so a model that means something different by the
    same name can still be excluded.
    """
    groups = {}
    for r in read_rows():
        if r["Status"].lower() != "proposed":
            continue
        g = groups.setdefault(r["GlossaryCode"], {
            "code": r["GlossaryCode"],
            "confidence": r["Confidence"],
            "rationale": r["Rationale"],
            "rows": [],
        })
        g["rows"].append(r)
    order = {"certain": 0, "likely": 1, "check": 2}
    return sorted(groups.values(),
                  key=lambda g: (order.get(g["confidence"], 3), -len(g["rows"])))


def counts():
    rows = read_rows()
    out = {"confirmed": 0, "proposed": 0, "rejected": 0}
    for r in rows:
        key = (r["Status"] or "confirmed").lower()
        out[key] = out.get(key, 0) + 1
    return out


def decide(code, status, excluded):
    """Apply one decision to every proposed row for a concept."""
    rows = read_rows()
    n = 0
    for r in rows:
        if r["Status"].lower() != "proposed" or r["GlossaryCode"] != code:
            continue
        if r["Model"] in excluded:
            r["Status"] = "rejected"
        else:
            r["Status"] = status
        n += 1
    write_rows(rows)
    return n


def run_step(key, models=None):
    step = next((s for s in STEPS if s[0] == key), None)
    if step is None:
        return 1, "unknown step: %s" % key
    _, _label, script, args, _why, takes_models, takes_draft = step
    cmd = [sys.executable, os.path.join(ROOT, script)] + list(args)
    if takes_models and models:
        cmd += ["--model"] + list(models)
        # Selecting a draft is how you ask for it; requiring a second switch
        # for something already ticked would only be a way to get it wrong.
        if takes_draft and any(m["draft"] for m in list_models()
                               if m["name"] in models):
            cmd.append("--include-draft")
    elif takes_draft:
        cmd.append("--include-draft")
    p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    return p.returncode, "$ %s\n\n%s" % (
        " ".join(os.path.basename(c) for c in cmd[1:]),
        (p.stdout or "") + (p.stderr or ""))


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _send(self, body, ctype="application/json"):
        data = body if isinstance(body, bytes) else body.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", ctype + "; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path == "/":
            return self._send(PAGE, "text/html")
        if self.path == "/api/state":
            return self._send(json.dumps({
                "counts": counts(),
                "groups": grouped(),
                "models": list_models(),
                "steps": [{"key": k, "label": l, "why": w, "models": tm}
                          for k, l, _s, _a, w, tm, _td in STEPS],
            }))
        self.send_error(404)

    def do_POST(self):
        n = int(self.headers.get("Content-Length") or 0)
        payload = json.loads(self.rfile.read(n) or b"{}")
        if self.path == "/api/run":
            rc, out = run_step(payload.get("step", ""), payload.get("models"))
            return self._send(json.dumps({"rc": rc, "output": out}))
        if self.path == "/api/decide":
            n = decide(payload.get("code", ""),
                       payload.get("status", "rejected"),
                       set(payload.get("excluded") or []))
            return self._send(json.dumps({"applied": n, "counts": counts()}))
        self.send_error(404)


PAGE = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>CareSets workbench</title>
<style>
:root { --line:#d9dde3; --ink:#1a1a1a; --muted:#5b6472; --bg:#f6f7f9;
        --accept:#15803d; --reject:#b91c1c; --warn:#b45309; }
* { box-sizing: border-box; }
body { margin:0; font:15px/1.5 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
       color:var(--ink); background:var(--bg); }
header { background:#fff; border-bottom:1px solid var(--line); padding:1rem 1.5rem; }
h1 { margin:0; font-size:1.15rem; }
.counts { color:var(--muted); font-size:.9rem; margin-top:.25rem; }
main { max-width:1100px; margin:0 auto; padding:1.5rem; }
.tabs { display:flex; gap:.5rem; margin-bottom:1rem; }
.tabs button { border:1px solid var(--line); background:#fff; padding:.5rem 1rem;
               border-radius:6px; cursor:pointer; font:inherit; }
.tabs button[aria-selected=true] { background:var(--ink); color:#fff; border-color:var(--ink); }
section[hidden] { display:none; }
.card { background:#fff; border:1px solid var(--line); border-radius:8px;
        padding:1rem 1.15rem; margin-bottom:.85rem; }
.card h3 { margin:0 0 .2rem; font-size:1rem; }
.why { color:var(--muted); font-size:.9rem; margin:0 0 .7rem; }
button.run { border:1px solid var(--line); background:#fff; padding:.4rem .9rem;
             border-radius:6px; cursor:pointer; font:inherit; }
button.run:hover { background:#eef1f5; }
button.run[disabled] { opacity:.5; cursor:default; }
pre { background:#11151a; color:#e6edf3; padding:.8rem; border-radius:6px;
      overflow:auto; max-height:22rem; font-size:.82rem; white-space:pre-wrap; margin:.7rem 0 0; }
.tag { display:inline-block; font-size:.75rem; padding:.1rem .45rem; border-radius:4px;
       border:1px solid var(--line); color:var(--muted); margin-left:.4rem; }
.tag.certain { color:var(--accept); border-color:var(--accept); }
.tag.likely  { color:var(--warn);   border-color:var(--warn); }
.tag.check   { color:var(--reject); border-color:var(--reject); }
table { width:100%; border-collapse:collapse; margin:.6rem 0; font-size:.88rem; }
th,td { text-align:left; padding:.35rem .5rem; border-bottom:1px solid var(--line);
        vertical-align:top; }
th { color:var(--muted); font-weight:600; }
td.desc { color:var(--muted); }
.actions { display:flex; gap:.5rem; align-items:center; margin-top:.6rem; }
.actions button { border:0; color:#fff; padding:.45rem 1rem; border-radius:6px;
                  cursor:pointer; font:inherit; }
.accept { background:var(--accept); } .reject { background:var(--reject); }
.done { color:var(--muted); font-style:italic; }
.picker { border:1px solid var(--line); border-radius:6px; margin:.6rem 0; }
.picker summary { cursor:pointer; padding:.45rem .7rem; color:var(--muted);
                  font-size:.9rem; }
.picker .body { padding:.5rem .7rem .7rem; border-top:1px solid var(--line); }
.picker input[type=search] { width:100%; padding:.35rem .5rem; font:inherit;
                             border:1px solid var(--line); border-radius:5px;
                             margin-bottom:.5rem; }
.picker .list { max-height:14rem; overflow:auto; display:grid;
                grid-template-columns:repeat(auto-fill,minmax(15rem,1fr));
                gap:.1rem .8rem; }
.picker label { display:flex; gap:.4rem; align-items:center; font-size:.87rem;
                padding:.1rem 0; }
.picker label.draft { color:var(--warn); }
.picker .bulk { margin-bottom:.4rem; display:flex; gap:.5rem; align-items:center; }
.picker .bulk button { border:1px solid var(--line); background:#fff;
                       padding:.2rem .6rem; border-radius:5px; cursor:pointer;
                       font:inherit; font-size:.8rem; }
</style></head><body>
<header>
  <h1>CareSets workbench</h1>
  <div class="counts" id="counts">loading…</div>
</header>
<main>
  <div class="tabs" role="tablist">
    <button id="tab-pipeline" role="tab" aria-selected="true">Pipeline</button>
    <button id="tab-mappings" role="tab" aria-selected="false">Mappings</button>
  </div>
  <section id="pipeline"></section>
  <section id="mappings" hidden></section>
</main>
<script>
const $ = s => document.querySelector(s);
let state = null;

function esc(s){ return (s||'').replace(/[&<>"]/g, c =>
  ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c])); }

async function load(){
  state = await (await fetch('/api/state')).json();
  const c = state.counts;
  $('#counts').textContent =
    `${c.confirmed||0} confirmed · ${c.proposed||0} proposed · ${c.rejected||0} rejected`;
  drawPipeline(); drawMappings();
}

function picker(key){
  return `
    <details class="picker" id="pick-${esc(key)}">
      <summary><span class="sel">all ${state.models.length} models</span> — click to choose</summary>
      <div class="body">
        <div class="bulk">
          <button data-all="1">All</button>
          <button data-none="1">None</button>
          <button data-published="1">Published only</button>
        </div>
        <input type="search" placeholder="filter…">
        <div class="list">
          ${state.models.map(m => `
            <label class="${m.draft ? 'draft' : ''}" title="${esc(m.title)}">
              <input type="checkbox" value="${esc(m.name)}">
              ${esc(m.name)}${m.draft ? ' (draft)' : ''}
            </label>`).join('')}
        </div>
      </div>
    </details>`;
}

function drawPipeline(){
  $('#pipeline').innerHTML = state.steps.map(s => `
    <div class="card">
      <h3>${esc(s.label)}</h3>
      <p class="why">${esc(s.why)}</p>
      ${s.models ? picker(s.key) : ''}
      <button class="run" data-step="${esc(s.key)}">Run</button>
      <pre id="out-${esc(s.key)}" hidden></pre>
    </div>`).join('');
  document.querySelectorAll('button.run').forEach(b =>
    b.addEventListener('click', () => runStep(b)));
  document.querySelectorAll('.picker').forEach(wirePicker);
}

function wirePicker(el){
  const boxes = () => [...el.querySelectorAll('.list input[type=checkbox]')];
  const label = () => {
    const on = boxes().filter(b => b.checked);
    el.querySelector('.sel').textContent = on.length
      ? `${on.length} model${on.length === 1 ? '' : 's'}`
      : `all ${state.models.length} models`;
  };
  el.querySelector('[data-all]').addEventListener('click', e => {
    e.preventDefault(); boxes().forEach(b => b.checked = true); label(); });
  el.querySelector('[data-none]').addEventListener('click', e => {
    e.preventDefault(); boxes().forEach(b => b.checked = false); label(); });
  el.querySelector('[data-published]').addEventListener('click', e => {
    e.preventDefault();
    const drafts = new Set(state.models.filter(m => m.draft).map(m => m.name));
    boxes().forEach(b => b.checked = !drafts.has(b.value));
    label(); });
  el.querySelector('input[type=search]').addEventListener('input', e => {
    const q = e.target.value.toLowerCase();
    el.querySelectorAll('.list label').forEach(l =>
      l.hidden = q && !l.textContent.toLowerCase().includes(q));
  });
  el.addEventListener('change', label);
  label();
}

async function runStep(btn){
  const key = btn.dataset.step, out = $('#out-'+key);
  const pick = $('#pick-'+key);
  // No tick means every model: the steps behaved that way before there was a
  // picker, and an empty selection reading as "none" would be a trap.
  const models = pick
    ? [...pick.querySelectorAll('.list input:checked')].map(i => i.value)
    : [];
  btn.disabled = true; btn.textContent = 'Running…';
  out.hidden = false;
  out.textContent = models.length
    ? `running over ${models.length} model(s)…` : 'running…';
  try {
    const r = await (await fetch('/api/run', {method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({step:key, models})})).json();
    out.textContent = r.output || '(no output)';
    btn.textContent = r.rc === 0 ? 'Run again' : 'Failed — run again';
  } catch(e){ out.textContent = String(e); btn.textContent = 'Run'; }
  btn.disabled = false;
  load();
}

function drawMappings(){
  if (!state.groups.length){
    $('#mappings').innerHTML =
      '<div class="card"><p class="done">Nothing proposed. Run ' +
      '<strong>Propose mappings</strong> on the Pipeline tab to look for more.</p></div>';
    return;
  }
  $('#mappings').innerHTML = state.groups.map(g => `
    <div class="card" data-code="${esc(g.code)}">
      <h3>${esc(g.code)}<span class="tag ${esc(g.confidence)}">${esc(g.confidence)}</span>
        <span class="tag">${g.rows.length} element${g.rows.length===1?'':'s'}</span></h3>
      <p class="why">${esc(g.rationale)}</p>
      <table>
        <tr><th>Model</th><th>Element</th><th>What the model says it is</th><th>Skip</th></tr>
        ${g.rows.map(r => `<tr>
          <td>${esc(r.Model)}</td>
          <td><code>${esc(r.ElementSuffix)}</code></td>
          <td class="desc">${esc(r.ElementDescription)}</td>
          <td><input type="checkbox" data-model="${esc(r.Model)}"
               title="Leave this model out"></td></tr>`).join('')}
      </table>
      <div class="actions">
        <button class="accept">Accept</button>
        <button class="reject">Reject</button>
        <span class="why" style="margin:0">Ticked models are rejected individually.</span>
      </div>
    </div>`).join('');
  document.querySelectorAll('#mappings .card').forEach(card => {
    const code = card.dataset.code;
    const excluded = () => [...card.querySelectorAll('input:checked')]
      .map(i => i.dataset.model);
    card.querySelector('.accept').addEventListener('click',
      () => decide(code, 'confirmed', excluded(), card));
    card.querySelector('.reject').addEventListener('click',
      () => decide(code, 'rejected', [], card));
  });
}

async function decide(code, status, excluded, card){
  card.querySelectorAll('button').forEach(b => b.disabled = true);
  await fetch('/api/decide', {method:'POST',
    headers:{'Content-Type':'application/json'},
    body: JSON.stringify({code, status, excluded})});
  card.innerHTML = `<p class="done">${esc(code)} — ${esc(status)}. ` +
    `Run <strong>Merge confirmed mappings</strong> on the Pipeline tab to apply it.</p>`;
  load();
}

$('#tab-pipeline').addEventListener('click', () => show('pipeline'));
$('#tab-mappings').addEventListener('click', () => show('mappings'));
function show(which){
  $('#pipeline').hidden = which !== 'pipeline';
  $('#mappings').hidden = which !== 'mappings';
  $('#tab-pipeline').setAttribute('aria-selected', which === 'pipeline');
  $('#tab-mappings').setAttribute('aria-selected', which === 'mappings');
}
load();
</script></body></html>
"""


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--no-browser", action="store_true")
    args = ap.parse_args()

    sys.stdout.reconfigure(encoding="utf-8")
    # Bound to the loopback address on purpose: this drives build scripts and
    # rewrites files in the project, and nothing about it should be reachable
    # from the network.
    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    url = "http://127.0.0.1:%d/" % args.port
    print("CareSets workbench: %s" % url)
    print("Ctrl+C to stop.")
    if not args.no_browser:
        threading.Timer(0.5, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")
    return 0


if __name__ == "__main__":
    sys.exit(main())
