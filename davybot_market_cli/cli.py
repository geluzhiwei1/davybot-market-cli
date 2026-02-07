"""DavyBot Market CLI entry point."""

import click
import sys
import httpx

from .commands import search, install, publish, info
from .exit_codes import (
    SUCCESS,
    ERROR_API_UNHEALTHY,
    ERROR_NETWORK,
    ExitCodeError,
)


@click.group(invoke_without_command=True)
@click.pass_context
@click.option(
    "--api-url", envvar="DAVYBOT_API_URL", help="API URL (default: http://localhost:8000/api/v1)"
)
@click.version_option(version="0.1.0", prog_name="davy")
def cli(ctx: click.Context, api_url: str):
    """DavyBot Market - AI Agent Resources CLI.

    \b
    Examples:

        \b
        # Search for resources
        davy search "web scraping"

        \b
        # Install a resource
        davy install skill://web-scraper

        \b
        # Get resource information
        davy info agent://data-analyst

        \b
        # Publish a new resource
        davy publish skill ./my-skill --name "my-skill" --description "Does cool stuff"

    \b
    Note: 'dawei' is also available as an alias for 'davy'.
    """
    ctx.ensure_object(dict)
    ctx.obj["api_url"] = api_url

    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@cli.command()
def health():
    """Check API health status."""
    import os

    api_url = os.environ.get("DAVYBOT_API_URL", "http://localhost:8000/api/v1").replace(
        "/api/v1", ""
    )
    try:
        response = httpx.get(f"{api_url}/health", timeout=5)
        response.raise_for_status()
        data = response.json()
        click.echo(click.style("[OK] API is healthy", fg="green", bold=True))
        click.echo(f"  Status: {data.get('status', 'unknown')}")
        click.echo(f"  Database: {data.get('database', 'unknown')}")
    except httpx.TimeoutException:
        click.echo(click.style("[ERROR] API timeout", fg="red", bold=True))
        raise ExitCodeError(ERROR_NETWORK, "Request timed out")
    except httpx.ConnectError:
        click.echo(click.style("[ERROR] Cannot connect to API", fg="red", bold=True))
        raise ExitCodeError(ERROR_NETWORK, "Connection failed")
    except httpx.HTTPStatusError as e:
        click.echo(
            click.style(
                f"[ERROR] API returned error: {e.response.status_code}", fg="red", bold=True
            )
        )
        raise ExitCodeError(ERROR_API_UNHEALTHY, f"API returned {e.response.status_code}")
    except Exception as e:
        click.echo(click.style(f"[ERROR] API is unhealthy: {e}", fg="red", bold=True))
        raise ExitCodeError(ERROR_API_UNHEALTHY, str(e))


# Add all commands
cli.add_command(search.search)
cli.add_command(install.install)
cli.add_command(publish.publish)
cli.add_command(info.info)


def main():
    """Main entry point with proper exit codes."""
    try:
        cli(standalone_mode=False)
    except ExitCodeError as e:
        if e.message:
            click.echo(click.style(f"[ERROR] {e.message}", fg="red"), err=True)
        sys.exit(e.exit_code)
    except click.exceptions.Abort:
        # User aborted (Ctrl+C or similar)
        sys.exit(130)  # Standard exit code for SIGINT
    except Exception as e:
        click.echo(click.style(f"[ERROR] Unexpected error: {e}", fg="red"), err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
