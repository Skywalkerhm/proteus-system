#!/bin/bash
# Proteus System - 清理私人信息脚本

echo "🧹 清理 Proteus System 中的私人信息..."

# 替换绝对路径为相对路径
find . -type f \( -name "*.md" -o -name "*.py" -o -name "*.sh" \) -exec sed -i '' \
  's|<project-root>|<project-root>|g' {} +

find . -type f \( -name "*.md" -o -name "*.py" -o -name "*.sh" \) -exec sed -i '' \
  's|<workspace>|<workspace>|g' {} +

find . -type f \( -name "*.md" -o -name "*.py" -o -name "*.sh" \) -exec sed -i '' \
  's|<user-home>|<user-home>|g' {} +

echo "✅ 清理完成！"
echo ""
echo "📝 已替换："
echo "   <project-root> → <project-root>"
echo "   <workspace> → <workspace>"
echo "   <user-home> → <user-home>"
echo ""
echo "⚠️  请手动检查以下文件是否还有私人信息："
echo "   - README.md"
echo "   - 各类完成报告"
echo "   - 示例脚本"
