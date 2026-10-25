/* SK data: lets the AI (Gemini online, Gemma offline) know the student's own app data.
   - the student's saved results ("Test Records", localStorage 'mst_records')
   - the question bank of all mock tests with chapter tags (files/kb.json, built on every GitHub build)
   MSAI.run() calls SKData.context(question, 'gemini' | 'device') and adds the returned text to the prompt.
   Nothing is sent anywhere by this file; Gemini only receives the short, relevant part for the question asked. */
(function (W) {
  'use strict';
  var REC_KEY = 'mst_records';
  var kbP = null;

  function loadKB() {
    if (!kbP) {
      kbP = fetch('files/kb.json').then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; });
    }
    return kbP;
  }
  function recs() {
    try { var a = JSON.parse(localStorage.getItem(REC_KEY) || '[]'); return Array.isArray(a) ? a : []; } catch (e) { return []; }
  }
  function pad2(n) { return (n < 10 ? '0' : '') + n; }
  function TN(n) { return 'Test ' + pad2(n); }
  function sq(s) { return String(s || '').toLowerCase().replace(/[^a-z0-9]+/g, ''); }
  function cut(s, n) { s = String(s || '').replace(/\s+/g, ' ').trim(); return s.length > n ? s.slice(0, n - 1) + '…' : s; }
  function fmtTime(sec) {
    sec = Math.max(0, sec | 0);
    var h = Math.floor(sec / 3600), m = Math.floor((sec % 3600) / 60);
    return h ? h + 'h ' + m + 'm' : (m || 1) + 'm';
  }
  function fmtDate(ts) {
    try { return new Date(ts).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' }); } catch (e) { return ''; }
  }
  function acc(r) { var a = r.correct + r.wrong; return a ? Math.round(r.correct / a * 100) : 0; }

  /* verdict of one stored row [qno, subjectIdx, chosen, key, verdict] -> 'g' correct, 'r' wrong, 's' skipped */
  function verdict(q) {
    var v = q[4];
    if (v) return v === 'b' ? 'g' : v === 'p' ? 'r' : v;
    return q[2] === 0 ? 's' : (q[2] === q[3] ? 'g' : 'r');
  }

  function attemptsByTest(rs) {
    var m = {};
    rs.forEach(function (r) { if (r && r.set) (m[r.set] = m[r.set] || []).push(r); });
    Object.keys(m).forEach(function (k) { m[k].sort(function (a, b) { return a.ts - b.ts; }); });
    return m;
  }

  /* ------------------------------------------------------------------ understanding the question */
  var STOP = {};
  ('about above after again also because been before being below between both bata batao batana bhi cheez dono does doing down during each '
    + 'from further have having here hona hota hote hain hoga honge ikatha into jaisa jitne just kaun kaunse kaunsa kitne kitna kitni kisi '
    + 'kise kiya kuch liye main mein mere meri mera more most nahi other ours over same should some such than that their them then there these '
    + 'they this those through under until very want what when where which while whom will with would yeh yahan unke unka uska iske isme usme '
    + 'sabhi saare tests test paper papers mock sawal sawaal question questions prashn list show give tell please sab saari wale wali wala '
    + 'related regarding concerning topic chapter unit').split(' ').forEach(function (w) { if (w) STOP[w] = 1; });

  function parse(q, kb) {
    var t = String(q || '').toLowerCase(), P = { t: t, tests: [], qnos: [], chapters: [] };
    var m, re;
    re = /(?:test|mock|paper|success\s*kit)\s*(?:no\.?|number|#|-)?\s*0?(\d{1,2})\b/g;
    while ((m = re.exec(t))) { var n = +m[1]; if (n >= 1 && n <= 60 && P.tests.indexOf(n) < 0) P.tests.push(n); }
    re = /\b0?(\d{1,2})\s*(?:st|nd|rd|th|va|wa|wen|ve|vi)?\s*(?:test|mock|paper)\b/g;
    while ((m = re.exec(t))) { var n2 = +m[1]; if (n2 >= 1 && n2 <= 60 && P.tests.indexOf(n2) < 0) P.tests.push(n2); }
    var ordw = { pehla: 1, pehle: 1, first: 1, dusra: 2, dusre: 2, doosra: 2, second: 2, teesra: 3, teesre: 3, third: 3, chautha: 4, chauthe: 4, fourth: 4, panchva: 5, panchwa: 5, paanchva: 5, fifth: 5 };
    re = /\b(pehla|pehle|first|dusra|dusre|doosra|second|teesra|teesre|third|chautha|chauthe|fourth|panchva|panchwa|paanchva|fifth)\s+(?:test|mock|paper)/g;
    while ((m = re.exec(t))) { var n3 = ordw[m[1]]; if (n3 && P.tests.indexOf(n3) < 0) P.tests.push(n3); }
    re = /\b(?:q|que|ques|question|qn|prashn|sawal|savaal)\.?\s*(?:no\.?|number|num|#)?\s*0?(\d{1,3})\b/g;
    while ((m = re.exec(t))) { var qn = +m[1]; if (qn >= 1 && qn <= 200 && P.qnos.indexOf(qn) < 0) P.qnos.push(qn); }
    re = /\b0?(\d{1,3})\s*(?:st|nd|rd|th|va|wa|wen|ve|vi|number|no\.?)?\s*(?:question|sawal|savaal|prashn)\b/g;
    while ((m = re.exec(t))) { var qn2 = +m[1]; if (qn2 >= 1 && qn2 <= 200 && P.qnos.indexOf(qn2) < 0 && P.tests.indexOf(qn2) < 0) P.qnos.push(qn2); }

    P.allTests = /\b(all|saare|sare|sabhi|pachon|panchon|paanchon|paanch|panch|five|every|har)\b[^.?!]{0,16}\b(tests?|mock|papers?)\b|\b(tests?|mock|papers?)\b[^.?!]{0,10}\b(all|saare|sabhi|combined|total|overall)\b|\b5\s*tests?\b|\bin\s+(?:in\s+)?(?:pa(?:n)?ch|paanch)\b/.test(t);
    P.personal = /\b(mera|mere|meri|mujhe|mujhse|maine|mai|main|my|me|i|hamara|humne|apna|apne)\b/.test(t);
    P.wrong = /galat|ghalat|gala?t|wrong|incorrect|mistake|galti|negative|nahi\s*(?:aaya|aaye|bana|hua)|fail/.test(t);
    P.skip = /skip|chhod|chod|unattempt|not\s*attempt|bina\s*attempt|attempt\s*nahi|left/.test(t);
    P.right = /sahi|correct|right\b|theek|thik/.test(t);
    P.marks = /marks?\b|score|scored|result|percent|accuracy|rank|performance|kitne\s*(?:marks|number)|total|kaisa\s*(?:gaya|raha)|report/.test(t);
    P.weak = /weak|strong|kamzor|kamjor|improve|revise|revision|focus|dhyan|sudhar|best\s*chapter|worst|sabse\s*(?:zyada|jyada|kam)|analysis|analyse|analyze|suggest|plan/.test(t);
    P.subject = /physics|chemistry|botany|zoology|biology|\bbio\b|\bphy\b|\bchem\b/.test(t);
    P.listI = /sawal|savaal|question|prashn|kaun|kon\b|konse|kaunse|which|kitne|how\s*many|list|bata|dikha|show|find|mil|aaye|aaya|aaye\s*hain|hain\b/.test(t);
    P.testWord = /\b(tests?|mock|papers?|series)\b/.test(t);

    // chapters named in the question
    if (kb && kb.chapters) {
      var qs = sq(t), best = [];
      kb.chapters.forEach(function (c, ci) {
        var len = 0;
        c.alias.forEach(function (a) { var s = sq(a); if (s.length >= 5 && qs.indexOf(s) >= 0 && s.length > len) len = s.length; });
        if (len) best.push({ ci: ci, len: len });
      });
      best.sort(function (a, b) { return b.len - a.len; });
      if (best.length) {
        var top = best[0].len;
        P.chapters = best.filter(function (b) { return b.len >= Math.min(top, 8) || b.len === top; }).slice(0, 3).map(function (b) { return b.ci; });
      }
    }
    // words for a free keyword search when no chapter name matched
    P.words = [];
    String(t).split(/[^a-z0-9]+/).forEach(function (w) { if (w.length >= 4 && !STOP[w] && !/^\d+$/.test(w) && P.words.indexOf(w) < 0) P.words.push(w); });

    var personalData = P.wrong || P.skip || P.marks || P.weak;
    P.gate = !!(P.tests.length || P.allTests || (personalData && (P.personal || P.testWord || P.qnos.length)) ||
      (P.chapters.length && (P.listI || P.testWord || P.personal)) || (P.weak && (P.personal || P.testWord || /chapter|topic|unit/.test(t))));
    return P;
  }

  /* ------------------------------------------------------------------ data helpers */
  function qrow(kb, n, qno) { var rows = kb && kb.tests && kb.tests[String(n)]; return rows ? rows[qno - 1] : null; }
  function chapterNames(kb, row, max) {
    if (!kb || !row || !row[3] || !row[3].length) return '';
    return row[3].slice(0, max || 1).map(function (c) { return kb.chapters[c].name; }).join(' / ');
  }
  function statusOf(att, qno) {
    if (!att) return null;
    var row = null;
    for (var i = 0; i < att.qs.length; i++) if (att.qs[i][0] === qno) { row = att.qs[i]; break; }
    if (!row) return null;
    var v = verdict(row);
    return { v: v, chosen: row[2], key: row[3] };
  }
  function statusText(st) {
    if (!st) return 'not attempted (test not taken yet)';
    if (st.v === 'g') return 'you got it RIGHT';
    if (st.v === 's') return 'you SKIPPED it';
    return 'you got it WRONG (chose ' + st.chosen + ', correct ' + (st.key === 5 ? 'bonus' : st.key) + ')';
  }
  function subjName(kb, sidx) { return (kb && kb.subjects && kb.subjects[sidx]) || ''; }

  /* ------------------------------------------------------------------ sections */
  function overview(kb, byTest, G) {
    var nums = kb && kb.tests ? Object.keys(kb.tests).map(Number).sort(function (a, b) { return a - b; }) : Object.keys(byTest).map(Number).sort(function (a, b) { return a - b; });
    var out = [];
    nums.forEach(function (n) {
      var a = byTest[n];
      if (!a || !a.length) { out.push(G ? TN(n) + ': NOT attempted yet.' : 'T' + n + ': not taken'); return; }
      var r = a[a.length - 1], best = a.reduce(function (x, y) { return y.score > x.score ? y : x; });
      if (!G) { out.push('T' + n + ': ' + r.score + '/' + r.max + ' right ' + r.correct + ' wrong ' + r.wrong + ' skipped ' + r.skipped); return; }
      var subs = (r.subjects || []).map(function (s, i) { return s + ' ' + r.subj[i] + '/' + r.subjMax[i]; }).join(', ');
      out.push(TN(n) + ': latest attempt (' + fmtDate(r.ts) + ') scored ' + r.score + '/' + r.max + ' | right ' + r.correct + ', wrong ' + r.wrong + ', skipped ' + r.skipped +
        ' | accuracy ' + acc(r) + '% | time used ' + fmtTime(r.timeSec) + ' | subject marks: ' + subs +
        (a.length > 1 ? ' | attempts: ' + a.length + ', best ' + best.score + '/' + best.max : ''));
    });
    return out;
  }

  function testDetail(kb, n, att, P, G) {
    var cap = G ? 45 : 8, snip = G ? 170 : 80, out = [];
    if (!att) { out.push(TN(n) + ': not attempted yet, so there are no mistakes to show.'); return out; }
    var wrong = [], skipped = [], right = [];
    att.qs.forEach(function (row) { var v = verdict(row); (v === 'r' ? wrong : v === 's' ? skipped : right).push(row); });
    out.push(TN(n) + ' details (latest attempt, ' + fmtDate(att.ts) + '): ' + att.score + '/' + att.max + ', right ' + right.length + ', wrong ' + wrong.length + ', skipped ' + skipped.length + '.');
    var showWrong = P.wrong || (!P.skip && !P.right && P.listI);
    if (showWrong || P.weak) {
      out.push('WRONG questions in ' + TN(n) + ' (' + wrong.length + '):');
      wrong.slice(0, cap).forEach(function (row) {
        var qr = qrow(kb, n, row[0]);
        out.push('- Q' + row[0] + ' [' + subjName(kb, row[1]) + (qr && chapterNames(kb, qr) ? ' / ' + chapterNames(kb, qr) : '') + '] chose ' + (row[2] || '-') + ', correct ' + (row[3] === 5 ? 'bonus' : row[3]) + (qr ? ': ' + cut(qr[4], snip) : ''));
      });
      if (wrong.length > cap) out.push('  …and ' + (wrong.length - cap) + ' more wrong questions.');
    }
    if (P.skip) {
      out.push('SKIPPED questions in ' + TN(n) + ' (' + skipped.length + '): ' + skipped.slice(0, G ? 90 : 20).map(function (r) { return 'Q' + r[0]; }).join(', ') + (skipped.length > (G ? 90 : 20) ? ' …' : ''));
    }
    if (P.right) {
      out.push('RIGHT questions in ' + TN(n) + ' (' + right.length + '): ' + right.slice(0, G ? 120 : 20).map(function (r) { return 'Q' + r[0]; }).join(', ') + (right.length > (G ? 120 : 20) ? ' …' : ''));
    }
    return out;
  }

  function questionDetail(kb, n, qno, att, G) {
    var qr = qrow(kb, n, qno);
    if (!qr) return [TN(n) + ' Q' + qno + ': not found in the question bank.'];
    var lines = [TN(n) + ' Q' + qno + ' [' + subjName(kb, qr[1]) + (chapterNames(kb, qr, 2) ? ' / ' + chapterNames(kb, qr, 2) : '') + '] correct option: ' + (qr[2] === 5 ? 'bonus' : qr[2]) +
      ' | ' + statusText(statusOf(att, qno))];
    lines.push('  Question: ' + cut(qr[4], G ? 650 : 260) + (qr[6] ? ' (this question also has a figure/diagram that is not in text)' : ''));
    lines.push('  Solution (short): ' + cut(qr[5], G ? 420 : 150));
    return lines;
  }

  function chapterList(kb, byTest, P, G, chapIdx, testsFilter) {
    var out = [], cap = G ? 85 : 8, snip = G ? 190 : 85, found = [], counts = { g: 0, r: 0, s: 0, n: 0 };
    var nums = Object.keys(kb.tests).map(Number).sort(function (a, b) { return a - b; });
    nums.forEach(function (n) {
      if (testsFilter.length && testsFilter.indexOf(n) < 0) return;
      var a = byTest[n], att = a && a.length ? a[a.length - 1] : null;
      kb.tests[String(n)].forEach(function (row) {
        if (!row[3] || !row[3].some(function (c) { return chapIdx.indexOf(c) >= 0; })) return;
        var st = statusOf(att, row[0]);
        counts[st ? st.v : 'n']++;
        found.push({ n: n, row: row, st: st });
      });
    });
    var names = chapIdx.map(function (c) { return kb.chapters[c].name; }).join(' + ');
    out.push('CHAPTER "' + names + '": ' + found.length + ' questions found across ' + (testsFilter.length ? testsFilter.map(TN).join(', ') : 'all the tests') +
      '. Your result on them (latest attempts): right ' + counts.g + ', wrong ' + counts.r + ', skipped ' + counts.s + ', in tests not taken yet ' + counts.n + '.');
    var per = {};
    found.forEach(function (f) { per[f.n] = (per[f.n] || 0) + 1; });
    out.push('Count per test: ' + Object.keys(per).map(function (k) { return TN(+k) + ' = ' + per[k]; }).join(', ') + '.');
    // "my wrong / skipped / right questions in this chapter": list only those
    var want = P.wrong ? 'r' : P.skip ? 's' : P.right ? 'g' : '';
    if (want) {
      var only = found.filter(function (f) { return f.st && f.st.v === want; });
      out.push('Listing only the ones you got ' + (want === 'r' ? 'WRONG' : want === 's' ? 'SKIPPED' : 'RIGHT') + ' (' + only.length + '):');
      found = only;
    }
    found.slice(0, cap).forEach(function (f) {
      out.push('- ' + TN(f.n) + ' Q' + f.row[0] + ' (' + subjName(kb, f.row[1]) + ') [' + (f.st ? (f.st.v === 'g' ? 'right' : f.st.v === 's' ? 'skipped' : 'WRONG') : 'not attempted') + ']: ' + cut(f.row[4], snip));
    });
    if (found.length > cap) out.push('  …and ' + (found.length - cap) + ' more (not listed here to keep this short; the counts above include them).');
    out.push('(chapter tags are made automatically from keywords, so a question can occasionally be tagged to a nearby chapter.)');
    return out;
  }

  function keywordList(kb, byTest, P, G, testsFilter) {
    var out = [], cap = G ? 60 : 8, snip = G ? 190 : 85, hits = [];
    if (!P.words.length) return out;
    Object.keys(kb.tests).map(Number).sort(function (a, b) { return a - b; }).forEach(function (n) {
      if (testsFilter.length && testsFilter.indexOf(n) < 0) return;
      var a = byTest[n], att = a && a.length ? a[a.length - 1] : null;
      kb.tests[String(n)].forEach(function (row) {
        var tx = (' ' + row[4] + ' ' + row[5]).toLowerCase(), sc = 0;
        P.words.forEach(function (w) { if (tx.indexOf(w) >= 0) sc++; });
        if (sc) hits.push({ n: n, row: row, sc: sc, st: statusOf(att, row[0]) });
      });
    });
    if (!hits.length) return out;
    hits.sort(function (a, b) { return b.sc - a.sc || a.n - b.n || a.row[0] - b.row[0]; });
    var need = Math.max(1, Math.min(2, hits[0].sc));
    hits = hits.filter(function (h) { return h.sc >= need; });
    out.push('QUESTIONS matching the words "' + P.words.slice(0, 6).join(', ') + '": ' + hits.length + ' found.');
    hits.slice(0, cap).forEach(function (f) {
      out.push('- ' + TN(f.n) + ' Q' + f.row[0] + ' (' + subjName(kb, f.row[1]) + ') [' + (f.st ? (f.st.v === 'g' ? 'right' : f.st.v === 's' ? 'skipped' : 'WRONG') : 'not attempted') + ']: ' + cut(f.row[4], snip));
    });
    if (hits.length > cap) out.push('  …and ' + (hits.length - cap) + ' more.');
    return out;
  }

  function weakStrong(kb, byTest, G) {
    var out = [], stats = {}, subj = {};
    Object.keys(byTest).forEach(function (k) {
      var a = byTest[k], att = a[a.length - 1];
      (att.subjects || []).forEach(function (s, i) {
        var x = subj[s] = subj[s] || { m: 0, mx: 0 }; x.m += att.subj[i]; x.mx += att.subjMax[i];
      });
      if (!kb || !kb.tests[k]) return;
      att.qs.forEach(function (row) {
        var qr = qrow(kb, +k, row[0]); if (!qr || !qr[3].length) return;
        var c = qr[3][0], s = stats[c] = stats[c] || { c: 0, w: 0, s: 0 }, v = verdict(row);
        if (v === 'g') s.c++; else if (v === 'r') s.w++; else s.s++;
      });
    });
    var sn = Object.keys(subj);
    if (sn.length) out.push('SUBJECT-WISE (all attempted tests, latest attempts): ' + sn.map(function (s) { return s + ' ' + subj[s].m + '/' + subj[s].mx + ' (' + Math.round(subj[s].m / subj[s].mx * 100) + '%)'; }).join(', ') + '.');
    var arr = Object.keys(stats).map(function (c) { var s = stats[c]; return { c: +c, s: s, n: s.c + s.w + s.s, lost: s.w * 5 + s.s * 4 }; });
    if (arr.length && kb) {
      var weak = arr.filter(function (x) { return x.s.w + x.s.s >= 1; }).sort(function (a, b) { return b.lost - a.lost; }).slice(0, G ? 12 : 4);
      var strong = arr.filter(function (x) { return x.n >= 3 && x.s.w === 0; }).sort(function (a, b) { return b.s.c - a.s.c; }).slice(0, G ? 6 : 2);
      out.push('WEAKEST CHAPTERS (marks lost = 5 per wrong + 4 per skipped): ' + weak.map(function (x) { return kb.chapters[x.c].name + ' (right ' + x.s.c + ', wrong ' + x.s.w + ', skipped ' + x.s.s + ')'; }).join('; ') + '.');
      if (strong.length) out.push('STRONG CHAPTERS (no mistakes): ' + strong.map(function (x) { return kb.chapters[x.c].name + ' (' + x.s.c + ' right)'; }).join('; ') + '.');
    }
    return out;
  }

  /* ------------------------------------------------------------------ main entry */
  function trimTo(text, max) {
    if (text.length <= max) return text;
    var cutAt = text.lastIndexOf('\n', max);
    return text.slice(0, cutAt > max * 0.6 ? cutAt : max) + '\n…(trimmed)';
  }

  async function context(q, engine) {
    var G = engine === 'gemini';
    var kb = await loadKB();
    var P = parse(q, kb);
    if (!P.gate) return '';
    var rs = recs(), byTest = attemptsByTest(rs), L = [];
    var tNums = kb && kb.tests ? Object.keys(kb.tests).map(Number) : [];
    var asked = P.tests.filter(function (n) { return tNums.length ? tNums.indexOf(n) >= 0 : true; });

    if (G) {
      L.push("=== STUDENT'S APP DATA (read from this phone just now; authoritative) ===");
      L.push('Marking: +4 right, -1 wrong, 0 skipped; 180 questions and 720 marks per test. "Test 03" means "Success Kit Test 03" in the app. Subject labels follow the paper order (Q1-45 Physics, 46-90 Chemistry, 91-135 Botany, 136-180 Zoology). ' +
        'USE THIS DATA to answer questions about the student\'s marks, mistakes and which questions belong to a chapter. Quote test and question numbers exactly as written here (e.g. "Test 03 Q153"). Where the data says right / wrong / skipped, tell the student that. ' +
        'If the data does not contain what is asked, say so plainly; never invent marks or question numbers. If a test is "not attempted", tell the student to take it first.');
    } else {
      L.push('STUDENT DATA (from the app; answer only from this):');
    }
    L.push(rs.filter(function (r) { return r.set; }).length ? 'Saved results:' : 'The student has NOT submitted any mock test yet, so there are no marks or mistakes saved.');
    overview(kb, byTest, G).forEach(function (x) { L.push(x); });

    // specific test(s) or "all tests" for mistakes / skipped / right
    var wantDetail = (P.wrong || P.skip || P.right) && !(P.chapters.length && !asked.length);
    var detailTests = asked.length ? asked : (wantDetail ? Object.keys(byTest).map(Number).sort(function (a, b) { return b - a; }) : []);
    if (!G) detailTests = detailTests.slice(0, 2);
    if (wantDetail || P.qnos.length === 0 && asked.length && (P.listI && !P.marks)) {
      detailTests.forEach(function (n) {
        var a = byTest[n];
        testDetail(kb, n, a && a.length ? a[a.length - 1] : null, P, G).forEach(function (x) { L.push(x); });
      });
    }
    // asked about particular question numbers
    if (P.qnos.length && kb) {
      var qt = asked.length ? asked : tNums.slice().sort(function (a, b) { return a - b; });
      var shown = 0, maxQ = G ? 8 : 2;
      qt.forEach(function (n) {
        P.qnos.forEach(function (qno) {
          if (shown >= maxQ) return;
          var a = byTest[n];
          questionDetail(kb, n, qno, a && a.length ? a[a.length - 1] : null, G).forEach(function (x) { L.push(x); });
          shown++;
        });
      });
    }
    // chapter / topic across the tests
    if (kb && P.chapters.length) {
      chapterList(kb, byTest, P, G, P.chapters, asked).forEach(function (x) { L.push(x); });
    } else if (kb && !P.qnos.length && !wantDetail && !P.marks && !P.weak && P.words.length && (P.testWord || P.allTests || asked.length)) {
      keywordList(kb, byTest, P, G, asked).forEach(function (x) { L.push(x); });
    }
    if (P.weak) weakStrong(kb, byTest, G).forEach(function (x) { L.push(x); });

    return trimTo(L.join('\n'), G ? 38000 : 2300);
  }

  W.SKData = { context: context, parse: parse, _loadKB: loadKB };
})(window);
