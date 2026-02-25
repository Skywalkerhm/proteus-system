#!/bin/bash
# Proteus System - 快速发布到 GitHub 脚本

echo "🚀 Proteus System - GitHub 发布助手"
echo "=================================="
echo ""

# 检查 Git 是否安装
if ! command -v git &> /dev/null; then
    echo "❌ 错误：Git 未安装"
    echo "请先安装 Git: https://git-scm.com/"
    exit 1
fi

# 获取 GitHub 用户名
read -p "请输入你的 GitHub 用户名：" GITHUB_USERNAME

if [ -z "$GITHUB_USERNAME" ]; then
    echo "❌ 错误：GitHub 用户名不能为空"
    exit 1
fi

echo ""
echo "📝 准备发布到：https://github.com/$GITHUB_USERNAME/proteus-system"
echo ""

# 初始化 Git
echo "🔧 初始化 Git..."
git init
git add .
git commit -m "feat: initial release v1.0.0"

# 添加远程仓库
echo "🔗 添加远程仓库..."
git remote add origin https://github.com/$GITHUB_USERNAME/proteus-system.git

# 推送
echo "📤 推送到 GitHub..."
git branch -M main
git push -u origin main

echo ""
echo "✅ 发布成功！"
echo ""
echo "📦 项目地址：https://github.com/$GITHUB_USERNAME/proteus-system"
echo ""
echo "🎉 下一步:"
echo "1. 访问上面的 GitHub 地址"
echo "2. 完善 README 中的用户名"
echo "3. 创建第一个 Release"
echo "4. 分享给你的朋友们！"
echo ""
