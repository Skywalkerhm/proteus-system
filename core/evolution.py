#!/usr/bin/env python3
"""
🧬 Proteus Evolution System - 个体与群体进化

进化机制：
1. 个体进化：Agent 根据执行历史更新能力画像
2. 群体进化：系统从成功任务中发现新模式、优化规则
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from collections import defaultdict

class EvolutionEngine:
    """
    进化引擎
    
    负责分析任务执行记录，驱动系统进化
    """
    
    def __init__(self, memory_path: Path, evolution_path: Path):
        self.memory_path = memory_path
        self.evolution_path = evolution_path
        self.evolution_path.mkdir(parents=True, exist_ok=True)
        
        # 进化日志
        self.evolution_log = self.evolution_path / "evolution_log.jsonl"
        
        print("🧬 Evolution Engine 已初始化")
        print(f"   记忆路径：{memory_path}")
        print(f"   进化日志：{self.evolution_log}")
    
    # ========== 个体进化 ==========
    
    def evolve_agent(self, agent_id: str, task_result: Dict, semantic_memory):
        """
        个体进化：更新 Agent 画像
        
        Args:
            agent_id: Agent ID
            task_result: 任务执行结果
            semantic_memory: 语义记忆对象
        """
        profile = semantic_memory.get_agent_profile(agent_id)
        if not profile:
            print(f"   ⚠️  Agent {agent_id} 不存在")
            return
        
        print(f"   🧬 进化 Agent: {agent_id}")
        
        # 更新执行统计
        if "stats" not in profile:
            profile["stats"] = {"total": 0, "success": 0, "total_time": 0}
        
        if "tasks" not in profile["stats"]:
            profile["stats"]["tasks"] = []
        
        profile["stats"]["total"] += 1
        if task_result.get("success", False):
            profile["stats"]["success"] += 1
        
        exec_time = task_result.get("execution_time", 0)
        if exec_time:
            profile["stats"]["total_time"] += exec_time
        
        # 记录任务历史
        profile["stats"]["tasks"].append({
            "task_id": task_result.get("task_id"),
            "success": task_result.get("success", False),
            "timestamp": datetime.now().isoformat()
        })
        
        # 保持最近 50 个任务
        if len(profile["stats"]["tasks"]) > 50:
            profile["stats"]["tasks"] = profile["stats"]["tasks"][-50:]
        
        # 计算成功率
        total = profile["stats"]["total"]
        success = profile["stats"]["success"]
        profile["stats"]["success_rate"] = round(success / total, 2) if total > 0 else 0
        
        # 计算平均执行时间
        profile["stats"]["avg_time"] = round(
            profile["stats"]["total_time"] / total, 1
        ) if total > 0 else 0
        
        # 发现新技能（从任务中提取）
        new_skills = task_result.get("new_skills", [])
        if new_skills:
            current_skills = set(profile.get("skills", []))
            for skill in new_skills:
                if skill not in current_skills:
                    profile["skills"].append(skill)
                    print(f"      ✨ 发现新技能：{skill}")
        
        # 更新协作偏好
        partners = task_result.get("collaboration_partners", [])
        if partners:
            if "preferred_partners" not in profile:
                profile["preferred_partners"] = []
            for partner in partners:
                if partner not in profile["preferred_partners"]:
                    profile["preferred_partners"].append(partner)
        
        # 保存更新后的画像
        semantic_memory.register_agent(agent_id, profile)
        
        # 记录进化日志
        self._log_evolution("agent_evolution", {
            "agent_id": agent_id,
            "success_rate": profile["stats"]["success_rate"],
            "avg_time": profile["stats"]["avg_time"],
            "total_tasks": total,
            "new_skills": new_skills
        })
        
        print(f"      成功率：{profile['stats']['success_rate']:.0%}")
        print(f"      平均时间：{profile['stats']['avg_time']}min")
    
    # ========== 群体进化 ==========
    
    def discover_patterns(self, episodic_memory, semantic_memory, min_successes: int = 3):
        """
        群体进化：从成功任务中发现新模式
        
        Args:
            episodic_memory: 场景记忆对象
            semantic_memory: 语义记忆对象
            min_successes: 最小成功次数
        """
        print("\n🧬 群体进化：发现新模式")
        
        # 获取所有成功任务
        task_ids = episodic_memory.list_tasks()
        successful_tasks = []
        
        for task_id in task_ids:
            task_data = episodic_memory.load(task_id)
            if task_data and task_data.get("context", {}).get("success", False):
                successful_tasks.append(task_data)
        
        print(f"   找到 {len(successful_tasks)} 个成功任务")
        
        if len(successful_tasks) < min_successes:
            print(f"   ⚠️  成功任务不足 {min_successes} 个，跳过模式发现")
            return []
        
        # 分析任务相似性
        patterns = self._cluster_similar_tasks(successful_tasks)
        
        new_patterns = []
        for cluster in patterns:
            if len(cluster) >= min_successes:
                pattern = self._extract_pattern(cluster)
                if pattern:
                    pattern_id = f"auto_{pattern['name'].lower().replace(' ', '_')}"
                    semantic_memory.save_pattern(pattern_id, pattern)
                    new_patterns.append(pattern)
                    print(f"      ✨ 发现新模式：{pattern['name']}")
        
        # 记录进化日志
        self._log_evolution("pattern_discovery", {
            "total_tasks": len(successful_tasks),
            "patterns_found": len(new_patterns),
            "patterns": [p["name"] for p in new_patterns]
        })
        
        return new_patterns
    
    def _cluster_similar_tasks(self, tasks: List[Dict]) -> List[List[Dict]]:
        """
        聚类相似任务
        
        简化版本：基于任务描述关键词聚类
        """
        clusters = defaultdict(list)
        
        for task in tasks:
            task_desc = task.get("context", {}).get("task_desc", "").lower()
            
            # 简单关键词分类
            if "社交媒体" in task_desc or "内容" in task_desc:
                clusters["social_media"].append(task)
            elif "研究" in task_desc or "报告" in task_desc:
                clusters["research"].append(task)
            elif "代码" in task_desc or "编程" in task_desc:
                clusters["coding"].append(task)
            else:
                clusters["generic"].append(task)
        
        return list(clusters.values())
    
    def _extract_pattern(self, tasks: List[Dict]) -> Optional[Dict]:
        """
        从任务簇中提取模式
        """
        if not tasks:
            return None
        
        # 分析最常见的子任务序列
        all_subtasks = []
        for task in tasks:
            subtasks = task.get("context", {}).get("subtasks", [])
            if subtasks:
                all_subtasks.append(subtasks)
        
        if not all_subtasks:
            return None
        
        # 提取最常见的子任务（简化）
        common_subtasks = all_subtasks[0]  # 取第一个作为模板
        
        # 计算平均执行时间
        avg_time = sum(
            st.get("estimated_time", 30)
            for st in common_subtasks
        )
        
        # 提取推荐 Claw
        agents_used = defaultdict(int)
        for task in tasks:
            claw = task.get("context", {}).get("claw", {})
            for member in claw.get("members", []):
                agents_used[member.get("agent_id", "unknown")] += 1
        
        top_agents = sorted(agents_used.items(), key=lambda x: -x[1])[:3]
        
        # 提取最佳实践
        best_practices = [
            "任务执行前明确目标和成功标准",
            "定期同步进度，及时沟通障碍",
            "完成后进行复盘，记录经验教训"
        ]
        
        return {
            "pattern_id": "auto_pattern",  # 会被覆盖
            "name": f"自动发现的模式-{len(tasks)} 次成功",
            "description": f"从 {len(tasks)} 个成功任务中提取的通用模式",
            "subtasks": common_subtasks,
            "recommended_claw": {
                "members": [agent_id for agent_id, _ in top_agents],
                "rationale": f"基于 {len(tasks)} 次成功协作历史"
            },
            "best_practices": best_practices,
            "estimated_total_time": avg_time,
            "success_rate": 1.0,  # 都是成功任务
            "sample_size": len(tasks)
        }
    
    def optimize_rules(self, episodic_memory, semantic_memory):
        """
        优化协作规则
        
        分析冲突和异常情况，更新规则库
        """
        print("\n🧬 优化协作规则")
        
        # 获取所有异常日志
        exceptions = []
        for task_id in episodic_memory.list_tasks():
            task_data = episodic_memory.load(task_id)
            messages = task_data.get("messages", [])
            for msg in messages:
                if msg.get("content", "").startswith("异常") or "错误" in msg.get("content", ""):
                    exceptions.append({
                        "task_id": task_id,
                        "message": msg
                    })
        
        if not exceptions:
            print("   ✅ 无异常，规则运行良好")
            return []
        
        print(f"   分析 {len(exceptions)} 个异常")
        
        # 分析异常类型（简化）
        rule_updates = []
        
        # 如果发现沟通相关的异常
        communication_errors = [e for e in exceptions if "沟通" in str(e)]
        if communication_errors:
            rule_updates.append({
                "rule_id": "communication_enhancement",
                "name": "沟通增强规则",
                "description": "加强 Agent 间沟通，减少信息不对称",
                "content": [
                    "1. 任务开始前明确期望输出",
                    "2. 执行中每 30 分钟同步进度",
                    "3. 遇到障碍立即上报，不超过 10 分钟",
                    "4. 任务完成后提交详细报告"
                ]
            })
        
        # 保存新规则
        for rule in rule_updates:
            semantic_memory.save_rule(rule["rule_id"], rule)
            print(f"      ✨ 新增规则：{rule['name']}")
        
        # 记录进化日志
        self._log_evolution("rule_optimization", {
            "exceptions_analyzed": len(exceptions),
            "rules_added": len(rule_updates)
        })
        
        return rule_updates
    
    # ========== 辅助方法 ==========
    
    def _log_evolution(self, event_type: str, data: Dict):
        """记录进化日志"""
        log_entry = {
            "event": event_type,
            "data": data,
            "timestamp": datetime.now().isoformat()
        }
        with open(self.evolution_log, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
    
    def get_evolution_history(self, limit: int = 10) -> List[Dict]:
        """获取进化历史"""
        if not self.evolution_log.exists():
            return []
        
        history = []
        with open(self.evolution_log, 'r', encoding='utf-8') as f:
            for line in f:
                history.append(json.loads(line))
        
        return history[-limit:]


if __name__ == "__main__":
    # 测试进化引擎
    from memory import MemorySystem
    
    memory = MemorySystem()
    engine = EvolutionEngine(
        memory_path=Path(__file__).parent.parent / "memory",
        evolution_path=Path(__file__).parent.parent / "evolution"
    )
    
    # 模拟任务结果
    task_result = {
        "task_id": "test_001",
        "success": True,
        "execution_time": 45,
        "new_skills": ["advanced_analysis"],
        "collaboration_partners": ["research_agent", "review_agent"]
    }
    
    # 测试 Agent 进化
    print("\n🧬 测试 Agent 进化:")
    engine.evolve_agent("content_agent", task_result, memory.semantic)
    
    # 查看进化历史
    print("\n📜 进化历史:")
    history = engine.get_evolution_history()
    for entry in history:
        print(f"   {entry['event']}: {entry['timestamp']}")
    
    print("\n✅ 进化引擎测试完成")
