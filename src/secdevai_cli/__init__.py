#!/usr/bin/env python3
"""
SecDevAI CLI - Setup tool for SecDevAI

Usage:
    uv tool install .
    secdevai <project-path>
"""

import os
import sys
import stat
from pathlib import Path
from typing import Optional, Dict

import typer
from rich.console import Console
from rich.panel import Panel

# Initialize console
console = Console()

# Constants
TAGLINE = "AI-powered security code review tool with slash command integration"

app = typer.Typer(help=TAGLINE)


def main():
    """Entry point for CLI."""
    app()


# Make app callable for entry point
if __name__ == "__main__":
    main()


@app.callback(invoke_without_command=True)
def default(
    ctx: typer.Context,
    project_path: Optional[str] = typer.Argument(".", help="Path to project directory (defaults to current directory)"),
):
    """Initialize SecDevAI in a project directory."""
    if ctx.invoked_subcommand is None:
        init(project_path)


@app.command()
def export(
    input_file: str = typer.Argument(..., help="Input JSON file with security review results"),
    output_dir: Optional[str] = typer.Option(None, "--output-dir", "-o", help="Output directory (default: prompt)"),
    command_type: str = typer.Option("review", "--type", "-t", help="Command type (review, fix, tool)"),
):
    """Export security review results to Markdown and SARIF formats."""
    import json
    from secdevai_cli.results_exporter import export_results
    
    input_path = Path(input_file)
    
    if not input_path.exists():
        console.print(f"[red]Error:[/red] Input file not found: {input_file}")
        raise typer.Exit(1)
    
    # Load JSON data
    try:
        data = json.loads(input_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        console.print(f"[red]Error:[/red] Invalid JSON in input file: {e}")
        raise typer.Exit(1)
    
    # Determine output directory
    result_dir = None
    if output_dir:
        result_dir = Path(output_dir).expanduser().resolve()
        result_dir.mkdir(parents=True, exist_ok=True)
    
    # Export results
    markdown_path, sarif_path = export_results(data, result_dir, command_type)
    
    console.print(f"\n[bold green]✓ Export complete![/bold green]")
    console.print(f"  Markdown: {markdown_path}")
    console.print(f"  SARIF: {sarif_path}\n")


@app.command()
def init(
    project_path: Optional[str] = typer.Argument(".", help="Path to project directory (defaults to current directory)"),
):
    """Initialize SecDevAI in a project directory."""
    if project_path:
        target_dir = Path(project_path).expanduser().resolve()
    else:
        # Default to current directory if nothing specified
        target_dir = Path.cwd()

    if not target_dir.exists():
        console.print(f"[red]Error:[/red] Directory does not exist: {target_dir}")
        raise typer.Exit(1)

    console.print(f"\n[bold blue]Initializing SecDevAI in:[/bold blue] {target_dir}\n")

    # Get templates directory
    # Strategy: Check multiple possible locations
    templates_dir = None
    
    # 1. Check if running from source (development mode)
    # __file__ is src/secdevai_cli/__init__.py, so go up to project root
    source_templates = Path(__file__).parent.parent.parent / "templates"
    if source_templates.exists():
        templates_dir = source_templates
    
    # 2. Check uv tools installation directory
    # uv tool install puts packages in ~/.local/share/uv/tools/
    # Templates are installed via shared-data at share/secdevai-cli/templates
    if not templates_dir or not templates_dir.exists():
        uv_tools_dir = Path.home() / ".local" / "share" / "uv" / "tools" / "secdevai-cli"
        # Check shared-data location first
        uv_templates = uv_tools_dir / "share" / "secdevai-cli" / "templates"
        if not uv_templates.exists():
            # Fallback to direct templates location
            uv_templates = uv_tools_dir / "templates"
        if uv_templates.exists():
            templates_dir = uv_templates
    
    # 3. Check installed package shared data location
    # When installed via wheel, templates are in share/secdevai-cli/templates
    if not templates_dir or not templates_dir.exists():
        import site
        for site_dir in site.getsitepackages():
            shared_templates = Path(site_dir).parent / "share" / "secdevai-cli" / "templates"
            if shared_templates.exists():
                templates_dir = shared_templates
                break
    
    # 4. Check relative to installed package location
    if not templates_dir or not templates_dir.exists():
        installed_templates = Path(__file__).parent.parent.parent / "templates"
        if installed_templates.exists():
            templates_dir = installed_templates

    if not templates_dir or not templates_dir.exists():
        console.print(f"[red]Error:[/red] Templates directory not found.")
        console.print(f"[dim]Checked:[/dim] {source_templates}")
        console.print("[yellow]Hint:[/yellow] Make sure templates are included when installing the package.")
        raise typer.Exit(1)

    # Deploy templates
    deployer = TemplateDeployer(templates_dir)
    deployer.deploy(target_dir)

    console.print("\n[bold green]✓ SecDevAI initialized successfully![/bold green]\n")
    console.print("You can now use [bold]/secdevai[/bold] in your AI assistant.")


class TemplateDeployer:
    """Service for deploying templates to project directory."""

    def __init__(self, templates_dir: Path):
        """Initialize template deployer."""
        self.templates_dir = templates_dir

    def get_file_mapping(self) -> Dict[str, str]:
        """Get mapping of template files to target paths."""
        return {
            # Context files
            "context/security-review.context": ".secdevai/context/security-review.context",
            "context/security-rules.md": ".secdevai/context/security-rules.md",
            "context/wstg-testing.context": ".secdevai/context/wstg-testing.context",
            # Scripts
            "scripts/security-review.sh": ".secdevai/scripts/security-review.sh",
            # Commands (will be deployed to platform-specific dirs)
            "commands/secdevai.md": "secdevai.md",  # Temporary, will be copied to each platform
        }

    def detect_platforms(self, target_dir: Path) -> list[str]:
        """Detect which AI assistant platforms are present."""
        platforms = []
        platform_dirs = {
            "cursor": ".cursor/commands",
            "claude": ".claude/commands",
            "gemini": ".gemini/commands",
        }

        for platform, cmd_dir in platform_dirs.items():
            if (target_dir / cmd_dir).exists() or (target_dir / f".{platform}").exists():
                platforms.append(platform)

        # If no platforms detected, default to cursor and claude
        if not platforms:
            platforms = ["cursor", "claude"]

        return platforms

    def _convert_md_to_toml(self, md_content: str) -> str:
        """Convert markdown command template to Gemini CLI .toml format.
        
        According to Gemini CLI documentation:
        - https://cloud.google.com/blog/topics/developers-practitioners/gemini-cli-custom-slash-commands
        - Uses .toml format with 'description' and 'prompt' fields
        - Supports {{args}} for arguments and !{...} for shell commands
        """
        import re
        
        # Extract description from markdown (usually in "## Description" section)
        description_match = re.search(r'##\s+Description\s*\n+(.+?)(?=\n##|\n```|$)', md_content, re.DOTALL)
        if description_match:
            description = description_match.group(1).strip()
            # Clean up description - remove markdown formatting, take first line or first sentence
            description = re.sub(r'^\*\*.*?\*\*:\s*', '', description)  # Remove bold prefixes
            description = re.sub(r'\n.*', '', description)  # Take first line only
            description = description.strip()
        else:
            # Fallback: use first line or a default description
            first_line = md_content.split('\n')[0].strip()
            description = first_line.replace('#', '').strip() if first_line.startswith('#') else "SecDevAI command"
        
        # Escape quotes in description
        description = description.replace('"', '\\"')
        
        # Use the full markdown content as the prompt
        # Escape triple quotes in the content
        prompt_content = md_content.replace('"""', '\\"\\"\\"')
        
        # Build TOML format
        toml_content = f'''description="{description}"
prompt = """
{prompt_content}
"""
'''
        return toml_content

    def deploy(self, target_dir: Path):
        """Deploy all templates to target directory."""
        file_mapping = self.get_file_mapping()
        platforms = self.detect_platforms(target_dir)

        console.print(f"[dim]Detected platforms: {', '.join(platforms)}[/dim]\n")

        # Deploy context and script files
        for source_file, target_file in file_mapping.items():
            if target_file == "secdevai.md":
                continue  # Handle commands separately

            source_path = self.templates_dir / source_file
            if not source_path.exists():
                console.print(f"[yellow]Warning:[/yellow] Template not found: {source_file}")
                continue

            target_path = target_dir / target_file
            target_path.parent.mkdir(parents=True, exist_ok=True)

            content = source_path.read_text()
            target_path.write_text(content)

            # Make scripts executable
            if target_file.endswith(".sh"):
                self._make_executable(target_path)

            console.print(f"[green]✓[/green] Deployed: {target_file}")

        # Deploy commands to platform-specific directories
        command_files = [
            "secdevai.md",
            "secdevai-review.md",
            "secdevai-fix.md",
            "secdevai-help.md",
            "secdevai-tool.md",
        ]
        
        platform_dirs = {
            "cursor": ".cursor/commands",
            "claude": ".claude/commands",
            "gemini": ".gemini/commands",
        }

        for platform in platforms:
            cmd_dir = platform_dirs.get(platform, ".cursor/commands")
            target_cmd_dir = target_dir / cmd_dir
            target_cmd_dir.mkdir(parents=True, exist_ok=True)

            for cmd_file in command_files:
                command_source = self.templates_dir / "commands" / cmd_file
                if command_source.exists():
                    md_content = command_source.read_text()
                    
                    # Gemini CLI uses .toml format, Cursor and Claude use .md
                    if platform == "gemini":
                        # Convert .md to .toml format for Gemini
                        toml_content = self._convert_md_to_toml(md_content)
                        # Change extension from .md to .toml
                        target_cmd_file = cmd_file.replace(".md", ".toml")
                        target_cmd_path = target_cmd_dir / target_cmd_file
                        target_cmd_path.write_text(toml_content)
                        console.print(f"[green]✓[/green] Deployed command to: {cmd_dir}/{target_cmd_file}")
                    else:
                        # Use .md format for Cursor and Claude
                        target_cmd_path = target_cmd_dir / cmd_file
                        target_cmd_path.write_text(md_content)
                        console.print(f"[green]✓[/green] Deployed command to: {cmd_dir}/{cmd_file}")
                else:
                    console.print(f"[yellow]Warning:[/yellow] Command template not found: {cmd_file}")

        # Create .secdevaiignore file if it doesn't exist
        ignore_file = target_dir / ".secdevaiignore"
        if not ignore_file.exists():
            ignore_content = """# SecDevAI ignore patterns
# Files and directories to exclude from security reviews

# Dependencies
node_modules/
venv/
.venv/
__pycache__/
*.pyc

# Build artifacts
dist/
build/
*.egg-info/

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db
"""
            ignore_file.write_text(ignore_content)
            console.print(f"[green]✓[/green] Created: .secdevaiignore")

    def _make_executable(self, file_path: Path):
        """Make file executable by adding +x permissions."""
        current_permissions = file_path.stat().st_mode
        file_path.chmod(current_permissions | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)


if __name__ == "__main__":
    main()

