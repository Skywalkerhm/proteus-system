# 🤖 Proteus System LLM 集成指南

> **完整支持真实 LLM API 调用** - 任务分解 + 任务执行全流程

---

## 📋 功能概览

Proteus System 已完整支持真实 LLM 集成：

| 功能模块 | 模拟模式 | 真实 LLM | 状态 |
|---------|---------|---------|------|
| **任务分解** | ✅ 关键词匹配 | ✅ OpenAI/Anthropic | ✅ 完成 |
| **任务执行** | ✅ 模板生成 | ✅ OpenAI/Anthropic | ✅ 完成 |
| **自动 Fallback** | - | ✅ API 失败降级 | ✅ 完成 |

---

## 🚀 快速开始

### 方式 1: 使用 OpenAI

```bash
# 配置环境变量
export OLYMPUS_LLM_PROVIDER=openai
export OPENAI_API_KEY=sk-your-api-key-here

# 运行演示
python3 demo_evolution.py
```

**预期输出**：
```
🧠 OpenAI Client 已初始化 (模型：gpt-4o)
📋 任务：为一个小型创业团队生成一周的社交媒体内容计划

🤖 使用 LLM 分解任务...
✅ 分解为 5 个子任务:
   1. 调研目标受众和行业趋势 (athena, 45min) [🤖 LLM]
   2. 制定内容主题和发布日历 (apollo, 30min) [🤖 LLM]
   3. 撰写每日文案草稿 (apollo, 90min) [🤖 LLM]
   4. 设计视觉风格和配图建议 (hephaestus, 60min) [🤖 LLM]
   5. 质量审核与优化 (themis, 30min) [🤖 LLM]

🎤 [Hub] 开始执行任务...
🤖 [athena] 执行：调研目标受众... [🤖 LLM]
```

### 方式 2: 使用 Anthropic

```bash
export OLYMPUS_LLM_PROVIDER=anthropic
export ANTHROPIC_API_KEY=sk-ant-your-api-key-here

python3 demo_evolution.py
```

### 方式 3: 模拟模式（无需 API Key）

```bash
export OLYMPUS_LLM_PROVIDER=mock
# 或不设置任何环境变量

python3 demo_evolution.py
```

---

## 🔧 配置选项

### 环境变量

| 变量名 | 说明 | 示例值 |
|--------|------|--------|
| `OLYMPUS_LLM_PROVIDER` | LLM 提供商 | `openai` / `anthropic` / `mock` |
| `OPENAI_API_KEY` | OpenAI API Key | `sk-...` |
| `ANTHROPIC_API_KEY` | Anthropic API Key | `sk-ant-...` |

### .env 文件配置

```bash
# .env 文件

# 选择 LLM 提供商
OLYMPUS_LLM_PROVIDER=openai

# OpenAI 配置
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx

# Anthropic 配置（如果选择 anthropic）
# ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxx
```

---

## 📊 LLM 调用流程

### 1. 任务分解阶段

```python
# hub.py
subtasks = self.llm.decompose_task(task_desc, context)

# llm_integration.py
if self.provider in ["openai", "anthropic"] and self.api_key:
    return self._llm_decompose(task_desc, context)  # 真实 LLM
else:
    return self._mock_decompose(task_desc)  # 模拟模式
```

**LLM 提示词示例**：
```
系统：你是一个专业的任务规划专家。请将复杂任务分解为可执行的子任务。

用户：请分解以下任务：
任务：为一个小型创业团队生成一周的社交媒体内容计划

请返回子任务列表（JSON 数组格式）：
```

**LLM 返回**：
```json
[
  {
    "desc": "调研目标受众和行业趋势",
    "required_skills": ["research", "analysis"],
    "agent_type": "athena",
    "estimated_time": 45
  },
  ...
]
```

### 2. 任务执行阶段

```python
# hub.py
result = self.llm.execute_agent_task(
    agent_type,
    subtask["desc"],
    context=self.memory.working.get_context()
)

# llm_integration.py
if self.provider in ["openai", "anthropic"] and self.api_key:
    return self._llm_execute(agent_type, task_desc, context)  # 真实 LLM
else:
    return self._mock_execute(agent_type, task_desc)  # 模拟模式
```

**LLM 提示词示例**：
```
系统：你是一个专业的 athena Agent（研究专家）。
请根据任务描述完成工作，并返回结构化的结果。

返回格式（JSON）：
{
    "success": true/false,
    "output": "任务输出的详细描述",
    "execution_time": 执行时间（分钟）,
    "artifacts": ["产出的文件列表"],
    "logs": ["执行日志"],
    "confidence": 置信度 (0.0-1.0)
}

用户：请完成以下任务：
任务描述：调研目标受众和行业趋势
```

**LLM 返回**：
```json
{
    "success": true,
    "output": "完成目标受众调研，识别出 3 个主要用户群体...",
    "execution_time": 45,
    "artifacts": ["调研报告.md", "用户画像.xlsx", "数据分析.csv"],
    "logs": ["收集行业数据...", "分析用户行为...", "生成报告..."],
    "confidence": 0.92
}
```

---

## 🧪 测试验证

### 测试 1: 检查 LLM 连接

```bash
python3 -c "
from core.llm_integration import LLMClient

llm = LLMClient()
print(f'提供商：{llm.provider}')
print(f'API Key: {\"已配置\" if llm.api_key else \"未配置\"}')
print(f'OpenAI 客户端：{\"✅\" if llm.openai_client else \"❌\"}')
print(f'Anthropic 客户端：{\"✅\" if llm.anthropic_client else \"❌\"}')
"
```

### 测试 2: 测试任务分解

