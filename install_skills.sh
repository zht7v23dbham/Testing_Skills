#!/bin/bash

# 定义源目录和目标目录
SOURCE_DIR="$(pwd)/.trae/skills"
TARGET_DIR="$HOME/.trae/skills"

echo "正在准备安装 Skills 到 TRAE 全局目录..."
echo "源目录: $SOURCE_DIR"
echo "目标目录: $TARGET_DIR"

# 检查源目录是否存在
if [ ! -d "$SOURCE_DIR" ]; then
    echo "错误: 未找到源 Skills 目录 (.trae/skills)"
    exit 1
fi

# 创建目标目录
if [ ! -d "$TARGET_DIR" ]; then
    echo "创建全局 Skills 目录: $TARGET_DIR"
    mkdir -p "$TARGET_DIR"
else
    echo "全局 Skills 目录已存在"
fi

# 复制 Skills
echo "正在复制 Skills..."
cp -R "$SOURCE_DIR"/* "$TARGET_DIR/"

if [ $? -eq 0 ]; then
    echo "✅ 安装成功！"
    echo "已安装的 Skills:"
    ls "$TARGET_DIR"
    echo ""
    echo "请重启 TRAE 或重新加载窗口以使 Skills 生效。"
else
    echo "❌ 安装失败，请检查权限。"
fi
