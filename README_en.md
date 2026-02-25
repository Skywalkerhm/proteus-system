# 🧬 Olympus System

> **Self-Collaborating, Adaptive, Evolving Agent Management System**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Version: 1.1.0](https://img.shields.io/badge/version-1.1.0-green.svg)](https://github.com/Skywalkerhm/proteus-system)

---

## 📖 Introduction

**Olympus System** is a task-driven agent management system that can:

- 🎯 **Task-Driven** - Accept complex tasks, automatically decompose, plan, and assign to suitable Agents
- 🤝 **Self-Collaborating** - Agents collaborate effectively based on rules and context, dynamically adjusting strategies
- 🧬 **Continuously Evolving** - Both the system and individual Agents iteratively learn through task execution feedback, becoming smarter over time

Inspired by **Proteus** from Greek mythology, the sea god who could change his form at will while always maintaining his essence—symbolizing the system's **adaptability** and **continuous evolution**.

---

## 🚀 Core Features

### 1. Hub-Spoke Architecture

```
                    ┌─────────────┐
                    │     Hub     │
                    │ (Scheduler) │
                    └──────┬──────┘
                           │
         ┌─────────────────┼─────────────────┐
         │                 │                 │
    ┌────▼────┐      ┌────▼────┐      ┌────▼────┐
    │ Spoke 1 │      │ Spoke 2 │      │ Spoke 3 │
    │(Agent)  │      │(Agent)  │      │(Agent)  │
    └─────────┘      └─────────┘      └─────────┘
```

- **Hub**: Central scheduler, responsible for task reception, decomposition, assignment, and result integration
- **Spoke**: Specialized Agents, each focusing on their specific domain

### 2. Three-Layer Memory Framework

| Memory Type | Purpose | Lifecycle |
|------------|---------|-----------|
| **Working Memory** | Current task context, Agent communication | During task |
| **Episodic Memory** | Complete task execution trajectory, decision points | Permanent |
| **Semantic Memory** | Agent profiles, task patterns, rule base | Continuously evolving |

### 3. Dynamic Work Groups (Claw)

For complex tasks, the Hub doesn't assign to a single Agent directly, but instead:

1. Analyzes required skills
2. Matches best candidates from Agent profile database
3. Forms a temporary work group (Claw)
4. Assigns a lead Agent for coordination

### 4. Dual-Track Evolution Mechanism

**Individual Evolution**:
- Updates Agent capability profile after each task
- Records success rate, average execution time, collaboration preferences
- Automatically discovers new skills

**Collective Evolution**:
- Analyzes success patterns every 5 tasks
- Discovers new task templates (SOP)
- Optimizes collaboration rules

---

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/Skywalkerhm/proteus-system.git
cd proteus-system

# Install dependencies
pip install -r requirements.txt

# Run demo
python demo_evolution.py
```

---

## 🎯 Quick Start

### Example 1: Simple Task

```python
from core.hub import OlympusHub

# Initialize Hub
hub = OlympusHub()

# Receive task
task_id = hub.receive_task(
    "Generate a week-long social media content plan for a startup",
    user_id="demo_user",
    priority="normal"
)

# Parse task (auto-matches patterns or LLM decomposition)
hub.parse_task(task_id)

# Form Claw (dynamic team)
claw = hub.form_claw(task_id)

# Execute task
hub.execute_task(task_id)

# Deliver task
result = hub.deliver_task(
    task_id,
    result="Generated 7-day social media content plan",
    feedback="Excellent, ready to use"
)
```

### Example 2: Complex Task

```python
# Complex task: Complete website development
task_id = hub.receive_task(
    "Develop a complete website for an AI startup, including frontend, backend, database, and deployment",
    priority="high"
)

# Automatically decomposed into multiple subtasks
# → Frontend development (Hephaestus Agent)
# → Backend API (Hephaestus Agent)
# → Database design (Daedalus Agent)
# → Deployment configuration (Hephaestus Agent)
# → Quality review (Themis Agent)

hub.parse_task(task_id)
hub.form_claw(task_id)
hub.execute_task(task_id)
hub.deliver_task(task_id, "Website development complete", "Satisfied")
```

---

## 🏛️ Olympus Agents (Greek Mythology)

| Agent | Mythology Identity | Role | Emoji |
|-------|-------------------|------|-------|
| **Echo** | Echo Goddess | Hub - Central Scheduler | 🎤 |
| **Hermes** | Messenger of Gods | CTO - Technical Decision | 🚀 |
| **Aphrodite** | Goddess of Love & Beauty | CMO - Marketing Strategy | 💫 |
| **Hestia** | Goddess of Home & Hearth | Butler - Task Management | 🏠 |
| **Hephaestus** | God of Fire & Forge | Full-Stack Engineer | 🔨 |
| **Muse** | Muse Goddess | Science Writer - Inspiration | ✨ |
| **Athena** | Goddess of Wisdom | Research Expert | 🦉 |
| **Apollo** | God of Art & Light | Content Expert | ☀️ |
| **Daedalus** | Legendary Craftsman | Code Expert - Architecture | 🏛️ |
| **Themis** | Goddess of Justice | Review Expert - Quality | ⚖️ |

---

## 🔧 LLM Configuration

### Supported Providers

- **OpenAI** (GPT-4, GPT-4o)
- **Anthropic** (Claude 3.5 Sonnet, Claude 3 Opus)
- **Mock Mode** (default, no API key required)

### Setup

```bash
# Copy environment template
cp .env.example .env

# Edit .env file
nano .env

# Configure API key
OLYMPUS_LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-api-key-here
```

### Test Connection

```bash
python core/llm_integration.py
```

**Expected Output**:
```
🧠 LLM Client Initialized
   Provider: openai
   API Key: Configured
   ✅ OpenAI client initialized

✅ Decomposed into 5 subtasks:
   1. Research target audience and industry trends (athena, 45min) [🤖 LLM]
   2. Plan content themes and publishing calendar (apollo, 30min) [🤖 LLM]
   ...
```

📖 **Detailed Guide**: [LLM_SETUP.md](LLM_SETUP.md)

---

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific test
pytest tests/test_complex_collaboration.py -v

# Run demo
python demo_evolution.py
```

---

## 📊 System Architecture

```
proteus-system/
├── core/
│   ├── memory.py           # Three-layer memory system
│   ├── hub.py              # Central scheduler
│   ├── llm_integration.py  # LLM integration (OpenAI/Anthropic)
│   ├── evolution.py        # Evolution engine
│   ├── adaptive.py         # Adaptive adjustment
│   └── agent_registry.py   # Agent registration (Greek mythology)
│
├── memory/
│   ├── working/            # Working memory (temporary)
│   ├── episodic/           # Episodic memory (task records)
│   └── semantic/
│       ├── agents/         # Agent profiles (10 Greek gods)
│       ├── patterns/       # Task patterns
│       └── rules/          # Collaboration rules
│
├── tests/
│   ├── test_complex_collaboration.py
│   └── test_adaptive.py
│
├── examples/
│   └── social_media_plan.py
│
├── logs/
│   ├── tasks/              # Task execution logs
│   └── evolution/          # Evolution logs
│
└── demo_evolution.py       # Demo script
```

---

## 🎓 Use Cases

### 1. Content Creation
- Social media content plans
- Blog post writing
- Marketing copy creation

### 2. Research & Analysis
- Market research reports
- Competitive analysis
- Literature review

### 3. Software Development
- Website development
- API design
- Code review

### 4. Investment Decision
- Quantitative strategy research
- Market analysis
- Risk assessment

---

## 🧬 Evolution Effects

As the system executes more tasks, it becomes:

1. **Agents Get Smarter** - Success rate improves, execution time shortens
2. **Pattern Library Enriches** - Accumulates more task templates and best practices
3. **Rules Optimize** - Collaboration flows smoother, fewer conflicts
4. **System Becomes Easier to Use** - Task decomposition more accurate, Agent matching more precise

**Example Evolution Data** (after 6 tasks):
```
Completed Tasks: 6
Evolution Events: 10
Available Agents: 10
Average Success Rate: 100%

Individual Evolution:
  - Hephaestus: 4 tasks, 100% success rate
  - Athena: 3 tasks, 100% success rate
  - Apollo: 3 tasks, 100% success rate
```

---

## 🔒 Security

### API Key Management

- ✅ API keys obtained via environment variables only
- ✅ No hardcoded credentials in code
- ✅ `.env` file excluded from Git (in `.gitignore`)
- ✅ Automatic fallback to mock mode if no API key

### Best Practices

```bash
# ✅ Correct: Use environment variables
export OPENAI_API_KEY=sk-xxx

# ✅ Correct: Use .env file (already in .gitignore)
cp .env.example .env

# ❌ Wrong: Hardcode in code
api_key = "sk-xxxxx"  # Never do this!
```

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

### Quick Start

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Team

All Agents are named after Greek mythology figures:

- **🎤 Echo** - Central Scheduler (Hub) - Echo Goddess
- **🚀 Hermes** - CTO - Messenger of Gods
- **💫 Aphrodite** - CMO - Goddess of Love & Beauty
- **🏠 Hestia** - Butler - Goddess of Home
- **🔨 Hephaestus** - Full-Stack Engineer - God of Forge
- **✨ Muse** - Science Writer - Muse Goddess
- **🦉 Athena** - Research Expert - Goddess of Wisdom
- **☀️ Apollo** - Content Expert - God of Art
- **🏛️ Daedalus** - Code Expert - Legendary Craftsman
- **⚖️ Themis** - Review Expert - Goddess of Justice

---

## 📞 Contact

- **Project Homepage**: https://github.com/Skywalkerhm/proteus-system
- **Issue Tracker**: https://github.com/Skywalkerhm/proteus-system/issues
- **Discussions**: https://github.com/Skywalkerhm/proteus-system/discussions

---

## 🙏 Acknowledgments

This project is inspired by:
- **Hub-Spoke Architecture** - Classic distributed system design
- **ClawWork** - Dynamic work group collaboration framework
- **Agent_Evolver** - Agent self-evolution theory
- **Hive Mind** - Collective intelligence scheduling system

---

## 📈 Roadmap

### v1.1.0 (Current) ✅
- [x] Greek mythology naming
- [x] Real LLM API integration
- [x] Auto-fallback to mock mode
- [x] Security hardening

### v1.2.0 (Next)
- [ ] Vector database support (Chroma/Qdrant)
- [ ] More professional Agents (design/video/marketing)
- [ ] Multi-task parallel execution
- [ ] Visual dashboard

### v2.0.0 (Future)
- [ ] Multi-user support
- [ ] Plugin system
- [ ] Enterprise features
- [ ] Community contributions

---

*Last updated: 2026-02-25*

> *"True intelligence is not static capability, but the potential for continuous evolution."*

🏛️ **Olympus System - Powered by Greek Mythology & AI!**
