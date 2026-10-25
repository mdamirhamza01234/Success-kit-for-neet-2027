/* SK AI core - shared by the home chat (index.html) and the PDF viewer (pdf-viewer.html).
 *
 *  - Gemini (online): newest flash model first, automatic fallback, optional Google Search for live questions
 *  - Gemma 3 1B (offline): native plugin inside the APK (MediaPipe), optional WebGPU fallback in a browser
 *  - Math: every answer is rendered with real LaTeX (KaTeX + mhchem for chemistry, fully offline),
 *          with a small built-in converter as a safety net when KaTeX is missing
 *  - Settings are stored on the phone only (key 'mst_ai_settings') and shared by both screens
 */
(function () {
  'use strict';
  var W = window;

  /* ================= storage ================= */
  function lsGet(k, d) { try { var v = localStorage.getItem(k); return v == null ? d : JSON.parse(v); } catch (e) { return d; } }
  function lsSet(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }
  var SK = 'mst_ai_settings';
  function settings() { var s = lsGet(SK, {}) || {}; return { mode: s.mode || 'auto', key: String(s.key || '') }; }
  function saveSettings(s) { lsSet(SK, { mode: s.mode || 'auto', key: String(s.key || '').replace(/[\s"']/g, '') }); }

  /* ================= LaTeX -> HTML (tiny fallback, used only if KaTeX is not available) ================= */
  var SYM = { longrightarrow: '⟶', Longrightarrow: '⟹', longleftarrow: '⟵', rightleftharpoons: '⇌', leftrightharpoons: '⇌', rightleftarrows: '⇄', uparrow: '↑', downarrow: '↓', bullet: '•', checkmark: '✓',
    alpha: 'α', beta: 'β', gamma: 'γ', delta: 'δ', epsilon: 'ε', varepsilon: 'ε', zeta: 'ζ', eta: 'η', theta: 'θ', vartheta: 'ϑ', lambda: 'λ', mu: 'μ', nu: 'ν', xi: 'ξ', pi: 'π', rho: 'ρ', sigma: 'σ', tau: 'τ', phi: 'φ', varphi: 'φ', chi: 'χ', psi: 'ψ', omega: 'ω',
    Gamma: 'Γ', Delta: 'Δ', Theta: 'Θ', Lambda: 'Λ', Pi: 'Π', Sigma: 'Σ', Phi: 'Φ', Psi: 'Ψ', Omega: 'Ω',
    cdot: '·', times: '×', div: '÷', pm: '±', mp: '∓', approx: '≈', sim: '∼', simeq: '≃', ll: '≪', gg: '≫', le: '≤', leq: '≤', ge: '≥', geq: '≥', ne: '≠', neq: '≠', equiv: '≡', propto: '∝', infty: '∞',
    to: '→', rightarrow: '→', leftarrow: '←', Rightarrow: '⇒', Leftrightarrow: '⇔', leftrightarrow: '↔', partial: '∂', nabla: '∇', int: '∫', oint: '∮', sum: '∑', prod: '∏', circ: '°', degree: '°',
    ldots: '…', cdots: '⋯', dots: '…', therefore: '∴', because: '∵', angle: '∠', perp: '⊥', parallel: '∥', in: '∈', hbar: 'ħ', ell: 'ℓ', prime: '′', sqrt: '√' };
  var FUNCS = { sin: 1, cos: 1, tan: 1, cot: 1, sec: 1, csc: 1, cosec: 1, log: 1, ln: 1, exp: 1, lim: 1, min: 1, max: 1, sinh: 1, cosh: 1, tanh: 1 };
  var DP = { '(': 'M8 1Q1 50 8 99', ')': 'M2 1Q9 50 2 99', '[': 'M8 1H2V99H8', ']': 'M2 1H8V99H2', '|': 'M5 1V99', '{': 'M8 1Q4 1 4 10V40Q4 50 1 50Q4 50 4 60V90Q4 99 8 99', '}': 'M2 1Q6 1 6 10V40Q6 50 9 50Q6 50 6 60V90Q6 99 2 99' };
  function svgP(d) { return '<svg viewBox="0 0 10 100" preserveAspectRatio="none" aria-hidden="true"><path d="' + d + '" fill="none" stroke="currentColor" stroke-width="1.3" vector-effect="non-scaling-stroke"/></svg>'; }
  var SQRT = svgP('M0 62L2.5 56L5 98L10 1');
  function dsvg(ch) { return DP[ch] ? svgP(DP[ch]) : (ch === '.' ? '' : ch); }
  /* \ce{...} (chemistry) without mhchem: subscripts for counts, superscripts for charges, arrows */
  function ceFallback(s) {
    s = String(s).replace(/<=>|<->|\\rightleftharpoons/g, ' ⇌ ').replace(/-->|->|\\to|\\rightarrow/g, ' → ').replace(/<-/g, ' ← ');
    var out = '', i = 0, prev = '';
    while (i < s.length) {
      var c = s[i];
      if (c === '^') {
        i++; var g = '';
        if (s[i] === '{') { var k = s.indexOf('}', i); g = s.slice(i + 1, k < 0 ? s.length : k); i = k < 0 ? s.length : k + 1; }
        else { var m = s.slice(i).match(/^\d*[+\-−]?/); g = m ? m[0] : ''; i += g.length; }
        out += '<sup>' + g.replace(/-/g, '−') + '</sup>'; prev = ''; continue;
      }
      if (c === '_') { i++; var g2 = ''; if (s[i] === '{') { var k2 = s.indexOf('}', i); g2 = s.slice(i + 1, k2 < 0 ? s.length : k2); i = k2 < 0 ? s.length : k2 + 1; } else { g2 = s[i++] || ''; } out += '<sub>' + g2 + '</sub>'; prev = ''; continue; }
      if (/\d/.test(c) && /[A-Za-z)\]]/.test(prev)) { var d = s.slice(i).match(/^\d+/)[0]; out += '<sub>' + d + '</sub>'; i += d.length; prev = '0'; continue; }
      if (c === '{' || c === '}') { i++; continue; }
      out += c === '-' ? '−' : c; prev = c; i++;
    }
    return '<span class="up">' + out + '</span>';
  }
  function tex(s) {
    var i = 0, n = s.length;
    function delim() { while (s[i] === ' ') i++; var c = s[i++] || ''; if (c === '\\') { var m2 = s.slice(i).match(/^[a-zA-Z]+/); if (m2) { i += m2[0].length; return m2[0] === 'langle' ? '⟨' : m2[0] === 'rangle' ? '⟩' : ''; } c = s[i++] || ''; } return c; }
    function rawGroup() { if (s[i] !== '{') return s[i] ? s[i++] : ''; var d = 0, st = ++i; for (; i < n; i++) { if (s[i] === '{') d++; else if (s[i] === '}') { if (!d) break; d--; } } var r = s.slice(st, i); i++; return r; }
    function seq(stop) { var o = ''; while (i < n) { var c = s[i]; if (c === '}') { i++; if (stop) return o; continue; } o += withScripts(); } return o; }
    function withScripts() {
      var b = atom();
      for (;;) {
        var j = i; while (s[j] === ' ') j++;
        if (s[j] === '^') { i = j + 1; b += '<sup>' + atom() + '</sup>'; }
        else if (s[j] === '_') { i = j + 1; b += '<sub>' + atom() + '</sub>'; }
        else break;
      }
      return b;
    }
    function atom() {
      while (s[i] === ' ') i++;
      if (i >= n) return '';
      var c = s[i], m, nm;
      if (c === '{') { i++; return seq(true); }
      if (c === '\\') {
        i++; m = s.slice(i).match(/^[a-zA-Z]+/);
        if (!m) { nm = s[i++] || ''; if (nm === '\\') return '<br>'; if (nm === ',' || nm === ';' || nm === ':') return ' '; if (nm === '!') return ''; return nm; }
        nm = m[0]; i += nm.length;
        if (nm === 'frac' || nm === 'dfrac' || nm === 'tfrac') { var a = atom(), d = atom(); return '<span class="fr"><span class="nu">' + a + '</span><span class="de">' + d + '</span></span>'; }
        if (nm === 'binom') { var b1 = atom(), b2 = atom(); return '(<span class="fr"><span class="nu">' + b1 + '</span><span class="de">' + b2 + '</span></span>)'; }
        if (nm === 'sqrt') { if (s[i] === '[') { var k = s.indexOf(']', i); i = k < 0 ? n : k + 1; } return '<span class="sq"><span class="rd">' + SQRT + '</span><span class="ov">' + atom() + '</span></span>'; }
        if (nm === 'ce' || nm === 'pu') return ceFallback(rawGroup());
        if (nm === 'xrightarrow' || nm === 'xrightleftharpoons') { var top = ''; if (s[i] === '[') { var k3 = s.indexOf(']', i); i = k3 < 0 ? n : k3 + 1; } top = atom(); return '<span class="xa"><small>' + top + '</small>' + (nm === 'xrightarrow' ? '→' : '⇌') + '</span>'; }
        if (nm === 'text' || nm === 'mathrm' || nm === 'operatorname' || nm === 'textrm' || nm === 'rm') return '<span class="up">' + rawGroup() + '</span>';
        if (nm === 'mathbf' || nm === 'textbf' || nm === 'boldsymbol' || nm === 'bf') return '<b>' + atom() + '</b>';
        if (nm === 'vec') return '<span class="vc">' + atom() + '</span>';
        if (nm === 'hat') return atom() + '\u0302';
        if (nm === 'bar' || nm === 'overline') return '<span class="ov">' + atom() + '</span>';
        if (nm === 'dot') return atom() + '\u0307';
        if (nm === 'left') { var lc = delim(), inner = ''; while (i < n && s.substr(i, 6) !== '\\right' && s[i] !== '}') inner += withScripts(); var rc = ''; if (s.substr(i, 6) === '\\right') { i += 6; rc = delim(); } return '<span class="dl"><span class="dg">' + dsvg(lc) + '</span><span class="in">' + inner + '</span><span class="dg">' + dsvg(rc) + '</span></span>'; }
        if (nm === 'right') { delim(); return ''; }
        if (nm === 'big' || nm === 'Big' || nm === 'bigg' || nm === 'Bigg' || nm === 'displaystyle' || nm === 'textstyle' || nm === 'limits' || nm === 'nolimits') return '';
        if (nm === 'quad' || nm === 'qquad') return '\u2003';
        if (FUNCS[nm]) return '<span class="up">' + nm + '</span>';
        return SYM[nm] || nm;
      }
      if (/[a-zA-Z]/.test(c)) { m = s.slice(i).match(/^[a-zA-Z]+/)[0]; if (FUNCS[m]) { i += m.length; return '<span class="up">' + m + '</span>'; } i++; return '<i>' + c + '</i>'; }
      if (c === '&') { m = s.slice(i).match(/^&[a-z]+;/); if (m) { i += m[0].length; return m[0]; } }
      if (c === '~') { i++; return ' '; }
      if (c === "'") { i++; return '′'; }
      if (c === '-') { i++; return '−'; }
      i++; return c;
    }
    try { return '<span class="mj">' + seq(false) + '</span>'; } catch (e) { return s; }
  }

  /* ================= math: KaTeX first, tiny converter as fallback ================= */
  var KMACROS = { '\\degC': '^{\\circ}\\mathrm{C}', '\\ohm': '\\Omega', '\\R': '\\mathbb{R}', '\\dd': '\\mathrm{d}' };
  function renderTex(body, disp) {
    body = String(body).trim();
    if (W.katex && W.katex.renderToString) {
      try { return W.katex.renderToString(body, { displayMode: !!disp, throwOnError: true, strict: 'ignore', trust: false, output: 'html', macros: KMACROS }); } catch (e) { /* fall through */ }
    }
    var h = tex(body);
    return disp ? '<span class="mb">' + h + '</span>' : h;
  }
  var MATH_RE = /\$\$([\s\S]+?)\$\$|\\\[([\s\S]+?)\\\]|\\\(([\s\S]+?)\\\)|\$([^$\n\s](?:[^$\n]*?[^$\n\s])?)\$/g;
  function extractMath(t, store) {
    return t.replace(MATH_RE, function (all, a, b, c, d) {
      var disp = a != null || b != null, body = a != null ? a : b != null ? b : c != null ? c : d;
      /* the text was HTML-escaped before; undo it so < > & work inside formulas */
      body = body.replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&');
      store.push(renderTex(body, disp));
      return '\u0001' + (store.length - 1) + '\u0002';
    });
  }

  /* ================= Markdown (headings, lists, tables, code, svg diagrams, math) ================= */
  function escH(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
  function inline(s) {
    return s.replace(/`([^`]+)`/g, '<code>$1</code>').replace(/\*\*([^*]+)\*\*/g, '<b>$1</b>').replace(/(^|[^*\w])\*([^*\n]+?)\*(?![*\w])/g, '$1<i>$2</i>');
  }
  function safeSvg(svg) {
    svg = String(svg).trim();
    if (!/^<svg[\s>]/i.test(svg) || !/<\/svg>\s*$/i.test(svg)) return '';
    if (/<script|<foreignObject|<image|<iframe|\son\w+\s*=|javascript:|(?:xlink:)?href\s*=\s*["']\s*(?:https?:|data:)|@import/i.test(svg)) return '';
    if (!/xmlns=/.test(svg)) svg = svg.replace(/^<svg/i, '<svg xmlns="http://www.w3.org/2000/svg"');
    return '<img class="svgfig" alt="diagram" src="data:image/svg+xml;charset=utf-8,' + encodeURIComponent(svg) + '">';
  }
  function splitRow(l) { var t = l.trim().replace(/^\|/, '').replace(/\|$/, ''); return t.split('|').map(function (x) { return x.trim(); }); }
  function md(src) {
    var store = [], text = String(src == null ? '' : src).replace(/\r/g, '');
    /* ```fenced``` blocks (svg diagrams are drawn as pictures, other code stays as code) */
    text = text.replace(/```([a-zA-Z]*)[ \t]*\n([\s\S]*?)```/g, function (all, lang, body) {
      var h;
      if (/^svg$/i.test(lang) || /^\s*<svg[\s>]/i.test(body)) { h = safeSvg(body) || '<pre><code>' + escH(body) + '</code></pre>'; }
      else h = '<pre><code>' + escH(body.replace(/\n$/, '')) + '</code></pre>';
      store.push('<div class="blk">' + h + '</div>'); return '\n\u0001' + (store.length - 1) + '\u0002\n';
    });
    /* an unfinished fence while the answer is still streaming */
    var open = text.lastIndexOf('```');
    if (open > -1) { var tail = text.slice(open); if (/^```(svg)?/i.test(tail)) { store.push('<div class="blk"><small class="draw">Diagram ban raha hai…</small></div>'); text = text.slice(0, open) + '\n\u0001' + (store.length - 1) + '\u0002\n'; } }
    var lines = extractMath(escH(text), store).split('\n'), out = [], list = null, para = [], m, i = 0;
    function flushP() { if (para.length) { out.push('<p>' + inline(para.join('<br>')) + '</p>'); para = []; } }
    function closeL() { if (list) { out.push('</' + list + '>'); list = null; } }
    for (; i < lines.length; i++) {
      var l = lines[i];
      if (!l.trim()) { flushP(); closeL(); continue; }
      if (/^\s*\|.*\|\s*$/.test(l) && i + 1 < lines.length && /^\s*\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?\s*$/.test(lines[i + 1])) {
        flushP(); closeL();
        var head = splitRow(l), rows = []; i += 2;
        while (i < lines.length && /^\s*\|.*\|?\s*$/.test(lines[i]) && lines[i].trim()) { rows.push(splitRow(lines[i])); i++; }
        i--;
        out.push('<div class="tbw"><table><thead><tr>' + head.map(function (c) { return '<th>' + inline(c) + '</th>'; }).join('') + '</tr></thead><tbody>' +
          rows.map(function (r) { return '<tr>' + r.map(function (c) { return '<td>' + inline(c) + '</td>'; }).join('') + '</tr>'; }).join('') + '</tbody></table></div>');
        continue;
      }
      if ((m = l.match(/^\s*#{1,4}\s+(.*)/))) { flushP(); closeL(); out.push('<p class="h">' + inline(m[1]) + '</p>'); continue; }
      if (/^\s*([-*_])\1{2,}\s*$/.test(l)) { flushP(); closeL(); out.push('<hr>'); continue; }
      if ((m = l.match(/^\s*&gt;\s?(.*)/))) { flushP(); closeL(); out.push('<blockquote>' + inline(m[1]) + '</blockquote>'); continue; }
      if ((m = l.match(/^\s*[-*•]\s+(.*)/))) { flushP(); if (list !== 'ul') { closeL(); out.push('<ul>'); list = 'ul'; } out.push('<li>' + inline(m[1]) + '</li>'); continue; }
      if ((m = l.match(/^\s*\d+[.)]\s+(.*)/))) { flushP(); if (list !== 'ol') { closeL(); out.push('<ol>'); list = 'ol'; } out.push('<li>' + inline(m[1]) + '</li>'); continue; }
      closeL(); para.push(l);
    }
    flushP(); closeL();
    return out.join('').replace(/\u0001(\d+)\u0002/g, function (x, k) { return store[+k]; });
  }

  /* small models often forget the dollar signs: wrap bare LaTeX runs such as v_0 t or \frac{a}{b} */
  var BR = '(?:\\{(?:[^{}]|\\{(?:[^{}]|\\{[^{}]*\\})*\\})*\\})';
  var ATOM = '(?:\\\\[a-zA-Z]+' + BR + '*|[A-Za-z0-9]+(?:[_^](?:' + BR + '|\\w))+|[_^](?:' + BR + '|\\w))';
  var RUN_RE = new RegExp(ATOM + '(?:[ \\t]?(?:' + ATOM + '|[=+\\-*/()|<>]|(?:[A-Za-z]|\\d+(?:\\.\\d+)?)(?![A-Za-z])))*', 'g');
  function fixMath(t) {
    t = String(t || '').replace(/<\/?(?:start|end)_of_turn>/g, '').replace(/^\s*model\s*\n/, '');
    var parts = [], last = 0, m, re = new RegExp(MATH_RE.source, 'g');
    while ((m = re.exec(t))) { parts.push([t.slice(last, m.index), 0]); parts.push([m[0], 1]); last = m.index + m[0].length; }
    parts.push([t.slice(last), 0]);
    return parts.map(function (p) {
      if (p[1]) return p[0];
      return p[0].replace(RUN_RE, function (r) { var tr = r.replace(/\s+$/, ''), sp = r.slice(tr.length); return '$' + tr.replace(/\$/g, '') + '$' + sp; }).replace(/\$\$/g, '$ $');
    }).join('').replace(/\\\\(?![a-zA-Z])/g, '\n');
  }

  /* ================= Gemini (online) ================= */
  var FALLBACK_MODELS = ['gemini-flash-latest', 'gemini-2.5-flash', 'gemini-flash-lite-latest', 'gemini-2.5-flash-lite'];
  var VERTEX_MODELS = ['gemini-2.5-flash', 'gemini-flash-latest', 'gemini-2.5-flash-lite', 'gemini-flash-lite-latest'];
  var chainMem = null, cool = {};
  function GErr(status, msg) { this.status = status; this.msg = msg || ''; }
  function isKeyErr(e) { return e instanceof GErr && (e.status === 401 || e.status === 403 || (e.status === 400 && /api key|API_KEY/i.test(e.msg))); }
  function isVertexKey(k) { return /^AQ\./.test(k || ''); }
  function modelKind(n) { var m = /^gemini-(\d+(?:\.\d+)?)-flash(-lite)?(-preview[\w.-]*)?$/.exec(n); return m ? { v: parseFloat(m[1]), lite: m[2] ? 1 : 0, pre: m[3] ? 1 : 0 } : null; }
  async function modelChain(key) {
    if (isVertexKey(key)) return VERTEX_MODELS;
    if (chainMem && chainMem.k === key && Date.now() - chainMem.t < 6 * 3600e3) return chainMem.list;
    var list = [], cached = lsGet('mst_ai_models', null);
    if (cached && cached.k === key && cached.list && Date.now() - cached.t < 24 * 3600e3) list = cached.list;
    else {
      var res = null;
      try { res = await fetch('https://generativelanguage.googleapis.com/v1beta/models?pageSize=200', { headers: { 'x-goog-api-key': key } }); } catch (e) { res = null; }
      if (res && res.ok) {
        var j = await res.json(), found = [];
        (j.models || []).forEach(function (m) {
          var n = String(m.name || '').replace(/^models\//, ''), k = modelKind(n);
          if (k && (m.supportedGenerationMethods || []).indexOf('generateContent') > -1) found.push({ n: n, k: k });
        });
        found.sort(function (x, y) { return y.k.v - x.k.v || x.k.lite - y.k.lite || x.k.pre - y.k.pre; });
        list = found.slice(0, 3).map(function (x) { return x.n; });
        if (list.length) lsSet('mst_ai_models', { t: Date.now(), k: key, list: list });
      } else if (res) {
        var msg = ''; try { var jj = await res.json(); msg = jj.error && jj.error.message || ''; } catch (e) {}
        if (res.status === 400 || res.status === 401 || res.status === 403) throw new GErr(res.status, msg);
      }
    }
    var out = []; list.concat(FALLBACK_MODELS).forEach(function (n) { if (out.indexOf(n) < 0) out.push(n); });
    out = out.slice(0, 6); chainMem = { t: Date.now(), k: key, list: out };
    return out;
  }
  function gemParts(j) { var c = j && j.candidates && j.candidates[0], p = c && c.content && c.content.parts || [], t = ''; p.forEach(function (x) { if (x.text && !x.thought) t += x.text; }); return t; }
  /* new "AQ." keys: try Bearer, ?key= and Vertex until Google accepts one (the winner is remembered) */
  async function postAuth(key, model, body) {
    var enc = encodeURIComponent, json = { 'Content-Type': 'application/json' };
    var gl = 'https://generativelanguage.googleapis.com/v1beta/models/' + enc(model) + ':streamGenerateContent?alt=sse';
    function req(kind) {
      if (kind === 'bearer') return [gl, { 'Content-Type': 'application/json', Authorization: 'Bearer ' + key }];
      if (kind === 'query') return [gl + '&key=' + enc(key), json];
      if (kind === 'vertex') return ['https://aiplatform.googleapis.com/v1/publishers/google/models/' + enc(model) + ':streamGenerateContent?alt=sse&key=' + enc(key), json];
      return [gl, { 'Content-Type': 'application/json', 'x-goog-api-key': key }];
    }
    var aq = isVertexKey(key), kinds = aq ? ['bearer', 'query', 'vertex'] : ['header'], mem = lsGet('mst_ai_auth', null);
    if (aq && mem && kinds.indexOf(mem) > -1) kinds = [mem].concat(kinds.filter(function (k) { return k !== mem; }));
    var lastRes = null, lastErr = null;
    for (var i = 0; i < kinds.length; i++) {
      try {
        var r = req(kinds[i]), res = await fetch(r[0], { method: 'POST', headers: r[1], body: body });
        if (res.status === 401 || res.status === 403) { lastRes = res; continue; }
        if (aq && res.ok) lsSet('mst_ai_auth', kinds[i]);
        return res;
      } catch (e) { lastErr = e; }
    }
    if (lastRes) return lastRes;
    throw lastErr;
  }
  function liveInfo() {
    var today = ''; try { today = new Date().toLocaleDateString('en-IN', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' }); } catch (e) { today = new Date().toDateString(); }
    return '\n\nTODAY IS ' + today + ' (date on the student\'s phone). You have Google Search: for anything current or recent (exam dates, results, cut-offs, syllabus changes, news, latest-year papers) search first and trust the search results and today\'s date over your training memory. Never invent past-paper questions or claim a question came in a particular exam unless you found it by search or are certain. For comparisons or match-the-column use a Markdown table (header row, then a |---|---| row).' +
      '\n\nDIAGRAMS: when the student asks for a diagram, figure, chart, flowchart, graph, sketch or says draw/banao, never use ASCII art. Reply with ONE complete, valid, self-contained SVG inside a ```svg fenced block, then the explanation in text below it. SVG rules: <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 H"> with H between 380 and 620, no width/height attributes; first element a background <rect width="360" height="H" fill="#f8fafc"/>; a bold 15px title; all text in English (NCERT terms), font-size 11-13, dark fill (#0f172a), centred inside its shape, no overlapping text; soft pastel fills with darker strokes, real shapes (ellipses, paths, curves, axes with ticks and units), arrows with a <marker> arrowhead. Follow the NCERT figure and omit a detail rather than invent it. Forbidden: <script>, <foreignObject>, <image>, external links or fonts, event attributes. Keep the SVG under about 6000 characters.';
  }
  function thinkPlan(q, hasImg) {
    var t = String(q).toLowerCase(), words = t.split(/\s+/).filter(Boolean).length;
    var heavy = hasImg || /solve|calculate|calculation|derive|derivation|prove|proof|numerical|find the|nikalo|nikal do|hal karo|kitna|how much|\d+(\.\d+)?\s*(m\/s|kg|n\b|j\b|w\b|hz|cm|mm|ml|mol|k\b|°|rad|m\b|s\b)|integrate|differentiate|assertion|reason|statement|match|why .*(not|only)|compare and explain/.test(t);
    var quick = !heavy && (words <= 7 || /^(hi|hello|hey|namaste|thanks|thank you|ok|okay|shukriya|dhanyavad)\b/.test(t) || /(full form|definition|define|kya hota hai|kya hai|meaning|formula|unit|si unit|kaun|which|who |name the|list)\b/.test(t) && words <= 14);
    var long = /diagram|table|column|flowchart|draw|banao|sketch/.test(t);
    var live = /latest|today|aaj|current|news|result|cutoff|cut off|kab hai|exam date|admit card|notification|202[5-9]|syllabus|rank|price|live|abhi|recent/.test(t);
    var lvl = heavy ? 'deep' : (quick ? 'quick' : 'mid');
    return { lvl: lvl, level: lvl === 'deep' ? 'medium' : (lvl === 'quick' ? 'minimal' : 'low'), budget: lvl === 'deep' ? 6000 : (lvl === 'quick' ? 0 : 1024), maxTok: (long ? 8192 : 3072) + (lvl === 'deep' ? 6000 : (lvl === 'quick' ? 0 : 1024)), search: live, to: lvl === 'deep' ? 70000 : 30000 };
  }
  function withTimeout(p, ms) {
    return new Promise(function (ok, no) {
      var t = setTimeout(function () { var ge = new GErr(0, 'Gemini ne bahut der tak jawab nahi diya'); ge.timeout = true; no(ge); }, ms);
      p.then(function (v) { clearTimeout(t); ok(v); }, function (e) { clearTimeout(t); no(e); });
    });
  }
  async function callModel(key, model, sys, msgs, onText, opt) {
    function mk(search, think) {
      var o = {
        systemInstruction: { parts: [{ text: sys + liveInfo() }] },
        contents: msgs.map(function (m) { var pt = [{ text: m.text }]; if (m.img && m.img.data) pt.push({ inlineData: { mimeType: m.img.mime, data: m.img.data } }); return { role: m.role === 'user' ? 'user' : 'model', parts: pt }; }),
        generationConfig: { temperature: 0.4, maxOutputTokens: opt.maxTok }
      };
      if (think) o.generationConfig.thinkingConfig = /gemini-3/.test(model) ? { thinkingLevel: opt.level } : { thinkingBudget: opt.budget };
      if (search) o.tools = [{ google_search: {} }];
      return JSON.stringify(o);
    }
    var res = await withTimeout(postAuth(key, model, mk(opt.search, true)), opt.to);
    if (!res.ok && (res.status === 400 || res.status === 403 || res.status === 429)) {
      try {
        var res2 = res.status === 400 ? await withTimeout(postAuth(key, model, mk(opt.search, false)), opt.to) : await withTimeout(postAuth(key, model, mk(false, true)), opt.to);
        if (!res2.ok) res2 = await withTimeout(postAuth(key, model, mk(false, false)), opt.to);
        if (res2.ok) res = res2;
      } catch (e) {}
    }
    if (!res.ok) { var msg = ''; try { var j = await res.json(); msg = j.error && j.error.message || ''; } catch (e) {} throw new GErr(res.status, msg); }
    var full = '';
    if (!res.body || !res.body.getReader) { var jj = await res.text(); try { JSON.parse(jj).forEach(function (x) { full += gemParts(x); }); } catch (e) {} if (full) onText(full); }
    else {
      var reader = res.body.getReader(), dec = new TextDecoder(), buf = '';
      for (;;) {
        var r; try { r = await withTimeout(reader.read(), opt.to + 15000); } catch (te) { try { reader.cancel(); } catch (x) {} if (full) break; throw te; }
        if (r.done) break;
        buf += dec.decode(r.value, { stream: true });
        var i;
        while ((i = buf.indexOf('\n')) > -1) {
          var line = buf.slice(0, i).replace(/\r$/, '').trim(); buf = buf.slice(i + 1);
          if (line.indexOf('data:') !== 0) continue;
          var d = line.slice(5).trim(); if (!d || d === '[DONE]') continue;
          try { var t = gemParts(JSON.parse(d)); if (t) { full += t; onText(full); } } catch (e) {}
        }
      }
    }
    if (!full) throw new GErr(0, 'Khaali jawab aaya.');
    return full;
  }
  async function askGemini(sys, msgs, onText, opt) {
    var key = settings().key;
    var models = await modelChain(key), avail = models.filter(function (m) { return !(cool[m] > Date.now()); }), lastErr = null, tmo = 0;
    if (!avail.length) { cool = {}; avail = models; }
    for (var i = 0; i < avail.length; i++) {
      try { return { text: await callModel(key, avail[i], sys, msgs, onText, opt), model: avail[i] }; }
      catch (e) {
        lastErr = e;
        if (!(e instanceof GErr) || isKeyErr(e)) throw e;
        if (e.timeout && ++tmo >= 2) throw e;
        if (e.status === 429 || e.status === 503) cool[avail[i]] = Date.now() + 60000;
        if (e.status === 404 || e.status === 400) chainMem = null;
      }
    }
    throw lastErr || new GErr(0, 'Koi model available nahi.');
  }
  function friendly(e) {
    if (e instanceof GErr) {
      if (isKeyErr(e)) return (e.status === 400 ? 'Gemini API key galat lag rahi hai. Settings mein dobara check karo.' : 'Gemini ne is key ko allow nahi kiya (' + e.status + '). Naya key aistudio.google.com/apikey se banao (AIza... se shuru hota hai).') + (e.msg ? '\n\nGoogle ka message: ' + e.msg.slice(0, 220) : '');
      if (e.status === 429) return 'Gemini ki free limit abhi poori ho gayi hai. Thodi der baad try karo.';
      if (e.status === 503 || e.status === 500) return 'Gemini abhi busy hai. Thodi der baad try karo.';
      if (e.timeout) return 'Gemini ne bahut der tak jawab nahi diya. Internet check karke dobara try karo.';
      return 'Gemini se jawab nahi aaya' + (e.status ? ' (' + e.status + ')' : '') + (e.msg ? ': ' + e.msg : '') + '.';
    }
    if (e && e.userMsg) return e.message;
    return e && e.message && !/Failed to fetch|NetworkError|Load failed/i.test(e.message) ? e.message : 'Internet ya Gemini se connect nahi ho paya.';
  }

  /* ================= Gemma (offline) ================= */
  var G = null;
  try { if (W.Capacitor && W.Capacitor.isPluginAvailable && W.Capacitor.isPluginAvailable('Gemma')) G = W.Capacitor.Plugins.Gemma; } catch (e) { G = null; }
  var webLlm = null;
  function uerr(msg) { var e = new Error(msg); e.userMsg = true; return e; }
  var Gemma = {
    native: !!G,
    loaded: function () { return !!webLlm || Gemma._nativeLoaded === true; },
    hasModel: async function () {
      if (G) { try { return !!(await G.status()).hasModel; } catch (e) { return false; } }
      return !!webLlm;
    },
    /* loads a model that is already saved in the app (native) or already picked (browser) */
    ensure: async function () {
      if (G) {
        var s = await G.status();
        if (!s.hasModel) throw uerr('Gemma model abhi set nahi hai. AI Settings mein "Choose file" se model chuno.');
        if (!s.loaded) await G.load();
        Gemma._nativeLoaded = true; return;
      }
      if (!webLlm) throw uerr('Offline Gemma sirf installed app mein chalta hai (ya AI Settings se model load karo).');
    },
    /* native: pick the .task file once, the app copies it inside itself */
    pick: async function (onProgress) {
      if (!G) throw uerr('File picker sirf installed app mein hai.');
      var h = await G.addListener('progress', function (p) { if (onProgress) onProgress(p.pct); });
      try { await G.pickModel(); } finally { try { h.remove(); } catch (e) {} }
      await G.load(); Gemma._nativeLoaded = true;
    },
    loadSaved: async function () { if (!G) throw uerr('Saved model sirf installed app mein hota hai.'); await G.load(); Gemma._nativeLoaded = true; },
    /* browser only: MediaPipe in a WebGPU browser */
    loadWeb: async function (source) {
      if (!('gpu' in navigator)) throw uerr('Is browser/WebView mein WebGPU nahi hai, isliye on-device AI nahi chalega.');
      var tries = [['./libs/genai_bundle.mjs', './libs/wasm'], ['https://cdn.jsdelivr.net/npm/@mediapipe/tasks-genai@latest/genai_bundle.mjs', 'https://cdn.jsdelivr.net/npm/@mediapipe/tasks-genai@latest/wasm']];
      var mod = null, fileset = null;
      for (var i = 0; i < tries.length && !mod; i++) {
        try { var m = await import(tries[i][0]); fileset = await m.FilesetResolver.forGenAiTasks(tries[i][1]); mod = m; } catch (e) { mod = null; }
      }
      if (!mod) throw uerr('Engine files nahi mili (libs/genai_bundle.mjs). Installed app mein ye sab apne aap kaam karta hai.');
      var base = typeof source === 'string' ? { modelAssetPath: source } : { modelAssetBuffer: source.stream().getReader() };
      webLlm = await mod.LlmInference.createFromOptions(fileset, { baseOptions: base, maxTokens: 2048, topK: 40, temperature: 0.5, randomSeed: 101 });
    },
    generate: async function (prompt, onText) {
      var clean = function (t) { return fixMath(String(t || '').replace(/<end_of_turn>[\s\S]*$/, '').trim()); };
      if (G) { var r = await G.generate({ prompt: prompt }); var out = clean(r.text); if (onText) onText(out); return out; }
      var full = '';
      await webLlm.generateResponse(prompt, function (part) { full += part; if (onText) onText(clean(full)); });
      return clean(full);
    }
  };

  /* ================= prompts ================= */
  var RULES = 'You are "SK AI", a friendly NEET tutor (Physics, Chemistry, Botany, Zoology) inside the Success Kit app (PW NEET Success Kit 2026-27 tests, Class 11 + 12 NCERT based). ' +
    'Rules:\n- Reply in the same language the student uses (Hindi, English or Hinglish). Keep it short and step by step.\n' +
    '- For an MCQ: first write the correct option like "**Answer: (3)**", then the reason in a few lines, then a quick trick or NCERT point, and one line on why the tempting wrong option is wrong. If options are not visible, solve it and say so.\n' +
    '- For a numerical: show the steps with units and a clear final answer. For theory: give the key points the way NCERT states them.\n' +
    '- MATH: write every formula in LaTeX between dollar signs, e.g. $v = u + at$, $s = ut + \\frac{1}{2}at^2$, $\\sqrt{gR}$, $\\Delta T$, $\\omega$, $\\vec{F} = m\\vec{a}$. Put an important formula alone on a line as $$ ... $$. Units go in \\text{}, e.g. $9.8\\ \\text{m/s}^2$. Never write math with curly braces in plain text.\n' +
    '- CHEMISTRY: write formulas and reactions with \\ce{}, e.g. $\\ce{H2SO4}$, $\\ce{SO4^2-}$, $\\ce{2H2 + O2 -> 2H2O}$, $\\ce{N2 + 3H2 <=> 2NH3}$.\n' +
    '- If you are not sure, say so. Do not invent facts, numbers or question numbers.';
  var G_RULES = 'You are SK AI, a NEET tutor (Physics, Chemistry, Biology). Answer in simple English or the student\'s language, short and correct. Use only standard textbook formulas; never invent numbers. ' +
    'Write every formula inside dollar signs like $v = u + at$ or $F = \\frac{G m_1 m_2}{r^2}$, and chemistry like $\\ce{H2O}$ or $\\ce{2H2 + O2 -> 2H2O}$. Use bullet points starting with "- ". For an MCQ start with "Answer: (option number)". If asked for a diagram, give a short numbered flow instead of drawing.';
  function gemmaPrompt(ctx, q) {
    return '<start_of_turn>user\n' + G_RULES + (ctx ? '\n\nCONTEXT:\n' + ctx : '') + '\n\nQuestion: ' + q + '<end_of_turn>\n<start_of_turn>model\n';
  }

  /* ================= engine choice + one call that does everything ================= */
  async function engineInfo(hasImg) {
    var S = settings(), online = navigator.onLine !== false, dev = await Gemma.hasModel(), eng = 'none';
    if (S.mode === 'device') eng = dev ? 'device' : 'none';
    else if (S.mode === 'gemini') eng = S.key ? 'gemini' : 'none';
    else if (S.key && online) eng = 'gemini';
    else if (dev) eng = 'device';
    else eng = S.key ? 'gemini' : 'none';
    if (hasImg && eng === 'device') eng = S.key ? 'gemini' : 'none';
    return { engine: eng, S: S, online: online, device: dev };
  }
  /* o = { q, img, past:[{role:'user'|'ai', text}], sys (extra system text for Gemini), ctx (short context for Gemma), onText(html-source), onStage(text) }
     returns { text, label }. Throws on failure (use friendly(e) for the message). */
  async function run(o) {
    var info = await engineInfo(!!o.img), eng = info.engine, S = info.S;
    if (eng === 'none') {
      if (o.img && !S.key) throw uerr('Photo / page image samajhne ke liye Gemini chahiye. AI Settings mein Gemini API key daalo. Gemma 1B (offline) sirf text padh sakta hai.');
      throw uerr('AI abhi set up nahi hai. AI Settings mein Gemini API key daalo (online ke liye) ya Gemma model chuno (offline ke liye).');
    }
    var onText = o.onText || function () {};
    if (eng === 'gemini') {
      var past = [], hs = (o.past || []).slice();
      for (var hi = 0; hi + 1 < hs.length; hi++) { if (hs[hi].role === 'user' && hs[hi + 1].role !== 'user') { past.push({ role: 'user', text: hs[hi].text }, { role: 'model', text: hs[hi + 1].text }); hi++; } }
      past = past.slice(-6);
      var msgs = past.concat([{ role: 'user', text: o.q, img: o.img || null }]);
      try {
        var g = await askGemini(RULES + (o.sys ? '\n\n' + o.sys : ''), msgs, onText, thinkPlan(o.q, !!o.img));
        return { text: g.text, label: 'Gemini · ' + g.model };
      } catch (e) {
        if (!(S.mode === 'auto' && !o.img && !isKeyErr(e) && info.device)) throw e;
        if (o.onStage) o.onStage('Gemini nahi chala, offline Gemma se jawab…');
      }
    }
    if (o.onStage) o.onStage('Gemma soch raha hai…');
    await Gemma.ensure();
    var text = await Gemma.generate(gemmaPrompt(o.ctx, o.q), onText);
    if (!text) throw uerr('Khaali jawab aaya.');
    return { text: text, label: 'Gemma · on-device' };
  }

  /* ================= images ================= */
  function imageFromFile(file, maxDim) {
    maxDim = maxDim || 1400;
    return new Promise(function (ok, no) {
      var rd = new FileReader();
      rd.onerror = function () { no(new Error('Photo padh nahi paya.')); };
      rd.onload = function () {
        var im = new Image();
        im.onload = function () {
          var sc = Math.min(1, maxDim / Math.max(im.width, im.height)), cv = document.createElement('canvas');
          cv.width = Math.max(1, Math.round(im.width * sc)); cv.height = Math.max(1, Math.round(im.height * sc));
          var cx = cv.getContext('2d'); cx.fillStyle = '#fff'; cx.fillRect(0, 0, cv.width, cv.height); cx.drawImage(im, 0, 0, cv.width, cv.height);
          var url = cv.toDataURL('image/jpeg', 0.85); ok({ mime: 'image/jpeg', data: url.split(',')[1], url: url });
        };
        im.onerror = function () { no(new Error('Ye photo khul nahi payi.')); };
        im.src = rd.result;
      };
      rd.readAsDataURL(file);
    });
  }
  function imageFromCanvas(cv, maxDim) {
    maxDim = maxDim || 1500;
    var sc = Math.min(1, maxDim / Math.max(cv.width, cv.height)), t = document.createElement('canvas');
    t.width = Math.max(1, Math.round(cv.width * sc)); t.height = Math.max(1, Math.round(cv.height * sc));
    var cx = t.getContext('2d'); cx.fillStyle = '#fff'; cx.fillRect(0, 0, t.width, t.height); cx.drawImage(cv, 0, 0, t.width, t.height);
    var url = t.toDataURL('image/jpeg', 0.82); return { mime: 'image/jpeg', data: url.split(',')[1], url: url };
  }

  /* ================= styles shared by both screens ================= */
  var css = document.createElement('style');
  css.textContent =
    '.md p{margin:0 0 8px}.md p:last-child{margin-bottom:0}.md ul,.md ol{margin:4px 0 8px 20px;padding:0}.md li{margin:2px 0}' +
    '.md b{color:#fff}.md .h{font-weight:700;color:#fff}.md hr{border:none;border-top:1px solid var(--line,rgba(255,255,255,.14));margin:8px 0}' +
    '.md blockquote{margin:6px 0;padding:4px 10px;border-left:3px solid rgba(16,185,129,.7);color:var(--soft,#8FB0A0)}' +
    '.md code{background:rgba(255,255,255,.08);padding:1px 6px;border-radius:6px;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:13.5px}' +
    '.md pre{background:rgba(0,0,0,.35);border-radius:10px;padding:10px 12px;overflow-x:auto;margin:6px 0}.md pre code{background:none;padding:0}' +
    '.md .tbw{overflow-x:auto;margin:6px 0;-webkit-overflow-scrolling:touch}.md table{border-collapse:collapse;font-size:13.5px;min-width:100%}' +
    '.md th,.md td{border:1px solid var(--line,rgba(255,255,255,.18));padding:6px 9px;text-align:left;vertical-align:top}.md th{background:rgba(255,255,255,.07)}' +
    '.md .blk{margin:6px 0}.md .svgfig{display:block;width:100%;max-width:420px;height:auto;margin:0 auto;border-radius:12px;background:#f8fafc}.md .draw{color:var(--soft,#8FB0A0)}' +
    '.md .katex{font-size:1.06em}.md .katex-display{margin:8px 0;overflow-x:auto;overflow-y:hidden;padding:2px 0}.md .katex-display>.katex{white-space:nowrap}' +
    '.md .mj{font-family:"Times New Roman",Georgia,serif;font-size:1.1em}.md .mj i{font-style:italic}.md .mj .up{font-style:normal}.md .mj sup,.md .mj sub{font-size:.72em;line-height:0}' +
    '.md .sq{display:inline-flex;align-items:stretch;vertical-align:middle}.md .sq>.rd{position:relative;width:.8em;flex:none}.md .rd svg,.md .dg svg{position:absolute;left:0;top:0;width:100%;height:100%;overflow:visible}' +
    '.md .sq>.ov{padding:2px .2em 0 .05em}.md .dl{display:inline-flex;align-items:stretch;vertical-align:middle}.md .dl>.dg{position:relative;width:.5em;flex:none}.md .dl>.in{padding:0 1px}' +
    '.md .mb{display:block;text-align:center;margin:8px 0;overflow-x:auto;padding:4px 0}.md .fr{display:inline-flex;flex-direction:column;vertical-align:middle;text-align:center;margin:0 3px;font-size:.95em}' +
    '.md .fr>.nu{border-bottom:1px solid currentColor;padding:0 4px}.md .fr>.de{padding:0 4px}.md .ov{border-top:1px solid currentColor;padding:0 1px}' +
    '.md .vc{position:relative;display:inline-block}.md .vc::before{content:"\\2192";position:absolute;top:-.62em;left:0;right:0;text-align:center;font-size:.7em;font-style:normal}' +
    '.md .xa{display:inline-flex;flex-direction:column;align-items:center;vertical-align:middle;margin:0 3px}.md .xa small{font-size:.65em;line-height:1}';
  (document.head || document.documentElement).appendChild(css);

  /* ================= status pill + settings sheet (same UI on both screens) ================= */
  async function statusInfo() {
    var S = settings(), online = navigator.onLine !== false, dev = await Gemma.hasModel(), txt, on = false;
    if (S.mode === 'device') { txt = dev ? 'Gemma · offline ready' : 'Gemma · model not set'; on = dev; }
    else if (S.mode === 'gemini') { txt = S.key ? (online ? 'Gemini · online' : 'Gemini · no internet') : 'Add Gemini key in settings'; on = !!S.key && online; }
    else if (S.key && online) { txt = 'Gemini · online'; on = true; }
    else if (dev) { txt = 'Gemma · offline'; on = true; }
    else { txt = S.key ? 'Offline · set up Gemma in settings' : 'Not set up · open settings'; }
    return { text: txt, on: on };
  }
  var sheetCss = document.createElement('style');
  sheetCss.textContent =
    '.msai-bg{position:fixed;inset:0;z-index:2147483000;background:rgba(0,0,0,.6);display:flex;align-items:flex-end;justify-content:center}' +
    '.msai-sheet{width:min(100%,560px);max-height:92vh;overflow-y:auto;background:#0F2419;color:#F4F6FB;border:1px solid rgba(255,255,255,.14);border-radius:22px 22px 0 0;padding:18px 18px calc(18px + env(safe-area-inset-bottom));font:14.5px/1.5 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}' +
    '.msai-sheet h3{margin:0 0 6px;font-size:18px}.msai-sheet .hint{margin:0 0 12px;color:#8FB0A0;font-size:13px;line-height:1.55}' +
    '.msai-sheet label{display:block;margin:12px 0 6px;font-size:12.5px;font-weight:700;color:#8FB0A0}' +
    '.msai-sheet select,.msai-sheet input[type=text],.msai-sheet input[type=password]{width:100%;box-sizing:border-box;background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.16);border-radius:12px;color:#F4F6FB;font:inherit;padding:12px;outline:none}' +
    '.msai-sheet select option{color:#000}.msai-sheet .pw{display:flex;gap:8px}.msai-sheet .box{margin-top:16px;padding:12px;border:1px solid rgba(255,255,255,.14);border-radius:14px;background:rgba(255,255,255,.04)}' +
    '.msai-sheet .box h4{margin:0 0 6px;font-size:14px}.msai-sheet .row{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px}' +
    '.msai-sheet button{font:inherit;font-weight:700;border-radius:12px;padding:11px 14px;border:1px solid rgba(255,255,255,.16);background:rgba(255,255,255,.07);color:#F4F6FB;cursor:pointer}' +
    '.msai-sheet button.go{background:linear-gradient(135deg,#10B981,#047857);border-color:transparent;color:#fff}.msai-sheet button:disabled{opacity:.45}' +
    '.msai-sheet .st{margin-top:10px;font-size:13px;color:#8FB0A0}.msai-sheet .st.ok{color:#4ADE80}.msai-sheet .st.bad{color:#F87171}' +
    '.msai-sheet .acts{display:flex;gap:10px;margin-top:18px}.msai-sheet .acts button{flex:1}';
  (document.head || document.documentElement).appendChild(sheetCss);

  function openSettings(onDone) {
    var S = settings(), bg = document.createElement('div'); bg.className = 'msai-bg';
    var isApp = Gemma.native;
    bg.innerHTML =
      '<div class="msai-sheet" role="dialog" aria-modal="true" aria-label="AI settings"><h3>AI Settings</h3>' +
      '<p class="hint">Online mein <b>Gemini</b>, offline mein phone par chalne wala <b>Gemma</b>. Key sirf is phone mein save hoti hai.</p>' +
      '<label for="msaiMode">Mode</label><select id="msaiMode"><option value="auto">Auto (online → Gemini, offline → Gemma)</option><option value="gemini">Only Gemini (online)</option><option value="device">Only Gemma (offline)</option></select>' +
      '<label for="msaiKey">Gemini API key</label><div class="pw"><input id="msaiKey" type="password" autocomplete="off" autocapitalize="off" spellcheck="false" placeholder="AIza…"><button id="msaiShow" type="button">Show</button></div>' +
      '<div class="hint" style="margin-top:6px">Free key: aistudio.google.com/apikey</div>' +
      '<div class="box"><h4>Offline Gemma 3 1B</h4><div class="hint" id="msaiGHint" style="margin:0">' +
      (isApp ? 'Gemma 3 1B <b>.task</b> file (~528 MB) <b>Choose model file</b> se ek baar chuno. App use apne andar copy karke hamesha yaad rakhegi, phir bina internet ke chalega.' :
        'Browser mein Gemma ke liye WebGPU chahiye. Pakka offline AI ke liye APK app use karo.') +
      '</div><div class="row">' +
      (isApp ? '<button id="msaiPick" type="button">Choose model file…</button><button id="msaiLoad" type="button">Load saved model</button>' :
        '<button id="msaiPickW" type="button">Choose file…</button><button id="msaiLoadW" type="button">Load from models/</button><input id="msaiFile" type="file" accept=".task,.bin,.litertlm" hidden>') +
      '</div><div class="st" id="msaiSt">…</div></div>' +
      '<div class="acts"><button id="msaiClose" type="button">Close</button><button id="msaiSave" class="go" type="button">Save</button></div></div>';
    document.body.appendChild(bg);
    var $ = function (id) { return bg.querySelector('#' + id); };
    function say(t, cls) { var e = $('msaiSt'); e.textContent = t; e.className = 'st' + (cls ? ' ' + cls : ''); }
    function lock(b) { ['msaiPick', 'msaiLoad', 'msaiPickW', 'msaiLoadW'].forEach(function (id) { var e = $(id); if (e) e.disabled = b; }); }
    $('msaiMode').value = S.mode; $('msaiKey').value = S.key;
    function close() { if (bg.parentNode) bg.parentNode.removeChild(bg); if (onDone) onDone(); }
    $('msaiClose').onclick = close;
    bg.addEventListener('click', function (e) { if (e.target === bg) close(); });
    $('msaiShow').onclick = function () { var f = $('msaiKey'), sh = f.type === 'password'; f.type = sh ? 'text' : 'password'; this.textContent = sh ? 'Hide' : 'Show'; };
    $('msaiSave').onclick = function () { saveSettings({ mode: $('msaiMode').value, key: $('msaiKey').value }); chainMem = null; close(); };
    Gemma.hasModel().then(function (h) { say(h ? (Gemma.loaded() ? 'Gemma ready ✓' : 'Saved model mila ✓ (pehle sawal par load hoga)') : 'Model abhi set nahi hai.', h ? 'ok' : ''); });
    function guard(fn) { lock(true); fn().then(function () { say('Gemma ready ✓ (model app mein saved hai)', 'ok'); }, function (e) { say(e && e.message ? e.message : 'Gemma load nahi hua.', 'bad'); }).then(function () { lock(false); }); }
    if (isApp) {
      $('msaiPick').onclick = function () { say('File copy ho rahi hai… 0%'); guard(function () { return Gemma.pick(function (p) { say('Model app mein copy ho raha hai… ' + p + '% (sirf ek baar)'); }).then(function () { say('Gemma load ho raha hai…'); }); }); };
      $('msaiLoad').onclick = function () { say('Gemma load ho raha hai… (kuch seconds)'); guard(function () { return Gemma.loadSaved(); }); };
    } else {
      $('msaiPickW').onclick = function () { $('msaiFile').click(); };
      $('msaiFile').onchange = function () { var f = this.files && this.files[0]; if (f) { say('Gemma load ho raha hai… (thoda time lagega)'); guard(function () { return Gemma.loadWeb(f); }); } };
      $('msaiLoadW').onclick = function () { say('Gemma load ho raha hai…'); guard(function () { return Gemma.loadWeb('models/gemma3-1b-it-int4.task'); }); };
    }
  }

  W.MSAI = {
    settings: settings, saveSettings: saveSettings,
    md: md, fixMath: fixMath, renderTex: renderTex, tex: tex,
    Gemma: Gemma, run: run, engineInfo: engineInfo, friendly: friendly, isKeyErr: isKeyErr,
    thinkPlan: thinkPlan, RULES: RULES, imageFromFile: imageFromFile, imageFromCanvas: imageFromCanvas,
    statusInfo: statusInfo, openSettings: openSettings,
    hasKatex: function () { return !!(W.katex && W.katex.renderToString); }
  };
})();
