#!/usr/bin/env python3
"""
🧬 Proteus System - Evolution Phase 演示

演示完整功能：
1. LLM 智能任务分解
2. 真实 Agent 执行
3. 执行日志记录
4. 个体进化 + 群体进化
"""

import sys
from pathlib import Path

# 添加核心模块路径
sys.path.insert(0, str(Path(__file__).parent / "core"))

from hub import ProteusHub

def run_demo():
    print("=" * 70)
    print("🧬 Proteus System - Evolution Phase Demo")
    print("=" * 70)
    print()
    
    # 初始化 Hub（增强版）
    hub = ProteusHub()
    
    # ========== 演示任务 1: 社交媒体内容计划 ==========
    print("\n" + "=" * 70)
    print("📱 任务 1: 社交媒体内容计划")
    print("=" * 70)
    
    task1_id = hub.receive_task(
        "为一个小型创业团队生成一周的社交媒体内容计划",
        user_id="demo_user",
        priority="normal"
    )
    
    hub.parse_task(task1_id)
    claw1 = hub.form_claw(task1_id)
    hub.execute_task(task1_id)
    hub.deliver_task(
        task1_id,
        result="已生成 7 天社交媒体内容计划，包含 14 条文案和视觉指南",
        feedback="非常好，内容质量高，可以直接使用"
    )
    
    # ========== 演示任务 2: 市场研究报告 ==========
    print("\n" + "=" * 70)
    print("📊 任务 2: 市场研究报告")
    print("=" * 70)
    
    task2_id = hub.receive_task(
        "为中国新能源汽车市场写一份研究报告",
        user_id="demo_user",
        priority="high"
    )
    
    hub.parse_task(task2_id)
    claw2 = hub.form_claw(task2_id)
    hub.execute_task(task2_id)
    hub.deliver_task(
        task2_id,
        result="完成 30 页研究报告，包含市场规模、竞争格局、趋势预测",
        feedback="很好，数据详实，分析深入"
    )
    
    # ========== 演示任务 3: Python 代码开发 ==========
    print("\n" + "=" * 70)
    print("💻 任务 3: Python 代码开发")
    print("=" * 70)
    
    task3_id = hub.receive_task(
        "用 Python 写一个数据分析工具，处理 CSV 文件并生成可视化报告",
        user_id="demo_user",
        priority="normal"
    )
    
    hub.parse_task(task3_id)
    claw3 = hub.form_claw(task3_id)
    hub.execute_task(task3_id)
    hub.deliver_task(
        task3_id,
        result="完成数据分析工具，包含数据清洗、分析、可视化功能",
        feedback="代码质量不错，但需要增加更多注释"
    )
    
    # ========== 系统状态与进化总结 ==========
    print("\n" + "=" * 70)
    print("📊 系统状态")
    print("=" * 70)
    status = hub.get_status()
    for key, value in status.items():
        print(f"   {key}: {value}")
    
    # 查看进化历史
    print("\n" + "=" * 70)
    print("🧬 进化历史")
    print("=" * 70)
    evolution_history = hub.evolution.get_evolution_history(limit=10)
    for entry in evolution_history:
        print(f"   {entry['event']}: {entry['timestamp'][:19]}")
        if 'data' in entry:
            data = entry['data']
            if 'success_rate' in data:
                print(f"      成功率：{data['success_rate']:.0%}")
            if 'patterns_found' in data:
                print(f"      发现模式：{data['patterns_found']} 个")
    
    # 查看 Agent 进化情况
    print("\n" + "=" * 70)
    print("🤖 Agent 进化情况")
    print("=" * 70)
    for agent_id in ["content_agent", "research_agent", "code_agent", "review_agent"]:
        profile = hub.memory.semantic.get_agent_profile(agent_id)
        if profile:
            stats = profile.get("stats", {})
            print(f"   {profile.get('name', agent_id)}:")
            print(f"      总任务：{stats.get('total', 0)}")
            print(f"      成功率：{stats.get('success_rate', 0):.0%}")
            print(f"      平均时间：{stats.get('avg_time', 0)}min")
    
    print("\n" + "=" * 70)
    print("✅ Evolution Phase Demo 完成！")
    print("=" * 70)
    print()
    print("📁 查看详细信息:")
    print(f"   - 执行日志：{hub.base_path / 'logs' / 'tasks'}")
    print(f"   - 进化日志：{hub.base_path / 'evolution' / 'evolution_log.jsonl'}")
    print(f"   - 场景记忆：{hub.base_path / 'memory' / 'episodic'}")
    print()

if __name__ == "__main__":
    run_demo()
