#!/usr/bin/env python3
"""
🧠 Proteus Memory System - 三层记忆框架

- Working Memory（工作记忆）：当前任务上下文，临时状态，任务后清空
- Episodic Memory（场景记忆）：任务执行轨迹，用于复盘学习
- Semantic Memory（语义记忆）：核心知识库，Agent 画像、任务模式、规则库
"""

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

class MemoryLayer:
    """记忆层基类"""
    
    def __init__(self, storage_path: Path):
        self.storage_path = storage_path
        self.storage_path.mkdir(parents=True, exist_ok=True)
    
    def save(self, key: str, data: Dict) -> str:
        raise NotImplementedError
    
    def load(self, key: str) -> Optional[Dict]:
        raise NotImplementedError
    
    def clear(self):
        raise NotImplementedError


class WorkingMemory(MemoryLayer):
    """
    工作记忆层
    - 存储当前任务链的上下文
    - Agent 间通信消息
    - 临时状态
    - 任务结束后清空
    """
    
    def __init__(self, storage_path: Path):
        super().__init__(storage_path)
        self.current_task_id: Optional[str] = None
        self.context: Dict[str, Any] = {}
        self.messages: List[Dict] = []
    
    def init_task(self, task_id: str, task_desc: str):
        """初始化新任务的工作记忆"""
        self.current_task_id = task_id
        self.context = {
            "task_id": task_id,
            "task_desc": task_desc,
            "created_at": datetime.now().isoformat(),
            "status": "active"
        }
        self.messages = []
        print(f"🧠 [WorkingMemory] 任务 {task_id[:8]} 已初始化")
    
    def add_message(self, sender: str, receiver: str, content: str, metadata: Dict = None):
        """记录 Agent 间通信"""
        msg = {
            "timestamp": datetime.now().isoformat(),
            "sender": sender,
            "receiver": receiver,
            "content": content,
            "metadata": metadata or {}
        }
        self.messages.append(msg)
    
    def update_context(self, key: str, value: Any):
        """更新上下文"""
        self.context[key] = value
    
    def get_context(self, key: str = None) -> Any:
        """获取上下文"""
        if key:
            return self.context.get(key)
        return self.context
    
    def clear(self):
        """清空工作记忆（任务完成后调用）"""
        task_id = self.current_task_id
        self.current_task_id = None
        self.context = {}
        self.messages = []
        print(f"🧠 [WorkingMemory] 任务 {task_id[:8] if task_id else 'N/A'} 已清空")
    
    def export_to_episodic(self, episodic_memory: 'EpisodicMemory'):
        """导出到场景记忆（任务完成时）"""
        if self.current_task_id:
            episodic_data = {
                "task_id": self.current_task_id,
                "context": self.context,
                "messages": self.messages,
                "completed_at": datetime.now().isoformat()
            }
            episodic_memory.save(self.current_task_id, episodic_data)
            print(f"🧠 [WorkingMemory] 已导出到场景记忆")


class EpisodicMemory(MemoryLayer):
    """
    场景记忆层
    - 以任务 ID 为单位存储完整执行轨迹
    - 记录决策点、Agent 调用序列、协作记录
    - 用于复盘和学习
    """
    
    def save(self, task_id: str, data: Dict) -> str:
        """保存任务记录"""
        filepath = self.storage_path / f"{task_id}.json"
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"🧠 [EpisodicMemory] 任务 {task_id[:8]} 已保存")
        return task_id
    
    def load(self, task_id: str) -> Optional[Dict]:
        """加载任务记录"""
        filepath = self.storage_path / f"{task_id}.json"
        if filepath.exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
    
    def list_tasks(self) -> List[str]:
        """列出所有任务 ID"""
        return [f.stem for f in self.storage_path.glob("*.json")]
    
    def get_similar_tasks(self, task_desc: str, limit: int = 5) -> List[Dict]:
        """获取相似任务（用于模式匹配）"""
        # TODO: 实现语义相似度搜索
        # 当前简单返回最近的任务
        tasks = []
        for task_id in self.list_tasks()[:limit]:
            task_data = self.load(task_id)
            if task_data:
                tasks.append(task_data)
        return tasks
    
    def clear(self):
        """不清空场景记忆（永久存储）"""
        pass


