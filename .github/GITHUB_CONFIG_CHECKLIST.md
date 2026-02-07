# GitHub Environments 配置快速验证

## ✅ 已配置项

你已经完成以下配置:

### GitHub Environments
- ✅ `pypi` 环境 - 包含 `PYPI_API_TOKEN` secret
- ✅ `testpypi` 环境 - 包含 `TEST_PYPI_API_TOKEN` secret

### 工作流配置
- ✅ `.github/workflows/ci.yml` - CI 检查
- ✅ `.github/workflows/publish.yml` - 自动发布
- ✅ 包名已更新为 `davybot-market-cli`

## 📍 配置位置

访问以下链接确认配置:

```
GitHub Environments:
https://github.com/geluzhiwei1/davybot-market-cli/settings/environments
```

**应该看到**:
1. **pypi** 环境
   - Environment secrets: `PYPI_API_TOKEN`
   - Environment URL: https://pypi.org/p/davybot-market-cli

2. **testpypi** 环境
   - Environment secrets: `TEST_PYPI_API_TOKEN`
   - Environment URL: https://test.pypi.org/p/davybot-market-cli

## 🔍 验证 Secrets

### 方法 1: 通过 GitHub UI

1. 访问 Environments 页面
2. 点击 `pypi` 环境
3. 确认看到 `PYPI_API_TOKEN` secret (值是隐藏的)
4. 返回并点击 `testpypi` 环境
5. 确认看到 `TEST_PYPI_API_TOKEN` secret

### 方法 2: 通过工作流日志

1. 访问 GitHub Actions 页面
2. 查看 "Publish to PyPI" 工作流
3. 如果 secret 配置正确,不会看到 "secret not found" 错误
4. 如果失败,检查日志中的具体错误信息

## 🚀 当前状态

### 已推送的标签
```
Tag: v0.1.0
Status: Pushed to remote
Trigger: Auto-publish workflow
```

### 预期流程

1. **CI Workflow** ✅
   - Black, Ruff, MyPy 检查
   - 多平台测试
   - 构建包

2. **Publish Workflow** 🔄
   - 发布到 TestPyPI (使用 `TEST_PYPI_API_TOKEN`)
   - 发布到 PyPI (使用 `PYPI_API_TOKEN`)
   - 创建 GitHub Release

## 📊 监控链接

### 实时监控
```
Actions Dashboard:
https://github.com/geluzhiwei1/davybot-market-cli/actions

CI Workflow:
https://github.com/geluzhiwei1/davybot-market-cli/actions/workflows/ci.yml

Publish Workflow:
https://github.com/geluzhiwei1/davybot-market-cli/actions/workflows/publish.yml
```

### 查看最新运行
```
https://github.com/geluzhiwei1/davybot-market-cli/actions/workflows/publish.yml?query=branch%3Amain
```

## ✅ 成功标志

当配置正确且发布成功时,你将看到:

1. **CI Workflow**: ✅ 绿色对勾
   - All checks passed
   - Build successful
   - Tests passed

2. **Publish Workflow**: ✅ 绿色对勾
   - Published to TestPyPI
   - Published to PyPI
   - GitHub Release created

3. **PyPI 页面可访问**
   ```
   https://pypi.org/pypi/davybot-market-cli/
   ```

4. **可以安装包**
   ```bash
   pip install davybot-market-cli==0.1.0
   ```

## ❌ 如果失败

### 常见错误和解决方案

**错误 1: "Secret not found"**
```
解决方案:
1. 检查 secret 名称是否完全匹配:
   - PYPI_API_TOKEN (不是 PYPI_TOKEN 或 API_TOKEN)
   - TEST_PYPI_API_TOKEN (不是 TEST_TOKEN)
2. 确认 secret 在正确的 environment 中
3. 重新添加 secret
```

**错误 2: "403 Forbidden from PyPI"**
```
解决方案:
1. 检查 token 是否正确
2. 确认 token scope 是 "Entire account"
3. 验证 token 未过期
4. 重新生成 token
```

**错误 3: "Project already exists"**
```
解决方案:
1. 检查 PyPI 上包名是否已被占用
2. 访问: https://pypi.org/pypi/davybot-market-cli/
3. 如果存在,需要修改包名或联系原作者
```

**错误 4: "Invalid package name"**
```
解决方案:
1. 检查 pyproject.toml 中的包名
2. 确认与 GitHub Environment URL 一致
3. 包名应该是: davybot-market-cli
```

## 🔄 重试发布

如果需要重新触发发布:

```bash
# 删除本地标签
git tag -d v0.1.0

# 删除远程标签
git push origin :refs/tags/v0.1.0

# 重新创建标签
git tag -a v0.1.0 -m "Release v0.1.0"

# 推送标签
git push origin v0.1.0
```

## 📝 配置检查清单

使用此清单确认所有配置正确:

- [ ] PyPI 账号已注册
- [ ] TestPyPI 账号已注册
- [ ] PyPI API token 已创建
- [ ] TestPyPI API token 已创建
- [ ] GitHub `pypi` environment 已创建
- [ ] GitHub `testpypi` environment 已创建
- [ ] `PYPI_API_TOKEN` secret 已添加到 `pypi` 环境
- [ ] `TEST_PYPI_API_TOKEN` secret 已添加到 `testpypi` 环境
- [ ] 标签 v0.1.0 已推送
- [ ] CI workflow 已通过
- [ ] Publish workflow 正在运行

## 📞 获取帮助

如果遇到问题:

1. **查看详细日志**: 点击失败的工作流查看完整错误信息
2. **参考文档**: `docs/PYPI_SETUP.md`
3. **运行本地检查**: `./scripts/check-release-status.sh`
4. **查看发布摘要**: `docs/RELEASE_v0.1.0.md`

## 🎯 下一步

一旦发布成功:

1. ✅ 验证 TestPyPI 安装
2. ✅ 验证 PyPI 安装
3. ✅ 测试 CLI 命令
4. ✅ 测试 SDK 导入
5. ✅ 分享发布链接
6. ✅ 更新 README 徽章

---

**配置状态**: ✅ Complete
**发布状态**: 🔄 In Progress
**最后更新**: 2026-02-07
