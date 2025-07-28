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
    
    # 改进GitHub token处理
    github_token = os.environ.get('GITHUB_TOKEN')
    if not github_token:
        print("⚠️  警告：未找到GITHUB_TOKEN环境变量")
        print("   将使用无token模式（可能遇到速率限制）")
        github_token = None  # 允许无token运行
    else:
        print("✅ 找到GitHub Token，使用认证模式")
    
    # GitHub仓库的语言列表
    languages = [
        'JavaScript', 'Python', 'Java', 'TypeScript', 'C#', 'C++', 'C', 'Go', 'Rust',
        'Kotlin', 'Swift', 'Ruby', 'PHP', 'Scala', 'HTML', 'CSS', 'Shell', 'PowerShell',
        'Dart', 'Lua', 'R', 'MATLAB', 'Objective-C', 'Perl', 'Haskell', 'Clojure', 
        'Elixir', 'Julia', 'Vim script', 'TeX'
    ]
    
    try:
        # 步骤1: 获取排名数据
        print("\n📊 开始获取GitHub仓库数据...")
        ranking = GitHubRanking(token=github_token)
        data = ranking.get_top_repositories(languages=languages, top_n=100)
        
        # 新增：获取两种趋势数据（优先成长最快）
        print("\n📈 获取本周成长最快项目...")
        growing_data = ranking.get_fastest_growing_repos(top_n=20)
        data['📈 本周成长最快'] = growing_data
        
        print("\n🆕 获取当周热门新项目...")
        new_trending_data = ranking.get_trending_new_repos(top_n=20)
        data['🆕 当周热门新项目'] = new_trending_data
        
        # 保存原始数据
        print("\n💾 保存数据文件...")
        ranking.save_to_json(data, "github_ranking.json")
        ranking.save_to_csv(data, "data")
        
        # 步骤2: 初始化翻译器并生成HTML页面
        print("\n🔄 初始化DeepSeek翻译器...")
        api_key = os.environ.get("DEEPSEEK_API_KEY")
        if not api_key:
            print("⚠️  警告：未找到DEEPSEEK_API_KEY环境变量，翻译功能将不可用")
            api_key = None
        else:
            print("✅ 找到DeepSeek API密钥，启用翻译功能")
        
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