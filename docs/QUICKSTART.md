# Quick Start Guide

Get SecDevAI up and running in your project in just a few steps.

## Installation

```bash
# Clone the repository first
git clone git@github.com:RedHatProductSecurity/secdevai.git
cd secdevai
# Install from local directory
uv tool install --no-cache .
```

Make sure `~/.local/bin` is in your PATH if using uv.

## Initialize SecDevAI in Your Project

Navigate to the project you want to review (not the secdevai project itself):

```bash
cd your-project  # Your application/codebase to review
secdevai          # Defaults to current directory
# or specify a path
secdevai .
```

This will:
- Create `.secdevai/` directory with context files and scripts
- Deploy slash commands to platform-specific directories (see Platform Detection below)
- Create `.secdevaiignore` file

**Platform Detection:**
SecDevAI automatically detects which AI assistant platforms are present in your project:
- If `.claude/` directory exists → commands are deployed to `.claude/commands/` (`.md` format)
- If `.cursor/` directory exists → commands are deployed to `.cursor/commands/` (`.md` format)
- If `.gemini/` directory exists → commands are deployed to `.gemini/commands/` (`.toml` format)
- If **no platform directories are detected** → defaults to `.cursor/commands/` only

**Note:** Gemini CLI uses `.toml` format for commands (as per [Gemini CLI documentation](https://cloud.google.com/blog/topics/developers-practitioners/gemini-cli-custom-slash-commands)), while Cursor and Claude use `.md` format. SecDevAI automatically converts commands to the appropriate format for each platform.

To use commands in multiple platforms, create the platform directories before running `secdevai`:
```bash
mkdir -p .claude .cursor .gemini  # Create directories for all platforms
secdevai                           # Commands will be deployed to all detected platforms
```

## Use the Command

In your AI assistant (Cursor, Claude Code, or Gemini CLI), type:

```
/secdevai                      # Show help (default)
/secdevai help                 # Show all available commands
/secdevai review               # Review selected code (if selected) or full codebase scan
/secdevai review @ file        # Review specific file
/secdevai review last-commit   # Review last commit
/secdevai review last-commit --number N  # Review last N commits
/secdevai fix [severity high]  # Apply suggested fixes (with approval, optional severity filter)
/secdevai tool bandit          # Use specific tool (bandit, scorecard, all)
/secdevai git-commit           # Commit approved fixes (requires git config and approved fixes)
```

**Command Aliases** (for convenience):
```
/secdevai-review               # Alias for /secdevai review
/secdevai-fix                  # Alias for /secdevai fix
/secdevai-help                 # Alias for /secdevai help
/secdevai-tool                 # Alias for /secdevai tool
```

## Example Workflow

1. **Initialize SecDevAI**:
   ```bash
   secdevai
   ```

2. **Review a specific file**:
   - In the AI assistant, type: `/secdevai review @ src/api/auth.py`
   - Review the security findings for that file

3. **Review code**:
   - Type: `/secdevai review`
   - If code is selected: Reviews only the selected code
   - If no selection: Reviews entire codebase (full scan)

4. **Review last commit**:
   - Type: `/secdevai review last-commit`
   - Review security findings in the last commit

5. **Apply fixes** (with approval):
   - Type: `/secdevai fix` to apply all fixes
   - Or: `/secdevai fix severity high` to apply only high/critical severity fixes
   - Review suggested changes
   - Approve individual fixes

6. **Commit fixes** (optional):
   - Type: `/secdevai git-commit`
   - Only works if fixes were approved and git is configured

**Note**: Security review results are automatically saved to the `secdevai-results` directory in your project root. Each review creates timestamped subdirectories with Markdown and SARIF reports. See the [Usage Guide](usage.md) for more details on results storage.

## Optional: Install Security Tools

For enhanced analysis, install optional tools:

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

