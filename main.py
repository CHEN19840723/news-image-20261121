#!/usr/bin/env python3
"""news-image-20261121 entry (Python 3.13, standard library only).

The entry image lives beside this file as entry.png; the program copies it
to /output/entry.png (or $MAKEFUN_OUTPUT_DIR when run outside the grader).
Copying the same bytes on every run makes the output deterministic.
"""
import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    src = os.path.join(HERE, "entry.png")
    if not os.path.isfile(src):
        print("error: entry.png is missing from the repository", file=sys.stderr)
        raise SystemExit(1)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    # A failed or partial copy must fail loudly, never ship a broken entry:
    # the copy must match the source byte for byte, not just in size.
    if not os.path.isfile(dst) or os.path.getsize(dst) != os.path.getsize(src):
        print("error: copy to %s is incomplete" % dst, file=sys.stderr)
        raise SystemExit(1)
    if sha256_of(dst) != sha256_of(src):
        print("error: copy to %s differs from the source" % dst, file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
