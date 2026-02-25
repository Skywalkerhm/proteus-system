#!/usr/bin/env python3
"""
🧬 Proteus System - 快速启动与演示

演示任务：为一个小型创业团队生成一周的社交媒体内容计划
"""

import sys
from pathlib import Path

# 添加核心模块路径
sys.path.insert(0, str(Path(__file__).parent / "core"))

from hub import ProteusHub

def main():
    print("=" * 70)
    print("🧬 Proteus System - Genesis Demo")
    print("=" * 70)
    print()
    
    # 初始化 Hub
    hub = ProteusHub()
    
    print("\n" + "=" * 70)
    print("📋 演示任务：为一个小型创业团队生成一周的社交媒体内容计划")
    print("=" * 70)
    
    # 1. 任务接收
    task_id = hub.receive_task(
        "为一个小型创业团队生成一周的社交媒体内容计划",
        user_id="demo_user",
        priority="normal"
    )
    
    # 2. 任务解析
    parse_result = hub.parse_task(task_id)
    
    # 3. 动态组队
    claw = hub.form_claw(task_id)
    
    # 4. 任务执行
    exec_result = hub.execute_task(task_id)
    
    # 5. 任务交付
    deliver_result = hub.deliver_task(
        task_id,
        result="已生成 7 天社交媒体内容计划，包含小红书、微博、抖音三个平台",
        feedback="很好，内容质量高，可以直接使用"
    )
    
    # 6. 系统状态
    print("\n" + "=" * 70)
    print("📊 系统状态")
    print("=" * 70)
    status = hub.get_status()
    for key, value in status.items():
        print(f"   {key}: {value}")
    
    print("\n" + "=" * 70)
    print("✅ Demo 完成！")
    print("=" * 70)
    print()
    print("📁 查看详细信息:")
    print(f"   - 系统文档：{hub.base_path}/README.md")
    print(f"   - 初始化日志：{hub.base_path}/logs/initialization_log.md")
    print(f"   - 记忆存储：{hub.base_path}/memory/")
    print()

if __name__ == "__main__":
    main()
