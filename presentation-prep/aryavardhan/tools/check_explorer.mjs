// Checks the study page's explorer math against values exported from code/model.py.
// Run: node check_explorer.mjs   (after python3 export_reference.py)
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { coverage, rStar, phiStar, clusterOptions } from "./explorer_math.js";

const here = dirname(fileURLToPath(import.meta.url));
const ref = JSON.parse(readFileSync(join(here, "explorer_reference.json"), "utf8"));
const fails = [];
let count = 0;
const check = (ok, msg) => { count++; if (!ok) fails.push(msg); };

for (const row of ref) {
  const P = { x: row.x, m: row.m, n: row.n, k: row.k, c: row.c };
  const ps = phiStar(P);
  check(Math.abs(ps - row.phi_star) <= 1e-3, `phiStar ${JSON.stringify(P)}: js ${ps} vs py ${row.phi_star}`);
  for (const [phi, rs] of Object.entries(row.r_star_at)) {
    const js = rStar(Number(phi), P);
    check(Math.abs(js - rs) <= 1e-3, `rStar phi=${phi} ${JSON.stringify(P)}: js ${js} vs py ${rs}`);
  }
}
// Review Focus cases from the plan
check(JSON.stringify(clusterOptions(5)) === "[1,5]", `clusterOptions(5) = ${JSON.stringify(clusterOptions(5))}`);
check(JSON.stringify(clusterOptions(4)) === "[1,2,4]", `clusterOptions(4) = ${JSON.stringify(clusterOptions(4))}`);
check(phiStar({ x: 0.3, m: 2, n: 4, k: 2, c: 4 }) === 0, "collapsed at phi=0 should give phiStar 0");
check(coverage(0.5, 0, { x: 0.9, m: 1, n: 2, k: 3, c: 2 }) === 0, "k > n should give coverage 0");
check(phiStar({ x: 0.9, m: 1, n: 2, k: 3, c: 2 }) === 0, "k > n should give phiStar 0");
// Example 1 (pairs result) as quoted in the paper
const ex = (c) => phiStar({ x: 0.9, m: 1, n: 4, k: 2, c });
check(Math.abs(ex(1) - 0.195) < 1e-3 && Math.abs(ex(2) - 0.171) < 1e-3 && Math.abs(ex(4) - 0.195) < 1e-3,
  `Example 1: ${ex(1)}, ${ex(2)}, ${ex(4)}`);

if (fails.length) {
  console.log(`FAIL ${fails.length}/${count}`);
  for (const f of fails.slice(0, 20)) console.log("  " + f);
  process.exit(1);
}
console.log(`OK ${count}`);
