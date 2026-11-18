// news-image-20261118: entrypoint.
//
// Copies the composed front page (entry.png) to the output directory.
// The image is built at authoring time by compose.py (Pillow) from a fresh
// hero illustration generated in-session and verified 18-November-2026
// stories; this program needs no network and is deterministic: every run
// writes the same bytes.
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const src = new URL("./entry.png", import.meta.url);
const bytes = readFileSync(src);

// Guardrails from the competition gate: the file must be a whole PNG of at
// most 1 MiB and at most 1024 by 1024 pixels. Fail loudly instead of
// writing an entry the gate would refuse.
const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (!bytes.subarray(0, 8).equals(PNG_MAGIC)) {
  throw new Error("entry.png is not a PNG file");
}
if (bytes.length > 1048576) {
  throw new Error(`entry.png is ${bytes.length} bytes, over the 1 MiB cap`);
}
const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
if (width > 1024 || height > 1024) {
  throw new Error(`entry.png is ${width}x${height}, over the 1024x1024 cap`);
}

mkdirSync(outDir, { recursive: true });
writeFileSync(join(outDir, "entry.png"), bytes);
console.log(
  `wrote ${join(outDir, "entry.png")} (${bytes.length} bytes, ${width}x${height})`,
);
