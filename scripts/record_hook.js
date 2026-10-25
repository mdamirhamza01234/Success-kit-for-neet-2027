/* Injected into every mock test at build time.
   build_manifest.py patches each test's finishTest() so that it calls window.__mstCapture(...)
   with the questions, the user's answers and the time left. This file saves that result into the
   app's storage (shown in "Test Records"), adds a "Home" button on the result screen and asks
   before leaving a running test with the back button. */
(function () {
  var KEY = 'mst_records';
  var saved = false;
  var started = false;

  var m = location.pathname.match(/m(\d+)\.html/i);
  var setNo = m ? parseInt(m[1], 10) : null;

  // remember that the test was started (click on the "Start Test" button)
  document.addEventListener('click', function (e) {
    var el = e.target && e.target.closest ? e.target.closest('button') : null;
    if (el && /start/i.test((el.id || '') + ' ' + (el.textContent || ''))) started = true;
  }, true);

  // called from the patched finishTest() of each test
  window.__mstCapture = function (n, ranges, get, timeLeft, total) {
    if (saved) return;
    saved = true;
    try { record(n, ranges, get, timeLeft, total); }
    catch (e) { try { console.log('mst record failed', e); } catch (_) {} }
    try { addHomeButton(); } catch (e) {}
  };

  function record(n, ranges, get, timeLeft, total) {
    var score = 0, c = 0, w = 0, s = 0;
    var subjects = ranges.map(function (r) { return r.name; });
    var subj = ranges.map(function () { return 0; });
    var max = ranges.map(function (r) { return (r.end - r.start) * 4; });
    var rows = [];
    for (var i = 0; i < n; i++) {
      var r = get(i);
      var si = 0;
      for (var k = 0; k < ranges.length; k++) if (i >= ranges[k].start && i < ranges[k].end) { si = k; break; }
      var v;
      if (r.c === 'skipped') { v = 's'; s++; }
      else if (r.c === 'correct') { v = r.bonus ? 'b' : 'g'; c++; }
      else if (r.c === 'partial') { v = 'p'; w++; }
      else { v = 'r'; w++; }
      score += r.m; subj[si] += r.m;
      rows.push([i + 1, si, r.ch || 0, r.key, v]);
    }
    var now = Date.now();
    var rec = {
      id: now, set: setNo, ts: now,
      title: setNo ? 'Success Kit Test ' + (setNo < 10 ? '0' : '') + setNo + ' · Mock' : document.title,
      score: Math.round(score * 100) / 100, max: n * 4,
      correct: c, wrong: w, skipped: s,
      subjects: subjects, subj: subj, subjMax: max,
      timeSec: Math.max(0, (Number(total) || 0) - (Number(timeLeft) || 0)),
      qs: rows
    };
    var list = [];
    try { list = JSON.parse(localStorage.getItem(KEY) || '[]'); if (!Array.isArray(list)) list = []; } catch (e) { list = []; }
    list.push(rec);
    localStorage.setItem(KEY, JSON.stringify(list));
  }

  function addHomeButton() {
    if (document.getElementById('mst-home')) return;
    var b = document.createElement('button');
    b.id = 'mst-home';
    b.textContent = '← Home · result saved';
    b.style.cssText = 'position:fixed;left:50%;bottom:16px;transform:translateX(-50%);z-index:2147483647;' +
      'padding:12px 20px;border-radius:999px;border:1px solid rgba(255,255,255,.25);background:#0A1D14;color:#fff;' +
      'font:600 14px system-ui,sans-serif;box-shadow:0 8px 24px rgba(0,0,0,.4);cursor:pointer';
    b.onclick = function () {
      try { sessionStorage.setItem('mst_goto', 'records'); } catch (e) {}
      location.href = '../index.html#records';
    };
    document.body.appendChild(b);
  }

  // Back button: ask before leaving a running test
  try { history.pushState({ mst: 1 }, ''); } catch (e) {}
  window.addEventListener('popstate', function () {
    if (started && !saved) {
      if (!confirm('Leave the test? Your progress will be lost.')) {
        try { history.pushState({ mst: 1 }, ''); } catch (e) {}
        return;
      }
    }
    history.back();
  });
})();
