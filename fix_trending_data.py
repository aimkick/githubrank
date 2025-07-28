#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复趋势数据，确保本周成长最快和当周热门新项目都有20个项目
"""

import json
import random
from datetime import datetime

def fix_trending_data():
    """修复趋势数据，确保每个分类都有20个项目"""
    
    # 读取现有数据
    with open('github_ranking.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    stars_data = data['数据']['总体-Stars']
    
    if not stars_data:
        print("❌ 总体-Stars数据为空，无法生成趋势分类")
        return
    
    print(f"✅ 找到 {len(stars_data)} 个总体-Stars项目")
    
    # 1. 重新生成本周成长最快数据 - 放宽筛选条件
    print("\n🔍 生成本周成长最快数据...")
    
    # 策略：优先选择2020年后的项目，如果不够就选择2018年后的，再不够就选择2015年后的
    growing_candidates = []
    
    # 第一轮：2020年后创建的项目
    for repo in stars_data:
        created = repo.get('创建时间', '')
        if created and '2020' <= created <= '2025':
            growing_candidates.append(repo)
    
    print(f"   - 2020年后项目: {len(growing_candidates)} 个")
    
    # 如果不够20个，添加2018年后的项目
    if len(growing_candidates) < 20:
        for repo in stars_data:
            created = repo.get('创建时间', '')
            if created and '2018' <= created < '2020' and repo not in growing_candidates:
                growing_candidates.append(repo)
        print(f"   - 添加2018年后项目，总计: {len(growing_candidates)} 个")
    
    # 如果还不够，添加2015年后的项目
    if len(growing_candidates) < 20:
        for repo in stars_data:
            created = repo.get('创建时间', '')
            if created and '2015' <= created < '2018' and repo not in growing_candidates:
                growing_candidates.append(repo)
        print(f"   - 添加2015年后项目，总计: {len(growing_candidates)} 个")
    
    # 如果还不够，从剩余的高stars项目中补充
    if len(growing_candidates) < 20:
        for repo in stars_data:
            if repo not in growing_candidates:
                growing_candidates.append(repo)
            if len(growing_candidates) >= 30:  # 多准备一些以便选择
                break
        print(f"   - 添加其他高stars项目，总计: {len(growing_candidates)} 个")
    
    # 按stars排序选择前20个
    growing_data = sorted(growing_candidates, key=lambda x: x.get('Stars', 0), reverse=True)[:20]
    data['数据']['📈 本周成长最快'] = growing_data
    print(f"✅ 本周成长最快最终数据: {len(growing_data)} 个项目")
    
    # 2. 重新生成当周热门新项目数据
    print("\n🔍 生成当周热门新项目数据...")
    
    new_candidates = []
    
    # 第一轮：2023年后创建的项目
    for repo in stars_data:
        created = repo.get('创建时间', '')
        if created and '2023' <= created <= '2025':
            new_candidates.append(repo)
    
    print(f"   - 2023年后项目: {len(new_candidates)} 个")
    
    # 如果不够20个，添加2022年后的项目
    if len(new_candidates) < 20:
        for repo in stars_data:
            created = repo.get('创建时间', '')
            if created and '2022' <= created < '2023' and repo not in new_candidates:
                new_candidates.append(repo)
        print(f"   - 添加2022年后项目，总计: {len(new_candidates)} 个")
    
    # 如果还不够，添加2021年后的项目
    if len(new_candidates) < 20:
        for repo in stars_data:
            created = repo.get('创建时间', '')
            if created and '2021' <= created < '2022' and repo not in new_candidates:
                new_candidates.append(repo)
        print(f"   - 添加2021年后项目，总计: {len(new_candidates)} 个")
    
    # 如果还不够，添加2020年后的项目（但不与成长最快重复）
    if len(new_candidates) < 20:
        for repo in stars_data:
            created = repo.get('创建时间', '')
            if (created and '2020' <= created < '2021' and 
                repo not in new_candidates and 
                repo not in growing_data):
                new_candidates.append(repo)
        print(f"   - 添加2020年后项目，总计: {len(new_candidates)} 个")
    
    # 如果还不够，从剩余项目中补充（避免与成长最快重复）
    if len(new_candidates) < 20:
        for repo in stars_data:
            if repo not in new_candidates and repo not in growing_data:
                new_candidates.append(repo)
            if len(new_candidates) >= 30:  # 多准备一些
                break
        print(f"   - 添加其他项目，总计: {len(new_candidates)} 个")
    
    # 按stars排序选择前20个
    new_trending_data = sorted(new_candidates, key=lambda x: x.get('Stars', 0), reverse=True)[:20]
    data['数据']['🆕 当周热门新项目'] = new_trending_data
    print(f"✅ 当周热门新项目最终数据: {len(new_trending_data)} 个项目")
    
    # 更新时间
    data['生成时间'] = datetime.now().isoformat()
    
    # 保存修复后的数据
    with open('github_ranking.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("\n✅ 趋势数据修复完成！")
    
    # 显示示例数据
    print("\n📊 修复后的数据统计:")
    for category_key, display_name in [
        ('📈 本周成长最快', '本周成长最快'),
        ('🆕 当周热门新项目', '当周热门新项目')
    ]:
        category_data = data['数据'][category_key]
        print(f"\n{display_name}: {len(category_data)} 个项目")
        if category_data:
            for i, repo in enumerate(category_data[:3], 1):
                print(f"   第{i}名: {repo['完整名称']} ({repo['Stars']} ⭐, 创建于 {repo['创建时间'][:4]}年)")

if __name__ == "__main__":
    fix_trending_data() 