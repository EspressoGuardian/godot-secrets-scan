#!/usr/bin/env python3
"""
godot-secrets-scan.py

Scans staged or tracked files for potential secrets (API keys, tokens, private keys).
Tailored for Godot projects but works for any git repository.

License: MIT
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Iterable, List, Tuple


BANNED_FILE_EXTS = {
    ".jks", ".keystore", ".p12", ".pfx", ".pem", ".key", ".der",
}

SCAN_TEXT_EXTS = {
    ".gd", ".cs", ".py", ".sh", ".yml", ".yaml", ".json", ".cfg", ".ini",
    ".xml", ".tscn", ".tres", ".gradle", ".properties", ".txt", ".env",
}

SECRET_PATTERNS: List[Tuple[str, re.Pattern]] = [
    ("PRIVATE_KEY_BLOCK", re.compile(r"-----BEGIN (?:RSA|EC|OPENSSH|DSA|PGP)? ?PRIVATE KEY-----")),
    ("AWS_ACCESS_KEY_ID", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("GOOGLE_API_KEY", re.compile(r"\bAIza[0-9A-Za-z\-_]{35}\b")),
    ("SLACK_TOKEN", re.compile(r"\bxox[baprs]-[0-9A-Za-z-]{10,48}\b")),
    ("ABSOLUTE_PATH", re.compile(r"/home/[a-z]+/")),
    ("GENERIC_SECRET_ASSIGN", re.compile(
        r"(?i)\b(api[_-]?key|secret|token|password)\b\s*[:=]\s*[\"'][^\"']{12,}[\"']"
    )),
]


def _run_git(repo: Path, args: List[str]) -> str:
    out = subprocess.check_output(["git", *args], cwd=str(repo), stderr=subprocess.STDOUT)
    return out.decode("utf-8", errors="replace")


def _find_repo_root(start: Path) -> Path:
    cur = start.resolve()
    for _ in range(15):
        if (cur / ".git").exists():
            return cur
        if cur.parent == cur:
            break
        cur = cur.parent
    raise RuntimeError("Not inside a git repository (could not find .git).")


def _iter_files(repo: Path, mode: str) -> Iterable[Path]:
    if mode == "staged":
        names = _run_git(repo, ["diff", "--cached", "--name-only", "--diff-filter=ACMR"]).splitlines()
        for n in names:
            if n.strip():
                yield repo / n.strip()
    elif mode == "tracked":
        names = _run_git(repo, ["ls-files"]).splitlines()
        for n in names:
            if n.strip():
                yield repo / n.strip()
    else:
        raise ValueError("mode must be 'staged' or 'tracked'")


def _is_probably_text(path: Path) -> bool:
    return path.suffix.lower() in SCAN_TEXT_EXTS


def _read_text_safely(path: Path, max_bytes: int = 1024 * 1024) -> str:
    try:
        data = path.read_bytes()
    except Exception:
        return ""
    if len(data) > max_bytes:
        data = data[:max_bytes]
    return data.decode("utf-8", errors="ignore")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["staged", "tracked"], default="staged")
    args = ap.parse_args()

    try:
        repo = _find_repo_root(Path.cwd())
    except Exception as e:
        print(f"[secrets_scan] ERROR: {e}", file=sys.stderr)
        return 2

    offenders: List[str] = []

    for p in _iter_files(repo, args.mode):
        rel = p.relative_to(repo)

        if not p.exists():
            continue

        if rel.parts and rel.parts[0].lower() == "secrets":
            offenders.append(f"{rel} (file inside secrets/)")
            continue

        if p.suffix.lower() in BANNED_FILE_EXTS:
            offenders.append(f"{rel} (banned file extension: {p.suffix})")
            continue

        if _is_probably_text(p):
            text = _read_text_safely(p)
            for label, pat in SECRET_PATTERNS:
                if pat.search(text):
                    offenders.append(f"{rel} (matched pattern: {label})")
                    break

    if offenders:
        print("[secrets_scan] FAILED. Potential secrets detected:", file=sys.stderr)
        for o in offenders:
            print(f"  - {o}", file=sys.stderr)
        return 1

    print("[secrets_scan] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
