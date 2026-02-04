"""Tests for CLI commands."""
import pytest
from click.testing import CliRunner
from davybot_market.cli import cli


@pytest.fixture
def runner():
    """Create CLI runner."""
    return CliRunner()


def test_cli_help(runner):
    """Test CLI help command."""
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "DavyBot Market" in result.output


def test_cli_version(runner):
    """Test CLI version command."""
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0


def test_search_command_help(runner):
    """Test search command help."""
    result = runner.invoke(cli, ["search", "--help"])
    assert result.exit_code == 0
    assert "Search for resources" in result.output


def test_health_command_help(runner):
    """Test health command help."""
    result = runner.invoke(cli, ["health", "--help"])
    assert result.exit_code == 0
    assert "Check API health status" in result.output
