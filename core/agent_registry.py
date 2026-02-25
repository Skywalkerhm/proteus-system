#!/usr/bin/env python3
"""
🏛️ Olympus Agent Registry - 希腊神话 Agent 画像

所有 Agent 基于希腊神话人物命名
"""

from pathlib import Path
from datetime import datetime

# 希腊神话 Agent 列表
OLYMPUS_AGENTS = {
    "echo": {
        "agent_id": "echo",
        "name": "Echo",
        "emoji": "🎤",
        "role": "Hub - 意图理解与任务分发",
        "level": "hub",
        "skills": ["intent_analysis", "task_decomposition", "agent_matching", "coordination"],
        "description": "回声女神，善于传递信息和协调各方",
        "color": "#FF6B6B",
        "mythology": "希腊神话中的回声女神"
    },
    "hermes": {
        "agent_id": "hermes",
        "name": "Hermes",
        "emoji": "🚀",
        "role": "CTO - 技术决策",
        "level": "spoke",
        "skills": ["architecture", "technical_decision", "innovation", "risk_assessment"],
        "description": "众神使者，聪明机智，技术高超",
        "color": "#4ECDC4",
        "mythology": "希腊神话中的众神使者"
    },
    "aphrodite": {
        "agent_id": "aphrodite",
        "name": "Aphrodite",
        "emoji": "💫",
        "role": "CMO - 市场策略",
        "level": "spoke",
        "skills": ["marketing", "branding", "growth_strategy", "user_analysis"],
        "description": "爱与美之神，善于吸引和影响",
        "color": "#45B7D1",
        "mythology": "希腊神话中的爱与美之神"
    },
    "hestia": {
        "agent_id": "hestia",
        "name": "Hestia",
        "emoji": "🏠",
        "role": "管家 - 任务管理与服务",
        "level": "specialist",
        "skills": ["task_management", "quality_control", "detail_oriented", "proactive_service"],
        "description": "家庭与炉灶女神，稳定可靠",
        "color": "#FFEAA7",
        "mythology": "希腊神话中的家庭女神"
    },
    "hephaestus": {
        "agent_id": "hephaestus",
        "name": "Hephaestus",
        "emoji": "🔨",
        "role": "全栈工程师 - 系统构建",
        "level": "specialist",
        "skills": ["full_stack_development", "system_architecture", "tool_creation", "debugging"],
        "description": "火与工匠之神，创造力最强",
        "color": "#F7DC6F",
        "mythology": "希腊神话中的工匠之神"
    },
    "muse": {
        "agent_id": "muse",
        "name": "Muse",
        "emoji": "✨",
        "role": "科普作家 - 灵感创作",
        "level": "specialist",
        "skills": ["science_writing", "content_creation", "storytelling", "inspiration"],
        "description": "缪斯女神，灵感与艺术的源泉",
        "color": "#BB8FCE",
        "mythology": "希腊神话中的缪斯女神"
    },
    "athena": {
        "agent_id": "athena",
        "name": "Athena",
        "emoji": "🦉",
        "role": "研究专家 - 智慧分析",
        "level": "specialist",
        "skills": ["scientific_research", "data_analysis", "strategic_thinking", "pattern_recognition"],
        "description": "智慧女神，善于分析和战略思考",
        "color": "#98D8C8",
        "mythology": "希腊神话中的智慧女神"
    },
    "apollo": {
        "agent_id": "apollo",
        "name": "Apollo",
        "emoji": "☀️",
        "role": "内容专家 - 艺术创作",
        "level": "specialist",
        "skills": ["content_creation", "artistic_expression", "communication", "storytelling"],
        "description": "艺术与光明之神，善于表达和创作",
        "color": "#FFD700",
        "mythology": "希腊神话中的艺术之神"
    },
    "daedalus": {
        "agent_id": "daedalus",
        "name": "Daedalus",
        "emoji": "🏛️",
        "role": "代码专家 - 架构设计",
        "level": "specialist",
        "skills": ["code_architecture", "complex_systems", "algorithm_design", "optimization"],
        "description": "传奇工匠，善于建造复杂结构",
        "color": "#DDA0DD",
        "mythology": "希腊神话中的传奇工匠"
    },
    "themis": {
        "agent_id": "themis",
        "name": "Themis",
        "emoji": "⚖️",
        "role": "审核专家 - 质量把控",
        "level": "specialist",
        "skills": ["quality_assurance", "code_review", "standard_enforcement", "feedback"],
        "description": "正义与秩序女神，公正严谨",
        "color": "#96CEB4",
        "mythology": "希腊神话中的正义女神"
    }
}

def get_all_agents():
    """获取所有 Agent"""
    return OLYMPUS_AGENTS

def get_agent(agent_id: str):
    """获取单个 Agent"""
    return OLYMPUS_AGENTS.get(agent_id)

def register_to_memory(semantic_memory):
    """注册到语义记忆"""
    for agent_id, profile in OLYMPUS_AGENTS.items():
        profile["migrated_at"] = datetime.now().isoformat()
        semantic_memory.register_agent(agent_id, profile)
    print(f"🏛️ 已注册 {len(OLYMPUS_AGENTS)} 个 Olympus Agent")

if __name__ == "__main__":
    print("🏛️ Olympus System - Agent Registry")
    print("=" * 50)
    for agent_id, info in OLYMPUS_AGENTS.items():
        print(f"   {info['emoji']} {info['name']} - {info['role']}")
    print(f"\n总计：{len(OLYMPUS_AGENTS)} 个 Agent")
