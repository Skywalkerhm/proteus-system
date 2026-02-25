#!/usr/bin/env python3
"""
🔍 Proteus System 独立部署检查脚本

检查项目：
1. 隐私信息（路径、API key、个人信息）
2. 依赖配置
3. 环境变量
4. 示例数据
5. 文档完整性

使用方式：
python3 scripts/deployment_check.py
"""

import os
import sys
import json
from pathlib import Path

# 颜色输出
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

def check_privacy_info():
    """检查隐私信息"""
    print(f"\n{BLUE}🔒 检查隐私信息...{RESET}")
    
    project_root = Path(__file__).parent.parent
    issues = []
    
    # 检查敏感路径
    sensitive_patterns = [
        "/Users/your-username",  # 示例：检查用户目录
        "/Volumes/YourDisk",     # 示例：检查挂载点
        "your-project-name"      # 示例：检查项目名
    ]
    
    for pattern in sensitive_patterns:
        # 排除检查脚本自身和文档中的示例
        result = os.popen(f"grep -r '{pattern}' --include='*.py' --include='*.md' --include='*.json' {project_root} 2>/dev/null | grep -v 'deployment_check.py' | grep -v 'DEPLOYMENT_GUIDE.md'").read()
        if result:
            issues.append(f"发现敏感路径 '{pattern}':\n{result[:200]}")
    
    if issues:
        print(f"{RED}❌ 发现隐私信息泄露风险:{RESET}")
        for issue in issues[:3]:  # 只显示前 3 个
            print(f"  - {issue[:100]}...")
        return False
    else:
        print(f"{GREEN}✅ 未发现隐私信息{RESET}")
        return True

def check_env_config():
    """检查环境配置"""
    print(f"\n{BLUE}⚙️  检查环境配置...{RESET}")
    
    project_root = Path(__file__).parent.parent
    env_example = project_root / ".env.example"
    
    if not env_example.exists():
        print(f"{RED}❌ 缺少 .env.example 文件{RESET}")
        return False
    
    # 检查 .env.example 是否包含真实 key
    with open(env_example, 'r') as f:
        content = f.read()
        if 'sk-' in content and 'your-api-key' not in content:
            print(f"{RED}❌ .env.example 包含真实 API key{RESET}")
            return False
    
    print(f"{GREEN}✅ 环境配置安全{RESET}")
    return True

def check_dependencies():
    """检查依赖配置"""
    print(f"\n{BLUE}📦 检查依赖配置...{RESET}")
    
    project_root = Path(__file__).parent.parent
    requirements = project_root / "requirements.txt"
    
    if not requirements.exists():
        print(f"{RED}❌ 缺少 requirements.txt{RESET}")
        return False
    
    with open(requirements, 'r') as f:
        content = f.read()
        required_packages = ['requests', 'openai', 'anthropic']
        missing = []
        
        for pkg in required_packages:
            if pkg not in content.lower():
                missing.append(pkg)
        
        if missing:
            print(f"{YELLOW}⚠️  缺少推荐依赖：{', '.join(missing)}{RESET}")
            return False
    
    print(f"{GREEN}✅ 依赖配置完整{RESET}")
    return True

def check_demo_data():
    """检查演示数据"""
    print(f"\n{BLUE}📊 检查演示数据...{RESET}")
    
    project_root = Path(__file__).parent.parent
    
    # 检查 Agent 配置文件
    agents_path = project_root / "memory" / "semantic" / "agents"
    if not agents_path.exists():
        print(f"{RED}❌ 缺少 Agent 配置文件{RESET}")
        return False
    
    agent_files = list(agents_path.glob("*.json"))
    if len(agent_files) < 5:
        print(f"{YELLOW}⚠️  Agent 配置文件过少：{len(agent_files)} 个{RESET}")
        return False
    
    # 检查是否有隐私信息
    for agent_file in agent_files:
        with open(agent_file, 'r') as f:
            data = json.load(f)
            if isinstance(data, dict):
                # 检查敏感字段
                if 'email' in data or 'phone' in data or 'password' in data:
                    print(f"{RED}❌ Agent 配置包含敏感信息：{agent_file.name}{RESET}")
                    return False
    
    print(f"{GREEN}✅ 演示数据安全 ({len(agent_files)} 个 Agent){RESET}")
    return True

def check_documentation():
    """检查文档完整性"""
    print(f"\n{BLUE}📚 检查文档完整性...{RESET}")
    
    project_root = Path(__file__).parent.parent
    required_docs = [
        "README.md",
        "LICENSE",
        ".env.example",
        "requirements.txt"
    ]
    
    missing = []
    for doc in required_docs:
        if not (project_root / doc).exists():
            missing.append(doc)
    
    if missing:
        print(f"{RED}❌ 缺少必要文档：{', '.join(missing)}{RESET}")
        return False
    
    print(f"{GREEN}✅ 文档完整{RESET}")
    return True

def check_llm_fallback():
    """检查 LLM fallback 机制"""
    print(f"\n{BLUE}🤖 检查 LLM fallback 机制...{RESET}")
    
    project_root = Path(__file__).parent.parent
    llm_file = project_root / "core" / "llm_integration.py"
    
    if not llm_file.exists():
        print(f"{RED}❌ 缺少 LLM 集成模块{RESET}")
        return False
    
    with open(llm_file, 'r') as f:
        content = f.read()
        
        # 检查是否有模拟模式
        if 'mock' not in content.lower() and 'fallback' not in content.lower():
            print(f"{YELLOW}⚠️  未检测到 LLM fallback 机制{RESET}")
            return False
        
        # 检查环境变量获取
        if 'os.getenv' not in content:
            print(f"{YELLOW}⚠️  未使用环境变量获取 API key{RESET}")
            return False
    
    print(f"{GREEN}✅ LLM fallback 机制正常{RESET}")
    return True

def main():
    print("=" * 70)
    print("🔍 Proteus System 独立部署检查")
    print("=" * 70)
    
    results = {
        "隐私信息": check_privacy_info(),
        "环境配置": check_env_config(),
        "依赖配置": check_dependencies(),
        "演示数据": check_demo_data(),
        "文档完整性": check_documentation(),
        "LLM fallback": check_llm_fallback()
    }
    
    print("\n" + "=" * 70)
    print("📊 检查结果汇总")
    print("=" * 70)
    
    for item, passed in results.items():
        status = f"{GREEN}✅{RESET}" if passed else f"{RED}❌{RESET}"
        print(f"{status} {item}")
    
    passed_count = sum(results.values())
    total_count = len(results)
    
    print(f"\n通过率：{passed_count}/{total_count}")
    
    if passed_count == total_count:
        print(f"\n{GREEN}🎉 所有检查通过！系统可以安全部署。{RESET}")
        return 0
    else:
        print(f"\n{RED}⚠️  存在 {total_count - passed_count} 个问题，请修复后重新部署。{RESET}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
