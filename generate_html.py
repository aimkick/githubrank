#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub风格的HTML页面生成器
生成美观的GitHub风格排名展示页面
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any
from deepseek_translator import init_translator, translate_text

class GitHubStyleGenerator:
    def __init__(self):
        self.output_dir = "docs"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_github_style_page(self, data: Dict[str, List[Dict]], title: str = "GitHub仓库排名") -> str:
        """
        生成GitHub风格的主页HTML
        """
        update_time = datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")
        
        # 计算统计数据  
        data_dict = data.get('数据', data) if isinstance(data, dict) and '数据' in data else data
        
        # 只保留4个主要分类
        main_categories = [
            "📈 本周成长最快",
            "🆕 当周热门新项目", 
            "总体-Stars",
            "总体-Forks"
        ]
        
        # 过滤数据，只保留主要分类
        filtered_data = {}
        for category in main_categories:
            if category in data_dict:
                filtered_data[category] = data_dict[category]
        
        total_repos = sum(len(repos) for repos in filtered_data.values()) if filtered_data else 0
        total_categories = len(filtered_data) if filtered_data else 0
        
        html = """<!DOCTYPE html>
<html lang="zh-CN" data-color-mode="auto" data-light-theme="light" data-dark-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>📊 Github排行榜中文版</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.1.0/github-markdown-light.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/octicons/18.2.0/octicons.min.css">
    <style>
        :root {
            --color-accent-fg: #0969da;
            --color-success-fg: #1a7f37;
            --color-attention-fg: #9a6700;
            --color-danger-fg: #d1242f;
            --color-border-default: #d0d7de;
            --color-bg-default: #ffffff;
            --color-bg-subtle: #f6f8fa;
            --color-fg-default: #24292f;
            --color-fg-muted: #656d76;
            --color-canvas-default: #ffffff;
            --color-canvas-subtle: #f6f8fa;
        }
        
        @media (prefers-color-scheme: dark) {
            :root {
                --color-accent-fg: #58a6ff;
                --color-success-fg: #56d364;
                --color-attention-fg: #e3b341;
                --color-danger-fg: #f85149;
                --color-border-default: #30363d;
                --color-bg-default: #0d1117;
                --color-bg-subtle: #161b22;
                --color-fg-default: #e6edf3;
                --color-fg-muted: #8b949e;
                --color-canvas-default: #0d1117;
                --color-canvas-subtle: #161b22;
            }
        }
        
        * {
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif;
            font-size: 14px;
            line-height: 1.5;
            color: var(--color-fg-default);
            background-color: var(--color-canvas-default);
            margin: 0;
            padding: 0;
        }
        
        .header {
            background-color: var(--color-canvas-subtle);
            border-bottom: 1px solid var(--color-border-default);
            padding: 16px 0;
            position: sticky;
            top: 0;
            z-index: 100;
        }
        
        .container {
            max-width: 1280px;
            margin: 0 auto;
            padding: 0 16px;
        }
        
        .header-content {
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 16px;
        }
        
        .logo {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 20px;
            font-weight: 600;
            color: var(--color-fg-default);
            text-decoration: none;
        }
        
        .logo .octicon {
            width: 24px;
            height: 24px;
        }
        
        .stats-summary {
            display: flex;
            gap: 24px;
            font-size: 12px;
            color: var(--color-fg-muted);
        }
        
        .stat-item {
            display: flex;
            align-items: center;
            gap: 4px;
        }
        
        .main-content {
            padding: 24px 0;
        }
        
        .page-header {
            margin-bottom: 24px;
            padding-bottom: 16px;
            border-bottom: 1px solid var(--color-border-default);
        }
        
        .page-title {
            font-size: 24px;
            font-weight: 600;
            margin: 0 0 8px 0;
            color: var(--color-fg-default);
        }
        
        .page-description {
            font-size: 14px;
            color: var(--color-fg-muted);
            margin: 0;
        }
        
        .navigation {
            background-color: var(--color-bg-subtle);
            border: 1px solid var(--color-border-default);
            border-radius: 6px;
            padding: 16px;
            margin-bottom: 24px;
        }
        
        .nav-title {
            font-size: 14px;
            font-weight: 600;
            margin: 0 0 12px 0;
            color: var(--color-fg-default);
        }
        
        .nav-tabs {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }
        
        .nav-tab {
            padding: 6px 12px;
            background-color: var(--color-canvas-default);
            border: 1px solid var(--color-border-default);
            border-radius: 6px;
            text-decoration: none;
            color: var(--color-fg-default);
            font-size: 12px;
            font-weight: 500;
            transition: all 0.15s ease;
        }
        
        .nav-tab:hover {
            background-color: var(--color-bg-subtle);
            border-color: var(--color-accent-fg);
        }
        
        .section {
            background-color: var(--color-canvas-default);
            border: 1px solid var(--color-border-default);
            border-radius: 6px;
            margin-bottom: 24px;
            overflow: hidden;
        }
        
        .section-header {
            padding: 16px;
            background-color: var(--color-bg-subtle);
            border-bottom: 1px solid var(--color-border-default);
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        
        .section-title {
            font-size: 16px;
            font-weight: 600;
            margin: 0;
            color: var(--color-fg-default);
        }
        
        .section-meta {
            font-size: 12px;
            color: var(--color-fg-muted);
        }
        
        .repo-list {
            list-style: none;
            margin: 0;
            padding: 0;
        }
        
        .repo-item {
            padding: 16px;
            border-bottom: 1px solid var(--color-border-default);
            display: grid;
            grid-template-columns: 32px 1fr auto auto;
            align-items: flex-start;
            gap: 16px;
        }
        
        .repo-item:last-child {
            border-bottom: none;
        }
        
        .repo-item:hover {
            background-color: var(--color-bg-subtle);
        }
        
        .repo-rank {
            flex-shrink: 0;
            width: 32px;
            height: 32px;
            background-color: var(--color-accent-fg);
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 12px;
            font-weight: 600;
        }
        
        .repo-rank.gold { background-color: #ffd700; color: #000; }
        .repo-rank.silver { background-color: #c0c0c0; color: #000; }
        .repo-rank.bronze { background-color: #cd7f32; color: #fff; }
        
        .repo-content {
            flex: 1;
            min-width: 0;
        }
        
        .repo-header {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 4px;
        }
        
        .repo-name {
            font-size: 16px;
            font-weight: 600;
            color: var(--color-accent-fg);
            text-decoration: none;
            word-break: break-word;
        }
        
        .repo-name:hover {
            text-decoration: underline;
        }
        
        .repo-visibility {
            padding: 2px 6px;
            background-color: var(--color-bg-subtle);
            border: 1px solid var(--color-border-default);
            border-radius: 12px;
            font-size: 10px;
            font-weight: 500;
            color: var(--color-fg-muted);
        }
        
        .repo-description {
            color: var(--color-fg-muted);
            font-size: 14px;
            margin: 4px 0 8px 0;
            line-height: 1.4;
        }
        
        .repo-meta {
            display: flex;
            align-items: center;
            gap: 16px;
            font-size: 12px;
            color: var(--color-fg-muted);
            flex-wrap: wrap;
        }
        
        .repo-language {
            display: flex;
            align-items: center;
            gap: 4px;
        }
        
        .language-color {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            border: 1px solid var(--color-border-default);
        }
        
        .repo-stats {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        
        .stat {
            display: flex;
            align-items: center;
            gap: 4px;
            color: var(--color-fg-muted);
        }
        
        .stat.stars { color: var(--color-attention-fg); }
        .stat.forks { color: var(--color-accent-fg); }
        
        .stats-column {
            display: flex;
            align-items: center;
            justify-content: flex-end;
            min-width: 80px;
            font-size: 14px;
            font-weight: 600;
        }
        
        .stats-column.stars {
            color: var(--color-attention-fg);
        }
        
        .stats-column.forks {
            color: var(--color-accent-fg);
        }
        
        .footer {
            padding: 40px 0;
            text-align: center;
            color: var(--color-fg-muted);
            font-size: 12px;
            border-top: 1px solid var(--color-border-default);
            background-color: var(--color-bg-subtle);
            margin-top: 40px;
        }
        
        .footer a {
            color: var(--color-accent-fg);
            text-decoration: none;
        }
        
        .footer a:hover {
            text-decoration: underline;
        }
        
        /* 响应式设计 */
        @media (max-width: 768px) {
            .container {
                padding: 0 12px;
            }
            
            .header-content {
                flex-direction: column;
                align-items: flex-start;
            }
            
            .stats-summary {
                flex-wrap: wrap;
            }
            
            .nav-tabs {
                justify-content: flex-start;
            }
            
            .repo-meta {
                flex-direction: column;
                align-items: flex-start;
                gap: 8px;
            }
        }
        
        .new-badge {
            background: linear-gradient(45deg, #00b894, #00cec9);
            color: white;
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 10px;
            font-weight: 600;
            text-transform: uppercase;
            margin-left: 8px;
        }
        
        .hot-badge {
            background: linear-gradient(45deg, #e84393, #fd79a8);
            color: white;
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 10px;
            font-weight: 600;
            text-transform: uppercase;
            margin-left: 8px;
        }
    </style>
</head>
<body>
    <header class="header">
        <div class="container">
            <div class="header-content">
                <a href="#" class="logo">
                    <svg class="octicon octicon-mark-github" viewBox="0 0 16 16" width="24" height="24" aria-hidden="true">
                        <path fill="currentColor" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"></path>
                    </svg>
                    Github排行榜中文版
                </a>
                <div class="stats-summary">
                    <p>📅 最后更新 {update_time}</p>
                    <p>🔄 自动更新 每周一 08:00</p>
                    <p>�� 总计 {total_repos} 个项目，{total_categories} 个分类</p>
                </div>
            </div>
        </div>
    </header>
    
    <main class="main-content">
        <div class="container">
            <div class="page-header">
                <h1 class="page-title">⭐ Github排行榜中文版</h1>
                <p class="page-description">
                    发现GitHub上最受欢迎的开源项目，展示最具影响力和快速成长的代码仓库
                </p>
            </div>
            
"""
        
        # 生成4个主要分类的排名列表
        for category in main_categories:
            if not filtered_data.get(category):
                continue
                
            safe_category = category.replace('/', '_').replace(' ', '_')
            html += f"""
            <div class="section" id="{safe_category}">
                <div class="section-header">
                    <h2 class="section-title">{category}</h2>
                    <div class="section-meta">Top {min(len(filtered_data[category]), 20)} 项目</div>
                </div>
                <ol class="repo-list">"""
            
            # 所有分类都显示20个
            display_count = 20
            for i, repo in enumerate(filtered_data[category][:display_count], 1):
                repo_name = repo.get('完整名称', repo.get('项目名称', ''))
                repo_link = repo.get('仓库链接', '')
                description = repo.get('描述', '暂无描述')
                if description in [None, '', 'null']:
                    description = '暂无描述'
                else:
                    # 使用DeepSeek API翻译描述
                    description = translate_text(description)
                    
                language = repo.get('语言', '未知')
                if language in [None, '', 'null']:
                    language = '未知'
                    
                stars = repo.get('Stars', 0)
                forks = repo.get('Forks', 0)
                updated = repo.get('更新时间', '')
                
                # 格式化更新时间
                if updated:
                    try:
                        dt = datetime.fromisoformat(updated.replace('Z', '+00:00'))
                        updated_str = dt.strftime('%Y-%m-%d')
                    except:
                        updated_str = updated[:10] if len(updated) >= 10 else updated
                else:
                    updated_str = '未知'
                
                # 限制描述长度
                if len(description) > 120:
                    description = description[:120] + '...'
                
                # 排名样式
                rank_class = "repo-rank"
                if i == 1:
                    rank_class += " gold"
                elif i == 2:
                    rank_class += " silver" 
                elif i == 3:
                    rank_class += " bronze"
                
                # 语言颜色
                language_colors = {
                    'JavaScript': '#f1e05a',
                    'Python': '#3572A5', 
                    'Java': '#b07219',
                    'TypeScript': '#3178c6',
                    'C++': '#f34b7d',
                    'C#': '#239120',
                    'C': '#555555',
                    'Go': '#00ADD8',
                    'Rust': '#dea584',
                    'Ruby': '#701516',
                    'PHP': '#4F5D95',
                    'Swift': '#fa7343',
                    'Kotlin': '#A97BFF',
                    'HTML': '#e34c26',
                    'CSS': '#1572B6',
                    'Shell': '#89e051',
                    'Markdown': '#083fa1'
                }
                language_color = language_colors.get(language, '#586069')
                
                html += f"""
                    <li class="repo-item">
                        <div class="{rank_class}">{i}</div>
                        <div class="repo-content">
                            <div class="repo-header">
                                <a href="{repo_link}" class="repo-name" target="_blank">{repo_name}</a>
                                <span class="repo-visibility">Public</span>
                            </div>
                            <p class="repo-description">{description}</p>
                            <div class="repo-meta">
                                <div class="repo-language">
                                    <span class="language-color" style="background-color: {language_color}"></span>
                                    <span>{language}</span>
                                </div>
                                <div>更新于 {updated_str}</div>
                            </div>
                        </div>
                        <div class="stats-column stars">
                            <svg class="octicon octicon-star" viewBox="0 0 16 16" width="16" height="16" style="margin-right: 4px;">
                                <path fill="currentColor" d="M8 .25a.75.75 0 01.673.418l1.882 3.815 4.21.612a.75.75 0 01.416 1.279l-3.046 2.97.719 4.192a.75.75 0 01-1.088.791L8 12.347l-3.766 1.98a.75.75 0 01-1.088-.79l.72-4.194L.818 6.374a.75.75 0 01.416-1.28l4.21-.611L7.327.668A.75.75 0 718 .25zm0 2.445L6.615 5.5a.75.75 0 01-.564.41l-3.097.45 2.24 2.184a.75.75 0 01.216.664l-.528 3.084 2.769-1.456a.75.75 0 01.698 0l2.77 1.456-.53-3.084a.75.75 0 01.216-.664l2.24-2.183-3.096-.45a.75.75 0 01-.564-.41L8 2.694v.001z"></path>
                            </svg>
                            {stars:,}
                        </div>
                        <div class="stats-column forks">
                            <svg class="octicon octicon-repo-forked" viewBox="0 0 16 16" width="16" height="16" style="margin-right: 4px;">
                                <path fill="currentColor" d="M5 3.25a.75.75 0 11-1.5 0 .75.75 0 011.5 0zm0 2.122a2.25 2.25 0 10-1.5 0v.878A2.25 2.25 0 005.75 8.5h1.5v2.128a2.251 2.251 0 101.5 0V8.5h1.5a2.25 2.25 0 002.25-2.25v-.878a2.25 2.25 0 10-1.5 0v.878a.75.75 0 01-.75.75h-4.5A.75.75 0 015 6.25v-.878zm3.75 7.378a.75.75 0 11-1.5 0 .75.75 0 011.5 0zm3-8.75a.75.75 0 11-1.5 0 .75.75 0 011.5 0z"></path>
                            </svg>
                            {forks:,}
                        </div>
                    </li>"""
            
            html += """
                </ol>
            </div>"""
        
        html += """
        </div>
    </main>
    
    <footer class="footer">
        <div class="container">
            <p>
                数据来源：<a href="https://api.github.com" target="_blank">GitHub API</a> | 
                项目开源：<a href="https://github.com/aimkick/githubrank" target="_blank">GitHub</a> | 
                每日自动更新
            </p>
            <p>© 2025 Github排行榜中文版 | 发现优秀的开源项目</p>
        </div>
    </footer>
    
    <script>
        // 平滑滚动
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
        
        // 深色模式切换
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)');
        function updateTheme(e) {
            document.documentElement.setAttribute('data-color-mode', 
                e.matches ? 'dark' : 'light');
        }
        prefersDark.addListener(updateTheme);
        updateTheme(prefersDark);
    </script>
</body>
</html>"""
        
        # 替换模板中的变量
        html = html.replace('{update_time}', update_time)
        html = html.replace('{total_repos}', str(total_repos))
        html = html.replace('{total_categories}', str(total_categories))
        
        return html
    
    def save_github_style_page(self, data: Dict[str, List[Dict]]):
        """
        保存GitHub风格的HTML页面
        """
        html_content = self.generate_github_style_page(data)
        with open(f"{self.output_dir}/index.html", 'w', encoding='utf-8') as f:
            f.write(html_content)
        print("已生成GitHub风格主页: docs/index.html")

def main():
    """
    主函数 - 从JSON数据生成GitHub风格HTML页面
    """
    if not os.path.exists("github_ranking.json"):
        print("错误：未找到 github_ranking.json 文件")
        print("请先运行 github_ranking.py 获取数据")
        return
    
    try:
        # 初始化DeepSeek翻译器
        api_key = os.environ.get("DEEPSEEK_API_KEY")
        if not api_key:
            print("⚠️  警告：未找到DEEPSEEK_API_KEY环境变量，翻译功能将不可用")
            api_key = None
        else:
            print("✅ 找到DeepSeek API密钥，启用翻译功能")
        
        init_translator(api_key)
        
        with open("github_ranking.json", 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        
        data = json_data.get("数据", {})
        if not data:
            print("错误：JSON文件中没有找到数据")
            return
        
        # 生成GitHub风格页面
        generator = GitHubStyleGenerator()
        generator.save_github_style_page(data)
        
        print("GitHub风格HTML页面生成完成！")
        print("可以在浏览器中打开 docs/index.html 查看结果")
        
    except Exception as e:
        print(f"生成HTML页面时出错: {e}")

if __name__ == "__main__":
    main() 