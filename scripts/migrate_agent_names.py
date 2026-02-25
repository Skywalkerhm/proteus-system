#!/usr/bin/env python3
"""
🏛️ Olympus System - Agent 命名迁移脚本

将希腊神话名字应用到所有 Agent 配置文件
"""

import json
from pathlib import Path

AGENTS_DIR = Path(__file__).parent.parent / "memory" / "semantic" / "agents"

# 命名映射
NAME_MAPPING = {
    "echo": {"name": "Echo", "emoji": "🎤", "role": "Hub - 意图理解与任务分发"},
    "hermes": {"name": "Hermes", "emoji": "🚀", "role": "CTO - 技术决策"},
    "aphrodite": {"name": "Aphrodite", "emoji": "💫", "role": "CMO - 市场策略"},
    "hestia": {"name": "Hestia", "emoji": "🏠", "role": "管家 - 任务管理与服务"},
    "hephaestus": {"name": "Hephaestus", "emoji": "🔨", "role": "全栈工程师 - 系统构建"},
    "muse": {"name": "Muse", "emoji": "✨", "role": "科普作家 - 灵感创作"},
    "athena": {"name": "Athena", "emoji": "🦉", "role": "研究专家 - 智慧分析"},
    "apollo": {"name": "Apollo", "emoji": "☀️", "role": "内容专家 - 艺术创作"},
    "daedalus": {"name": "Daedalus", "emoji": "🏛️", "role": "代码专家 - 架构设计"},
    "themis": {"name": "Themis", "emoji": "⚖️", "role": "审核专家 - 质量把控"}
}

def migrate_agent_names():
    """迁移 Agent 名字"""
    print("🏛️ Olympus System - Agent 命名迁移")
    print("=" * 50)
    
    # 重命名文件
    file_mappings = {
        "elon.json": "hermes.json",
        "henry.json": "aphrodite.json",
        "butler.json": "hestia.json",
        "coder.json": "hephaestus.json",
        "xhso.json": "muse.json",
        "research_agent.json": "athena.json",
        "content_agent.json": "apollo.json",
        "code_agent.json": "daedalus.json",
        "review_agent.json": "themis.json"
    }
    
    for old_name, new_name in file_mappings.items():
        old_file = AGENTS_DIR / old_name
        new_file = AGENTS_DIR / new_name
        
        if old_file.exists():
            # 读取旧文件
            with open(old_file, 'r', encoding='utf-8') as f:
                agent_data = json.load(f)
            
            # 更新名字
            agent_id = new_name.replace(".json", "")
            agent_data["agent_id"] = agent_id
            agent_data["name"] = NAME_MAPPING[agent_id]["name"]
            agent_data["emoji"] = NAME_MAPPING[agent_id]["emoji"]
            agent_data["role"] = NAME_MAPPING[agent_id]["role"]
            agent_data["mythology"] = f"希腊神话中的{NAME_MAPPING[agent_id]['name']}"
            
            # 保存新文件
            with open(new_file, 'w', encoding='utf-8') as f:
                json.dump(agent_data, f, indent=2, ensure_ascii=False)
            
            # 删除旧文件
            old_file.unlink()
            
            print(f"✅ {old_name} → {new_name}")
    
    # 更新索引
    index_file = AGENTS_DIR / "agents_index.json"
    agent_ids = list(NAME_MAPPING.keys())
    with open(index_file, 'w', encoding='utf-8') as f:
        json.dump(agent_ids, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ 索引已更新：{len(agent_ids)} 个 Agent")
    print("\n🏛️ Olympus System Agent 列表:")
    for agent_id, info in NAME_MAPPING.items():
        print(f"   {info['emoji']} {info['name']} - {info['role']}")

if __name__ == "__main__":
    migrate_agent_names()
