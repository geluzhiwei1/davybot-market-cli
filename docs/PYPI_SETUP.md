# PyPI 发布配置指南

本文档说明如何配置 PyPI 发布认证。

## 方式一: API Token (推荐新手)

### 1. 注册账号

**PyPI (生产环境)**:
- 访问: https://pypi.org/account/register/
- 完成注册和邮箱验证

**TestPyPI (测试环境)**:
- 访问: https://test.pypi.org/account/register/
- 使用相同邮箱注册(需要单独注册)

### 2. 创建 API Token

#### PyPI Token
1. 登录 https://pypi.org/
2. 进入 Account Settings → API tokens
3. 点击 "Add API token"
4. 配置:
   - Scope: `Entire account` (首次发布必需)
   - Token name: `davybot-market-cli-github`
5. 点击 "Add token"
6. **立即复制 token** (只显示一次!)

#### TestPyPI Token
1. 登录 https://test.pypi.org/
2. 进入 Account Settings → API tokens
3. 点击 "Add API token"
4. 配置:
   - Scope: `Entire account`
   - Token name: `davybot-market-cli-github-test`
5. 复制 token

### 3. 配置 GitHub Environments

1. **访问仓库设置**:
   ```
   https://github.com/geluzhiwei1/davybot-market-cli/settings/environments
   ```

2. **创建 `pypi` 环境**:
   - 点击 "New environment"
   - Name: `pypi`
   - 创建后点击环境名称进入配置
   - 在 "Environment secrets" 部分:
     - 点击 "Add secret"
     - Name: `PYPI_API_TOKEN`
     - Value: 粘贴 PyPI token
   - 保存

3. **创建 `testpypi` 环境**:
   - 点击 "New environment"
   - Name: `testpypi`
   - 创建后点击环境名称进入配置
   - 在 "Environment secrets" 部分:
     - 点击 "Add secret"
     - Name: `TEST_PYPI_API_TOKEN`
     - Value: 粘贴 TestPyPI token
   - 保存

### 4. 提交配置

配置已添加到 `.github/workflows/publish.yml`,提交更新:

```bash
git add .github/workflows/publish.yml
git commit -m "chore: configure PyPI token authentication"
git push origin main
```

### 5. 重新触发发布

删除并重新推送标签:

```bash
git tag -d v0.1.0
git push origin :refs/tags/v0.1.0
git tag -a v0.1.0 -m "Release v0.1.0"
git push origin v0.1.0
```

## 方式二: OIDC (推荐高级用户,更安全)

OIDC (OpenID Connect) 无需存储 token,更安全但配置稍复杂。

### 1. 在 PyPI 配置 OIDC

1. **登录 PyPI** → Publishing → Add a new pending publisher

2. **填写配置**:
   - PyPI Project Name: `davybot-market-cli`
   - Owner: `geluzhiwei1` (你的 GitHub 用户名)
   - Repository name: `davybot-market-cli`
   - Workflow name: `publish.yml`
   - Environment name: `pypi`

3. **复制 PyPI 提供的配置信息**

### 2. 在 GitHub 配置 OIDC

1. **访问仓库设置**:
   ```
   Settings → Environments → pypi
   ```

2. **添加 OIDC 配置** (不需要 secret)
   - 环境已存在,只需确保 publish.yml 中的 permissions 包含 `id-token: write`

### 3. 切换到 OIDC 模式

修改 `.github/workflows/publish.yml`:

```yaml
permissions:
  contents: read
  id-token: write  # 启用 OIDC

jobs:
  publish-to-pypi:
    environment:
      name: pypi
      url: https://pypi.org/p/davybot-market-cli
    # ... 其他配置保持不变
```

## 验证配置

### 测试 TestPyPI 发布

推送一个测试标签:

```bash
git tag v0.0.1-test -m "Test release"
git push origin v0.0.1-test
```

访问 GitHub Actions 查看是否成功:
```
https://github.com/geluzhiwei1/davybot-market-cli/actions
```

### 验证 TestPyPI 发布

```bash
pip install --index-url https://test.pypi.org/simple/ \
    --extra-index-url https://pypi.org/simple/ \
    davybot-market-cli==0.0.1-test
```

## 常见问题

### Token 无效
- 检查 token 是否正确复制
- 确认 token scope 是 "Entire account"
- 尝试重新生成 token

### 包名已存在
- 确认 `davybot-market-cli` 在 PyPI 上未被占用
- 如已被占用,需要在 `pyproject.toml` 中修改包名

### 权限错误
- 检查 GitHub environment 配置正确
- 确认 secret 名称完全匹配: `PYPI_API_TOKEN` 和 `TEST_PYPI_API_TOKEN`

### 发布失败
- 查看 GitHub Actions 日志
- 确认版本号在 `pyproject.toml` 中已更新
- 检查 tag 格式必须是 `v*.*.*`

## 相关链接

- [PyPI 官方文档](https://pypi.org/)
- [TestPyPI](https://test.pypi.org/)
- [GitHub Actions PyPI 发布](https://github.com/marketplace/actions/pypi-publish)
- [OIDC 配置指南](https://docs.pypi.org/trusted-publishers/)

## 最佳实践

1. **首次发布**: 先在 TestPyPI 测试
2. **Token 安全**: 不要在代码中硬编码 token
3. **版本管理**: 使用语义化版本号
4. **监控发布**: 在 Actions 页面查看发布状态
5. **验证安装**: 发布后立即测试安装
