# Installation Guide

## Prerequisites

- Python 3.11 or higher
- `uv` package manager

## Installation Options

### Using uv (Recommended)

**Install from local source:**
```bash
git clone git@github.com:RedHatProductSecurity/secdevai.git
cd secdevai
uv tool install --no-cache .
```

## Verify Installation

```bash
secdevai --help
```

You should see the SecDevAI CLI help message.

## Next Steps

After installation, initialize SecDevAI in your project:

```bash
cd your-project
secdevai          # Defaults to current directory
# or specify a path
secdevai /path/to/project
```

See [Usage Guide](usage.md) for details on using the security review commands.

