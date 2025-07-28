# ⭐ GitHub仓库排名 ⭐

[![更新状态](https://github.com/你的用户名/github-ranking/workflows/更新GitHub仓库排名/badge.svg)](https://github.com/你的用户名/github-ranking/actions)
[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-部署中-brightgreen)](https://你的用户名.github.io/github-ranking/)
[![Python](https://img.shields.io/badge/Python-3.9+-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

## 🎯 项目简介

这是一个**中文版GitHub仓库排名项目**，灵感来源于 [EvanLi/Github-Ranking](https://github.com/EvanLi/Github-Ranking)。

**主要功能：**
- 📊 展示GitHub上最受欢迎的开源项目排行榜
- 🌍 支持多种编程语言分类排名
- 🤖 每日自动更新数据
- 🎨 美观的中文界面展示
- 📱 响应式设计，支持移动端

## 🚀 在线访问

**网站地址：** [https://你的用户名.github.io/github-ranking/](https://你的用户名.github.io/github-ranking/)

*最后更新时间: 每日北京时间 12:00*

## 📋 排行榜分类

### 总体排名
- **总体-Stars**: 按照Star数量排序的所有仓库
- **总体-Forks**: 按照Fork数量排序的所有仓库

### 编程语言排名
- **前端开发**: JavaScript, TypeScript, HTML, CSS
- **后端开发**: Python, Java, Go, Rust, C++, C#
- **移动开发**: Swift, Kotlin, Dart
- **系统编程**: C, Rust, Go
- **脚本语言**: Python, Ruby, PHP, Shell
- **其他语言**: Scala, Haskell, Clojure, Elixir, Julia 等

## 🛠️ 技术架构

```
GitHub仓库排名项目
├── 数据获取层 (GitHub API)
├── 数据处理层 (Python)
├── 展示层 (HTML/CSS/JS)
└── 自动化层 (GitHub Actions)
```

### 核心组件

| 文件 | 功能描述 |
|------|----------|
| `github_ranking.py` | GitHub API数据获取和处理 |
| `generate_html.py` | HTML页面生成器 |
| `update_ranking.py` | 主更新脚本 |
| `.github/workflows/update-ranking.yml` | 自动化工作流 |

## 📦 本地运行

### 环境要求
- Python 3.9+
- Git

### 安装步骤

1. **克隆项目**
```bash
git clone https://github.com/你的用户名/github-ranking.git
cd github-ranking
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **设置GitHub Token (可选但推荐)**
```bash
# Linux/Mac
export GITHUB_TOKEN=your_github_token_here

# Windows
set GITHUB_TOKEN=your_github_token_here
```

4. **运行更新脚本**
```bash
python update_ranking.py
```

5. **查看结果**
```bash
# 打开生成的HTML文件
open docs/index.html  # Mac
start docs/index.html # Windows
xdg-open docs/index.html # Linux
```

## 🔧 配置说明

### GitHub Token配置
为了避免API速率限制，建议设置GitHub Personal Access Token：

1. 访问 [GitHub Settings > Developer settings > Personal access tokens](https://github.com/settings/tokens)
2. 点击 "Generate new token"
3. 选择 `public_repo` 权限
4. 复制生成的token
5. 在环境变量中设置 `GITHUB_TOKEN`

### 自定义配置
你可以在 `update_ranking.py` 中修改以下配置：

```python
# 修改要抓取的编程语言
languages = [
    "JavaScript", "Python", "Java", "TypeScript", 
    # 添加你感兴趣的语言
]

# 修改每个分类的项目数量
top_n = 100  # 默认100个
```

## 🤖 自动化部署

项目使用GitHub Actions实现自动化：

### 触发条件
- ⏰ **定时触发**: 每天UTC 04:00 (北京时间12:00)
- 🔧 **代码更新**: 推送到main/master分支
- 👆 **手动触发**: 在Actions页面手动运行

### 部署流程
1. 获取最新的GitHub仓库数据
2. 生成HTML展示页面
3. 提交更新到仓库
4. 部署到GitHub Pages

### 启用自动化
1. Fork 这个项目到你的GitHub账户
2. 在仓库设置中启用GitHub Pages
3. 选择 `gh-pages` 分支作为源
4. 等待第一次自动运行完成

## 📊 数据说明

### 数据来源
- **API**: GitHub REST API v3
- **更新频率**: 每日一次
- **数据范围**: 公开仓库

### 排名算法
- **Stars排名**: 按照仓库的Star数量降序排列
- **Forks排名**: 按照仓库的Fork数量降序排列
- **语言分类**: 基于GitHub检测的主要编程语言

### 数据字段
| 字段 | 说明 |
|------|------|
| 排名 | 在该分类中的排名 |
| 项目名称 | 仓库的完整名称 |
| 描述 | 项目描述信息 |
| 语言 | 主要编程语言 |
| Stars | Star数量 |
| Forks | Fork数量 |
| Issues | 开放的Issue数量 |
| 更新时间 | 最后提交时间 |

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

### 如何贡献
1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建Pull Request

### 改进建议
- 🎨 改进界面设计
- 📊 增加更多统计维度
- 🌐 添加国际化支持
- 📱 优化移动端体验
- ⚡ 提升性能

## 📄 许可证

本项目采用 [MIT License](LICENSE) 开源协议。

## 🙏 致谢

- 感谢 [EvanLi/Github-Ranking](https://github.com/EvanLi/Github-Ranking) 提供的灵感
- 感谢 GitHub 提供的优秀API服务
- 感谢所有开源项目的贡献者

## 📞 联系方式

如有问题或建议，请通过以下方式联系：

- 📧 Email: your-email@example.com
- 💬 GitHub Issues: [提交Issue](https://github.com/你的用户名/github-ranking/issues)
- 🐦 Twitter: [@你的Twitter](https://twitter.com/你的Twitter)

---

⭐ 如果这个项目对你有帮助，请给它一个Star！ 