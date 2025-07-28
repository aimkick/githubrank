#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub API调试脚本
检查API返回的数据格式和内容
"""

import requests
import json
import os
from datetime import datetime

def debug_github_api():
    """
    调试GitHub API，检查返回的数据
    """
    print("🔍 GitHub API 调试开始")
    print("=" * 50)
    
    # 获取GitHub Token
    github_token = os.environ.get('GITHUB_TOKEN')
    
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "GitHub-Ranking-Debug"
    }
    
    if github_token:
        headers["Authorization"] = f"token {github_token}"
        print("✅ 使用GitHub Token认证")
    else:
        print("⚠️  未使用GitHub Token，可能遇到API限制")
    
    # 测试简单查询
    print("\n📊 测试API查询...")
    
    try:
        # 查询最受欢迎的仓库
        url = "https://api.github.com/search/repositories"
        params = {
            "q": "stars:>100000",
            "sort": "stars",
            "order": "desc",
            "per_page": 5
        }
        
        response = requests.get(url, headers=headers, params=params)
        print(f"HTTP状态码: {response.status_code}")
        print(f"API限制: {response.headers.get('X-RateLimit-Remaining', 'N/A')}/{response.headers.get('X-RateLimit-Limit', 'N/A')}")
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"\n📈 API响应数据:")
            print(f"总数量: {data.get('total_count', 0)}")
            print(f"返回数量: {len(data.get('items', []))}")
            
            # 检查前3个仓库的详细信息
            for i, repo in enumerate(data.get('items', [])[:3], 1):
                print(f"\n🔸 仓库 {i}: {repo.get('full_name', 'N/A')}")
                print(f"  名称: {repo.get('name', 'N/A')}")
                print(f"  描述: {repo.get('description', 'N/A')}")
                print(f"  语言: {repo.get('language', 'N/A')}")
                print(f"  Stars: {repo.get('stargazers_count', 'N/A')}")
                print(f"  Forks: {repo.get('forks_count', 'N/A')}")
                print(f"  创建时间: {repo.get('created_at', 'N/A')}")
                print(f"  更新时间: {repo.get('updated_at', 'N/A')}")
                print(f"  链接: {repo.get('html_url', 'N/A')}")
                
                # 检查owner信息
                owner = repo.get('owner', {})
                print(f"  作者: {owner.get('login', 'N/A')}")
        
        else:
            print(f"❌ API请求失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")
    
    print("\n" + "=" * 50)
    print("🔍 调试完成")

def test_specific_repo():
    """
    测试获取特定仓库的详细信息
    """
    print("\n🎯 测试特定仓库API...")
    
    github_token = os.environ.get('GITHUB_TOKEN')
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "GitHub-Ranking-Debug"
    }
    
    if github_token:
        headers["Authorization"] = f"token {github_token}"
    
    # 测试freeCodeCamp仓库
    try:
        url = "https://api.github.com/repos/freeCodeCamp/freeCodeCamp"
        response = requests.get(url, headers=headers)
        
        print(f"HTTP状态码: {response.status_code}")
        
        if response.status_code == 200:
            repo = response.json()
            print(f"\n📊 freeCodeCamp仓库信息:")
            print(f"  名称: {repo.get('name')}")
            print(f"  完整名称: {repo.get('full_name')}")
            print(f"  描述: {repo.get('description')}")
            print(f"  语言: {repo.get('language')}")
            print(f"  Stars: {repo.get('stargazers_count'):,}")
            print(f"  Forks: {repo.get('forks_count'):,}")
            print(f"  Issues: {repo.get('open_issues_count')}")
            print(f"  创建时间: {repo.get('created_at')}")
            print(f"  更新时间: {repo.get('updated_at')}")
        else:
            print(f"❌ 获取仓库信息失败: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")

if __name__ == "__main__":
    debug_github_api()
    test_specific_repo()
    
    print("\n💡 建议:")
    print("1. 如果看到正确的数据，说明API工作正常")
    print("2. 如果数据缺失，可能是API限制或网络问题")
    print("3. 建议设置GitHub Token以获得更高的API限制")
    print("4. 可以尝试使用更具体的查询条件") 