# godot-secrets-scan

PRE-staging PII & API key scanner for Godot projects (and others).

`godot-secrets-scan` is a lightweight Python script that prevents you from accidentally committing API keys, private keys, or PII. It is specifically pre-configured to handle common Godot file extensions like `.tscn`, `.tres`, and `.gd`.

## Features

- **Godot Focused**: Scans engine-specific text formats.
- **Fast**: Only scans changed (staged) files by default.
- **Safe**: Hard-blocks anything in a `secrets/` directory or with sensitive extensions (`.pem`, `.keystore`, etc).

## Installation

1. Copy `secrets_scan.py` to your project.
2. Ensure you have Python 3 installed.

## Usage

Scan staged changes before commit (ideal for a pre-commit hook):

```bash
python3 secrets_scan.py --mode staged
```

Audit the entire repository:

```bash
python3 secrets_scan.py --mode tracked
```

## Principles

- **Privacy First**: Keep your credentials out of git history.
- **No Dependencies**: Standard library Python only.

## License

MIT
