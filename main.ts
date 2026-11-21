// Entry program for make.fun news-image-20261121.
//
// The front page is drawn by render.py (same repository) and shipped as
// entry.png. This program verifies that image against the competition's
// gate and copies it to the output directory, deterministically.
import { copyFileSync, readFileSync, statSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const HERE = dirname(fileURLToPath(import.meta.url));
const SRC = join(HERE, "entry.png");
const OUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const DST = join(OUT_DIR, "entry.png");

const MAX_BYTES = 1048576;
const MAX_DIM = 1024;

const buf = readFileSync(SRC);
if (buf.length < 8 || buf[0] !== 0x89 || buf[1] !== 0x50 || buf[2] !== 0x4e ||
    buf[3] !== 0x47 || buf[4] !== 0x0d || buf[5] !== 0x0a || buf[6] !== 0x1a ||
    buf[7] !== 0x0a) {
  throw new Error("entry.png is not a PNG file");
}
if (buf.length > MAX_BYTES) {
  throw new Error(`entry.png is ${buf.length} bytes, over the 1 MiB cap`);
}
const width = buf.readUInt32BE(16);
const height = buf.readUInt32BE(20);
if (width > MAX_DIM || height > MAX_DIM) {
  throw new Error(`entry.png is ${width}x${height}, over the 1024 cap`);
}

mkdirSync(OUT_DIR, { recursive: true });
copyFileSync(SRC, DST);
const out = statSync(DST);
console.log(`wrote ${DST} (${width}x${height}, ${out.size} bytes)`);
