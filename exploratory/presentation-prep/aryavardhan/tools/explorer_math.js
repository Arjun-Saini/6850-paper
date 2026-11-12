// Model math for the study page's explorer: the paper's eq. (2) with c equal supplier clusters.
// Mirrors code/model.py (F, largest_fixed_point, phi_star). Pure functions, no DOM.
// P = {x, m, n, k, c}: strength, inputs, suppliers per input, suppliers needed, clusters (c divides n).

export function binomTail(k, N, p) {            // P[Bin(N, p) >= k]
  if (k <= 0) return 1;
  if (N < k) return 0;
  let term = Math.pow(1 - p, N), cdf = 0;        // accumulate P[Bin = j] for j < k
  for (let j = 0; j < k; j++) {
    if (j > 0) term *= ((N - j + 1) / j) * (p / (1 - p));
    cdf += term;
  }
  if (p >= 1) return 1;
  return Math.min(1, Math.max(0, 1 - cdf));
}

function choose(n, j) { let r = 1; for (let i = 1; i <= j; i++) r = (r * (n - j + i)) / i; return r; }

export function coverage(r, phi, P) {           // P[an input has >= k usable suppliers]
  const b = P.n / P.c, s = 1 - phi;
  let tot = 0;
  for (let j = 0; j <= P.c; j++) {               // j clusters' regions survive
    const w = choose(P.c, j) * Math.pow(s, j) * Math.pow(phi, P.c - j);
    if (w > 0) tot += w * binomTail(P.k, j * b, P.x * r);
  }
  return tot;
}

export function F(r, phi, P) { return Math.pow(coverage(r, phi, P), P.m); }

const GRID_N = 4000;
export function rStar(phi, P, gridN = GRID_N) {  // largest root of F(r) = r on (0, 1], else 0
  const g = (r) => F(r, phi, P) - r;
  if (g(1) >= 0) return 1;
  let last = -1;
  for (let i = gridN; i >= 1; i--) {             // scan down from r = 1 for the first r with g >= 0
    if (g(i / gridN) >= 0) { last = i; break; }
  }
  if (last < 0) return 0;
  let lo = last / gridN, hi = (last + 1) / gridN;
  for (let t = 0; t < 50; t++) { const mid = (lo + hi) / 2; if (g(mid) >= 0) lo = mid; else hi = mid; }
  const r = (lo + hi) / 2;
  return r > 1e-4 ? r : 0;
}

export function phiStar(P) {                    // largest regional shock with r* > 0
  if (rStar(0, P) === 0) return 0;
  let lo = 0, hi = 1;
  for (let t = 0; t < 30; t++) { const mid = (lo + hi) / 2; if (rStar(mid, P) > 0) lo = mid; else hi = mid; }
  return lo;
}

export function clusterOptions(n) {             // valid cluster counts: divisors of n
  const out = [];
  for (let d = 1; d <= n; d++) if (n % d === 0) out.push(d);
  return out;
}
