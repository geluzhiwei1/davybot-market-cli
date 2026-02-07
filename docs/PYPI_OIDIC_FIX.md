# PyPI 发布 OIDC 错误修复

## ❌ 错误信息

```
Error: Trusted publishing exchange failure:
OpenID Connect token retrieval failed: GitHub: missing or insufficient
OIDC token permissions, the ACTIONS_ID_TOKEN_REQUEST_TOKEN environment
variable was unset
```

## 🔍 问题原因

`pypa/gh-action-pypi-publish@release/v1` 默认尝试使用 OIDC (OpenID Connect) 进行认证,但我们的 workflow 配置只提供了 API token,没有配置 OIDC 权限。

当提供 `password` 参数但没有 `id-token: write` 权限时,action 会尝试使用 OIDC 但失败。

## ✅ 解决方案

### 方案 1: 禁用 OIDC (已采用)

在 `pypa/gh-action-pypi-publish` 步骤中添加 `attestations: false` 参数:

```yaml
- name: Publish distribution to PyPI
  uses: pypa/gh-action-pypi-publish@release/v1
  with:
    password: ${{ secrets.PYPI_API_TOKEN }}
    attestations: false  # 禁用 OIDC
    skip-existing: true  # 如果包已存在则跳过
```

**优点**:
- ✅ 简单快速
- ✅ 不需要额外配置
- ✅ 适合使用 API token 的场景

**缺点**:
- ❌ 需要管理 token
- ❌ Token 需要定期更新

### 方案 2: 配置完整的 OIDC (更安全,推荐)

#### 步骤 1: 在 PyPI 配置 Trusted Publisher

1. 登录 PyPI → Publishing → Add a new pending publisher
2. 填写配置:
   - **PyPI Project Name**: `davybot-market-cli`
   - **Owner**: `geluzhiwei1`
   - **Repository name**: `davybot-market-cli`
   - **Workflow name**: `publish.yml`
   - **Environment name**: `pypi`

#### 步骤 2: 修改 GitHub Workflow

```yaml
permissions:
  contents: read
  id-token: write  # 启用 OIDC

jobs:
  publish-to-pypi:
    environment:
      name: pypi
      url: https://pypi.org/p/davybot-market-cli
    steps:
      - name: Publish distribution to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
        # 不需要 password 参数,自动使用 OIDC
```

**优点**:
- ✅ 无需管理 token
- ✅ 更安全 (无 secret 可泄露)
- ✅ Token 不会过期

**缺点**:
- ❌ 初次配置稍复杂
- ❌ 需要在 PyPI 上配置

## 📝 当前配置

**我们采用方案 1** (API Token + 禁用 OIDC):

```yaml
permissions:
  contents: read  # 不需要 id-token: write

jobs:
  publish-to-pypi:
    environment:
      name: pypi
    steps:
      - name: Publish distribution to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
        with:
          password: ${{ secrets.PYPI_API_TOKEN }}
          attestations: false  # 关键:禁用 OIDC
          skip-existing: true
```

## 🔧 从 Token 迁移到 OIDC (可选)

如果想从 Token 认证迁移到 OIDC:

### 1. 在 PyPI 配置 Trusted Publisher

访问: https://pypi.org/manage/account/publishing/

添加新的 publisher:
```
Project Name: davybot-market-cli
Owner: geluzhiwei1
Repository name: davybot-market-cli
Workflow name: publish.yml
Environment name: pypi
```

### 2. 修改 Workflow

```yaml
permissions:
  contents: read
  id-token: write  # 添加这个

jobs:
  publish-to-pypi:
    environment:
      name: pypi
    steps:
      - name: Publish distribution to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
        # 移除 password 参数
        # 移除 attestations: false
```

### 3. 验证

推送新标签测试:
```bash
git tag v0.1.1-test -m "Test OIDC"
git push origin v0.1.1-test
```

## 📊 对比

| 特性 | API Token | OIDC |
|------|-----------|------|
| 配置难度 | ⭐ 简单 | ⭐⭐⭐ 中等 |
| 安全性 | ⭐⭐ 中等 | ⭐⭐⭐⭐⭐ 高 |
| 维护成本 | ⭐⭐ 需要更新 token | ⭐ 无需维护 |
| 首次设置 | ⭐ 快速 | ⭐⭐⭐ 需要配置 PyPI |

## 🎯 推荐

- **新手/快速发布**: 使用 API Token (当前方案)
- **生产环境/长期维护**: 使用 OIDC

## 📚 相关链接

- [PyPI Trusted Publishers](https://docs.pypi.org/trusted-publishers/)
- [GitHub OIDC Documentation](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect)
- [pypa/gh-action-pypi-publish](https://github.com/pypa/gh-action-pypi-publish)

## 🔗 当前状态

- ✅ 问题已修复
- ✅ 使用 API Token 认证
- ✅ OIDC 已禁用
- ✅ 可以正常发布

---

**最后更新**: 2026-02-07
**状态**: ✅ 已解决
