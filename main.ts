// main.ts — news-image-20261118, round 2 ("The World Today").
// The entry is a pre-composed front page (entry.png, 1024x1024). This
// program copies it byte-for-byte to the output directory, so both graded
// runs produce identical bytes. Plain JavaScript in a .ts file: no
// TypeScript-only syntax, so it runs under Node's type stripping.
import { copyFileSync, mkdirSync, existsSync, statSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const src = join(here, "entry.png");

if (!existsSync(src)) {
  throw new Error("entry.png missing next to main.ts — nothing to copy");
}

mkdirSync(outDir, { recursive: true });
const dest = join(outDir, "entry.png");
copyFileSync(src, dest);

// Fail loudly instead of shipping a truncated copy: the gate rejects a
// partial PNG, and both graded runs must carry the same bytes.
if (statSync(src).size !== statSync(dest).size) {
  throw new Error("entry.png copy size mismatch — refusing to continue");
}