```bash
python3 -c "
from core.llm_integration import LLMClient

llm = LLMClient()
task = '为 AI 创业公司写一份商业计划书'
subtasks = llm.decompose_task(task)

print(f'分解为 {len(subtasks)} 个子任务:')
for i, st in enumerate(subtasks, 1):
    llm_tag = '🤖 LLM' if st.get('llm_generated') else '💾 Mock'
    print(f'{i}. {st[\"desc\"]} ({st[\"agent_type\"]}) [{llm_tag}]')
"
```

### 测试 3: 测试任务执行

```bash
python3 -c "
from core.llm_integration import LLMClient

llm = LLMClient()
result = llm.execute_agent_task(
    'athena',
    '调研中国新能源汽车市场',
    context={'industry': 'EV', 'region': 'China'}
)

print(f'执行结果:')
print(f'  成功：{result[\"success\"]}')
print(f'  输出：{result[\"output\"][:100]}...')
print(f'  时间：{result[\"execution_time\"]}分钟')
print(f'  产物：{result[\"artifacts\"]}')
print(f'  置信度：{result[\"confidence\"]}')
"
```

---

## 📈 性能对比

| 指标 | 模拟模式 | 真实 LLM |
|------|---------|---------|
| **任务分解质量** | ⭐⭐⭐ 固定模板 | ⭐⭐⭐⭐⭐ 智能适配 |
| **任务执行质量** | ⭐⭐ 通用回复 | ⭐⭐⭐⭐⭐ 专业输出 |
| **响应速度** | ⚡ <1 秒 | 🐢 5-30 秒 |
| **成本** | 💰 免费 | 💰💰 API 费用 |
| **适用场景** | 开发测试 | 生产环境 |

---

## 🔒 安全与成本控制

### API Key 安全

```bash
# ✅ 正确：使用环境变量
export OPENAI_API_KEY="sk-..."

# ✅ 正确：使用 .env 文件（已在 .gitignore 中）
cp .env.example .env
nano .env

# ❌ 错误：硬编码在代码中
api_key = "sk-xxxxx"  # 不要这样做！
```

### 成本估算

**OpenAI GPT-4o 定价**：
- 输入：$0.005 / 1K tokens
- 输出：$0.015 / 1K tokens

**示例任务成本**：
```
任务分解：~500 tokens → $0.01
任务执行：~1000 tokens → $0.02
总成本：~$0.03 / 任务
```

**月度预算建议**：
- 开发测试：$5-10/月
- 小规模使用：$30-50/月
- 生产环境：$100+/月

### 限流保护

```python
# 自动重试机制
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential())
def call_llm():
    return client.chat.completions.create(...)
```

---

## ⚠️ 故障排除

### 问题 1: LLM 初始化失败

```
⚠️  LLM 调用失败：OpenAI API key not found
🔄 Fallback 到模拟模式
```

**解决**：
```bash
# 检查环境变量
echo $OPENAI_API_KEY

# 如果为空，设置它
export OPENAI_API_KEY="sk-..."

# 或检查 .env 文件
cat .env
```

### 问题 2: API 调用超时

```
⚠️  LLM 调用失败：Connection timeout
🔄 Fallback 到模拟模式
```

**解决**：
```bash
# 检查网络
curl https://api.openai.com

# 使用代理（如果需要）
export HTTP_PROXY="http://proxy:port"
export HTTPS_PROXY="http://proxy:port"

# 或切换到模拟模式
export OLYMPUS_LLM_PROVIDER=mock
```

### 问题 3: JSON 解析失败

```
⚠️  LLM 返回格式错误
🔄 Fallback 到模拟模式
```

**解决**：
- 系统已自动处理（提取 JSON、修复格式）
- 如频繁发生，检查 LLM 模型版本
- 或降低 temperature 参数

---

## 🎯 最佳实践

### 1. 开发阶段

```bash
# 使用模拟模式（快速迭代）
export OLYMPUS_LLM_PROVIDER=mock

# 快速测试
python3 demo.py
```

### 2. 测试阶段

```bash
# 使用真实 LLM（小流量）
export OLYMPUS_LLM_PROVIDER=openai
export OPENAI_API_KEY="sk-..."

# 验证功能
python3 demo_evolution.py
```

### 3. 生产环境

```bash
# 配置完整环境变量
export OLYMPUS_LLM_PROVIDER=openai
export OPENAI_API_KEY="sk-..."
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# 运行主程序
python3 main.py
```

### 4. 日志记录

```python
# 记录 LLM 调用
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ProteusLLM")

logger.info(f"LLM Provider: {provider}")
logger.info(f"Task: {task_desc[:50]}...")
logger.info(f"Result: {result['success']}")
```

---

## 📚 相关文档

- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - 独立部署指南
- [LLM_SETUP.md](LLM_SETUP.md) - LLM 配置指南
- [README.md](README.md) - 项目说明
- [examples/](examples/) - 使用示例

---

## 🙋 FAQ

### Q: 必须配置 API Key 吗？
**A**: 不必须。系统支持模拟模式，无需 API Key 即可运行。但真实 LLM 能提供更高质量的输出。

### Q: 支持哪些 LLM 提供商？
**A**: 目前支持 OpenAI (GPT-4/GPT-4o) 和 Anthropic (Claude 3.5)。未来可能支持更多。

### Q: 可以在本地运行 LLM 吗？
**A**: 当前版本不支持。如需本地 LLM，可考虑 Ollama + OpenAI 兼容 API。

### Q: API 调用失败怎么办？
**A**: 系统会自动 Fallback 到模拟模式，确保程序不会崩溃。

### Q: 如何查看 LLM 调用日志？
**A**: 日志保存在 `logs/llm_calls/` 目录，包含请求和响应详情。

---

*Last updated: 2026-02-25*

> **提示**: 首次使用建议从模拟模式开始，熟悉系统后再配置真实 API。