class SemanticMemory(MemoryLayer):
    """
    语义记忆层
    - Agent 能力画像库
    - 任务模式库（SOP、最佳实践）
    - 规则与启发式库
    """
    
    def __init__(self, storage_path: Path):
        super().__init__(storage_path)
        
        # 初始化三个子库
        self.agents_path = self.storage_path / "agents"
        self.patterns_path = self.storage_path / "patterns"
        self.rules_path = self.storage_path / "rules"
        
        for path in [self.agents_path, self.patterns_path, self.rules_path]:
            path.mkdir(parents=True, exist_ok=True)
        
        # 初始化索引文件
        self._init_index("agents")
        self._init_index("patterns")
        self._init_index("rules")
    
    def _init_index(self, category: str):
        """初始化索引文件"""
        index_path = self.storage_path / f"{category}_index.json"
        if not index_path.exists():
            with open(index_path, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False)
    
    # ========== Agent 能力画像库 ==========
    
    def register_agent(self, agent_id: str, profile: Dict):
        """注册/更新 Agent 画像"""
        profile["updated_at"] = datetime.now().isoformat()
        filepath = self.agents_path / f"{agent_id}.json"
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(profile, f, indent=2, ensure_ascii=False)
        
        # 更新索引
        self._update_index("agents", agent_id)
        print(f"🧠 [SemanticMemory] Agent {agent_id} 已注册")
    
    def get_agent_profile(self, agent_id: str) -> Optional[Dict]:
        """获取 Agent 画像"""
        filepath = self.agents_path / f"{agent_id}.json"
        if filepath.exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
    
    def match_agents(self, required_skills: List[str]) -> List[Dict]:
        """根据技能需求匹配 Agent"""
        matched = []
        for filepath in self.agents_path.glob("*.json"):
            # 跳过索引文件
            if filepath.name == "agents_index.json":
                continue
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    profile = json.load(f)
                    
                    # 确保是字典格式（兼容旧数据）
                    if isinstance(profile, list):
                        continue
                    
                    skills = profile.get("skills", [])
                    # 计算匹配度
                    match_score = len(set(required_skills) & set(skills)) / len(required_skills) if required_skills else 0
                    if match_score > 0:
                        matched.append((match_score, profile))
            except Exception as e:
                print(f"⚠️ 读取 Agent 文件失败 {filepath.name}: {e}")
                continue
        
        # 按匹配度排序
        matched.sort(key=lambda x: -x[0])
        return [profile for score, profile in matched]
    
    def update_agent_stats(self, agent_id: str, success: bool, execution_time: float = None):
        """更新 Agent 执行统计（用于进化）"""
        profile = self.get_agent_profile(agent_id)
        if profile:
            if "stats" not in profile:
                profile["stats"] = {"total": 0, "success": 0, "total_time": 0}
            
            profile["stats"]["total"] += 1
            if success:
                profile["stats"]["success"] += 1
            if execution_time:
                profile["stats"]["total_time"] += execution_time
            
            self.register_agent(agent_id, profile)
    
    # ========== 任务模式库 ==========
    
    def save_pattern(self, pattern_id: str, pattern: Dict):
        """保存任务模式"""
        pattern["updated_at"] = datetime.now().isoformat()
        filepath = self.patterns_path / f"{pattern_id}.json"
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(pattern, f, indent=2, ensure_ascii=False)
        
        self._update_index("patterns", pattern_id)
        print(f"🧠 [SemanticMemory] 任务模式 {pattern_id} 已保存")
    
    def get_pattern(self, pattern_id: str) -> Optional[Dict]:
        """获取任务模式"""
        filepath = self.patterns_path / f"{pattern_id}.json"
        if filepath.exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
    
    def match_pattern(self, task_desc: str) -> Optional[Dict]:
        """匹配相似任务模式"""
        # TODO: 实现语义匹配
        # 当前简单返回第一个模式
        for filepath in self.patterns_path.glob("*.json"):
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
    
    # ========== 规则库 ==========
    
    def save_rule(self, rule_id: str, rule: Dict):
        """保存规则"""
        rule["updated_at"] = datetime.now().isoformat()
        filepath = self.rules_path / f"{rule_id}.json"
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(rule, f, indent=2, ensure_ascii=False)
        
        self._update_index("rules", rule_id)
        print(f"🧠 [SemanticMemory] 规则 {rule_id} 已保存")
    
    def get_rule(self, rule_id: str) -> Optional[Dict]:
        """获取规则"""
        filepath = self.rules_path / f"{rule_id}.json"
        if filepath.exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
    
    def get_all_rules(self) -> List[Dict]:
        """获取所有规则"""
        rules = []
        for filepath in self.rules_path.glob("*.json"):
            with open(filepath, 'r', encoding='utf-8') as f:
                rules.append(json.load(f))
        return rules
    
    # ========== 辅助方法 ==========
    
    def _update_index(self, category: str, item_id: str):
        """更新索引"""
        index_path = self.storage_path / f"{category}_index.json"
        with open(index_path, 'r', encoding='utf-8') as f:
            index = json.load(f)
        
        if item_id not in index:
            index.append(item_id)
            with open(index_path, 'w', encoding='utf-8') as f:
                json.dump(index, f, ensure_ascii=False)
    
    def clear(self):
        """不清空语义记忆（永久存储）"""
        pass


