# DavyBot Market - CLI & SDK

Unified CLI and Python SDK for DavyBot Market - AI Agent Resources.

## Installation

```bash
pip install davybot-market-cli
```

Or install from source:

```bash
cd davybot-market-cli
pip install -e .
```

## CLI Usage

> **Note:** The CLI is available as both `davy` (primary command) and `dawei` (alias). Both commands work identically.

### Search Resources

```bash
# Search all resources
davy search "web scraping"

# Filter by type
davy search "agent" --type agent

# Limit results
davy search "data" --limit 50

# JSON output
davy search "ml" --output json
```

### Install Resources

```bash
# Install a skill
davy install skill://web-scraper

# Install to specific directory
davy install agent://data-analyst --output ./my-agents

# Install by ID
davy install abc123-def456
```

### Publish Resources

```bash
# Publish a skill
davy publish skill ./my-skill --name "web-scraper" --description "Scrapes web data"

# Publish with tags
davy publish agent ./my-agent --name "data-analyst" --tag data --tag ml

# Publish with metadata
davy publish skill ./skill --name "my-skill" --metadata metadata.json
```

### View Resource Info

```bash
# Get resource details
davy info skill://web-scraper

# Show similar resources
davy info agent://data-analyst --similar

# JSON output
davy info abc123-def456 --output json
```

### Health Check

```bash
# Check API status
davy health
```

## Python SDK Usage

### Basic Usage

```python
from davybot_market_cli import DavybotMarketClient

# Initialize client
with DavybotMarketClient() as client:
    # Check API health
    health = client.health()
    print(f"API Status: {health['status']}")

    # Search for resources
    results = client.search("web scraping")
    print(f"Found {results['total']} resources")

    # List all skills
    skills = client.list_skills()
    for skill in skills['items']:
        print(f"- {skill['name']}: {skill['description']}")

    # Get specific resource
    skill = client.get_skill("skill-id-here")
    print(f"Skill: {skill['name']} v{skill['version']}")

    # Download a resource
    client.download("skill", "skill-id", "./downloads")
```

### Async Usage

```python
import asyncio
from davybot_market_cli import DavybotMarketClient

async def main():
    async with DavybotMarketClient() as client:
        # Search resources
        results = await client.search("machine learning")
        print(f"Found {results['total']} results")

asyncio.run(main())
```

### Create Resources

```python
with DavybotMarketClient() as client:
    # Create a skill
    skill = client.create_skill(
        name="web-scraper",
        description="Scrapes web data efficiently",
        files={
            "scraper.py": "# Your scraper code here",
            "config.json": '{"timeout": 30}',
        },
        tags=["web", "scraping", "data"],
        author="Your Name"
    )
    print(f"Created skill with ID: {skill['id']}")
```

### Download Resources

```python
with DavybotMarketClient() as client:
    # Download to specific directory
    client.download("skill", "skill-id", "./my-skills")

    # Download with specific format
    client.download("agent", "agent-id", "./agents", format="python")

    # Download specific version
    client.download("skill", "skill-id", "./skills", version="2.0.0")
```

### Ratings and Reviews

```python
with DavybotMarketClient() as client:
    # Rate a resource
    client.rate_resource("resource-id", score=5, comment="Excellent!")

    # Get all ratings
    ratings = client.get_resource_ratings("resource-id")

    # Get average rating
    avg = client.get_average_rating("resource-id")
    print(f"Average: {avg['average_rating']} ({avg['total_ratings']} ratings)")
```

## Configuration

### Environment Variables

- `DAVYBOT_API_URL`: API base URL (default: `http://localhost:8000/api/v1`)
- `DAVYBOT_API_KEY`: API key for authentication

### Client Options

```python
# Custom API URL
client = DavybotMarketClient(base_url="https://api.market.davybot.ai/api/v1")

# With API key
client = DavybotMarketClient(api_key="your-api-key")

# With custom timeout
client = DavybotMarketClient(timeout=60.0)

# Disable SSL verification (not recommended for production)
client = DavybotMarketClient(verify_ssl=False)
```

## Commands Reference

| Command | Description |
|---------|-------------|
| `davy search QUERY` | Search for resources |
| `davy install RESOURCE_URI` | Install a resource |
| `davy publish TYPE PATH` | Publish a new resource |
| `davy info RESOURCE_URI` | View resource details |
| `davy health` | Check API health |
| `davy --help` | Show help message |
| `davybot --version` | Show version |

## Examples

### Complete CLI Workflow

```bash
# Search for a skill
davy search "web scraper" --type skill

# View details
davy info skill://web-scraper

# Install
davy install skill://web-scraper
```

### Publishing a New Skill

```bash
# Create your skill
mkdir my-skill
cd my-skill

# Create skill.py
cat > skill.py << 'EOF'
def execute(input_data):
    """Execute the skill."""
    return {"result": "success"}
EOF

# Publish to market
davy publish skill . --name "my-skill" --description "My awesome skill"
```

### Python SDK Integration

```python
from davybot_market_cli import DavybotMarketClient

# Integrate into your application
def find_and_download_skill(query: str, output_dir: str):
    with DavybotMarketClient() as client:
        # Search
        results = client.search(query, resource_type="skill", limit=1)
        if not results['results']:
            print("No skills found")
            return

        skill = results['results'][0]
        print(f"Found: {skill['name']}")

        # Download
        client.download("skill", skill['id'], output_dir)
        print(f"Downloaded to {output_dir}")
```

## Error Handling

```python
from davybot_market_cli import (
    DavybotMarketClient,
    AuthenticationError,
    NotFoundError,
    ValidationError,
    APIError
)

with DavybotMarketClient() as client:
    try:
        skill = client.get_skill("invalid-id")
    except NotFoundError:
        print("Resource not found!")
    except AuthenticationError:
        print("Invalid API key!")
    except APIError as e:
        print(f"API error: {e}")
```

## License

MIT
