"""Install command for CLI."""

import click
import httpx
import zipfile
import tarfile
from pathlib import Path
from ..utils import get_api_client, parse_resource_uri


@click.command()
@click.argument("resource_uri")
@click.option(
    "--format", "-f", type=click.Choice(["zip", "python"]), default="zip", help="Download format"
)
@click.option("--output", "-o", type=click.Path(), default=".", help="Output directory")
@click.option("--dev", is_flag=True, help="Install in development mode")
def install(resource_uri: str, format: str, output: str, dev: bool):
    """Install a resource from the market.

    RESOURCE_URI can be:
    - Full URI: skill://skill-name or agent://agent-name
    - Resource ID: abc123-def456

    Examples:

        dawi install skill://web-scraper

        dawi install agent://data-analyst --format python

        dawi install abc123-def456 --output ./my-skills
    """
    output_dir = Path(output)
    output_dir.mkdir(parents=True, exist_ok=True)

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
                    click.echo(f"Found: {resource['name']} ({resource_type})")
                else:
                    click.echo(
                        click.style(f"Resource '{resource_id}' not found.", fg="red"), err=True
                    )
                    raise click.Abort()
            except httpx.HTTPError as e:
                click.echo(click.style(f"Error searching: {e}", fg="red"), err=True)
                raise click.Abort()

    with get_api_client() as client:
        try:
            click.echo(f"Downloading {resource_type}...")
            downloaded_path = client.download_resource(
                resource_type, resource_id, format=format, output_dir=output_dir
            )

            click.echo(click.style(f"Downloaded to: {downloaded_path}", fg="green", bold=True))

            # Extract if zip
            if format == "zip" and downloaded_path.suffix == ".zip":
                click.echo("Extracting...")
                with zipfile.ZipFile(downloaded_path, "r") as zip_ref:
                    zip_ref.extractall(output_dir)
                    extracted_files = zip_ref.namelist()
                click.echo(click.style(f"Extracted {len(extracted_files)} files.", fg="green"))

                # Optionally remove zip file
                # downloaded_path.unlink()

            click.echo(click.style("Installation complete!", fg="green", bold=True))

        except httpx.HTTPError as e:
            click.echo(click.style(f"Error downloading: {e}", fg="red"), err=True)
            raise click.Abort()
        except Exception as e:
            click.echo(click.style(f"Error: {e}", fg="red"), err=True)
            raise click.Abort()
