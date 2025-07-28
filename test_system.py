#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub排名系统测试脚本
验证整个系统是否正常工作
"""

import os
import json
import sys
from datetime import datetime
from github_ranking import GitHubRanking
from generate_html import HTMLGenerator

def test_github_api():
    """测试GitHub API连接"""
    print("🔍 测试GitHub API连接...")
    try:
        ranking = GitHubRanking()
        # 测试简单查询
        test_repos = ranking.search_repositories("stars:>50000", max_pages=1, per_page=5)
        if test_repos:
            print(f"✅ API连接正常，获取到 {len(test_repos)} 个测试仓库")
            return True
        else:
            print("❌ API连接失败，未获取到数据")
            return False
    except Exception as e:
        print(f"❌ API测试失败: {e}")
        return False

def test_data_collection():
    """测试数据收集功能"""
    print("\n📊 测试数据收集功能...")
    try:
        ranking = GitHubRanking()
        # 测试小规模数据收集
        test_languages = ["Python", "JavaScript"]
        data = ranking.get_top_repositories(languages=test_languages, top_n=10)
        
        if data and len(data) > 0:
            total_repos = sum(len(repos) for repos in data.values())
            print(f"✅ 数据收集成功，获取 {len(data)} 个分类，{total_repos} 个仓库")
            return data
        else:
            print("❌ 数据收集失败")
            return None
    except Exception as e:
        print(f"❌ 数据收集测试失败: {e}")
        return None

def test_json_export(data):
    """测试JSON导出功能"""
    print("\n💾 测试JSON导出功能...")
    try:
        ranking = GitHubRanking()
        test_file = "test_ranking.json"
        ranking.save_to_json(data, test_file)
        
        if os.path.exists(test_file):
            with open(test_file, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
            print(f"✅ JSON导出成功，文件大小: {os.path.getsize(test_file)} 字节")
            os.remove(test_file)  # 清理测试文件
            return True
        else:
            print("❌ JSON文件未生成")
            return False
    except Exception as e:
        print(f"❌ JSON导出测试失败: {e}")
        return False

def test_html_generation(data):
    """测试HTML生成功能"""
    print("\n🌐 测试HTML生成功能...")
    try:
        generator = HTMLGenerator()
        html_content = generator.generate_index_page(data, "测试页面")
        
        if html_content and len(html_content) > 1000:
            print(f"✅ HTML生成成功，内容长度: {len(html_content)} 字符")
            
            # 保存测试HTML文件
            test_dir = "test_docs"
            os.makedirs(test_dir, exist_ok=True)
            test_file = f"{test_dir}/test_index.html"
            
            with open(test_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"✅ 测试HTML文件已保存: {test_file}")
            return True
        else:
            print("❌ HTML生成失败")
            return False
    except Exception as e:
        print(f"❌ HTML生成测试失败: {e}")
        return False

def test_file_structure():
    """测试项目文件结构"""
    print("\n📁 检查项目文件结构...")
    
    required_files = [
        "github_ranking.py",
        "generate_html.py", 
        "update_ranking.py",
        "requirements.txt",
        "README.md",
        ".github/workflows/update-ranking.yml"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ 缺少文件: {', '.join(missing_files)}")
        return False
    else:
        print("✅ 所有必要文件都存在")
        return True

def cleanup_test_files():
    """清理测试文件"""
    print("\n🧹 清理测试文件...")
    test_files = [
        "test_ranking.json",
        "test_docs"
    ]
    
    for item in test_files:
        try:
            if os.path.isfile(item):
                os.remove(item)
                print(f"  删除文件: {item}")
            elif os.path.isdir(item):
                import shutil
                shutil.rmtree(item)
                print(f"  删除目录: {item}")
        except Exception as e:
            print(f"  清理失败 {item}: {e}")

def main():
    """主测试函数"""
    print("🚀 GitHub仓库排名系统测试开始")
    print("=" * 50)
    
    # 测试结果
    test_results = []
    
    # 1. 检查文件结构
    test_results.append(("文件结构", test_file_structure()))
    
    # 2. 测试GitHub API
    test_results.append(("GitHub API", test_github_api()))
    
    # 3. 测试数据收集
    data = test_data_collection()
    test_results.append(("数据收集", data is not None))
    
    if data:
        # 4. 测试JSON导出
        test_results.append(("JSON导出", test_json_export(data)))
        
        # 5. 测试HTML生成
        test_results.append(("HTML生成", test_html_generation(data)))
    else:
        test_results.append(("JSON导出", False))
        test_results.append(("HTML生成", False))
    
    # 显示测试结果
    print("\n" + "=" * 50)
    print("📋 测试结果汇总:")
    print("=" * 50)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {test_name:<12} {status}")
        if result:
            passed += 1
    
    print("=" * 50)
    print(f"总测试: {total}, 通过: {passed}, 失败: {total - passed}")
    
    if passed == total:
        print("🎉 所有测试通过！系统运行正常。")
        success = True
    else:
        print("⚠️  部分测试失败，请检查相关功能。")
        success = False
    
    # 清理测试文件
    cleanup_test_files()
    
    print("\n💡 下一步操作:")
    if success:
        print("  1. 运行 'python update_ranking.py' 获取完整数据")
        print("  2. 推送代码到GitHub仓库")
        print("  3. 在GitHub仓库设置中启用GitHub Pages")
        print("  4. 等待自动部署完成")
    else:
        print("  1. 检查网络连接和GitHub API访问")
        print("  2. 确认所有依赖已正确安装")
        print("  3. 检查代码文件是否完整")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 