# 🔧 Proteus System 独立部署指南

> **重要**: 本指南适用于不依赖 OpenClaw 的独立部署场景

---

## 📋 部署前检查清单

### 1. 系统要求

| 项目 | 要求 | 检查命令 |
|------|------|---------|
| Python | 3.9+ | `python3 --version` |
| 内存 | ≥2GB | - |
| 存储 | ≥500MB | - |
| 网络 | 需要（LLM API） | - |

### 2. 安全检查

运行自动检查脚本：

```bash
cd proteus-system
python3 scripts/deployment_check.py
```

**检查项目**：
- ✅ 隐私信息（路径、API key、个人信息）
- ✅ 环境配置
- ✅ 依赖配置
- ✅ 演示数据
- ✅ 文档完整性
- ✅ LLM fallback 机制

---

## 🚀 快速部署

### 步骤 1: 克隆仓库

```bash
git clone https://github.com/Skywalkerhm/proteus-system.git
cd proteus-system
```

### 步骤 2: 安装依赖

```bash
pip3 install -r requirements.txt
```

### 步骤 3: 配置环境变量

```bash
# 复制示例配置
cp .env.example .env

# 编辑 .env 文件
nano .env
```

**配置选项**：

```bash
# 选项 1: 使用 OpenAI
OLYMPUS_LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-api-key-here

# 选项 2: 使用 Anthropic
OLYMPUS_LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-your-api-key-here

# 选项 3: 模拟模式（无需 API key）
OLYMPUS_LLM_PROVIDER=mock
```

### 步骤 4: 运行演示

```bash
# 运行 Evolution 演示
python3 demo_evolution.py

# 运行简单演示
python3 demo.py
```

---

## 🔍 独立部署关键问题

### 问题 1: 路径依赖

**❌ 错误示例**：
```python
# 硬编码路径
memory_path = Path("/absolute/path/to/Proteus_Genesis/memory")
```

**✅ 正确做法**：
```python
# 使用相对路径
memory_path = Path(__file__).parent.parent / "memory"

# 或使用环境变量
memory_path = Path(os.getenv("PROTEUS_MEMORY_PATH", "./memory"))
```

**当前状态**: ✅ 已修复
- 所有路径使用相对路径
- 支持环境变量覆盖

---

### 问题 2: API Key 安全

**❌ 错误示例**：
```python
# 硬编码 API key
api_key = "sk-xxxxxxxxxxxxx"
```

**✅ 正确做法**：
```python
# 从环境变量获取
api_key = os.getenv("OPENAI_API_KEY")
```

**当前状态**: ✅ 已实现
- API key 通过环境变量获取
- .env 文件在 .gitignore 中
- 支持无 API key 的模拟模式

---

### 问题 3: 记忆系统初始化

**❌ 错误示例**：
```python
# 假设记忆文件已存在
with open("memory/agents/echo.json") as f:
    data = json.load(f)
```

**✅ 正确做法**：
```python
# 检查并创建目录
memory_path.mkdir(parents=True, exist_ok=True)

# 检查文件是否存在
if not agent_file.exists():
    # 创建默认 Agent
    create_default_agent()
```

**当前状态**: ✅ 已实现
- 自动创建记忆目录
- 支持 Agent 文件缺失时降级

---

### 问题 4: LLM Fallback

**场景**: 用户没有配置 API key

**解决方案**：
```python
# 自动降级到模拟模式
provider = os.getenv("OLYMPUS_LLM_PROVIDER", "mock")

if provider == "mock" or not api_key:
    # 使用模拟模式
    return mock_decompose(task)
```

**当前状态**: ✅ 已实现
- 默认使用模拟模式
- API 调用失败自动 fallback
- 明确提示用户当前模式

---

### 问题 5: 日志和进化数据

**风险**: 日志可能包含敏感信息

**解决方案**：
```python
# 仅记录必要信息
log_entry = {
    "event": "task_complete",
    "task_id": task_id,  # UUID，不含敏感信息
    "success": success,
    "timestamp": datetime.now().isoformat()
    # ❌ 不记录：用户输入、API 响应、个人数据
}
```

**当前状态**: ✅ 已实现
- 日志仅记录任务元数据
- 不包含用户输入内容
- 进化数据仅统计指标

---

## 📁 目录结构

