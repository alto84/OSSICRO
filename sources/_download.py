#!/usr/bin/env python3
"""Download the openly-available source originals discovered by the scrape waves.
Resilient: per-file timeout, skip-if-present, continue on error, TSV log.
Binaries land in sources/<category>/ (gitignored; indexed by MANIFEST.md)."""
import json, os, re, subprocess, sys

BASE = os.path.dirname(os.path.abspath(__file__))
items = json.load(open(os.path.join(BASE, "_to-download.json"), encoding="utf-8"))
log_path = os.path.join(BASE, "download-log.tsv")

def safe_name(m):
    fn = (m.get("suggested_filename") or "").strip()
    if not fn:
        tail = re.sub(r"[?#].*$", "", m.get("url", "").rstrip("/").split("/")[-1]) or "file"
        fn = tail
    fn = re.sub(r"[^A-Za-z0-9._-]+", "-", fn).strip("-")[:150]
    if not os.path.splitext(fn)[1]:
        fn += ".pdf"
    return fn

ok = err = skip = 0
with open(log_path, "w", encoding="utf-8", newline="\n") as log:
    log.write("status\tcategory\tpath\turl\n")
    for m in items:
        cat = re.sub(r"[^a-z0-9-]+", "-", (m.get("category") or "other").lower()) or "other"
        d = os.path.join(BASE, cat)
        os.makedirs(d, exist_ok=True)
        path = os.path.join(d, safe_name(m))
        url = m.get("url", "")
        if not url:
            continue
        if os.path.exists(path) and os.path.getsize(path) > 512:
            skip += 1; log.write(f"skip\t{cat}\t{path}\t{url}\n"); continue
        try:
            r = subprocess.run(
                ["curl", "-sSL", "--max-time", "45", "--retry", "1", "-A",
                 "Mozilla/5.0 (compatible; OSSICRO-archiver/1.0)", "-o", path, url],
                capture_output=True, timeout=70)
            sz = os.path.getsize(path) if os.path.exists(path) else 0
            head = b""
            if sz:
                with open(path, "rb") as fh: head = fh.read(200)
            is_html = head[:15].lower().lstrip().startswith((b"<!doctype", b"<html"))
            if r.returncode == 0 and sz > 512 and not is_html:
                ok += 1; log.write(f"ok\t{cat}\t{path}\t{url}\n")
            else:
                err += 1
                if os.path.exists(path) and (sz <= 512 or is_html):
                    os.remove(path)
                log.write(f"err\t{cat}\t{path}\t{url}\n")
        except Exception as e:
            err += 1
            if os.path.exists(path):
                try: os.remove(path)
                except OSError: pass
            log.write(f"err\t{cat}\t{path}\t{url}\n")
        if (ok + err + skip) % 50 == 0:
            print(f"progress: {ok} ok / {err} err / {skip} skip of {len(items)}", flush=True)

print(f"DONE: {ok} downloaded, {err} failed, {skip} skipped, of {len(items)} total")
print(f"log: {log_path}")
