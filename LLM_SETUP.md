# 🔧 Olympus System - LLM 配置指南

**更新日期**: 2026-02-25  
**版本**: v1.1.0

---

## 📋 目录

1. [快速开始](#快速开始)
2. [配置 API Key](#配置 api-key)
3. [测试连接](#测试连接)
4. [故障排除](#故障排除)

---

## 快速开始

### 1. 安装依赖

```bash
cd /Volumes/Soul/Proteus_Genesis
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
# 复制示例配置
cp .env.example .env

# 编辑 .env 文件
nano .env
```

### 3. 选择 LLM 提供商

在 `.env` 文件中设置：

```bash
# 选项 1: OpenAI (GPT-4)
OLYMPUS_LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-key-here

# 选项 2: Anthropic (Claude)
OLYMPUS_LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-your-key-here

# 选项 3: 模拟模式（无需 API key）
OLYMPUS_LLM_PROVIDER=mock
```

---

## 配置 API Key

### OpenAI

1. 访问 https://platform.openai.com/api-keys
2. 创建新的 API Key
3. 复制到 `.env` 文件：
   ```bash
   OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx
   ```

### Anthropic

1. 访问 https://console.anthropic.com/settings/keys
2. 创建新的 API Key
3. 复制到 `.env` 文件：
   ```bash
   ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxx
   ```

---

## 测试连接

### 测试 LLM 集成

```bash
cd /Volumes/Soul/Proteus_Genesis
python3 core/llm_integration.py
```

**预期输出**:

```
🧠 LLM Client 已初始化
   提供商：openai
   API Key: 已配置
   ✅ OpenAI 客户端已初始化

📋 任务：为一个小型创业团队生成一周的社交媒体内容计划

✅ 分解为 5 个子任务:
   1. 调研目标受众和行业趋势 (athena, 45min) [🤖 LLM]
   2. 制定内容主题和发布日历 (apollo, 30min) [🤖 LLM]
   3. 撰写每日文案草稿 (apollo, 90min) [🤖 LLM]
   4. 设计视觉风格和配图建议 (hephaestus, 60min) [🤖 LLM]
   5. 质量审核与优化 (themis, 30min) [🤖 LLM]

✅ 测试完成
```

### 测试完整系统

```bash
python3 demo_evolution.py
```

---

## 故障排除

### 问题 1: API Key 无效

**错误**: `401 Unauthorized`

**解决**:
1. 检查 `.env` 文件是否存在
2. 确认 API Key 复制正确（无空格）
3. 确认账户有余额

### 问题 2: 包未安装

**错误**: `ModuleNotFoundError: No module named 'openai'`

**解决**:
```bash
pip install openai anthropic
```

### 问题 3: 网络问题

**错误**: `Connection timeout`

**解决**:
1. 检查网络连接
2. 使用代理（如果需要）
3. 临时切换到模拟模式：
   ```bash
   OLYMPUS_LLM_PROVIDER=mock
   ```

### 问题 4: 自动 Fallback

如果 LLM 调用失败，系统会自动 Fallback 到模拟模式：

```
⚠️  LLM 调用失败：API error
🔄 Fallback 到模拟模式
```

这是正常行为，不影响系统运行。

---

## 安全提示

### ✅ 正确做法

1. **使用环境变量**
   ```bash
   export OPENAI_API_KEY=sk-xxx
   ```

2. **使用 .env 文件**
   ```bash
   cp .env.example .env
   # 编辑 .env（已在 .gitignore 中）
   ```

3. **限制权限**
   ```bash
   chmod 600 .env
   ```

### ❌ 错误做法

1. **不要硬编码在代码中**
   ```python
   # ❌ 错误
   api_key = "sk-xxxxx"
   
   # ✅ 正确
   api_key = os.getenv("OPENAI_API_KEY")
   ```

2. **不要提交 .env 到 Git**
   ```bash
   # .env 已在 .gitignore 中
   git add .env  # ❌ 不要这样做
   ```

3. **不要分享 API Key**
   - 不要发布到公开论坛
   - 不要上传到 GitHub
   - 定期轮换 Key

---

## 费用说明

### OpenAI 定价

| 模型 | 输入 | 输出 |
|------|------|------|
| GPT-4o | $0.005/1K tokens | $0.015/1K tokens |
| GPT-4 | $0.03/1K tokens | $0.06/1K tokens |

**示例**: 一次任务分解约 500 tokens，成本约 $0.01

### Anthropic 定价

| 模型 | 输入 | 输出 |
|------|------|------|
| Claude 3.5 Sonnet | $0.003/1K tokens | $0.015/1K tokens |
| Claude 3 Opus | $0.015/1K tokens | $0.075/1K tokens |

**建议**: 开发测试使用模拟模式，生产环境使用真实 API

---

## 性能优化

### 1. 缓存结果

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def decompose_task_cached(task_desc: str):
    return llm.decompose_task(task_desc)
```

### 2. 批量处理

```python
# 批量分解多个任务
tasks = ["任务 1", "任务 2", "任务 3"]
results = [llm.decompose_task(t) for t in tasks]
```

### 3. 超时设置

```python
import openai

client = openai.OpenAI(
    api_key=api_key,
    timeout=30.0  # 30 秒超时
)
```

---

## 下一步

配置完成后，可以：

1. ✅ 运行真实任务测试
2. ✅ 查看 LLM 分解效果
3. ✅ 对比模拟 vs 真实结果
4. ✅ 调整提示词优化输出

---

**需要帮助？**

- 查看文档：`README.md`
- 提交 Issue: https://github.com/Skywalkerhm/proteus-system/issues
- 讨论区：https://github.com/Skywalkerhm/proteus-system/discussions

---

*Last updated: 2026-02-25*
