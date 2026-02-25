#!/usr/bin/env python3
"""
🧠 Olympus LLM Integration - 智能任务分解与执行

支持：
- OpenAI API (GPT-4)
- Anthropic API (Claude)
- 本地模拟模式（无 API key 时）

安全提示：
- API key 通过环境变量获取
- 不会硬编码在代码中
- 支持 fallback 到模拟模式
"""

import json
import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional


class LLMClient:
    """
    LLM 客户端
    
    支持多种 LLM 提供商，自动 fallback 到模拟模式
    
    环境变量:
        OLYMPUS_LLM_PROVIDER: openai | anthropic | mock (default: mock)
        OPENAI_API_KEY: OpenAI API key
        ANTHROPIC_API_KEY: Anthropic API key
    """
    
    def __init__(self, provider: str = None, api_key: str = None):
        """
        初始化 LLM 客户端
        
        Args:
            provider: LLM 提供商 (openai/anthropic/mock)
            api_key: API key (优先使用环境变量)
        """
        # 从环境变量获取配置
        self.provider = provider or os.getenv("OLYMPUS_LLM_PROVIDER", "mock")
        self.api_key = api_key or self._get_api_key()
        
        # 客户端实例
        self.openai_client = None
        self.anthropic_client = None
        
        # 初始化对应的客户端
        self._initialize_client()
        
        print(f"🧠 LLM Client 已初始化")
        print(f"   提供商：{self.provider}")
        print(f"   API Key: {'已配置' if self.api_key else '未配置 (使用模拟模式)'}")
    
    def _get_api_key(self) -> Optional[str]:
        """安全获取 API key"""
        if self.provider == "openai":
            return os.getenv("OPENAI_API_KEY")
        elif self.provider == "anthropic":
            return os.getenv("ANTHROPIC_API_KEY")
        return None
    
    def _initialize_client(self):
        """初始化 LLM 客户端"""
        if self.provider == "openai" and self.api_key:
            try:
                import openai
                self.openai_client = openai.OpenAI(api_key=self.api_key)
                print("   ✅ OpenAI 客户端已初始化")
            except ImportError:
                print("   ⚠️  openai 包未安装，使用模拟模式")
                self.provider = "mock"
        
        elif self.provider == "anthropic" and self.api_key:
            try:
                import anthropic
                self.anthropic_client = anthropic.Anthropic(api_key=self.api_key)
                print("   ✅ Anthropic 客户端已初始化")
            except ImportError:
                print("   ⚠️  anthropic 包未安装，使用模拟模式")
                self.provider = "mock"
    
    def decompose_task(self, task_desc: str, context: Dict = None) -> List[Dict]:
        """
        使用 LLM 智能分解任务
        
        Args:
            task_desc: 任务描述
            context: 上下文信息
        
        Returns:
            子任务列表
        """
        if self.provider in ["openai", "anthropic"] and self.api_key:
            try:
                return self._llm_decompose(task_desc, context)
            except Exception as e:
                print(f"   ⚠️  LLM 调用失败：{e}")
                print("   🔄 Fallback 到模拟模式")
                return self._mock_decompose(task_desc)
        else:
            return self._mock_decompose(task_desc)
    
    def _llm_decompose(self, task_desc: str, context: Dict = None) -> List[Dict]:
        """使用真实 LLM 分解任务"""
        
        # 构建提示词
        system_prompt = """你是一个专业的任务规划专家。请将复杂任务分解为可执行的子任务。

每个子任务必须包含：
- desc: 任务描述（清晰具体）
- required_skills: 所需技能列表
- agent_type: 适合的 Agent 类型 (athena/hermes/apollo/hephaestus/muse/hestia/themis/aphrodite/echo/daedalus)
- estimated_time: 预估时间（分钟）

只返回 JSON 数组，不要其他内容。"""

        user_prompt = f"""请分解以下任务：

任务：{task_desc}

{'上下文：' + json.dumps(context, ensure_ascii=False) if context else ''}

请返回子任务列表（JSON 数组格式）："""

        if self.provider == "openai" and self.openai_client:
            return self._call_openai(system_prompt, user_prompt)
        elif self.provider == "anthropic" and self.anthropic_client:
            return self._call_anthropic(system_prompt, user_prompt)
        else:
            return self._mock_decompose(task_desc)
    
    def _call_openai(self, system_prompt: str, user_prompt: str) -> List[Dict]:
        """调用 OpenAI API"""
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            content = response.choices[0].message.content.strip()
            
            # 提取 JSON
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            subtasks = json.loads(content)
            
            # 确保格式正确
            return self._validate_subtasks(subtasks)
            
        except Exception as e:
            print(f"OpenAI API 调用失败：{e}")
            raise
    
    def _call_anthropic(self, system_prompt: str, user_prompt: str) -> List[Dict]:
        """调用 Anthropic API"""
        try:
            response = self.anthropic_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2000,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )
            
            content = response.content[0].text.strip()
            
            # 提取 JSON
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            subtasks = json.loads(content)
            
            # 确保格式正确
            return self._validate_subtasks(subtasks)
            
        except Exception as e:
            print(f"Anthropic API 调用失败：{e}")
            raise
    
    def _validate_subtasks(self, subtasks: List[Dict]) -> List[Dict]:
        """验证子任务格式"""
        validated = []
        for st in subtasks:
            validated.append({
                "subtask_id": str(uuid.uuid4())[:8],
                "desc": st.get("desc", "未命名任务"),
                "required_skills": st.get("required_skills", ["general"]),
                "agent_type": st.get("agent_type", "hephaestus"),
                "estimated_time": st.get("estimated_time", 30),
                "status": "pending",
                "llm_generated": True
            })
        return validated
    
    def _mock_decompose(self, task_desc: str) -> List[Dict]:
        """模拟任务分解（fallback）"""
        task_lower = task_desc.lower()
        
        if "社交媒体" in task_desc or "内容计划" in task_desc:
            return self._decompose_social_media(task_desc)
        elif "研究" in task_desc or "报告" in task_desc:
            return self._decompose_research(task_desc)
        elif "代码" in task_desc or "编程" in task_desc:
            return self._decompose_coding(task_desc)
        elif "网站" in task_desc or "开发" in task_desc:
            return self._decompose_web_development(task_desc)
        else:
            return self._decompose_generic(task_desc)
    
    def _decompose_social_media(self, task_desc: str) -> List[Dict]:
        """社交媒体任务分解"""
        return [
            {
                "subtask_id": str(uuid.uuid4())[:8],
                "desc": "调研目标受众和行业趋势",
                "required_skills": ["research", "analysis"],
                "agent_type": "athena",
                "estimated_time": 45,
                "status": "pending",
                "llm_generated": False
            },
            {
                "subtask_id": str(uuid.uuid4())[:8],
                "desc": "制定内容主题和发布日历",
                "required_skills": ["planning", "strategy", "social_media"],
                "agent_type": "apollo",
                "estimated_time": 30,
                "status": "pending",
                "llm_generated": False
            },
            {
                "subtask_id": str(uuid.uuid4())[:8],
                "desc": "撰写每日文案草稿",
                "required_skills": ["writing", "copywriting"],
                "agent_type": "apollo",
                "estimated_time": 90,
                "status": "pending",
                "llm_generated": False
            },
            {
                "subtask_id": str(uuid.uuid4())[:8],
                "desc": "设计视觉风格和配图建议",
                "required_skills": ["design", "visual"],
                "agent_type": "hephaestus",
                "estimated_time": 60,
                "status": "pending",
                "llm_generated": False
            },
            {
                "subtask_id": str(uuid.uuid4())[:8],
                "desc": "质量审核与优化",
                "required_skills": ["review", "quality_control"],
                "agent_type": "themis",
                "estimated_time": 30,
                "status": "pending",
                "llm_generated": False
            }
        ]
    
    def _decompose_research(self, task_desc: str) -> List[Dict]:
        """研究任务分解"""
        return [
            {
                "subtask_id": str(uuid.uuid4())[:8],
                "desc": "定义研究范围和问题",
                "required_skills": ["analysis", "planning"],
                "agent_type": "athena",
                "estimated_time": 30,
                "status": "pending",
                "llm_generated": False
            },
            {
                "subtask_id": str(uuid.uuid4())[:8],
                "desc": "搜集和整理资料",
                "required_skills": ["research", "data_collection"],
                "agent_type": "athena",
                "estimated_time": 90,
                "status": "pending",
                "llm_generated": False
            },
            {
                "subtask_id": str(uuid.uuid4())[:8],
                "desc": "分析和综合信息",
                "required_skills": ["analysis", "synthesis"],
                "agent_type": "athena",
                "estimated_time": 60,
                "status": "pending",
                "llm_generated": False
            },
            {
                "subtask_id": str(uuid.uuid4())[:8],
                "desc": "撰写研究报告",
                "required_skills": ["writing", "reporting"],
                "agent_type": "apollo",
                "estimated_time": 60,
                "status": "pending",
                "llm_generated": False
            }
        ]
    
    def _decompose_coding(self, task_desc: str) -> List[Dict]:
        """编程任务分解"""
        return [
            {
                "subtask_id": str(uuid.uuid4())[:8],
                "desc": "需求分析和架构设计",
                "required_skills": ["analysis", "architecture"],
                "agent_type": "daedalus",
                "estimated_time": 45,
                "status": "pending",
                "llm_generated": False
            },
            {
                "subtask_id": str(uuid.uuid4())[:8],
                "desc": "核心功能实现",
                "required_skills": ["coding", "implementation"],
                "agent_type": "hephaestus",
                "estimated_time": 120,
                "status": "pending",
                "llm_generated": False
            },
            {
                "subtask_id": str(uuid.uuid4())[:8],
                "desc": "单元测试编写",
                "required_skills": ["testing", "quality_control"],
                "agent_type": "themis",
                "estimated_time": 45,
                "status": "pending",
                "llm_generated": False
            },
            {
                "subtask_id": str(uuid.uuid4())[:8],
                "desc": "代码审查和优化",
                "required_skills": ["review", "optimization"],
                "agent_type": "themis",
                "estimated_time": 30,
                "status": "pending",
                "llm_generated": False
            }
        ]
    
    def _decompose_web_development(self, task_desc: str) -> List[Dict]:
        """网站开发任务分解"""
        return [
            {
                "subtask_id": str(uuid.uuid4())[:8],
                "desc": "需求分析和原型设计",
                "required_skills": ["analysis", "design"],
                "agent_type": "daedalus",
                "estimated_time": 60,
                "status": "pending",
                "llm_generated": False
            },
            {
                "subtask_id": str(uuid.uuid4())[:8],
                "desc": "前端页面开发",
                "required_skills": ["frontend", "html", "css", "javascript"],
                "agent_type": "hephaestus",
                "estimated_time": 120,
                "status": "pending",
                "llm_generated": False
            },
            {
                "subtask_id": str(uuid.uuid4())[:8],
                "desc": "后端 API 开发",
                "required_skills": ["backend", "api", "database"],
                "agent_type": "hephaestus",
                "estimated_time": 120,
                "status": "pending",
                "llm_generated": False
            },
            {
                "subtask_id": str(uuid.uuid4())[:8],
                "desc": "数据库设计与实现",
                "required_skills": ["database", "sql"],
                "agent_type": "daedalus",
                "estimated_time": 60,
                "status": "pending",
                "llm_generated": False
            },
            {
                "subtask_id": str(uuid.uuid4())[:8],
                "desc": "部署配置和测试",
                "required_skills": ["devops", "deployment", "testing"],
                "agent_type": "hephaestus",
                "estimated_time": 60,
                "status": "pending",
                "llm_generated": False
            }
        ]
    
    def _decompose_generic(self, task_desc: str) -> List[Dict]:
        """通用任务分解"""
        return [
            {
                "subtask_id": str(uuid.uuid4())[:8],
                "desc": "理解任务需求和目标",
                "required_skills": ["analysis"],
                "agent_type": "athena",
                "estimated_time": 20,
                "status": "pending",
                "llm_generated": False
            },
            {
                "subtask_id": str(uuid.uuid4())[:8],
                "desc": "制定执行计划",
                "required_skills": ["planning"],
                "agent_type": "hermes",
                "estimated_time": 30,
                "status": "pending",
                "llm_generated": False
            },
            {
                "subtask_id": str(uuid.uuid4())[:8],
                "desc": "执行核心任务",
                "required_skills": ["execution"],
                "agent_type": "hephaestus",
                "estimated_time": 90,
                "status": "pending",
                "llm_generated": False
            },
            {
                "subtask_id": str(uuid.uuid4())[:8],
                "desc": "质量检查与交付",
                "required_skills": ["review", "quality_control"],
                "agent_type": "themis",
                "estimated_time": 20,
                "status": "pending",
                "llm_generated": False
            }
        ]
    
    def execute_agent_task(self, agent_type: str, task_desc: str, context: Dict = None) -> Dict:
        """
        执行 Agent 任务
        
        Args:
            agent_type: Agent 类型
            task_desc: 任务描述
            context: 上下文信息
        
        Returns:
            执行结果
        """
        print(f"   🤖 [{agent_type}] 执行：{task_desc[:50]}...")
        
        # 如果有真实 LLM，可以调用它生成内容
        if self.provider in ["openai", "anthropic"] and self.api_key:
            try:
                return self._llm_execute(agent_type, task_desc, context)
            except Exception as e:
                print(f"   ⚠️  LLM 执行失败：{e}")
        
        # Fallback 到模拟执行
        return self._mock_execute(agent_type, task_desc)
    
    def _llm_execute(self, agent_type: str, task_desc: str, context: Dict = None) -> Dict:
        """使用真实 LLM 执行任务"""
        
        # 构建提示词
        system_prompt = f"""你是一个专业的 {agent_type} Agent。
请根据任务描述完成工作，并返回结构化的结果。

返回格式（JSON）：
{{
    "success": true/false,
    "output": "任务输出的详细描述",
    "execution_time": 执行时间（分钟）,
    "artifacts": ["产出的文件列表"],
    "logs": ["执行日志"],
    "confidence": 置信度 (0.0-1.0)
}}

请确保输出专业、详细且可执行。"""

        user_prompt = f"""请完成以下任务：

任务描述：{task_desc}
{'上下文：' + json.dumps(context, ensure_ascii=False) if context else ''}

请返回 JSON 格式的执行结果："""

        if self.provider == "openai" and self.openai_client:
            try:
                response = self.openai_client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.7,
                    max_tokens=2000
                )
                
                content = response.choices[0].message.content.strip()
                result = json.loads(content)
                
                # 确保必要字段存在
                if "success" not in result:
                    result["success"] = True
                if "output" not in result:
                    result["output"] = f"[{agent_type}] 完成任务：{task_desc[:50]}"
                if "execution_time" not in result:
                    result["execution_time"] = 30
                if "artifacts" not in result:
                    result["artifacts"] = []
                if "logs" not in result:
                    result["logs"] = [f"执行 {task_desc[:30]}..."]
                if "confidence" not in result:
                    result["confidence"] = 0.9
                
                return result
                
            except Exception as e:
                print(f"   ⚠️  LLM 执行失败：{e}")
                print("   🔄 Fallback 到模拟执行")
                return self._mock_execute(agent_type, task_desc)
        
        elif self.provider == "anthropic" and self.anthropic_client:
            try:
                response = self.anthropic_client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=2000,
                    system=system_prompt,
                    messages=[{"role": "user", "content": user_prompt}]
                )
                
                content = response.content[0].text.strip()
                result = json.loads(content)
                
                # 确保必要字段存在
                if "success" not in result:
                    result["success"] = True
                if "output" not in result:
                    result["output"] = f"[{agent_type}] 完成任务：{task_desc[:50]}"
                if "execution_time" not in result:
                    result["execution_time"] = 30
                if "artifacts" not in result:
                    result["artifacts"] = []
                if "logs" not in result:
                    result["logs"] = [f"执行 {task_desc[:30]}..."]
                if "confidence" not in result:
                    result["confidence"] = 0.9
                
                return result
                
            except Exception as e:
                print(f"   ⚠️  LLM 执行失败：{e}")
                print("   🔄 Fallback 到模拟执行")
                return self._mock_execute(agent_type, task_desc)
        
        else:
            return self._mock_execute(agent_type, task_desc)
    
    def _mock_execute(self, agent_type: str, task_desc: str) -> Dict:
        """模拟执行"""
        # 根据 Agent 类型生成不同的模拟结果
        artifacts_map = {
            "athena": ["调研报告.md", "数据分析.xlsx"],
            "apollo": ["内容日历.xlsx", "文案草稿.docx", "视觉指南.pdf"],
            "hephaestus": ["main.py", "tests.py", "README.md"],
            "themis": ["审核报告.md", "优化建议列表.txt"],
            "hermes": ["架构设计.md", "技术方案.docx"],
            "daedalus": ["system_design.md", "api_docs.md"],
            "muse": ["文章草稿.md", "灵感笔记.txt"],
            "hestia": ["任务清单.xlsx", "质量报告.md"],
            "aphrodite": ["营销策略.md", "品牌指南.pdf"]
        }
        
        artifacts = artifacts_map.get(agent_type, ["output.txt"])
        
        return {
            "success": True,
            "output": f"[{agent_type}] 完成任务：{task_desc[:50]}",
            "execution_time": 30,
            "artifacts": artifacts,
            "logs": [f"执行 {task_desc[:30]}..."]
        }


