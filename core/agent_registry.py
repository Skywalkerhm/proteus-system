#!/usr/bin/env python3
"""
🤖 Proteus Agent Registry - 复制 OpenClaw Agent 画像

从 OpenClaw/Hive Mind 复制现有 Agent 能力画像到 Proteus 语义记忆
"""

import json
from pathlib import Path
from datetime import datetime

# Hive Mind Agent 数据源
# 注意：使用前需要配置实际路径
HIVE_MIND_DATA = Path(__file__).parent.parent.parent / "hive-mind-data"

def load_hive_mind_agents():
    """从 Hive Mind 加载 Agent 数据"""
    # 从 dashboard 或 tasks.json 中提取 Agent 信息
    agents = {
        "echo": {
            "agent_id": "echo",
            "name": "Echo",
            "emoji": "🎤",
            "role": "Hub - 意图理解与任务分发",
            "level": "hub",
            "skills": ["intent_analysis", "task_decomposition", "agent_matching", "coordination"],
            "description": "中央调度器，负责任务接收、解析、分派和结果整合",
            "color": "#FF6B6B",
            "stats": {"total": 0, "success": 0, "total_time": 0}
        },
        "elon": {
            "agent_id": "elon",
            "name": "Elon",
            "emoji": "🚀",
            "role": "CTO - 技术决策",
            "level": "spoke",
            "skills": ["architecture", "technical_decision", "innovation", "risk_assessment"],
            "description": "技术决策者，负责架构设计、技术选型、风险评估",
            "color": "#4ECDC4",
            "stats": {"total": 0, "success": 0, "total_time": 0}
        },
        "henry": {
            "agent_id": "henry",
            "name": "Henry",
            "emoji": "📈",
            "role": "CMO - 市场策略",
            "level": "spoke",
            "skills": ["marketing", "branding", "growth_strategy", "user_analysis"],
            "description": "市场策略专家，负责品牌建设、增长策略、用户分析",
            "color": "#45B7D1",
            "stats": {"total": 0, "success": 0, "total_time": 0}
        },
        "butler": {
            "agent_id": "butler",
            "name": "Butler",
            "emoji": "🤵",
            "role": "管家",
            "level": "specialist",
            "skills": ["task_management", "quality_control", "detail_oriented", "proactive_service"],
            "description": "专业管家，细节控，负责任务管理、质量把控、主动服务",
            "color": "#FFEAA7",
            "stats": {"total": 0, "success": 0, "total_time": 0}
        },
            "agent_id": "xhso",
            "name": "xhso",
            "emoji": "📝",
            "role": "科普作家",
            "level": "specialist",
            "skills": ["science_writing", "content_creation", "storytelling", "social_media"],
            "description": "科普作家，百万粉丝博主，擅长科学传播、内容创作、故事化叙事",
            "color": "#BB8FCE",
            "stats": {"total": 0, "success": 0, "total_time": 0}
        }
    }
    return agents

def migrate_to_proteus():
    """迁移 Agent 到 Proteus 语义记忆"""
    # 加载 Hive Mind Agent
    agents = load_hive_mind_agents()
    
    # Proteus 语义记忆路径
    proteus_semantic = Path(__file__).parent.parent / "memory" / "semantic" / "agents"
    proteus_semantic.mkdir(parents=True, exist_ok=True)
    
    # 保存每个 Agent
    for agent_id, profile in agents.items():
        profile["migrated_from"] = "hive_mind"
        profile["migrated_at"] = datetime.now().isoformat()
        
        filepath = proteus_semantic / f"{agent_id}.json"
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(profile, f, indent=2, ensure_ascii=False)
        
        print(f"✅ 迁移 Agent: {agent_id} ({profile['name']})")
    
    # 更新索引
    index_path = proteus_semantic.parent / "agents_index.json"
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(list(agents.keys()), f, indent=2, ensure_ascii=False)
    
    print(f"\n🎉 完成！共迁移 {len(agents)} 个 Agent 到 Proteus System")
    print(f"📁 存储位置：{proteus_semantic}")
    
    return agents

if __name__ == "__main__":
    migrate_to_proteus()
