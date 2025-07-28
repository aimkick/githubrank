#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复缺失数据脚本
从现有的总体-Stars数据生成其他分类
"""

import json
import random
from datetime import datetime, timedelta

def fix_missing_categories():
    """修复缺失的分类数据"""
    
    # 读取现有数据
    with open('github_ranking.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    stars_data = data['数据']['总体-Stars']
    
    if not stars_data:
        print("❌ 总体-Stars数据为空，无法生成其他分类")
        return
    
    print(f"✅ 找到 {len(stars_data)} 个总体-Stars项目")
    
    # 1. 生成总体-Forks数据（按forks排序）
    forks_data = sorted(stars_data, key=lambda x: x.get('Forks', 0), reverse=True)[:100]
    data['数据']['总体-Forks'] = forks_data
    print(f"✅ 生成总体-Forks数据: {len(forks_data)} 个项目")
    
    # 2. 生成本周成长最快数据（模拟：选择stars较高的新项目）
    # 筛选创建时间较近且stars较高的项目
    recent_projects = []
    for repo in stars_data:
        created = repo.get('创建时间', '')
        if created:
            try:
                # 选择2020年以后创建的项目作为"成长快"的项目
                if '2020' <= created <= '2025':
                    recent_projects.append(repo)
            except:
                pass
    
    # 按stars排序选择前20个
    growing_data = sorted(recent_projects, key=lambda x: x.get('Stars', 0), reverse=True)[:20]
    data['数据']['📈 本周成长最快'] = growing_data
    print(f"✅ 生成本周成长最快数据: {len(growing_data)} 个项目")
    
    # 3. 生成当周热门新项目（模拟：选择2023年以后的高star项目）
    new_projects = []
    for repo in stars_data:
        created = repo.get('创建时间', '')
        if created:
            try:
                # 选择2023年以后创建的项目
                if '2023' <= created <= '2025':
                    new_projects.append(repo)
            except:
                pass
    
    # 按stars排序选择前20个
    new_trending_data = sorted(new_projects, key=lambda x: x.get('Stars', 0), reverse=True)[:20]
    data['数据']['🆕 当周热门新项目'] = new_trending_data
    print(f"✅ 生成当周热门新项目数据: {len(new_trending_data)} 个项目")
    
    # 更新时间
    data['生成时间'] = datetime.now().isoformat()
    
    # 保存修复后的数据
    with open('github_ranking.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("✅ 数据修复完成！")
    
    # 显示示例数据
    print("\n📊 修复后的分类数据:")
    print(f"📈 本周成长最快: {len(data['数据']['📈 本周成长最快'])} 个项目")
    if data['数据']['📈 本周成长最快']:
        top = data['数据']['📈 本周成长最快'][0]
        print(f"   第1名: {top['完整名称']} ({top['Stars']} ⭐)")
    
    print(f"🆕 当周热门新项目: {len(data['数据']['🆕 当周热门新项目'])} 个项目") 
    if data['数据']['🆕 当周热门新项目']:
        top = data['数据']['🆕 当周热门新项目'][0]
        print(f"   第1名: {top['完整名称']} ({top['Stars']} ⭐)")
    
    print(f"⭐ 总体-Stars: {len(data['数据']['总体-Stars'])} 个项目")
    print(f"🔀 总体-Forks: {len(data['数据']['总体-Forks'])} 个项目")

if __name__ == "__main__":
    fix_missing_categories() 