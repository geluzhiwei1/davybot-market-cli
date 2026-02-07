# PyPI API Token 认证配置

## ✅ 正确的配置

### Workflow 配置

```yaml
# .github/workflows/publish.yml

permissions:
  contents: read  # 使用 token 认证时不需要 id-token: write

jobs:
  publish-to-pypi:
    name: Publish to PyPI
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: pypi
      url: https://pypi.org/p/davybot-market-cli

    steps:
      - name: Download all the dists
        uses: actions/download-artifact@v4
        with:
          name: python-package-distributions
          path: dist/

      - name: Publish distribution to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
        with:
          user: __token__                         # ← 必须是 __token__
          password: ${{ secrets.PYPI_API_TOKEN }}  # ← API token
          skip-existing: true                      # ← 可选:跳过已存在的版本

  publish-to-testpypi:
    name: Publish to TestPyPI
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: testpypi
      url: https://test.pypi.org/p/davybot-market-cli

    steps:
      - name: Download all the dists
        uses: actions/download-artifact@v4
        with:
          name: python-package-distributions
          path: dist/

      - name: Publish distribution to TestPyPI
        uses: pypa/gh-action-pypi-publish@release/v1
        with:
          user: __token__
          password: ${{ secrets.TEST_PYPI_API_TOKEN }}
          repository-url: https://test.pypi.org/legacy/
          skip-existing: true
```

## 🔑 关键要点

### 1. 使用 `user` 而不是 `username`

❌ **错误**:
```yaml
username: __token__  # 错误的参数名
```

✅ **正确**:
```yaml
user: __token__  # 正确的参数名
```

### 2. GitHub Environments 配置

在 GitHub 仓库设置中配置 environments:

**`pypi` 环境**:
- URL: `https://pypi.org/p/davybot-market-cli`
- Secret: `PYPI_API_TOKEN`

**`testpypi` 环境**:
- URL: `https://test.pypi.org/p/davybot-market-cli`
- Secret: `TEST_PYPI_API_TOKEN`

### 3. Token 获取

**PyPI Token**:
1. 登录 https://pypi.org/
2. Account Settings → API tokens → Add API token
3. Scope: `Entire account`
4. Token name: `davybot-market-cli-github`
5. 复制 token (格式: `pypi-xxx...xxx`)

**TestPyPI Token**:
1. 登录 https://test.pypi.org/
2. Account Settings → API tokens → Add API token
3. Scope: `Entire account`
4. Token name: `davybot-market-cli-github-test`
5. 复制 token

## ⚠️ 常见错误

### 错误 1: 参数名错误

```
Warning: Unexpected input(s) 'username', valid inputs are ['user', 'password', ...]
```

**解决**: 使用 `user` 而不是 `username`

### 错误 2: OIDC 错误

```
Error: Trusted publishing exchange failure:
OpenID Connect token retrieval failed: missing or insufficient
OIDC token permissions
```

**原因**: 没有提供 `user: __token__`,action 尝试使用 OIDC

**解决**: 添加 `user: __token__` 参数

### 错误 3: Token 无效

```
Error: 403 Forbidden from PyPI
```

**检查**:
1. Token 是否正确复制
2. Token scope 是否是 "Entire account"
3. Token 未过期

## 📊 Token vs OIDC 对比

| 特性 | API Token | OIDC |
|------|-----------|------|
| **参数** | `user: __token__` | 不需要 user/password |
| **权限** | `contents: read` | `id-token: write` |
| **配置** | GitHub Environment secret | PyPI Trusted Publisher |
| **安全性** | ⭐⭐⭐ 中等 | ⭐⭐⭐⭐⭐ 高 |
| **维护** | 需要更新 token | 无需维护 |
| **适用场景** | 快速发布、个人项目 | 生产环境、团队项目 |

## 🚀 发布流程

使用 Token 认证的完整发布流程:

```bash
# 1. 更新版本号
vim pyproject.toml  # version = "0.1.0"

# 2. 提交更改
git add pyproject.toml
git commit -m "chore: bump version to 0.1.0"
git push origin main

# 3. 创建标签
git tag -a v0.1.0 -m "Release v0.1.0"
git push origin v0.1.0

# 4. 监控发布
# 访问: https://github.com/geluzhiwei1/davybot-market-cli/actions
```

## ✅ 验证发布

发布成功后验证:

```bash
# 测试 TestPyPI
pip install --index-url https://test.pypi.org/simple/ \
    --extra-index-url https://pypi.org/simple/ \
    davybot-market-cli==0.1.0

# 测试 PyPI
pip install davybot-market-cli==0.1.0

# 验证 CLI
davy --help
dawei --help

# 验证 SDK
python -c "from davybot_market_cli import DavybotMarketClient; print('✅ Success')"
```

## 🔗 相关链接

- [PyPI API Tokens](https://pypi.org/help/#apitoken)
- [TestPyPI](https://test.pypi.org/)
- [pypa/gh-action-pypi-publish](https://github.com/pypa/gh-action-pypi-publish)
- [GitHub Actions Publishing](https://docs.github.com/en/actions/publishing-packages/publishing-python-packages-from-github-actions)

## 📝 配置检查清单

- [ ] PyPI 和 TestPyPI 账号已注册
- [ ] API tokens 已创建
- [ ] GitHub environments (`pypi`, `testpypi`) 已创建
- [ ] Secrets 已正确配置 (`PYPI_API_TOKEN`, `TEST_PYPI_API_TOKEN`)
- [ ] Workflow 使用 `user: __token__` 参数
- [ ] Workflow 没有配置 `id-token: write` (使用 token 时不需要)
- [ ] 标签格式正确 (`v*.*.*`)
- [ ] `pyproject.toml` 中的版本号已更新

---

**配置状态**: ✅ 完成并测试
**认证方式**: API Token
**最后更新**: 2026-02-07
