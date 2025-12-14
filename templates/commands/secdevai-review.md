# SecDevAI Review Command (Alias)

## Description
Alias for `/secdevai review` - Perform security code review.

## Usage
```
/secdevai-review               # Review selected code (if selected) or full codebase scan
/secdevai-review @ file        # Review specific file
/secdevai-review last-commit    # Review last commit
/secdevai-review last-commit --number N  # Review last N commits
```

## What This Command Does
This is an alias for `/secdevai review`. See the main `/secdevai` command documentation for full details.

When invoked, this command:
- Loads `.secdevai/context/security-review.context` for security analysis guidelines
- Analyzes code for OWASP Top 10 patterns and common vulnerabilities
- Provides prioritized findings with severity classification
- Supports file, selection, and full codebase analysis

## Expected Response
See `/secdevai` command documentation. This alias executes `/secdevai review` with the same behavior.

**Important**: After presenting findings, always save results to Markdown and SARIF formats:
- Use `secdevai_cli.results_exporter.export_results()` to save results
- Prompt user to confirm result directory (default: `secdevai-results`)
- Save both markdown and SARIF files with timestamp

