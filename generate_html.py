#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub排名HTML页面生成器
生成美观的中文版GitHub仓库排名展示页面
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any

class HTMLGenerator:
    def __init__(self):
        self.template_dir = "templates"
        self.output_dir = "docs"
        os.makedirs(self.template_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_index_page(self, data: Dict[str, List[Dict]], title: str = "GitHub仓库排名") -> str:
        """
        生成主页HTML
        """
        # 获取更新时间
        update_time = datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")
        
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "Helvetica Neue", Helvetica, Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f8f9fa;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 40px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 60px 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        
        .header h1 {{
            font-size: 3rem;
            margin-bottom: 10px;
            font-weight: 700;
        }}
        
        .header .subtitle {{
            font-size: 1.2rem;
            opacity: 0.9;
            margin-bottom: 20px;
        }}
        
        .update-time {{
            font-size: 0.9rem;
            opacity: 0.8;
            background: rgba(255, 255, 255, 0.1);
            padding: 8px 16px;
            border-radius: 20px;
            display: inline-block;
        }}
        
        .navigation {{
            background: white;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 30px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }}
        
        .nav-title {{
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 15px;
            color: #2c3e50;
        }}
        
        .nav-links {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 10px;
        }}
        
        .nav-link {{
            padding: 12px 20px;
            background: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 6px;
            text-decoration: none;
            color: #495057;
            font-weight: 500;
            transition: all 0.3s ease;
            display: block;
            text-align: center;
        }}
        
        .nav-link:hover {{
            background: #007bff;
            color: white;
            border-color: #007bff;
            transform: translateY(-2px);
        }}
        
        .section {{
            background: white;
            border-radius: 10px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }}
        
        .section h2 {{
            font-size: 2rem;
            margin-bottom: 20px;
            color: #2c3e50;
            border-bottom: 3px solid #007bff;
            padding-bottom: 10px;
        }}
        
        .table-container {{
            overflow-x: auto;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        
        th, td {{
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid #e9ecef;
        }}
        
        th {{
            background: #f8f9fa;
            font-weight: 600;
            color: #495057;
            position: sticky;
            top: 0;
        }}
        
        tr:hover {{
            background: #f8f9fa;
        }}
        
        .rank {{
            font-weight: 700;
            color: #007bff;
        }}
        
        .repo-name {{
            font-weight: 600;
        }}
        
        .repo-name a {{
            color: #007bff;
            text-decoration: none;
        }}
        
        .repo-name a:hover {{
            text-decoration: underline;
        }}
        
        .description {{
            color: #6c757d;
            font-size: 0.9rem;
            max-width: 300px;
            word-wrap: break-word;
        }}
        
        .language {{
            display: inline-block;
            padding: 4px 8px;
            background: #007bff;
            color: white;
            border-radius: 4px;
            font-size: 0.8rem;
        }}
        
        .stats {{
            display: flex;
            gap: 15px;
            align-items: center;
        }}
        
        .stat {{
            display: flex;
            align-items: center;
            gap: 5px;
            font-size: 0.9rem;
        }}
        
        .star-icon, .fork-icon {{
            width: 16px;
            height: 16px;
        }}
        
        .footer {{
            text-align: center;
            padding: 40px 20px;
            color: #6c757d;
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }}
        
        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 2rem;
            }}
            
            .container {{
                padding: 10px;
            }}
            
            .section {{
                padding: 20px;
            }}
            
            th, td {{
                padding: 8px 10px;
                font-size: 0.9rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>⭐ GitHub仓库排名 ⭐</h1>
            <div class="subtitle">GitHub上最受欢迎的开源项目排行榜</div>
            <div class="update-time">最后更新时间: {update_time}</div>
        </div>
        
        <div class="navigation">
            <h3 class="nav-title">📊 排行榜分类</h3>
            <div class="nav-links">"""
        
        # 生成导航链接
        for category in data.keys():
            safe_category = category.replace('/', '_').replace(' ', '_')
            html += f'                <a href="#{safe_category}" class="nav-link">{category}</a>\n'
        
        html += """            </div>
        </div>"""
        
        # 生成各分类的排名表格
        for category, repos in data.items():
            if not repos:
                continue
                
            safe_category = category.replace('/', '_').replace(' ', '_')
            html += f"""
        <div class="section" id="{safe_category}">
            <h2>{category} Top 20</h2>
            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>排名</th>
                            <th>项目名称</th>
                            <th>描述</th>
                            <th>语言</th>
                            <th>统计</th>
                            <th>最后更新</th>
                        </tr>
                    </thead>
                    <tbody>"""
            
            # 显示前20个项目
            for i, repo in enumerate(repos[:20], 1):
                repo_name = repo.get('完整名称', repo.get('name', ''))
                repo_link = repo.get('仓库链接', '')
                description = repo.get('描述', '暂无描述')
                if description in [None, '', 'null']:
                    description = '暂无描述'
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
                if len(description) > 100:
                    description = description[:100] + '...'
                
                html += f"""
                        <tr>
                            <td class="rank">{i}</td>
                            <td class="repo-name">
                                <a href="{repo_link}" target="_blank">{repo_name}</a>
                            </td>
                            <td class="description">{description}</td>
                            <td><span class="language">{language}</span></td>
                            <td>
                                <div class="stats">
                                    <div class="stat">
                                        <span>⭐</span>
                                        <span>{stars:,}</span>
                                    </div>
                                    <div class="stat">
                                        <span>🍴</span>
                                        <span>{forks:,}</span>
                                    </div>
                                </div>
                            </td>
                            <td>{updated_str}</td>
                        </tr>"""
            
            html += """
                    </tbody>
                </table>
            </div>
        </div>"""
        
        html += """
        <div class="footer">
            <p>数据来源：GitHub API | 本项目开源，欢迎贡献</p>
            <p>© 2025 GitHub仓库排名 | 每日自动更新</p>
        </div>
    </div>
    
    <script>
        // 平滑滚动
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                document.querySelector(this.getAttribute('href')).scrollIntoView({
                    behavior: 'smooth'
                });
            });
        });
    </script>
