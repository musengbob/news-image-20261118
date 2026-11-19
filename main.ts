// news-image-20261118 round 3: copy the composed front page to the output dir.
// The image is built by compose.py (PIL) and committed as entry.png; this
// program only copies those bytes, so repeated runs are byte-identical.
import { copyFileSync, existsSync, mkdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
mkdirSync(outDir, { recursive: true });
const src = join(here, "entry.png");
if (!existsSync(src)) {
  throw new Error("entry.png missing next to main.ts");
}
copyFileSync(src, join(outDir, "entry.png"));
const bytes = statSync(join(outDir, "entry.png")).size;
console.log(`entry.png copied to ${outDir} (${bytes} bytes)`);
