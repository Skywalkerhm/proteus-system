# Contributing to Proteus System

首先，感谢你愿意为 Proteus System 贡献！🎉

## 📋 目录

- [行为准则](#行为准则)
- [如何贡献](#如何贡献)
- [开发环境设置](#开发环境设置)
- [提交指南](#提交指南)
- [测试](#测试)

---

## 行为准则

本项目采用 [Contributor Covenant](https://www.contributor-covenant.org/) 行为准则。请尊重所有贡献者，营造友好的协作环境。

---

## 如何贡献

### 1. 报告 Bug

如果你发现 Bug，请创建 Issue 并包含：
- 清晰的标题和描述
- 复现步骤
- 预期行为和实际行为
- 环境信息（Python 版本、操作系统等）

### 2. 提出新功能

新功能建议请创建 Issue 并说明：
- 功能描述
- 使用场景
- 预期效果

### 3. 提交代码

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 开发环境设置

### 1. 克隆仓库

```bash
git clone https://github.com/yourusername/proteus-system.git
cd proteus-system
```

### 2. 创建虚拟环境

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # 开发依赖
```

### 4. 运行测试

```bash
pytest tests/ -v
```

---

## 提交指南

### Git Commit 规范

我们遵循 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Type 类型**:
- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式（不影响代码运行）
- `refactor`: 重构（既不是新功能也不是 Bug 修复）
- `perf`: 性能优化
- `test`: 测试相关
- `chore`: 构建过程或辅助工具变动

**示例**:
```bash
git commit -m "feat(hub): 添加自适应恢复机制"
git commit -m "fix(memory): 修复场景记忆保存失败问题"
git commit -m "docs(readme): 更新快速开始指南"
```

### 代码规范

- 遵循 PEP 8 代码风格
- 使用 Black 格式化代码
- 添加必要的类型注解
- 编写清晰的文档字符串

```bash
# 代码格式化
black .

# 代码检查
flake8 .

# 类型检查
mypy .
```

---

## 测试

### 运行所有测试

```bash
pytest tests/ -v
```

### 运行特定测试

```bash
pytest tests/test_hub.py -v
pytest tests/test_memory.py -v
pytest tests/test_complex_collaboration.py -v
```

### 测试覆盖率

```bash
pytest --cov=core tests/
```

---

## 代码审查清单

提交 PR 前请确保：

- [ ] 代码通过所有测试
- [ ] 代码已格式化（Black）
- [ ] 添加了必要的测试
- [ ] 更新了文档（如适用）
- [ ] Commit 信息符合规范

---

## 问题？

有任何问题欢迎在 Issue 中提问，或联系项目维护者。

再次感谢你的贡献！🚀
