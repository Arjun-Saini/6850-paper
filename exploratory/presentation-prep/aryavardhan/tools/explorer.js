// Model explorer UI for the study page. Uses binomTail/coverage/F/rStar/phiStar/clusterOptions
// from explorer_math.js (inlined before this file by build_study_guide.py). Plots are plain SVG.
(function () {
  const root = document.getElementById("explorer");
  if (!root) return;
  const $ = (id) => document.getElementById(id);
  const NS = "http://www.w3.org/2000/svg";
  const SERIES = ["var(--s1)", "var(--s2)", "var(--s3)", "var(--s4)"];
  const DASH = ["", "6 4", "2 3", "10 3 2 3"];
  const NAMES = (n, c) => (c === 1 ? "co-located" : c === n ? "spread" : c === 2 && n === 4 ? "two pairs" : n / c === 2 ? `${c} pairs` : `${c} clusters of ${n / c}`);
  const PRESETS = {
    egl: { m: 2, n: 4, k: 1, c: 4, x: 0.6, phi: 0, note: "EGL's cliff: two inputs, one supplier each. Slide x down past about 0.52 and reliability jumps to zero." },
    newcliff: { m: 1, n: 4, k: 2, c: 4, x: 0.8, phi: 0, note: "Our new cliff: ONE input, but two suppliers needed. Slide x down past about 0.72." },
    smooth: { m: 1, n: 4, k: 1, c: 4, x: 0.5, phi: 0, note: "k = m = 1: a branching process. Reliability fades to zero gradually as x falls toward 1/n." },
    pairs: { m: 1, n: 4, k: 2, c: 2, x: 0.9, phi: 0.18, note: "Example 1: with k = 2, two pairs (c = 2) break at a smaller shock than both co-located and spread." },
    twoinputs: { m: 2, n: 4, k: 1, c: 1, x: 0.9, phi: 0.2, note: "Claim 2: with two inputs, co-located suppliers break much earlier than spread ones." },
  };
  const S = { m: 1, n: 4, k: 2, c: 2, x: 0.9, phi: 0.18 };
  window.__explorer = { phiStars: {} };

  function el(tag, attrs, parent) {
    const e = document.createElementNS(NS, tag);
    for (const [k, v] of Object.entries(attrs || {})) e.setAttribute(k, v);
    if (parent) parent.appendChild(e);
    return e;
  }

  // ---- generic line plot -------------------------------------------------------------
  function plot(svg, o) {
    while (svg.firstChild) svg.removeChild(svg.firstChild);
    const W = Math.max(260, Math.round((svg.parentElement.clientWidth || 380) - 20));
    const H = Math.round(W * (o.aspect || 0.68)), L = 44, R = 12, T = 14, B = 38;
    svg.setAttribute("viewBox", `0 0 ${W} ${H}`);
    const sx = (v) => L + ((v - o.x0) / (o.x1 - o.x0)) * (W - L - R);
    const sy = (v) => T + (1 - (v - o.y0) / (o.y1 - o.y0)) * (H - T - B);
    const g = el("g", {}, svg);
    for (const t of o.xticks) {
      el("line", { x1: sx(t), x2: sx(t), y1: T, y2: H - B, class: "grid" }, g);
      const tx = el("text", { x: sx(t), y: H - B + 14, class: "tick", "text-anchor": "middle" }, g);
      tx.textContent = o.xfmt ? o.xfmt(t) : String(t);
    }
    for (const t of o.yticks) {
      el("line", { x1: L, x2: W - R, y1: sy(t), y2: sy(t), class: "grid" }, g);
      const ty = el("text", { x: L - 6, y: sy(t) + 3, class: "tick", "text-anchor": "end" }, g);
      ty.textContent = String(t);
    }
    el("line", { x1: L, x2: W - R, y1: H - B, y2: H - B, class: "axis" }, g);
    el("line", { x1: L, x2: L, y1: T, y2: H - B, class: "axis" }, g);
    const xl = el("text", { x: (L + W - R) / 2, y: H - 6, class: "axlabel", "text-anchor": "middle" }, g);
    xl.textContent = o.xlabel;
    const yl = el("text", { x: 12, y: (T + H - B) / 2, class: "axlabel", "text-anchor": "middle", transform: `rotate(-90 12 ${(T + H - B) / 2})` }, g);
    yl.textContent = o.ylabel;
    for (const v of o.vlines || []) {
      el("line", { x1: sx(v.x), x2: sx(v.x), y1: T, y2: H - B, class: "vline", stroke: v.color || "var(--muted)" }, g);
    }
    for (const s of o.series) {
      const d = s.pts.map((p, i) => `${i ? "L" : "M"}${sx(p[0]).toFixed(1)},${sy(Math.max(o.y0, Math.min(o.y1, p[1]))).toFixed(1)}`).join("");
      el("path", { d, fill: "none", stroke: s.color, "stroke-width": s.width || 2, "stroke-dasharray": s.dash || "", "stroke-linejoin": "round" }, g);
    }
    for (const mk of o.markers || []) {
      el("circle", { cx: sx(mk.x), cy: sy(mk.y), r: 5, fill: mk.color, stroke: "var(--surface)", "stroke-width": 2 }, g);
    }
    return { sx, sy, W, H, L, R, T, B, g };
  }

  // ---- controls -----------------------------------------------------------------------
  function syncControls() {
    $("ex-k").max = String(Math.min(4, S.n));
    if (S.k > S.n) S.k = S.n;
    const opts = clusterOptions(S.n);
    if (!opts.includes(S.c)) S.c = S.n;
    $("ex-c").innerHTML = opts.map((c) => `<option value="${c}"${c === S.c ? " selected" : ""}>${c} (${NAMES(S.n, c)})</option>`).join("");
    for (const key of ["m", "k", "x", "phi"]) $(`ex-${key}`).value = String(S[key]);
    $("ex-n").value = String(S.n);
    $("ex-k-out").textContent = S.k;
    $("ex-m-out").textContent = S.m;
    $("ex-x-out").textContent = S.x.toFixed(3);
    $("ex-phi-out").textContent = S.phi.toFixed(3);
  }

  let pending = false;
  function schedule() {
    if (pending) return;
    pending = true;
    $("ex-status").textContent = "Computing…";
    requestAnimationFrame(() => setTimeout(() => { pending = false; render(); }, 0));
  }

  function bind(id, key, parse) {
    $(id).addEventListener("input", (e) => { S[key] = parse(e.target.value); syncControls(); schedule(); });
  }
  bind("ex-m", "m", Number); bind("ex-k", "k", Number); bind("ex-x", "x", Number); bind("ex-phi", "phi", Number);
  $("ex-n").addEventListener("change", (e) => { S.n = Number(e.target.value); syncControls(); schedule(); });
  $("ex-c").addEventListener("change", (e) => { S.c = Number(e.target.value); syncControls(); schedule(); });
  root.querySelectorAll("[data-preset]").forEach((b) => b.addEventListener("click", () => {
    const p = PRESETS[b.dataset.preset];
    Object.assign(S, { m: p.m, n: p.n, k: p.k, c: p.c, x: p.x, phi: p.phi });
    $("ex-note").textContent = p.note;
    root.querySelectorAll("[data-preset]").forEach((o) => o.setAttribute("aria-pressed", o === b ? "true" : "false"));
    syncControls(); schedule();
  }));

  // ---- render -------------------------------------------------------------------------
  let geoCache = null;
  function render() {
    const P = { x: S.x, m: S.m, n: S.n, k: S.k, c: S.c };
    const GRID = 600;
    // Panel A: cliff, r* against x at the current phi and c
    const xs = []; for (let i = 0; i <= 170; i++) xs.push(0.15 + (0.85 * i) / 170);
    const cliff = xs.map((x) => [x, rStar(S.phi, { ...P, x }, GRID)]);
    window.__explorer.cliffMin = Math.min(...cliff.map((p) => p[1]));
    const rNow = rStar(S.phi, P);
    plot($("ex-plot-cliff"), {
      x0: 0.15, x1: 1, y0: 0, y1: 1, xticks: [0.2, 0.4, 0.6, 0.8, 1], yticks: [0, 0.5, 1],
      xlabel: "relationship strength x", ylabel: "reliability r*",
      series: [{ pts: cliff, color: "var(--s1)" }], vlines: [{ x: S.x, color: "var(--accent)" }],
      markers: [{ x: S.x, y: rNow, color: "var(--accent)" }],
    });
    // Panel B: fixed point picture F(r) vs r
    const rs = []; for (let i = 0; i <= 120; i++) rs.push(i / 120);
    plot($("ex-plot-fp"), {
      x0: 0, x1: 1, y0: 0, y1: 1, xticks: [0, 0.5, 1], yticks: [0, 0.5, 1],
      xlabel: "r (suppliers work)", ylabel: "F(r) (firm works)",
      series: [
        { pts: [[0, 0], [1, 1]], color: "var(--muted)", dash: "3 3", width: 1.5 },
        { pts: rs.map((r) => [r, F(r, S.phi, P)]), color: "var(--s2)" },
      ],
      markers: rNow > 0 ? [{ x: rNow, y: rNow, color: "var(--accent)" }] : [],
    });
    // Panel C: geography, r* against phi for every cluster count
    const opts = clusterOptions(S.n);
    const ps = {};
    for (const c of opts) ps[c] = phiStar({ ...P, c });
    window.__explorer.phiStars = ps;
    const maxPs = Math.max(...Object.values(ps));
    const phiMax = Math.min(1, Math.max(0.05, Math.ceil((maxPs * 1.35 + 0.01) * 20) / 20));
    const phis = []; for (let i = 0; i <= 120; i++) phis.push((phiMax * i) / 120);
    const curves = opts.map((c, i) => ({ c, color: SERIES[i % 4], dash: DASH[i % 4], pts: phis.map((f) => [f, rStar(f, { ...P, c }, GRID)]) }));
    geoCache = { phis, curves, phiMax };
    const step = phiMax <= 0.1 ? 0.02 : phiMax <= 0.3 ? 0.05 : phiMax <= 0.6 ? 0.1 : 0.2;
    const xt = []; for (let t = 0; t <= phiMax + 1e-9; t += step) xt.push(Math.round(t * 100) / 100);
    $("ex-legend").innerHTML = curves.map((cv) => `<span><span class="swatch" style="background:${cv.color}"></span>${NAMES(S.n, cv.c)} (c = ${cv.c})</span>`).join("");
    const geo = plot($("ex-plot-geo"), {
      aspect: 0.5, x0: 0, x1: phiMax, y0: 0, y1: 1, xticks: xt, yticks: [0, 0.5, 1],
      xlabel: "shock size φ (chance a region is hit)", ylabel: "reliability r*",
      series: curves.map((cv) => ({ pts: cv.pts, color: cv.color, dash: cv.dash })),
      vlines: [{ x: Math.min(S.phi, phiMax), color: "var(--accent)" }],
    });
    attachHover($("ex-plot-geo"), geo);
    // Readout
    const worst = Math.min(...Object.values(ps));
    const abrupt = S.k * S.m >= 2;
    $("ex-readout").innerHTML =
      `<p class="verdict ${abrupt ? "abrupt" : "smooth"}"><strong>${abrupt ? "Abrupt collapse" : "Gradual collapse"}</strong> (k·m = ${S.k * S.m}${abrupt ? " ≥ 2: a cliff, by Claim 1" : ": a branching process"})</p>` +
      `<p>At the current settings: r* = <strong>${rNow.toFixed(3)}</strong> with c = ${S.c} (${NAMES(S.n, S.c)}).</p>` +
      `<table><thead><tr><th>Geography</th><th>c</th><th>Tolerable shock φ*</th></tr></thead><tbody>` +
      opts.map((c, i) => `<tr${ps[c] === worst && opts.length > 1 && Math.max(...Object.values(ps)) - worst > 1e-3 ? ' class="worst"' : ""}>` +
        `<td><span class="swatch" style="background:${SERIES[i % 4]}"></span>${NAMES(S.n, c)}</td><td>${c}</td><td>${ps[c].toFixed(3)}</td></tr>`).join("") +
      `</tbody></table>` +
      (opts.length > 2 ? `<p class="hint">${interiorWorst(opts, ps) ? "An <strong>intermediate</strong> split is the most fragile here: partial diversification backfires." : "Here the ordering is monotone: finer splits never break earlier."}</p>` : "");
    $("ex-status").textContent = "";
  }

  function interiorWorst(opts, ps) {
    const ends = Math.min(ps[opts[0]], ps[opts[opts.length - 1]]);
    return opts.slice(1, -1).some((c) => ps[c] < ends - 1e-3);
  }

  function attachHover(svg, geo) {
    const tip = $("ex-tip");
    svg.onpointermove = (ev) => {
      if (!geoCache) return;
      const box = svg.getBoundingClientRect();
      const vx = ((ev.clientX - box.left) / box.width) * geo.W;
      const f = ((vx - geo.L) / (geo.W - geo.L - geo.R)) * geoCache.phiMax;
      if (f < 0 || f > geoCache.phiMax) { tip.hidden = true; return; }
      const i = Math.round((f / geoCache.phiMax) * (geoCache.phis.length - 1));
      tip.innerHTML = `<strong>φ = ${geoCache.phis[i].toFixed(3)}</strong><br>` + geoCache.curves.map((cv) =>
        `<span class="swatch" style="background:${cv.color}"></span>${NAMES(S.n, cv.c)}: ${cv.pts[i][1].toFixed(3)}`).join("<br>");
      tip.hidden = false;
      const wrap = svg.parentElement.getBoundingClientRect();
      tip.style.left = `${Math.min(ev.clientX - wrap.left + 12, wrap.width - 170)}px`;
      tip.style.top = `${ev.clientY - wrap.top + 12}px`;
    };
    svg.onpointerleave = () => { tip.hidden = true; };
  }

  let rz = null;
  window.addEventListener("resize", () => { clearTimeout(rz); rz = setTimeout(schedule, 200); });
  // render once the panel is visible, so the plots can measure their width
  const panel = document.getElementById("panel-explorer");
  syncControls();
  if (panel && panel.hidden) {
    new MutationObserver((_, obs) => { if (!panel.hidden) { obs.disconnect(); render(); } }).observe(panel, { attributes: true, attributeFilter: ["hidden"] });
    render();
  } else render();
})();
