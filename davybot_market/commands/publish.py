"""Publish command for CLI."""
import click
import httpx
import json
from pathlib import Path
from typing import Dict
from ..utils import get_api_client


@click.command()
@click.argument("resource_type", type=click.Choice(["skill", "agent", "mcp", "knowledge"]))
@click.argument("path", type=click.Path(exists=True))
@click.option("--name", "-n", required=True, help="Resource name")
@click.option("--description", "-d", help="Resource description")
@click.option("--author", "-a", help="Author name")
@click.option("--tags", "-t", multiple=True, help="Resource tags (can be used multiple times)")
@click.option("--metadata", "-m", type=click.Path(exists=True), help="Path to JSON metadata file")
def publish(resource_type: str, path: str, name: str, description: str, author: str, tags: tuple, metadata: str):
    """Publish a resource to the market.

    Examples:

        dawi publish skill ./my-skill --name "web-scraper" --description "Scrapes web data"

        dawi publish agent ./my-agent --name "data-analyst" --author "John Doe" --tag data --tag ml

        dawi publish skill ./skill --name "my-skill" --metadata metadata.json
    """
    path_obj = Path(path)

    # Build files dictionary from path
    files: Dict[str, str] = {}

    if path_obj.is_file() and path_obj.suffix in [".zip", ".tar", ".gz"]:
        # It's an archive - we'd need to extract it
        click.echo(click.style("Archive publishing not yet supported. Please provide a directory.", fg="yellow"), err=True)
        raise click.Abort()
    elif path_obj.is_dir():
        # Read all files in directory
        for file_path in path_obj.rglob("*"):
            if file_path.is_file() and not any(part.startswith(".") for part in file_path.parts):
                try:
                    relative_path = file_path.relative_to(path_obj)
                    files[str(relative_path)] = file_path.read_text(encoding="utf-8", errors="ignore")
                except Exception:
                    # Skip binary files
                    pass

    if not files:
        click.echo(click.style(f"No files found in {path}", fg="yellow"), err=True)
        raise click.Abort()

    # Load metadata from file if provided
    extra_metadata = {}
    if metadata:
        metadata_path = Path(metadata)
        try:
            extra_metadata = json.loads(metadata_path.read_text())
        except Exception as e:
            click.echo(click.style(f"Error reading metadata file: {e}", fg="red"), err=True)
            raise click.Abort()

    # Build resource data
    resource_data = {
        "name": name,
        "files": files,
    }

    if description:
        resource_data["description"] = description
    if author:
        resource_data["author"] = author
    if tags:
        resource_data["tags"] = list(tags)
    if extra_metadata:
        resource_data["metadata"] = extra_metadata

    with get_api_client() as client:
        try:
            click.echo(f"Publishing {resource_type} '{name}'...")
            click.echo(f"  Files: {len(files)}")
            if tags:
                click.echo(f"  Tags: {', '.join(tags)}")

            result = client.create_resource(resource_type, **resource_data)

            click.echo(click.style(f"Successfully published!", fg="green", bold=True))
            click.echo(f"ID: {result.get('id')}")
            click.echo(f"Version: {result.get('version')}")

        except httpx.HTTPError as e:
            click.echo(click.style(f"Error publishing: {e}", fg="red"), err=True)
            raise click.Abort()
