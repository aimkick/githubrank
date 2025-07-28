#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 修复display_count逻辑
with open('generate_html.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 查找并替换错误的字符
import re

# 修复中文字符编码问题
content = re.sub(
    r"display_count = 20 if category in \[.*?\] else 10",
    "display_count = 20 if category in ['总体-Stars', '总体-Forks'] else 10",
    content
)

with open('generate_html.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ 修复display_count逻辑完成') 