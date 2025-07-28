#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub排名自动更新脚本
整合数据获取和HTML生成功能
"""

import os
import sys
from datetime import datetime
from github_ranking import GitHubRanking
from generate_html import GitHubStyleGenerator
from deepseek_translator import init_translator

def main():
    """
    主要更新流程
    """
    print("=" * 50)
    print("GitHub仓库排名自动更新开始")
    print(f"更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # 从环境变量获取GitHub Token（可选）
    github_token = os.environ.get('GITHUB_TOKEN')
    if github_token:
        print("✅ 检测到GitHub Token，将使用认证API")
    else:
        print("⚠️  未检测到GitHub Token，使用公共API（有速率限制）")
    
    # 定义要抓取的编程语言
    languages = [
        "JavaScript", "Python", "Java", "TypeScript", "C#", "C++", "C", 
        "Go", "Rust", "Kotlin", "Swift", "Ruby", "PHP", "Scala", 
        "HTML", "CSS", "Shell", "PowerShell", "Dart", "Lua", "R",
        "MATLAB", "Objective-C", "Perl", "Haskell", "Clojure", "Elixir",
        "Julia", "Vim script", "TeX"
    ]
    
    try:
        # 步骤1: 获取排名数据
        print("\n📊 开始获取GitHub仓库数据...")
        ranking = GitHubRanking(token=github_token)
        data = ranking.get_top_repositories(languages=languages, top_n=100)
        
        # 保存原始数据
        print("\n💾 保存数据文件...")
        ranking.save_to_json(data, "github_ranking.json")
        ranking.save_to_csv(data, "data")
        
        # 步骤2: 初始化翻译器并生成HTML页面
        print("\n🔄 初始化DeepSeek翻译器...")
        api_key = "sk-5a2d0c3852424a3ab303dd3ff4c1e667"
        init_translator(api_key)
        
        print("\n🌐 生成HTML展示页面...")
        generator = GitHubStyleGenerator()
        generator.save_github_style_page(data)
        
        # 步骤3: 生成统计信息
        print("\n📈 生成统计报告...")
        total_repos = sum(len(repos) for repos in data.values())
        total_categories = len(data)
        
        print(f"✅ 更新完成!")
        print(f"   - 总分类数: {total_categories}")
        print(f"   - 总仓库数: {total_repos}")
        print(f"   - 数据文件: github_ranking.json")
        print(f"   - 网页文件: docs/index.html")
        
        # 生成更新日志
        with open("update_log.txt", "a", encoding="utf-8") as f:
            f.write(f"{datetime.now().isoformat()}: 成功更新 {total_categories} 个分类，{total_repos} 个仓库\n")
        
    except Exception as e:
        error_msg = f"更新失败: {str(e)}"
        print(f"❌ {error_msg}")
        
        # 记录错误日志
        with open("error_log.txt", "a", encoding="utf-8") as f:
            f.write(f"{datetime.now().isoformat()}: {error_msg}\n")
        
        sys.exit(1)

if __name__ == "__main__":
    main() 