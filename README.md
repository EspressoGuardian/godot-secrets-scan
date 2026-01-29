# godot-secrets-scan 🔍

**PRE-staging PII & API key scanner for Godot projects.**

`godot-secrets-scan` is a lightweight Python script that prevents you from accidentally committing API keys, private keys, or PII. It is specifically pre-configured to handle common Godot text formats.

## Key Features

- **Deterministic**: Focuses on staged files to catch leaks before they hit your history.
- **Godot-Aware**: Scans `.tscn`, `.tres`, and `.gd` files for embedded credentials.
- **Safe-by-Default**: Automatically blocks commits if files are detected in `secrets/` or have sensitive extensions.

## Usage

Scan staged changes (perfect for a pre-commit hook):

```bash
python3 secrets_scan.py --mode staged
```

Perform a full repository audit:

```bash
python3 secrets_scan.py --mode tracked
```

## Principles

- **Privacy-First**: Keep credentials offline and out of history.
- **Zero Dependencies**: Pure Python standard library.

## Disclaimer

This software is provided "as is", without warranty of any kind. It is "vibe coded" and works effectively on my machine (TUXEDO OS / Linux), but may behave differently in other environments. Always verify scripts before running them in your critical workflows.

## License

MIT
