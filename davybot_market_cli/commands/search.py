"""Search command for CLI."""

import click
import httpx
from ..utils import get_api_client
from ..exit_codes import (
    ERROR_NETWORK,
    ERROR_API,
    ExitCodeError,
)
from ..exceptions import (
    NotFoundError,
    ValidationError,
    APIError,
    DavybotMarketError,
)


@click.command()
@click.argument("query")
@click.option(
    "--type",
    "-t",
    type=click.Choice(["skill", "agent", "mcp", "knowledge"]),
    help="Filter by resource type",
)
@click.option("--limit", "-l", default=20, help="Maximum number of results")
@click.option(
    "--output", "-o", type=click.Choice(["table", "json"]), default="table", help="Output format"
)
def search(query: str, type: str, limit: int, output: str) -> None:
    """Search for resources in the market.

    Examples:

        dawi search "web scraping"

        dawi search "agent" --type agent

        dawi search "data processing" --limit 50 --output json
    """
    with get_api_client() as client:
        try:
            result = client.search(query, resource_type=type, limit=limit)

            if output == "json":
                import json

                click.echo(json.dumps(result, indent=2))
            else:
                results = result.get("results", [])
                total = result.get("total", 0)

                if not results:
                    click.echo(click.style("No results found.", fg="yellow"))
                    return

                click.echo(click.style(f"Found {total} results for '{query}':", bold=True))
                click.echo()

                for i, resource in enumerate(results, 1):
                    click.echo(click.style(f"{i}. {resource['name']}", fg="cyan", bold=True))
                    click.echo(f"   Type: {resource['type']}")
                    if resource.get("description"):
                        click.echo(
                            f"   Description: {resource['description'][:80]}{'...' if len(resource['description']) > 80 else ''}"
                        )
                    click.echo(
                        f"   Rating: {resource['rating']:.1f} | Downloads: {resource['downloads']}"
                    )
                    if resource.get("tags"):
                        click.echo(f"   Tags: {', '.join(resource['tags'][:5])}")
                    click.echo()

        except NotFoundError:
            click.echo(click.style("Error: Resource not found", fg="red"), err=True)
            raise ExitCodeError(ERROR_API, "Not found")
        except ValidationError as e:
            click.echo(click.style(f"Error: Invalid request - {e}", fg="red"), err=True)
            raise ExitCodeError(ERROR_API, f"Validation error: {e}")
        except APIError as e:
            click.echo(click.style(f"Error: API error - {e}", fg="red"), err=True)
            raise ExitCodeError(ERROR_API, str(e))
        except httpx.TimeoutException:
            click.echo(click.style("Error: Request timed out", fg="red"), err=True)
            raise ExitCodeError(ERROR_NETWORK, "Request timed out")
        except httpx.ConnectError:
            click.echo(click.style("Error: Cannot connect to API", fg="red"), err=True)
            raise ExitCodeError(ERROR_NETWORK, "Connection failed")
        except (DavybotMarketError, httpx.HTTPError) as e:
            click.echo(click.style(f"Error searching: {e}", fg="red"), err=True)
            raise ExitCodeError(ERROR_NETWORK, str(e))
