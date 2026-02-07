# 部署文档

GitHub Actions CI/CD 自动化流水线。

## 流水线概览

```
Push/PR → CI (Lint+Test+Build) → Merge → Tag v*.*.* → Auto Publish PyPI
```

## 工作流

### CI (`.github/workflows/ci.yml`)
- **触发**: Push to `main`/`develop`, PR
- **检查**: Black → Ruff → MyPy → pytest (3.12/3.13 × Ubuntu/Windows/macOS) → Build → Install

### Publish (`.github/workflows/publish.yml`)
- **触发**: Push tag `v*.*.*`
- **流程**: Build → TestPyPI → PyPI → GitHub Release

### CodeQL & Dependabot
- **CodeQL**: 每周日自动安全扫描
- **Dependabot**: 每周日自动更新依赖

## 使用流程

### 开发
```bash
git checkout -b feature/xxx
pip install -e ".[dev]"

# 开发并本地测试
black davybot_market_cli tests && ruff check davybot_market_cli tests
mypy davybot_market_cli && pytest --cov=davybot_market_cli -v

git commit -am "feat: xxx" && git push origin feature/xxx
# 创建 PR,CI 自动运行,通过后合并
```

### 发布
```bash
# 1. 更新 pyproject.toml 版本号
vim pyproject.toml

# 2. 提交并打标签
git commit -am "chore: bump version to x.x.x" && git push
git tag -a vx.x.x -m "Release x.x.x" && git push origin vx.x.x

# 3. 自动发布到 PyPI,监控 Actions 状态
```

### 本地验证脚本
```bash
#!/bin/bash
set -e
echo "🔍 Lint..."
black --check davybot_market_cli tests
ruff check davybot_market_cli tests
mypy davybot_market_cli

echo "🧪 Test..."
pytest --cov=davybot_market_cli -v

echo "📦 Build..."
python -m build
twine check dist/*
echo "✅ All passed!"
```

## GitHub 配置

### 分支保护
- Require PR before merging
- Require status checks to pass
- Require branches to be up to date

### Environments
**`pypi`** (生产):
- 推荐使用 OIDC (PyPI → Publishing → Add pending publisher)
- 或配置 `PYPI_API_TOKEN` secret

**`testpypi`** (测试):
- 配置 `TEST_PYPI_API_TOKEN` secret

### PyPI Token 获取
1. PyPI → Account settings → API tokens → Add API token
2. Scope: Entire account
3. 复制 token 到 GitHub Environment secret

## 安装

```bash
# PyPI
pip install davybot-market-cli

# 源码
git clone https://github.com/your-org/davybot-market-cli.git
cd davybot-market-cli && pip install -e ".[dev]"

# TestPyPI
pip install --index-url https://test.pypi.org/simple/ \
    --extra-index-url https://pypi.org/simple/ davybot-market-cli
```

## 故障排除

### CI 失败
```bash
# Lint 失败
black davybot_market_cli tests
ruff check --fix davybot_market_cli tests

# 测试失败
pytest tests/ -v -s
pytest --cov=davybot_market_cli --cov-report=html

# 类型检查失败
mypy davybot_market_cli --show-error-codes
```

### 发布失败
- **PyPI 403**: 检查 token/版本号/包名
- **标签格式**: 必须是 `v1.0.0` (不是 `1.0.0`)
- **构建失败**: `rm -rf dist/ build/ *.egg-info && python -m build`

## 常用命令

```bash
# 本地检查
black --check . && ruff check . && mypy .
pytest -v && python -m build && twine check dist/*

# 发布
git tag vx.x.x && git push origin vx.x.x

# 验证
pip install davybot-market-cli==x.x.x
curl https://pypi.org/pypi/davybot-market-cli/json | jq .
```

## README 徽章

```markdown
[![CI](https://github.com/your-org/davybot-market-cli/actions/workflows/ci.yml/badge.svg)](https://github.com/your-org/davybot-market-cli/actions/workflows/ci.yml)
[![PyPI](https://badge.fury.io/py/davybot-market-cli.svg)](https://badge.fury.io/py/davybot-market-cli)
[![Python](https://img.shields.io/pypi/pyversions/davybot-market-cli)](https://pypi.org/pypi/davybot-market-cli)
```

## 关键文件

```
.github/
├── workflows/
│   ├── ci.yml              # 持续集成
│   ├── publish.yml         # 自动发布
│   ├── codeql.yml          # 安全扫描
│   └── dependabot.yml      # 依赖审查
├── dependabot.yml          # 自动更新配置
pyproject.toml              # 项目配置
```

## 最佳实践

1. 推送前本地测试
2. 小步快跑,频繁提交
3. 保护主分支,CI 通过才合并
4. 保持高测试覆盖率
5. 定期合并 Dependabot PR
6. 严格使用 `v*.*.*` 标签格式

## 相关文档

- [GitHub Actions](https://docs.github.com/en/actions)
- [PyPI 发布指南](https://packaging.python.org/tutorials/packaging-projects/)
- [语义化版本](https://semver.org/lang/zh-CN/)