```
proteus-system/
├── core/                  # 核心模块
│   ├── memory.py         # 三层记忆系统
│   ├── hub.py            # 中央调度器
│   ├── llm_integration.py # LLM 集成
│   ├── evolution.py      # 进化引擎
│   └── adaptive.py       # 自适应调整
│
├── memory/               # 记忆数据（运行时生成）
│   ├── semantic/
│   │   ├── agents/      # Agent 画像
│   │   ├── patterns/    # 任务模式
│   │   └── rules/       # 协作规则
│   ├── episodic/        # 任务记录
│   └── working/         # 临时状态
│
├── scripts/             # 工具脚本
│   └── deployment_check.py  # 部署检查
│
├── examples/            # 示例代码
├── tests/              # 测试用例
├── logs/               # 日志目录（运行时生成）
│
├── .env.example        # 环境变量示例
├── requirements.txt    # 依赖清单
├── README.md          # 使用文档
└── demo_evolution.py  # 演示脚本
```

---

## 🔒 安全最佳实践

### 1. 环境变量管理

```bash
# ✅ 正确：使用 .env 文件
cp .env.example .env
nano .env  # 编辑后保存

# ✅ 正确：设置文件权限
chmod 600 .env

# ❌ 错误：提交 .env 到 Git
git add .env  # 不要这样做！
```

### 2. API Key 保护

```bash
# ✅ 正确：使用环境变量
export OPENAI_API_KEY="sk-..."
python3 demo.py

# ❌ 错误：命令行明文
python3 demo.py --api-key "sk-..."  # 会留在历史记录中
```

### 3. 日志审查

```bash
# 定期检查日志
cat logs/evolution/evolution_log.jsonl | head

# 清理旧日志
rm logs/evolution/*.jsonl
```

---

## 🧪 测试验证

### 测试 1: 模拟模式运行

```bash
# 不配置 API key
unset OPENAI_API_KEY
unset ANTHROPIC_API_KEY
export OLYMPUS_LLM_PROVIDER=mock

# 运行演示
python3 demo_evolution.py

# 预期输出：
# 🧠 LLM Client 已初始化（模拟模式）
# ✅ 任务完成
```

### 测试 2: 真实 API 调用

```bash
# 配置 API key
export OPENAI_API_KEY="sk-..."
export OLYMPUS_LLM_PROVIDER=openai

# 运行演示
python3 demo_evolution.py

# 预期输出：
# 🧠 OpenAI Client 已初始化
# 🤖 使用 LLM 分解任务
# ✅ 任务完成
```

### 测试 3: 记忆系统

```bash
python3 -c "
from core.memory import MemorySystem
from pathlib import Path

m = MemorySystem(Path('./memory'))
print('✅ 记忆系统初始化成功')
print(f'Agent 数量：{len(list(m.semantic.agents_path.glob(\"*.json\")))}')
"
```

---

## ⚠️ 已知限制

### 1. LLM API 依赖

**限制**: 真实任务分解需要 LLM API

**解决方案**:
- 使用模拟模式（基于关键词匹配）
- 配置本地 LLM（如 Ollama）
- 使用免费额度（OpenAI 新用户有 $5 额度）

### 2. 中文支持

**限制**: 部分 Agent 名称和描述为中文

**解决方案**:
- 已提供英文版 README
- Agent 画像支持多语言
- 可自定义 Agent 配置

### 3. 跨平台兼容

**测试平台**:
- ✅ macOS (ARM/Intel)
- ✅ Linux (Ubuntu 20.04+)
- ⚠️ Windows (未完全测试)

---

## 🛠️ 故障排除

### 问题 1: 导入错误

```
ModuleNotFoundError: No module named 'core'
```

**解决**:
```bash
# 使用正确的方式运行
python3 demo_evolution.py

# 或添加路径
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### 问题 2: 权限错误

```
PermissionError: [Errno 13] Permission denied: 'memory'
```

**解决**:
```bash
# 创建目录并设置权限
mkdir -p memory/semantic/agents
chmod -R 755 memory/
```

### 问题 3: API 调用失败

```
openai.APIError: Connection timeout
```

**解决**:
```bash
# 检查网络
curl https://api.openai.com

# 使用模拟模式
export OLYMPUS_LLM_PROVIDER=mock
```

---

## 📞 获取帮助

- **文档**: README.md, LLM_SETUP.md
- **Issue**: https://github.com/Skywalkerhm/proteus-system/issues
- **讨论**: https://github.com/Skywalkerhm/proteus-system/discussions

---

## ✅ 部署完成检查清单

部署完成后，请确认：

- [ ] 所有依赖已安装
- [ ] .env 文件已配置
- [ ] 演示脚本运行成功
- [ ] 部署检查脚本通过
- [ ] 无隐私信息泄露
- [ ] 日志目录可写
- [ ] API key 已妥善保管

---

*Last updated: 2026-02-25*

> **提示**: 首次部署建议使用模拟模式，熟悉系统后再配置真实 API。
