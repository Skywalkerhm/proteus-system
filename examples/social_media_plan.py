#!/usr/bin/env python3
"""
📱 示例：社交媒体内容计划生成

演示 Proteus System 如何完成社交媒体内容策划任务
"""

from core.hub import ProteusHub

def main():
    # 初始化 Hub
    hub = ProteusHub()
    
    # 接收任务
    task_id = hub.receive_task(
        "为一个小型创业团队生成一周的社交媒体内容计划",
        user_id="demo_user",
        priority="normal"
    )
    
    # 解析任务
    print("\n📋 任务解析:")
    parse_result = hub.parse_task(task_id)
    
    # 组建 Claw
    print("\n🤝 组建 Claw:")
    claw = hub.form_claw(task_id)
    
    # 执行任务
    print("\n⚙️  执行任务:")
    exec_result = hub.execute_task(task_id)
    
    # 交付任务
    print("\n✅ 交付任务:")
    deliver_result = hub.deliver_task(
        task_id,
        result="已生成 7 天社交媒体内容计划，包含 14 条文案和视觉指南",
        feedback="非常好，内容质量高，可以直接使用"
    )
    
    # 查看进化结果
    print("\n🧬 进化结果:")
    status = hub.get_status()
    print(f"   完成任务：{status['completed_tasks']} 个")
    print(f"   可用 Agent: {status['available_agents']} 个")

if __name__ == "__main__":
    main()
