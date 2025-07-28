#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DeepSeek API翻译器
使用DeepSeek API提供高质量的英文到中文翻译
"""

import requests
import json
import time
from typing import Optional

class DeepSeekTranslator:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.deepseek.com/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # 缓存已翻译的内容，避免重复调用API
        self.translation_cache = {}
        
    def translate_description(self, text: str) -> str:
        """
        翻译项目描述
        """
        if not text or text.strip() in ['', 'null', None]:
            return '暂无描述'
        
        text = text.strip()
        
        # 检查缓存
        if text in self.translation_cache:
            return self.translation_cache[text]
        
        # 如果已经是中文为主，直接返回
        chinese_chars = len([c for c in text if '\u4e00' <= c <= '\u9fff'])
        if chinese_chars > len(text) * 0.3:
            return text
        
        try:
            # 构建翻译提示
            prompt = f"""请将以下GitHub项目描述翻译成中文，要求：
1. 准确翻译技术术语
2. 保持专业性和简洁性  
3. 保留emoji表情符号
4. 对于专有名词（如React、Vue、Python等）保持英文
5. 只返回翻译结果，不要添加任何解释

原文：{text}

翻译："""

            # 调用DeepSeek API
            response = self._call_api(prompt)
            
            if response:
                # 缓存结果
                self.translation_cache[text] = response
                return response
            else:
                # API失败时的备用翻译
                return self._fallback_translation(text)
                
        except Exception as e:
            print(f"翻译API调用失败: {e}")
            return self._fallback_translation(text)
    
    def _call_api(self, prompt: str) -> Optional[str]:
        """
        调用DeepSeek API
        """
        try:
            payload = {
                "model": "deepseek-chat",
                "messages": [
                    {
                        "role": "system",
                        "content": "你是一个专业的技术翻译专家，擅长将英文的GitHub项目描述翻译成自然流畅的中文。"
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                "max_tokens": 200,
                "temperature": 0.1,
                "stream": False
            }
            
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                translated = result["choices"][0]["message"]["content"].strip()
                
                # 清理可能的前缀
                if translated.startswith("翻译："):
                    translated = translated[3:].strip()
                elif translated.startswith("中文："):
                    translated = translated[3:].strip()
                
                return translated
            else:
                print(f"API调用失败，状态码: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"API调用异常: {e}")
            return None
    
    def _fallback_translation(self, text: str) -> str:
        """
        API失败时的备用翻译方案
        """
        # 简单的关键词替换作为备选
        fallback_translations = {
            "freeCodeCamp.org's open-source codebase and curriculum. Learn math, programming, and computer science for free.": 
                "freeCodeCamp.org的开源代码库和课程。免费学习数学、编程和计算机科学。",
            "Master programming by recreating your favorite technologies from scratch.": 
                "通过从零开始重新创建您喜欢的技术来掌握编程。",
            "😎 Awesome lists about all kinds of interesting topics": 
                "😎 关于各种有趣主题的精选列表",
            "📚 Freely available programming books": 
                "📚 免费提供的编程书籍",
            "A collective list of free APIs": 
                "免费API的集合列表",
            "The library for web and native user interfaces.": 
                "用于网页和原生用户界面的库。",
            "Python programming language": 
                "Python编程语言",
            "Linux kernel source tree": 
                "Linux内核源码树",
            "An Open Source Machine Learning Framework for Everyone": 
                "面向所有人的开源机器学习框架",
            "The React Framework": 
                "React框架",
            "The Progressive JavaScript Framework": 
                "渐进式JavaScript框架"
        }
        
        if text in fallback_translations:
            return fallback_translations[text]
        
        # 简单的词汇替换
        result = text
        basic_replacements = {
            'open-source': '开源',
            'framework': '框架',
            'library': '库', 
            'programming': '编程',
            'free': '免费',
            'tutorial': '教程',
            'project': '项目'
        }
        
        for en, zh in basic_replacements.items():
            if en in result.lower():
                result = result.replace(en, f"{en}({zh})", 1)
        
        return result
    
    def batch_translate(self, texts: list, batch_size: int = 5) -> dict:
        """
        批量翻译，避免频繁API调用
        """
        results = {}
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            
            for text in batch:
                results[text] = self.translate_description(text)
                # 简单的速率限制
                time.sleep(0.1)
        
        return results

# 创建全局翻译器实例
translator = None

def init_translator(api_key: str):
    """初始化翻译器"""
    global translator
    translator = DeepSeekTranslator(api_key)

def translate_text(text: str) -> str:
    """对外提供的翻译接口"""
    if translator is None:
        # 如果没有初始化，返回原文
        return text
    return translator.translate_description(text) 