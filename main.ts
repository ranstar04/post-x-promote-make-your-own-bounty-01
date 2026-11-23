// Entry program for the make.fun post-x-promote-make-your-own-bounty-01
// bounty (Node 22, standard library only).
//
// The entry itself is the X post: one post of the entrant's own that
// quotes make.fun's make-your-own-bounty post (or links to it), carries a
// photo of its own, and names make.fun, the @makefunai tag and the play
// code in its text. This program has one job for the grader: hand the
// post's address over. It reads POST.json from the repository root,
// checks that it really names an X post, and writes the same bytes to
// the output directory, where the gate reads them. It touches no network,
// no clock and no file outside the repository, so the grader's two runs
// always produce identical bytes.

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? "/bot";
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

const SOURCE_PATH = join(BOT_DIR, "POST.json");
const TARGET_PATH = join(OUTPUT_DIR, "POST.json");

const POST_ADDRESS = /^https:\/\/(www\.|mobile\.)?(x\.com|twitter\.com)\/\w+\/status\/\d+/;
// The sealed scorer refuses a POST.json over 16384 bytes, so refuse it
// here first, with a plain error, instead of handing the gate bad input.
const MAX_POST_BYTES = 16384;

const raw = readFileSync(SOURCE_PATH, "utf8");
if (Buffer.byteLength(raw, "utf8") > MAX_POST_BYTES) {
  throw new Error(`POST.json must be at most ${MAX_POST_BYTES} bytes`);
}
const parsed: unknown = JSON.parse(raw);
if (typeof parsed !== "object" || parsed === null || Array.isArray(parsed)) {
  throw new Error("POST.json must be a JSON object with a url field");
}
const url = (parsed as { url?: unknown }).url;
if (typeof url !== "string" || !POST_ADDRESS.test(url)) {
  throw new Error("POST.json url must be an https://x.com/<handle>/status/<id> address");
}

mkdirSync(OUTPUT_DIR, { recursive: true });
writeFileSync(TARGET_PATH, raw, "utf8");
console.log(`wrote ${TARGET_PATH} (${raw.length} bytes)`);
