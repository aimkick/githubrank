#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from deepseek_translator import init_translator, translate_text

# 初始化翻译器
api_key = "sk-5a2d0c3852424a3ab303dd3ff4c1e667"
init_translator(api_key)

# 测试用例
test_cases = [
    "All Algorithms implemented in Python",
    "Design patterns implemented in Java", 
    "Everything you need to know to get the job.",
    "A collection of useful .gitignore templates",
    "Fast, simple & powerful blog framework, powered by Node.js.",
    "The most popular HTML, CSS, and JavaScript framework for developing responsive, mobile first projects on the web.",
    "⚡️ The fastest way to build React UI",
    "Command-line program to download videos from YouTube.com and other video sites"
]

print("=" * 70)
print("DeepSeek API 翻译测试")
print("=" * 70)

for i, text in enumerate(test_cases, 1):
    print(f"\n{i}. 原文: {text}")
    translated = translate_text(text)
    print(f"   译文: {translated}")

print("\n" + "=" * 70) 