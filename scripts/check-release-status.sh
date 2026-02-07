#!/bin/bash
# Release Status Check Script
# This script checks the current status of the v0.1.0 release

set -e

echo "🔍 DavyBot Market CLI - Release v0.1.0 Status Check"
echo "=================================================="
echo ""

# Check git status
echo "📋 Git Status:"
echo "  Branch: $(git branch --show-current)"
echo "  Latest Commit: $(git log -1 --oneline)"
echo "  Tags: $(git tag -l | grep v0.1.0 || echo 'v0.1.0 (not found)')"
echo ""

# Check if tag is pushed
echo "🏷️  Tag Status:"
if git rev-parse v0.1.0 >/dev/null 2>&1; then
    echo "  ✓ Tag v0.1.0 exists locally"
    if git ls-remote --tags origin | grep -q "v0.1.0"; then
        echo "  ✓ Tag v0.1.0 pushed to remote"
    else
        echo "  ✗ Tag v0.1.0 NOT pushed to remote"
    fi
else
    echo "  ✗ Tag v0.1.0 does not exist"
fi
echo ""

# Check package files
echo "📦 Package Files:"
if [ -f "pyproject.toml" ]; then
    echo "  ✓ pyproject.toml exists"
    VERSION=$(grep "^version" pyproject.toml | head -1 | cut -d'"' -f2)
    echo "  Version: $VERSION"
    if [ "$VERSION" = "0.1.0" ]; then
        echo "  ✓ Version matches tag"
    else
        echo "  ✗ Version mismatch (expected 0.1.0)"
    fi
else
    echo "  ✗ pyproject.toml not found"
fi

if [ -d "davybot_market_cli" ]; then
    echo "  ✓ Package directory exists"
else
    echo "  ✗ Package directory not found"
fi
echo ""

# Check GitHub workflows
echo "⚙️  GitHub Workflows:"
if [ -f ".github/workflows/ci.yml" ]; then
    echo "  ✓ CI workflow exists"
    if grep -q "davybot_market_cli" .github/workflows/ci.yml; then
        echo "  ✓ CI workflow uses correct package name"
    else
        echo "  ✗ CI workflow has incorrect package name"
    fi
else
    echo "  ✗ CI workflow not found"
fi

if [ -f ".github/workflows/publish.yml" ]; then
    echo "  ✓ Publish workflow exists"
    if grep -q "PYPI_API_TOKEN" .github/workflows/publish.yml; then
        echo "  ✓ Publish workflow configured for token auth"
    else
        echo "  ✗ Publish workflow missing token configuration"
    fi
else
    echo "  ✗ Publish workflow not found"
fi
echo ""

# Check documentation
echo "📚 Documentation:"
if [ -f "docs/PYPI_SETUP.md" ]; then
    echo "  ✓ PyPI setup guide exists"
else
    echo "  ✗ PyPI setup guide not found"
fi

if [ -f "docs/deploy.md" ]; then
    echo "  ✓ Deployment docs exist"
else
    echo "  ✗ Deployment docs not found"
fi
echo ""

# Provide next steps
echo "📝 Next Steps:"
echo ""
echo "1. Monitor GitHub Actions:"
echo "   https://github.com/geluzhiwei1/davybot-market-cli/actions"
echo ""
echo "2. Verify PyPI Environments are configured:"
echo "   - pypi environment with PYPI_API_TOKEN"
echo "   - testpypi environment with TEST_PYPI_API_TOKEN"
echo ""
echo "3. After successful release, verify installation:"
echo "   pip install davybot-market-cli==0.1.0"
echo ""
echo "4. Test the CLI:"
echo "   davy --help"
echo "   dawei --help"
echo ""
echo "=================================================="