class ExecutionLogger:
    """执行日志记录器"""
    
    def __init__(self, log_path: Path):
        self.log_path = log_path
        self.log_path.mkdir(parents=True, exist_ok=True)
        print(f"📝 执行日志系统已初始化：{log_path}")
    
    def start_task(self, task_id: str, task_desc: str, claw_info: Dict):
        log_entry = {
            "event": "task_start",
            "task_id": task_id,
            "task_desc": task_desc,
            "claw_info": claw_info,
            "timestamp": datetime.now().isoformat()
        }
        self._save_log(task_id, log_entry)
    
    def log_subtask_start(self, task_id: str, subtask: Dict, agent_id: str):
        log_entry = {
            "event": "subtask_start",
            "subtask_id": subtask.get("subtask_id"),
            "subtask_desc": subtask.get("desc"),
            "agent_id": agent_id,
            "timestamp": datetime.now().isoformat()
        }
        self._save_log(task_id, log_entry)
    
    def log_subtask_complete(self, task_id: str, subtask_id: str, result: Dict):
        log_entry = {
            "event": "subtask_complete",
            "subtask_id": subtask_id,
            "result": result,
            "timestamp": datetime.now().isoformat()
        }
        self._save_log(task_id, log_entry)
    
    def log_decision(self, task_id: str, decision_type: str, decision: str, rationale: str):
        log_entry = {
            "event": "decision",
            "decision_type": decision_type,
            "decision": decision,
            "rationale": rationale,
            "timestamp": datetime.now().isoformat()
        }
        self._save_log(task_id, log_entry)
    
    def log_exception(self, task_id: str, error: str, resolution: str = None):
        log_entry = {
            "event": "exception",
            "error": error,
            "resolution": resolution,
            "timestamp": datetime.now().isoformat()
        }
        self._save_log(task_id, log_entry)
    
    def complete_task(self, task_id: str, result: Dict, feedback: str = None):
        log_entry = {
            "event": "task_complete",
            "result": result,
            "feedback": feedback,
            "timestamp": datetime.now().isoformat()
        }
        self._save_log(task_id, log_entry)
    
    def _save_log(self, task_id: str, log_entry: Dict):
        log_file = self.log_path / f"{task_id}.jsonl"
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
    
    def get_task_logs(self, task_id: str) -> List[Dict]:
        log_file = self.log_path / f"{task_id}.jsonl"
        if not log_file.exists():
            return []
        
        logs = []
        with open(log_file, 'r', encoding='utf-8') as f:
            for line in f:
                logs.append(json.loads(line))
        return logs


if __name__ == "__main__":
    # 测试 LLM 集成
    print("🧠 Olympus LLM Integration Test")
    print("=" * 50)
    
    # 初始化客户端
    llm = LLMClient()
    
    # 测试任务分解
    task_desc = "为一个小型创业团队生成一周的社交媒体内容计划"
    print(f"\n📋 任务：{task_desc}")
    
    subtasks = llm.decompose_task(task_desc)
    print(f"\n✅ 分解为 {len(subtasks)} 个子任务:")
    for i, st in enumerate(subtasks, 1):
        llm_generated = "🤖 LLM" if st.get("llm_generated") else "💾 Mock"
        print(f"   {i}. {st['desc']} ({st['agent_type']}, {st['estimated_time']}min) [{llm_generated}]")
    
    print("\n✅ 测试完成")
