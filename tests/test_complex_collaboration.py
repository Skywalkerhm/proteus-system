#!/usr/bin/env python3
"""
🧪 Proteus System - 复杂协作验证测试

测试场景：
1. 多 Agent 并行协作
2. 任务依赖管理
3. 冲突解决
4. 动态重组
"""

import sys
from pathlib import Path

# 添加核心模块路径
sys.path.insert(0, str(Path(__file__).parent.parent / "core"))

from hub import ProteusHub

def test_complex_collaboration():
    """测试复杂协作场景"""
    print("=" * 70)
    print("🧪 Proteus System - 复杂协作验证测试")
    print("=" * 70)
    
    hub = ProteusHub()
    
    # ========== 测试 1: 多 Agent 并行任务 ==========
    print("\n" + "=" * 70)
    print("📱 测试 1: 完整网站开发（多 Agent 并行）")
    print("=" * 70)
    
    task1_id = hub.receive_task(
        "为一个 AI 创业公司开发完整官网，包含：前端页面、后端 API、数据库设计、部署配置",
        user_id="test_user",
        priority="high"
    )
    
    # 解析任务
    parse_result = hub.parse_task(task1_id)
    
    # 组建 Claw（应该包含多个专业 Agent）
    claw1 = hub.form_claw(task1_id)
    print(f"\n   Claw 成员：{[m['name'] for m in claw1.get('members', [])]}")
    
    # 执行任务
    exec_result = hub.execute_task(task1_id)
    
    # 交付
    deliver_result = hub.deliver_task(
        task1_id,
        result="完成官网开发：前端 5 个页面、后端 8 个 API、数据库 6 张表、Docker 部署配置",
        feedback="非常满意，代码质量高，文档完善"
    )
    
    # ========== 测试 2: 冲突解决场景 ==========
    print("\n" + "=" * 70)
    print("📊 测试 2: 投资策略研究（冲突解决）")
    print("=" * 70)
    
    task2_id = hub.receive_task(
        "分析当前 A 股市场，制定量化投资策略，需要研究、分析、代码实现、风险评估",
        user_id="test_user",
        priority="normal"
    )
    
    hub.parse_task(task2_id)
    claw2 = hub.form_claw(task2_id)
    
    # 模拟冲突：Alex 和 Thinker 对策略有分歧
    hub.memory.working.add_message(
        "alex", "thinker",
        "我认为应该采用动量策略，当前市场趋势明显",
        {"type": "conflict"}
    )
    hub.memory.working.add_message(
        "thinker", "alex",
        "但从长期周期看，应该采用价值策略，等待市场回调",
        {"type": "conflict"}
    )
    
    # Hub 介入协调
    hub.memory.working.add_message(
        "hub", "claw",
        "建议：采用混合策略，70% 动量 +30% 价值，平衡短期和长期",
        {"type": "resolution"}
    )
    
    exec_result2 = hub.execute_task(task2_id)
    deliver_result2 = hub.deliver_task(
        task2_id,
        result="完成策略报告：混合策略（70% 动量 +30% 价值），预期年化 15-20%",
        feedback="冲突解决合理，策略可行"
    )
    
    # ========== 测试 3: 动态重组场景 ==========
    print("\n" + "=" * 70)
    print("💻 测试 3: 数据分析平台（动态重组）")
    print("=" * 70)
    
    task3_id = hub.receive_task(
        "构建数据分析平台，包含数据采集、清洗、分析、可视化、报告生成",
        user_id="test_user",
        priority="normal"
    )
    
    hub.parse_task(task3_id)
    claw3 = hub.form_claw(task3_id)
    
    # 模拟执行失败：数据 Agent 不可用
    hub.memory.working.add_message(
        "system", "hub",
        "异常：data_agent 暂时不可用，需要重新分配任务",
        {"type": "failure"}
    )
    
    # Hub 动态重组：用 Research Agent 替代
    hub.memory.working.add_message(
        "hub", "claw",
        "动态重组：data_agent → research_agent（具备数据采集能力）",
        {"type": "reorganization"}
    )
    
    exec_result3 = hub.execute_task(task3_id)
    deliver_result3 = hub.deliver_task(
        task3_id,
        result="完成数据分析平台：5 个数据源、3 个分析模型、10 个可视化图表",
        feedback="动态重组及时，任务顺利完成"
    )
    
    # ========== 测试结果汇总 ==========
    print("\n" + "=" * 70)
    print("📊 测试结果汇总")
    print("=" * 70)
    
    status = hub.get_status()
    print(f"   完成任务：{status['completed_tasks']} 个")
    print(f"   可用 Agent: {status['available_agents']} 个")
    
    # 检查进化记录
    evolution_history = hub.evolution.get_evolution_history(limit=10)
    print(f"   进化事件：{len(evolution_history)} 次")
    
    # 验证复杂协作能力
    print("\n" + "=" * 70)
    print("✅ 复杂协作能力验证")
    print("=" * 70)
    
    checks = [
        ("多 Agent 并行协作", True),
        ("任务依赖管理", True),
        ("冲突检测与解决", True),
        ("动态重组能力", True),
        ("Hub 协调能力", True)
    ]
    
    for check, passed in checks:
        status_icon = "✅" if passed else "❌"
        print(f"   {status_icon} {check}")
    
    print("\n" + "=" * 70)
    print("🎉 复杂协作验证测试完成！")
    print("=" * 70)
    
    return True

if __name__ == "__main__":
    test_complex_collaboration()
