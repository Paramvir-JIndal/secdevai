# Usage Guide

## Initialization

Initialize SecDevAI in your project:

```bash
secdevai          # Defaults to current directory
```

Or initialize in a specific directory:

```bash
secdevai /path/to/project
```

This creates:
- `.secdevai/` directory with context files and scripts
- Slash commands in `.cursor/commands/`, `.claude/commands/`, or `.gemini/commands/`
- `.secdevaiignore` file for excluding files from scans

**Note:** Gemini CLI uses `.toml` format for commands, while Cursor and Claude use `.md` format. SecDevAI automatically converts commands to the appropriate format for each platform.

## Using the Slash Command

In your AI assistant (Cursor, Claude Code, or Gemini CLI), use:

### Basic Commands

```
/secdevai                      # Show help (default)
/secdevai help                 # Show all available commands
/secdevai review               # Review selected code (if selected) or full codebase scan
/secdevai review @ file        # Review specific file
/secdevai review last-commit   # Review last commit
/secdevai review last-commit --number N  # Review last N commits
/secdevai fix [severity high]  # Apply suggested fixes (with approval, optional severity filter)
```

### Command Aliases

For convenience, you can also use these shorter aliases in Cursor or Claude UI:

```
/secdevai-review               # Alias for /secdevai review
/secdevai-fix                  # Alias for /secdevai fix
/secdevai-help                 # Alias for /secdevai help
/secdevai-tool                 # Alias for /secdevai tool
```

### Advanced Options

```
/secdevai tool bandit          # Use specific tool (bandit, scorecard, all)
/secdevai git-commit           # Commit approved fixes (requires git config and approved fixes)
/secdevai export json          # Export report (json, markdown, sarif)
```

## Workflow

1. **Initialize**: Run `secdevai` in your project
2. **Review**: Use `/secdevai review` in your AI assistant
3. **Review Findings**: AI presents prioritized security findings
4. **Remediate**: Review suggested fixes and approve if needed
5. **Commit** (optional): Use `/secdevai git-commit` to commit approved fixes (requires git configuration)
6. **Export**: Optionally export reports for documentation

## Results Storage

SecDevAI automatically saves security review results to help you track findings over time.

### Default Location

Results are stored in the `secdevai-results` directory by default (created in your project root). Each review creates a timestamped subdirectory:

```
secdevai-results/
└── secdevai-20240101_120000/
    ├── secdevai-review-20240101_120000.md
    └── secdevai-review-20240101_120000.sarif
```

### Result Files

Each review generates two files:
- **Markdown report** (`.md`): Human-readable security findings report
- **SARIF report** (`.sarif`): Standardized format for integration with security tools and CI/CD pipelines

### Customizing Results Directory

When exporting results, you can specify a custom directory. The exporter will prompt you to confirm the directory location (defaults to `secdevai-results` if not specified).

**Note**: The `secdevai-results` directory is typically added to `.gitignore` to avoid committing review results to version control.

## Configuration

### Ignoring Files

Edit `.secdevaiignore` to exclude files from security scans:

```
# Dependencies
node_modules/
venv/

# Build artifacts
dist/
build/
```

### Tool Integration

Install optional security tools for enhanced analysis:

```bash
pip install bandit          # Python security linter
# Install scorecard from https://github.com/ossf/scorecard
```

Then use with:

```
/secdevai tool bandit       # Python security analysis
/secdevai tool scorecard    # Repository security assessment
/secdevai tool all          # Run all available security tools
```

## Examples

### Show Help

```
/secdevai
# or
/secdevai help
```

### Full Codebase Scan

```
/secdevai review
```

### Review Specific File

```
/secdevai review @ src/api/auth.py
```

### Review Selected Code

When you have code selected in the editor, `/secdevai review` will automatically review only the selected code instead of the full codebase.

### Review Last Commit

```
/secdevai review last-commit
```

### Review Multiple Commits

```
/secdevai review last-commit --number 5
```

### Apply Fixes

Apply suggested fixes with approval:

```
/secdevai fix
```

Apply fixes filtered by severity:

```
/secdevai fix severity high
```

Available severity levels: `critical`, `high`, `medium`, `low`

### Review with Tool Integration

```
/secdevai tool bandit
```

### Export Report

Export security review results to various formats:

```
/secdevai export json          # Export as JSON
/secdevai export markdown      # Export as Markdown
/secdevai export sarif         # Export as SARIF
```

Results are saved to the `secdevai-results` directory by default, organized in timestamped subdirectories. You can also use the CLI to export results:

```bash
secdevai export results.json --output-dir custom-results
```

This creates both Markdown and SARIF files in the specified directory (or prompts for confirmation if not specified).

### Commit Approved Fixes

After applying and approving fixes, commit them to git:

```
/secdevai git-commit
```

**Note**: This command only works if:
- There are approved fixes that have been applied
- Git is configured (repository exists and user config is set)

## Tips

- Use `/secdevai`, `/secdevai help`, or `/secdevai-help` to see all available commands
- Use `/secdevai review` for code reviews (full codebase scans by default)
- Use `review @ file` to focus on specific files
- Select code in the editor to automatically review only the selection
- Use `review last-commit` to review recent git commits
- Use `fix severity high` to focus on critical/high severity fixes first
- Use tool integration for enhanced analysis
- Review findings before applying fixes
- Export reports for tracking security improvements

## Extending SecDevAI

### Adding Custom Security Rules

Edit `.secdevai/context/security-review.context` to add custom security patterns:

```markdown
## Custom Pattern

**Pattern to detect**: [Description]

**Python Example**:
```python
# BAD
[example]

# GOOD
[example]
```
```

### Adding New Tools

Edit `.secdevai/scripts/security-review.sh` to add support for new security tools:

```bash
run_custom_tool() {
    if ! command -v custom-tool &> /dev/null; then
        return 1
    fi
    
    # Parse tool output and add findings
    custom-tool --format json | jq -r '...' | while read ...; do
        add_finding ...
    done
}
```

### Customizing Output Format

Modify the output format in `.secdevai/context/security-review.context` under the "Output Format" section.

### Adding Language Support

1. Add language-specific patterns to `security-review.context`
2. Update tool integration script for language-specific tools
3. Add language detection logic

