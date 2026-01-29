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

## Safety & Support

This is a small tool I built for my own workflow and I’m sharing it in case it helps others.

- **Tested on**: Linux (TUXEDO OS)
- **Other platforms**: may work, but not regularly tested

Please review scripts before running, and try them on non-critical data first.

## License

MIT
