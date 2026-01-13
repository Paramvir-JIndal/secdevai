# SecDevAI - Secure Development Assistant Tool

Stop shipping security vulnerabilities. Start shipping secure code. Get instant security reviews and fixes right in your preferred AI coding assistant.

SecDevAI provides context-aware security analysis for Cursor, Claude Code, and Gemini CLI using simple slash commands.

[!WARNING]
 **SecDevAI is currently in active development** with various LLM models. Features, interfaces and behavior may change without notice. Use at your own risk and please report any issues you encounter. Contribution is welcome!

## Quick Start in 1 Minute

Three commands. Zero configuration. Start reviewing code for security issues immediately.

```bash
uv tool install git+https://github.com/RedHatProductSecurity/secdevai.git
cd your-code-project
secdevai .
```

Run your preferred AI tool (e.g., Claude Code, Cursor, Gemini-CLI) and type `/secdevai`.

![SecDevAI image](secdevai.png)

That's it! Try using the available commands.


## Overview

SecDevAI is an AI-powered secure development assistant that helps developers and security researchers build secure code. It provides security analysis with optional integration to existing security tools, supporting both targeted file/selection reviews and full codebase scans. The tool includes configurable rules covering OWASP Top 10 and common code patterns, making it valuable for both development teams and security researchers analyzing codebases and identifying vulnerabilities.


## Why SecDevAI?

While Cursor, Claude Code, and Gemini CLI offer built-in AI code review capabilities, SecDevAI adds **transparency and control** over the security review contexts. This enables you to:

- **Transparency**: See exactly what security patterns and rules are being applied to your code
- **Control**: Customize and extend security contexts to match your organization's specific needs
- **Continuous Improvement**: Update and refine security review templates based on your team's experience and evolving threats

This approach allows you to continuously improve the quality of security review results, rather than relying on opaque, fixed AI models that you cannot modify or enhance.

## Features

- **Slash Commands**: `/secdevai` works across Cursor, Claude Code, and Gemini CLI
- **Multi-Platform**: Commands work identically across different AI assistant platforms
- **Tool Integration**: Optional integration with Bandit and Scorecard (expandable)
- **Python-First**: Initial focus on Python security patterns, expandable to other languages
- **OWASP Top 10**: Comprehensive coverage of OWASP Top 10 security risks
- **Remediation**: Provides code fixes with preview and approval workflow
- **Security Research**: Helpful for security researchers analyzing codebases and identifying vulnerabilities


## Project Structure

```
secdevai/
├── templates/                 # Template system
│   ├── commands/             # Slash command templates
│   ├── context/              # Security analysis contexts
│   └── scripts/              # Helper scripts
├── src/secdevai_cli/         # CLI implementation
└── docs/                     # Documentation
```

## Next Steps
- Follow the [Quick Start Guide](docs/QUICKSTART.md) to get started
- Read [Usage Guide](docs/usage.md) for detailed usage and advanced features
- Check [Installation Guide](docs/installation.md) for more installation options
- Read [Contributing Guide](CONTRIBUTING.md) to customize rules and contribute

## Troubleshooting

### Command not found
- Make sure SecDevAI is installed: `secdevai --help`
- If using uv, ensure `~/.local/bin` is in your PATH

### Templates not found
- Ensure you're running `secdevai` from the project root
- Check that `.secdevai/` directory was created

### Platform not detected
- SecDevAI defaults to Cursor if no platform directories (`.cursor/`, `.claude/`, `.gemini/`) are detected
- If you want commands for Claude or Gemini, create the platform directory first:
  ```bash
  mkdir -p .claude  # Creates .claude/ directory
  secdevai          # Will now detect and deploy to .claude/commands/
  ```
- **Note:** Gemini CLI uses `.toml` format, so commands in `.gemini/commands/` will have `.toml` extension, while Cursor and Claude use `.md` format
- Alternatively, manually create the commands directories after initialization:
  ```bash
  mkdir -p .claude/commands .gemini/commands
  cp .cursor/commands/* .claude/commands/  # Works for Claude (same .md format)
  # For Gemini, you'll need to convert .md to .toml format manually
  ```
  
## License

This project is licensed under the MIT [License](LICENSE)

## Contributing

[CONTRIBUTING.md](CONTRIBUTING.md)

