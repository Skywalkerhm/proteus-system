#!/usr/bin/env python3
"""
🔄 Proteus Adaptive System - 自适应调整机制

功能：
1. 执行失败检测
2. 动态恢复策略
3. 备选方案生成
4. 人类介入请求
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

class AdaptiveEngine:
    """自适应引擎"""
    
    def __init__(self, hub):
        self.hub = hub
        self.failure_patterns = []
        self.recovery_strategies = {
            "agent_unavailable": "find_alternative_agent",
            "task_too_complex": "decompose_further",
            "skill_mismatch": "reassign_agent",
            "timeout": "request_extension_or_help",
            "conflict": "hub_mediation"
        }
        print("🔄 Adaptive Engine 已初始化")
    
    def detect_failure(self, task_id: str, subtask: Dict, error: str) -> Dict:
        """检测失败并分类"""
        failure_type = self._classify_failure(error)
        
        failure_record = {
            "task_id": task_id,
            "subtask_id": subtask.get("subtask_id"),
            "failure_type": failure_type,
            "error": error,
            "timestamp": datetime.now().isoformat(),
            "context": self.hub.memory.working.get_context()
        }
        
        self.failure_patterns.append(failure_record)
        
        print(f"   ⚠️  检测失败：{failure_type}")
        print(f"      错误：{error[:50]}...")
        
        return failure_record
    
    def _classify_failure(self, error: str) -> str:
        """失败分类"""
        error_lower = error.lower()
        
        if "unavailable" in error_lower or "not found" in error_lower:
            return "agent_unavailable"
        elif "too complex" in error_lower or "timeout" in error_lower:
            return "task_too_complex"
        elif "skill" in error_lower or "cannot" in error_lower:
            return "skill_mismatch"
        elif "conflict" in error_lower or "disagree" in error_lower:
            return "conflict"
        else:
            return "unknown"
    
    def generate_recovery_plan(self, failure: Dict) -> Dict:
        """生成恢复计划"""
        failure_type = failure["failure_type"]
        strategy = self.recovery_strategies.get(failure_type, "request_human_help")
        
        recovery_plan = {
            "strategy": strategy,
            "steps": [],
            "estimated_time": 0,
            "success_probability": 0.0
        }
        
        if strategy == "find_alternative_agent":
            recovery_plan = self._recover_agent_unavailable(failure)
        elif strategy == "decompose_further":
            recovery_plan = self._recover_task_too_complex(failure)
        elif strategy == "reassign_agent":
            recovery_plan = self._recover_skill_mismatch(failure)
        elif strategy == "hub_mediation":
            recovery_plan = self._recover_conflict(failure)
        else:
            recovery_plan = self._request_human_help(failure)
        
        return recovery_plan
    
    def _recover_agent_unavailable(self, failure: Dict) -> Dict:
        """Agent 不可用恢复"""
        # 查找替代 Agent
        required_skills = failure.get("context", {}).get("required_skills", [])
        alternatives = self.hub.memory.semantic.match_agents(required_skills)
        
        if alternatives:
            best_alternative = alternatives[0]  # 选择匹配度最高的
            
            return {
                "strategy": "find_alternative_agent",
                "steps": [
                    f"1. 识别替代 Agent: {best_alternative['name']}",
                    f"2. 转移任务上下文",
                    f"3. 重新执行子任务"
                ],
                "alternative_agent": best_alternative["agent_id"],
                "estimated_time": 15,
                "success_probability": 0.8
            }
        else:
            return self._request_human_help(failure)
    
    def _recover_task_too_complex(self, failure: Dict) -> Dict:
        """任务太复杂恢复"""
        # 重新分解任务
        original_task = failure.get("context", {}).get("task_desc", "")
        
        new_subtasks = self.hub.llm.decompose_task(
            f"简化版：{original_task[:100]}"
        )
        
        return {
            "strategy": "decompose_further",
            "steps": [
                "1. 重新分解为更小的子任务",
                f"2. 生成 {len(new_subtasks)} 个简化子任务",
                "3. 逐个执行子任务"
            ],
            "new_subtasks": new_subtasks,
            "estimated_time": 30,
            "success_probability": 0.7
            }
    
    def _recover_skill_mismatch(self, failure: Dict) -> Dict:
        """技能不匹配恢复"""
        # 重新分配 Agent
        subtask = failure.get("subtask_id")
        
        return {
            "strategy": "reassign_agent",
            "steps": [
                "1. 分析所需技能",
                "2. 查找匹配度更高的 Agent",
                "3. 重新分配任务"
            ],
            "estimated_time": 10,
            "success_probability": 0.75
        }
    
    def _recover_conflict(self, failure: Dict) -> Dict:
        """冲突恢复"""
        # Hub 调解
        
        return {
            "strategy": "hub_mediation",
            "steps": [
                "1. Hub 收集各方观点",
                "2. 分析冲突根源",
                "3. 提出折中方案",
                "4. 协调执行"
            ],
            "estimated_time": 20,
            "success_probability": 0.85
        }
    
    def _request_human_help(self, failure: Dict) -> Dict:
        """请求人类帮助"""
        
        return {
            "strategy": "request_human_help",
            "steps": [
                "1. 汇总失败信息",
                "2. 生成求助请求",
                "3. 等待人类指示"
            ],
            "help_request": f"任务 {failure['task_id'][:8]} 执行失败：{failure['error'][:100]}",
            "estimated_time": 0,  # 等待人类
            "success_probability": 0.95  # 人类通常能解决
        }
    
    def execute_recovery(self, task_id: str, recovery_plan: Dict) -> bool:
        """执行恢复计划"""
        print(f"\n🔄 执行恢复计划：{recovery_plan['strategy']}")
        
        for step in recovery_plan.get("steps", []):
            print(f"   {step}")
        
        # 记录恢复日志
        self.hub.logger.log_decision(
            task_id,
            "adaptive_recovery",
            recovery_plan["strategy"],
            f"自动恢复：{recovery_plan.get('success_probability', 0):.0%} 成功率"
        )
        
        # 模拟执行恢复
        # 实际应该根据策略执行不同操作
        return True
    
    def get_adaptive_stats(self) -> Dict:
        """获取自适应统计"""
        total_failures = len(self.failure_patterns)
        
        if total_failures == 0:
            return {
                "total_failures": 0,
                "recovery_success_rate": 0,
                "most_common_failure": "N/A"
            }
        
        # 统计失败类型
        failure_types = {}
        for failure in self.failure_patterns:
            ftype = failure["failure_type"]
            failure_types[ftype] = failure_types.get(ftype, 0) + 1
        
        most_common = max(failure_types.items(), key=lambda x: x[1])[0]
        
        return {
            "total_failures": total_failures,
            "recovery_success_rate": 0.85,  # 模拟值
            "most_common_failure": most_common,
            "failure_distribution": failure_types
        }


if __name__ == "__main__":
    # 测试自适应引擎
    from hub import ProteusHub
    
    hub = ProteusHub()
    engine = AdaptiveEngine(hub)
    
    # 模拟失败场景
    print("\n🧪 测试自适应引擎")
    
    # 场景 1: Agent 不可用
    failure1 = engine.detect_failure(
        "task_001",
        {"subtask_id": "st_1", "desc": "测试任务"},
        "Agent data_agent unavailable"
    )
    plan1 = engine.generate_recovery_plan(failure1)
    print(f"\n恢复计划 1: {plan1['strategy']}")
    print(f"成功率：{plan1.get('success_probability', 0):.0%}")
    
    # 场景 2: 技能不匹配
    failure2 = engine.detect_failure(
        "task_002",
        {"subtask_id": "st_2", "desc": "测试任务"},
        "Agent cannot perform task: skill mismatch"
    )
    plan2 = engine.generate_recovery_plan(failure2)
    print(f"\n恢复计划 2: {plan2['strategy']}")
    print(f"成功率：{plan2.get('success_probability', 0):.0%}")
    
    # 统计
    stats = engine.get_adaptive_stats()
    print(f"\n📊 自适应统计：{stats}")
    
    print("\n✅ 自适应引擎测试完成")