class MemorySystem:
    """
    三层记忆系统总控
    """
    
    def __init__(self, base_path: Path = None):
        if base_path is None:
            base_path = Path(__file__).parent / "memory"
        
        self.working = WorkingMemory(base_path / "working")
        self.episodic = EpisodicMemory(base_path / "episodic")
        self.semantic = SemanticMemory(base_path / "semantic")
        
        print("🧠 Proteus Memory System 已初始化")
    
    def start_task(self, task_id: str, task_desc: str):
        """开始新任务"""
        self.working.init_task(task_id, task_desc)
    
    def complete_task(self, success: bool, feedback: str = None):
        """完成任务"""
        # 更新上下文
        self.working.update_context("completed", True)
        self.working.update_context("success", success)
        if feedback:
            self.working.update_context("feedback", feedback)
        
        # 导出到场景记忆
        self.working.export_to_episodic(self.episodic)
        
        # 清空工作记忆
        self.working.clear()
    
    def initialize_default_agents(self):
        """初始化默认 Agent 画像"""
        agents = [
            {
                "agent_id": "research_agent",
                "name": "Research Agent",
                "emoji": "🔬",
                "role": "研究专家",
                "skills": ["research", "analysis", "data_collection", "summarization"],
                "description": "擅长信息搜集、数据分析、文献综述",
                "stats": {"total": 0, "success": 0, "total_time": 0}
            },
            {
                "agent_id": "code_agent",
                "name": "Code Agent",
                "emoji": "💻",
                "role": "编程专家",
                "skills": ["coding", "debugging", "testing", "architecture"],
                "description": "擅长代码编写、调试、架构设计",
                "stats": {"total": 0, "success": 0, "total_time": 0}
            },
            {
                "agent_id": "content_agent",
                "name": "Content Agent",
                "emoji": "✍️",
                "role": "内容专家",
                "skills": ["writing", "editing", "copywriting", "social_media"],
                "description": "擅长文案创作、内容策划、社交媒体运营",
                "stats": {"total": 0, "success": 0, "total_time": 0}
            },
            {
                "agent_id": "review_agent",
                "name": "Review Agent",
                "emoji": "👀",
                "role": "审核专家",
                "skills": ["review", "quality_control", "feedback", "optimization"],
                "description": "擅长质量审核、反馈优化、风险控制",
                "stats": {"total": 0, "success": 0, "total_time": 0}
            }
        ]
        
        for agent in agents:
            self.semantic.register_agent(agent["agent_id"], agent)
        
        print(f"🧠 已初始化 {len(agents)} 个默认 Agent")
    
    def initialize_default_rules(self):
        """初始化默认规则"""
        rules = [
            {
                "rule_id": "collaboration_protocol",
                "name": "协作协议",
                "description": "Agent 间通信和协作的基本规则",
                "content": [
                    "1. 所有 Agent 通信必须通过 Hub 或在工作群内公开",
                    "2. 遇到障碍立即上报，不得隐瞒",
                    "3. 任务完成后必须提交执行报告",
                    "4. 跨 Agent 依赖需提前声明"
                ]
            },
            {
                "rule_id": "conflict_resolution",
                "name": "冲突解决规则",
                "description": "当 Agent 间出现分歧时的处理流程",
                "content": [
                    "1. 优先通过讨论达成共识",
                    "2. 无法共识时由主导 Agent 决策",
                    "3. 重大分歧上报 Hub 仲裁",
                    "4. 所有冲突记录到场景记忆"
                ]
            },
            {
                "rule_id": "quality_standard",
                "name": "质量标准",
                "description": "任务交付的最低质量要求",
                "content": [
                    "1. 输出必须经过自检",
                    "2. 代码必须有注释和测试",
                    "3. 文案必须无语法错误",
                    "4. 研究报告必须有数据支撑"
                ]
            }
        ]
        
        for rule in rules:
            self.semantic.save_rule(rule["rule_id"], rule)
        
        print(f"🧠 已初始化 {len(rules)} 个默认规则")


if __name__ == "__main__":
    # 测试记忆系统
    memory = MemorySystem()
    
    # 初始化默认 Agent 和规则
    memory.initialize_default_agents()
    memory.initialize_default_rules()
    
    # 测试任务流程
    task_id = str(uuid.uuid4())
    memory.start_task(task_id, "测试任务")
    
    memory.working.update_context("test_key", "test_value")
    memory.working.add_message("hub", "research_agent", "请执行研究任务")
    
    memory.complete_task(success=True, feedback="任务完成良好")
    
    print("\n✅ 记忆系统测试完成")
