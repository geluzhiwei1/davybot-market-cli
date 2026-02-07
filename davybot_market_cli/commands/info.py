"""Info command for CLI."""

import click
import httpx
from ..utils import get_api_client, parse_resource_uri
from ..exceptions import NotFoundError, ValidationError, APIError, DavybotMarketError


@click.command()
@click.argument("resource_uri")
@click.option(
    "--output", "-o", type=click.Choice(["table", "json"]), default="table", help="Output format"
)
@click.option("--similar", "-s", is_flag=True, help="Show similar resources")
def info(resource_uri: str, output: str, similar: bool) -> None:
    """Show detailed information about a resource.

    RESOURCE_URI can be:
    - Full URI: skill://skill-name or agent://agent-name
    - Resource ID: abc123-def456

    Examples:

        dawi info skill://web-scraper

        dawi info abc123-def456

        dawi info agent://data-analyst --similar
    """
    # Parse resource URI
    resource_type, resource_id = parse_resource_uri(resource_uri)

    if resource_type is None:
        # Try to find by name
        click.echo(f"Searching for resource: {resource_id}...")
        with get_api_client() as client:
            try:
                search_result = client.search(resource_id, limit=1)
                results = search_result.get("results", [])
                if results:
                    resource = results[0]
                    resource_type = resource["type"]
                    resource_id = resource["id"]
                else:
                    click.echo(
                        click.style(f"Resource '{resource_id}' not found.", fg="red"), err=True
                    )
                    raise click.Abort()
            except httpx.HTTPError as e:
                click.echo(click.style(f"Error: {e}", fg="red"), err=True)
                raise click.Abort()

    with get_api_client() as client:
        try:
            resource = client.get_resource(resource_type, resource_id)

            if output == "json":
                import json

                click.echo(json.dumps(resource, indent=2))
            else:
                # Display formatted info
                click.echo(click.style(resource["name"], fg="cyan", bold=True))
                click.echo(f"{'=' * 60}")
                click.echo(f"Type:        {resource['type']}")
                click.echo(f"Version:     {resource['version']}")
                click.echo(f"Author:      {resource.get('author', 'Unknown')}")
                click.echo(f"Rating:      {resource['rating']:.1f}/5.0")
                click.echo(f"Downloads:   {resource['downloads']}")
                click.echo()

                if resource.get("description"):
                    click.echo(click.style("Description:", bold=True))
                    click.echo(resource["description"])
                    click.echo()

                if resource.get("tags"):
                    click.echo(click.style("Tags:", bold=True))
                    click.echo(", ".join(resource["tags"]))
                    click.echo()

                if resource.get("extra_metadata"):
                    click.echo(click.style("Metadata:", bold=True))
                    import json as json_mod

                    click.echo(json_mod.dumps(resource["extra_metadata"], indent=2))
                    click.echo()

                click.echo(click.style("Installation:", bold=True))
                click.echo(f"  dawi install {resource_type}://{resource['name']}")
                click.echo("  # or by ID:")
                click.echo(f"  dawi install {resource_id}")
                click.echo()

                # Show similar resources if requested
                if similar:
                    click.echo(click.style("Similar Resources:", bold=True))
                    try:
                        similar_result = client.get_similar(resource_id, limit=5)
                        similar_resources = similar_result.get("results", [])

                        if similar_resources:
                            for i, sim in enumerate(similar_resources, 1):
                                click.echo(
                                    f"{i}. {sim['name']} ({sim['type']}) - {sim['rating']:.1f}★"
                                )
                        else:
                            click.echo("  No similar resources found.")
                    except httpx.HTTPError:
                        click.echo("  Could not fetch similar resources.")

        except NotFoundError:
            click.echo(click.style("Error: Resource not found", fg="red"), err=True)
            raise click.Abort()
        except ValidationError as e:
            click.echo(click.style(f"Error: Invalid request - {e}", fg="red"), err=True)
            raise click.Abort()
        except APIError as e:
            click.echo(click.style(f"Error: API error - {e}", fg="red"), err=True)
            raise click.Abort()
        except (DavybotMarketError, httpx.HTTPError) as e:
            click.echo(click.style(f"Error fetching resource: {e}", fg="red"), err=True)
            raise click.Abort()
