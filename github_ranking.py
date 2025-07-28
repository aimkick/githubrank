#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub仓库排名爬虫
获取GitHub上按stars和forks排序的仓库数据
"""

import requests
import json
import time
from datetime import datetime
import csv
import os
from typing import List, Dict, Any

class GitHubRanking:
    def __init__(self, token: str = None):
        """
        初始化GitHub API客户端
        Args:
            token: GitHub Personal Access Token (可选，但建议使用以避免API限制)
        """
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "GitHub-Ranking-Script"
        }
        if token:
            self.headers["Authorization"] = f"token {token}"
        
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def search_repositories(self, query: str, sort: str = "stars", order: str = "desc", 
                          per_page: int = 100, max_pages: int = 10) -> List[Dict[str, Any]]:
        """
        搜索GitHub仓库
        Args:
            query: 搜索查询字符串
            sort: 排序方式 (stars, forks, updated)
            order: 排序顺序 (desc, asc)
            per_page: 每页结果数量
            max_pages: 最大页数
        Returns:
            List[Dict]: 仓库信息列表
        """
        repositories = []
        
        for page in range(1, max_pages + 1):
            try:
                url = f"{self.base_url}/search/repositories"
                params = {
                    "q": query,
                    "sort": sort,
                    "order": order,
                    "per_page": per_page,
                    "page": page
                }
                
                response = self.session.get(url, params=params)
                response.raise_for_status()
                
                data = response.json()
                repositories.extend(data.get("items", []))
                
                # 检查是否还有更多页面
                if len(data.get("items", [])) < per_page:
                    break
                
                # 避免API限制
                time.sleep(0.5)
                
            except requests.RequestException as e:
                print(f"请求失败: {e}")
                break
        
        return repositories
    
    def get_top_repositories(self, languages: List[str] = None, top_n: int = 100) -> Dict[str, List[Dict]]:
        """
        获取顶级仓库排名
        Args:
            languages: 编程语言列表，None表示获取所有语言
            top_n: 每个分类的top数量
        Returns:
            Dict: 分类排名数据
        """
        results = {}
        
        # 获取总体排名（按stars）
        print("正在获取总体排名（按stars）...")
        overall_stars = self.search_repositories("stars:>1", sort="stars", max_pages=10)
        results["总体-Stars"] = overall_stars[:top_n]
        
        # 获取总体排名（按forks）
        print("正在获取总体排名（按forks）...")
        overall_forks = self.search_repositories("forks:>1", sort="forks", max_pages=10)
        results["总体-Forks"] = overall_forks[:top_n]
        
        # 获取各语言排名
        if languages:
            for lang in languages:
                print(f"正在获取 {lang} 语言排名...")
                query = f"language:{lang}"
                repos = self.search_repositories(query, sort="stars", max_pages=5)
                results[lang] = repos[:top_n]
                
                # 避免API限制
                time.sleep(1)
        
        return results
    
    def format_repository_data(self, repo: Dict[str, Any]) -> Dict[str, Any]:
        """
        格式化仓库数据
        """
        return {
            "排名": 0,  # 将在生成报告时填充
            "项目名称": repo.get("name", ""),
            "完整名称": repo.get("full_name", ""),
            "作者": repo.get("owner", {}).get("login", ""),
            "描述": repo.get("description", ""),
            "语言": repo.get("language", ""),
            "Stars": repo.get("stargazers_count", 0),
            "Forks": repo.get("forks_count", 0),
            "Issues": repo.get("open_issues_count", 0),
            "创建时间": repo.get("created_at", ""),
            "更新时间": repo.get("updated_at", ""),
            "仓库链接": repo.get("html_url", ""),
            "主页链接": repo.get("homepage", ""),
            "许可证": repo.get("license", {}).get("name", "") if repo.get("license") else "",
            "大小(KB)": repo.get("size", 0),
            "是否Fork": repo.get("fork", False),
            "是否已归档": repo.get("archived", False)
        }
    
    def save_to_csv(self, data: Dict[str, List[Dict]], output_dir: str = "data"):
        """
        保存数据到CSV文件
        """
        os.makedirs(output_dir, exist_ok=True)
        
        for category, repos in data.items():
            filename = f"{output_dir}/{category.replace('/', '_')}_排名.csv"
            formatted_repos = []
            
            for i, repo in enumerate(repos, 1):
                formatted_repo = self.format_repository_data(repo)
                formatted_repo["排名"] = i
                formatted_repos.append(formatted_repo)
            
            # 保存CSV
            if formatted_repos:
                fieldnames = formatted_repos[0].keys()
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(formatted_repos)
                
                print(f"已保存 {category} 排名到 {filename}")
    
    def save_to_json(self, data: Dict[str, List[Dict]], filename: str = "github_ranking.json"):
        """
        保存数据到JSON文件
        """
        formatted_data = {}
        for category, repos in data.items():
            formatted_repos = []
            for i, repo in enumerate(repos, 1):
                formatted_repo = self.format_repository_data(repo)
                formatted_repo["排名"] = i
                formatted_repos.append(formatted_repo)
            formatted_data[category] = formatted_repos
        
        # 添加元数据
        output = {
            "生成时间": datetime.now().isoformat(),
            "数据": formatted_data
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        
        print(f"已保存排名数据到 {filename}")

    def get_trending_repositories(self, time_range='week', top_n=20):
        """
        获取趋势仓库 (当周/月成长最快)
        """
        print(f"🔥 正在获取{time_range}趋势仓库...")
        
        trending_repos = []
        
        # GitHub Search API for trending repos
        # 搜索最近一周/月创建或有大量stars的项目
        from datetime import datetime, timedelta
        
        if time_range == 'week':
            since_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
            query = f"created:>{since_date} stars:>50"
        else:  # month
            since_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
            query = f"created:>{since_date} stars:>100"
        
        # 分页获取
        page = 1
        while len(trending_repos) < top_n and page <= 5:
            url = f"{self.base_url}/search/repositories"
            params = {
                'q': query,
                'sort': 'stars',
                'order': 'desc',
                'per_page': min(100, top_n - len(trending_repos)),
                'page': page
            }
            
            try:
                response = self.session.get(url, params=params)
                response.raise_for_status()
                
                data = response.json()
                if response.status_code == 200 and 'items' in data:
                    for repo in data['items']:
                        if len(trending_repos) >= top_n:
                            break
                        
                        repo_info = self.format_repository_data(repo) # Use format_repository_data
                        if repo_info:
                            trending_repos.append(repo_info)
                    
                    # 如果返回的结果少于请求的数量，说明没有更多数据了
                    if len(data['items']) < params['per_page']:
                        break
                else:
                    break
                    
            except requests.RequestException as e:
                print(f"获取趋势仓库失败: {e}")
                break
            
            page += 1
            time.sleep(0.5)  # 避免触发速率限制
        
        print(f"✅ 获取到 {len(trending_repos)} 个趋势仓库")
        return trending_repos

def main():
    """
    主函数
    """
    # 常用编程语言列表
    languages = [
        "JavaScript", "Python", "Java", "TypeScript", "C#", "C++", "C", 
        "Go", "Rust", "Kotlin", "Swift", "Ruby", "PHP", "Scala", 
        "HTML", "CSS", "Shell", "PowerShell", "Dart", "Lua"
    ]
    
    # 创建排名获取器
    # 建议设置GitHub token: ranking = GitHubRanking(token="your_github_token")
    ranking = GitHubRanking()
    
    print("开始获取GitHub仓库排名数据...")
    print("注意：建议设置GitHub Personal Access Token以避免API限制")
    
    # 获取排名数据
    try:
        data = ranking.get_top_repositories(languages=languages, top_n=100)
        
        # 保存数据
        ranking.save_to_json(data)
        ranking.save_to_csv(data)
        
        print("数据获取完成！")
        print(f"获取了 {len(data)} 个分类的排名数据")
        
    except Exception as e:
        print(f"获取数据时出错: {e}")

if __name__ == "__main__":
    main() 