</body>
</html>"""
        
        return html
    
    def generate_category_page(self, category: str, repos: List[Dict], title: str = None) -> str:
        """
        生成单个分类的详细页面
        """
        if title is None:
            title = f"{category} - GitHub仓库排名"
        
        update_time = datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")
        
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        /* 这里可以放置相同的CSS样式，为了简洁省略 */
        /* 与主页相同的样式 */
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{category} 排行榜</h1>
            <div class="subtitle">GitHub上最受欢迎的{category}项目</div>
            <div class="update-time">最后更新时间: {update_time}</div>
        </div>
        
        <div class="section">
            <h2>{category} Top 100</h2>
            <!-- 详细的表格内容 -->
        </div>
    </div>
</body>
</html>"""
        
        return html
    
    def save_pages(self, data: Dict[str, List[Dict]]):
        """
        保存所有HTML页面
        """
        # 生成主页
        index_html = self.generate_index_page(data)
        with open(f"{self.output_dir}/index.html", 'w', encoding='utf-8') as f:
            f.write(index_html)
        print("已生成主页: docs/index.html")
        
        # 生成各分类详细页面
        for category, repos in data.items():
            if repos:
                safe_filename = category.replace('/', '_').replace(' ', '_')
                category_html = self.generate_category_page(category, repos)
                with open(f"{self.output_dir}/{safe_filename}.html", 'w', encoding='utf-8') as f:
                    f.write(category_html)
                print(f"已生成 {category} 页面: docs/{safe_filename}.html")

def main():
    """
    主函数 - 从JSON数据生成HTML页面
    """
    # 检查是否存在数据文件
    if not os.path.exists("github_ranking.json"):
        print("错误：未找到 github_ranking.json 文件")
        print("请先运行 github_ranking.py 获取数据")
        return
    
    # 读取数据
    try:
        with open("github_ranking.json", 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        
        data = json_data.get("数据", {})
        if not data:
            print("错误：JSON文件中没有找到数据")
            return
        
        # 生成HTML页面
        generator = HTMLGenerator()
        generator.save_pages(data)
        
        print("HTML页面生成完成！")
        print("可以在浏览器中打开 docs/index.html 查看结果")
        
    except Exception as e:
        print(f"生成HTML页面时出错: {e}")

if __name__ == "__main__":
    main() 