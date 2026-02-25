#!/usr/bin/env python3
"""
🎤 Proteus Hub - 中央调度器

系统唯一入口和总控，负责：
- 任务接收与解析
- 全局状态监控
- 规划与组队
- 最终输出整合
"""

import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

from memory import MemorySystem
from llm_integration import LLMClient, ExecutionLogger
from evolution import EvolutionEngine

class ProteusHub:
    """
    The Hub - 中央调度器
    """
    
    def __init__(self, base_path: Path = None):
        if base_path is None:
            base_path = Path(__file__).parent.parent
        
        self.memory = MemorySystem(base_path / "memory")
        self.base_path = base_path
        
        # 初始化 LLM 客户端
        self.llm = LLMClient()
        
        # 初始化执行日志
        self.logger = ExecutionLogger(base_path / "logs" / "tasks")
        
        # 初始化进化引擎
        self.evolution = EvolutionEngine(
            memory_path=base_path / "memory",
            evolution_path=base_path / "evolution"
        )
        
        # 系统状态
        self.active_tasks: Dict[str, Dict] = {}
        self.active_claws: Dict[str, Dict] = {}
        
        # 初始化默认 Agent 和规则
        self.memory.initialize_default_agents()
        self.memory.initialize_default_rules()
        
        print("🎤 Proteus Hub 已启动（增强版）")
        print(f"   基础路径：{base_path}")
        print(f"   LLM 集成：✅")
        print(f"   执行日志：✅")
        print(f"   进化引擎：✅")
        print(f"   已初始化 {len(self._list_agents())} 个 Agent")
    
    def _list_agents(self) -> List[str]:
        """列出所有可用 Agent"""
        return [f.stem for f in (self.base_path / "memory" / "semantic" / "agents").glob("*.json")]
    
    # ========== 任务接收与解析 ==========
    
    def receive_task(self, task_desc: str, user_id: str = "default", priority: str = "normal") -> str:
        """
        接收新任务
        
        Args:
            task_desc: 任务描述
            user_id: 用户 ID
            priority: 优先级 (low/normal/high/urgent)
        
        Returns:
            task_id: 任务 ID
        """
        task_id = str(uuid.uuid4())
        
        # 记录任务
        task = {
            "task_id": task_id,
            "task_desc": task_desc,
            "user_id": user_id,
            "priority": priority,
            "status": "received",
            "created_at": datetime.now().isoformat(),
            "assigned_claw": None,
            "subtasks": [],
            "logs": []
        }
        
        self.active_tasks[task_id] = task
        
        # 初始化工作记忆
        self.memory.start_task(task_id, task_desc)
        self.memory.working.add_message("user", "hub", task_desc, {"priority": priority})
        
        print(f"\n🎤 [Hub] 收到新任务 {task_id[:8]}")
        print(f"   描述：{task_desc[:50]}...")
        print(f"   优先级：{priority}")
        
        return task_id
    
    def parse_task(self, task_id: str) -> Dict:
        """
        解析任务
        
        1. 在语义记忆中匹配类似任务模式
        2. 如无匹配，使用 LLM 进行创造性分解
        3. 生成子任务列表
        """
        task = self.active_tasks.get(task_id)
        if not task:
            raise ValueError(f"任务 {task_id} 不存在")
        
        print(f"\n🎤 [Hub] 解析任务 {task_id[:8]}")
        
        # 尝试匹配任务模式
        pattern = self.memory.semantic.match_pattern(task["task_desc"])
        
        if pattern:
            print(f"   ✅ 匹配到任务模式：{pattern.get('pattern_id', 'N/A')}")
            subtasks = pattern.get("subtasks", [])
        else:
            print(f"   ⚠️  未匹配到模式，使用 LLM 创造性分解")
            subtasks = self.llm.decompose_task(task["task_desc"])
        
        # 更新任务
        task["subtasks"] = subtasks
        task["status"] = "parsed"
        
        self.memory.working.update_context("subtasks", subtasks)
        self.memory.working.add_message("hub", "system", f"任务已分解为 {len(subtasks)} 个子任务")
        
        # 记录决策
        self.logger.log_decision(
            task_id,
            "task_decomposition",
            f"分解为{len(subtasks)}个子任务",
            "模式匹配" if pattern else "LLM 创造性分解"
        )
        
        print(f"   分解为 {len(subtasks)} 个子任务:")
        for i, st in enumerate(subtasks, 1):
            print(f"     {i}. {st.get('desc', 'N/A')[:50]}...")
        
        return {"task_id": task_id, "subtasks": subtasks}
    
    def _creative_decompose(self, task_desc: str) -> List[Dict]:
        """
        创造性任务分解
        
        这是一个简化版本，实际应该用 LLM 进行智能分解
        """
        # 通用分解模板
        return [
            {
                "subtask_id": str(uuid.uuid4())[:8],
                "desc": f"分析任务需求：{task_desc[:50]}",
                "required_skills": ["analysis"],
                "estimated_time": 30,
                "status": "pending"
            },
            {
                "subtask_id": str(uuid.uuid4())[:8],
                "desc": "执行核心任务",
                "required_skills": ["execution"],
                "estimated_time": 60,
                "status": "pending"
            },
            {
                "subtask_id": str(uuid.uuid4())[:8],
                "desc": "质量审核与优化",
                "required_skills": ["review"],
                "estimated_time": 20,
                "status": "pending"
            }
        ]
    
    # ========== 规划与组队 ==========
    
    def form_claw(self, task_id: str) -> Dict:
        """
        组建动态工作小组（Claw）
        
        1. 根据子任务技能需求匹配 Agent
        2. 计算最佳匹配度
        3. 指定主导 Agent
        4. 创建 Claw
        """
        task = self.active_tasks.get(task_id)
        if not task or task["status"] != "parsed":
            raise ValueError(f"任务 {task_id} 未解析或不存在")
        
        print(f"\n🎤 [Hub] 为任务 {task_id[:8]} 组建 Claw")
        
        # 收集所有需要的技能
        required_skills = set()
        for subtask in task["subtasks"]:
            required_skills.update(subtask.get("required_skills", []))
        
        print(f"   需要技能：{list(required_skills)}")
        
        # 匹配 Agent
        matched_agents = self.memory.semantic.match_agents(list(required_skills))
        
        if not matched_agents:
            print(f"   ❌ 未找到匹配的 Agent")
            return {"error": "no_matched_agents"}
        
        print(f"   ✅ 匹配到 {len(matched_agents)} 个 Agent:")
        for agent in matched_agents:
            print(f"      - {agent.get('name', 'N/A')} ({agent.get('role', 'N/A')})")
        
        # 创建 Claw
        claw_id = f"claw_{task_id[:8]}"
        claw = {
            "claw_id": claw_id,
            "task_id": task_id,
            "members": [
                {
                    "agent_id": agent["agent_id"],
                    "name": agent["name"],
                    "role": agent["role"],
                    "emoji": agent.get("emoji", "🤖"),
                    "match_score": 1.0  # TODO: 计算实际匹配分
                }
                for agent in matched_agents
            ],
            "lead_agent": matched_agents[0]["agent_id"] if matched_agents else None,
            "status": "formed",
            "created_at": datetime.now().isoformat()
        }
        
        self.active_claws[claw_id] = claw
        task["assigned_claw"] = claw_id
        task["status"] = "ready"
        
        self.memory.working.update_context("claw", claw)
        self.memory.working.add_message("hub", "claw", f"Claw {claw_id[:8]} 已组建，主导 Agent: {claw['lead_agent']}")
        
        print(f"   🎯 Claw {claw_id[:8]} 已组建")
        print(f"      主导 Agent: {claw['lead_agent']}")
        print(f"      成员数：{len(claw['members'])}")
        
        return claw
    
    # ========== 执行与监控 ==========
    
    def execute_task(self, task_id: str) -> Dict:
        """
        执行任务（真实 Agent 调用）
        
        1. 遍历子任务
        2. 调用对应 Agent 执行
        3. 记录执行日志
        4. 处理异常
        """
        task = self.active_tasks.get(task_id)
        if not task:
            raise ValueError(f"任务 {task_id} 不存在")
        
        claw_id = task.get("assigned_claw")
        if not claw_id:
            raise ValueError(f"任务 {task_id} 未分配 Claw")
        
        claw = self.active_claws.get(claw_id)
        
        print(f"\n🎤 [Hub] 开始执行任务 {task_id[:8]}")
        print(f"   Claw: {claw_id[:8]}")
        print(f"   主导 Agent: {claw.get('lead_agent', 'N/A')}")
        
        # 记录任务开始
        self.logger.start_task(task_id, task["task_desc"], claw)
        
        task["status"] = "executing"
        claw["status"] = "executing"
        
        self.memory.working.update_context("status", "executing")
        self.memory.working.add_message("hub", "claw", "开始执行")
        
        # 执行每个子任务
        execution_results = []
        for i, subtask in enumerate(task["subtasks"]):
            agent_type = subtask.get("agent_type", "content_agent")
            
            # 记录子任务开始
            self.logger.log_subtask_start(task_id, subtask, agent_type)
            
            print(f"   执行子任务 {i+1}/{len(task['subtasks'])}: {subtask['desc'][:40]}...")
            
            try:
                # 真实调用 Agent
                result = self.llm.execute_agent_task(
                    agent_type,
                    subtask["desc"],
                    context=self.memory.working.get_context()
                )
                
                # 记录子任务完成
                self.logger.log_subtask_complete(task_id, subtask["subtask_id"], result)
                
                subtask["status"] = "completed"
                subtask["result"] = result
                execution_results.append(result)
                
                print(f"      ✅ 完成，产物：{result.get('artifacts', [])}")
                
            except Exception as e:
                # 记录异常
                self.logger.log_exception(task_id, str(e))
                subtask["status"] = "failed"
                subtask["error"] = str(e)
                print(f"      ❌ 失败：{e}")
        
        # 所有子任务完成
        task["status"] = "completed"
        claw["status"] = "completed"
        task["execution_results"] = execution_results
        
        print(f"   ✅ 任务执行完成")
        
        return {"task_id": task_id, "status": "completed", "results": execution_results}
    
    # ========== 整合与交付 ==========
    
    def deliver_task(self, task_id: str, result: str, feedback: str = None) -> Dict:
        """
        交付任务
        
        1. Hub 整合最终结果
        2. 记录用户反馈
        3. 触发进化机制
        4. 完成任务
        """
        task = self.active_tasks.get(task_id)
        if not task:
            raise ValueError(f"任务 {task_id} 不存在")
        
        print(f"\n🎤 [Hub] 交付任务 {task_id[:8]}")
        print(f"   结果：{result[:50]}...")
        
        success = feedback is None or "失败" not in feedback
        
        # 更新任务
        task["result"] = result
        task["feedback"] = feedback
        task["status"] = "delivered"
        
        # 记录任务完成
        self.logger.complete_task(task_id, {"result": result, "success": success}, feedback)
        
        # 完成记忆记录
        self.memory.complete_task(success=success, feedback=feedback)
        
        # 触发个体进化
        print(f"\n🧬 触发进化机制...")
        claw_id = task.get("assigned_claw")
        if claw_id:
            claw = self.active_claws.get(claw_id)
            for member in claw.get("members", []):
                agent_id = member.get("agent_id")
                if agent_id:
                    self.evolution.evolve_agent(
                        agent_id,
                        {
                            "task_id": task_id,
                            "success": success,
                            "execution_time": sum(
                                st.get("result", {}).get("execution_time", 0)
                                for st in task.get("subtasks", [])
                            ),
                            "new_skills": [],
                            "collaboration_partners": [
                                m["agent_id"] for m in claw.get("members", [])
                                if m["agent_id"] != agent_id
                            ]
                        },
                        self.memory.semantic
                    )
        
        # 定期触发群体进化（每 5 个任务）
        completed_count = len([t for t in self.active_tasks.values() if t["status"] == "delivered"])
        if completed_count % 5 == 0:
            print("\n🧬 触发群体进化...")
            self.evolution.discover_patterns(
                self.memory.episodic,
                self.memory.semantic
            )
        
        print(f"   ✅ 任务已交付")
        if feedback:
            print(f"   反馈：{feedback}")
        
        return {"task_id": task_id, "status": "delivered", "success": success}
    
    # ========== 系统状态 ==========
    
    def get_status(self) -> Dict:
        """获取系统状态"""
        return {
            "active_tasks": len([t for t in self.active_tasks.values() if t["status"] in ["received", "parsed", "ready", "executing"]]),
            "completed_tasks": len([t for t in self.active_tasks.values() if t["status"] == "delivered"]),
            "active_claws": len([c for c in self.active_claws.values() if c["status"] == "executing"]),
            "available_agents": len(self._list_agents())
        }
    
    def get_task_status(self, task_id: str) -> Optional[Dict]:
        """获取任务状态"""
        return self.active_tasks.get(task_id)


if __name__ == "__main__":
    # 测试 Hub
    hub = ProteusHub()
    
    # 测试任务流程
    task_id = hub.receive_task("为一个小型创业团队生成一周的社交媒体内容计划")
    hub.parse_task(task_id)
    claw = hub.form_claw(task_id)
    hub.execute_task(task_id)
    hub.deliver_task(task_id, "已生成 7 天的社交媒体内容计划", "很好，很满意")
    
    print("\n📊 系统状态:", hub.get_status())
