#!/usr/bin/env python3
"""
📊 大数据支持模块
提供全球求职市场的大数据分析和洞察

功能特性：
- 🏢 全球公司评价数据库
- 📈 行业薪资报告和趋势
- 🎯 技能价值评估系统
- 🔥 职位热度指数分析
- 🌍 全球就业市场洞察
- 📊 数据可视化支持
"""

import json
import random
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from collections import defaultdict

# ================================
# 🏢 全球公司数据库
# ================================

GLOBAL_COMPANIES_DATABASE = {
    # 科技巨头
    "Google": {
        "rating": 4.8,
        "size": "大型",
        "industry": "互联网",
        "locations": ["美国", "中国", "印度", "英国", "德国"],
        "salary_range": (200000, 800000),
        "work_life_balance": 4.2,
        "career_growth": 4.5,
        "benefits": 4.8,
        "culture": 4.6,
        "interview_difficulty": 4.8,
        "tags": ["AI", "云计算", "搜索", "广告", "移动"],
        "recent_trends": "AI领域大量招聘，重点关注LLM和机器学习"
    },
    "Microsoft": {
        "rating": 4.7,
        "size": "大型",
        "industry": "软件",
        "locations": ["美国", "中国", "印度", "爱尔兰", "加拿大"],
        "salary_range": (180000, 750000),
        "work_life_balance": 4.4,
        "career_growth": 4.3,
        "benefits": 4.7,
        "culture": 4.5,
        "interview_difficulty": 4.6,
        "tags": ["云计算", "办公软件", "游戏", "AI", "企业服务"],
        "recent_trends": "Azure云服务扩张，AI Copilot产品线招聘"
    },
    "Apple": {
        "rating": 4.6,
        "size": "大型",
        "industry": "消费电子",
        "locations": ["美国", "中国", "日本", "德国", "英国"],
        "salary_range": (190000, 700000),
        "work_life_balance": 3.8,
        "career_growth": 4.2,
        "benefits": 4.6,
        "culture": 4.3,
        "interview_difficulty": 4.7,
        "tags": ["硬件", "软件", "设计", "移动", "AR/VR"],
        "recent_trends": "Vision Pro和AI功能开发，硬件工程师需求大"
    },
    "Amazon": {
        "rating": 4.2,
        "size": "大型",
        "industry": "电商/云计算",
        "locations": ["美国", "中国", "印度", "德国", "英国"],
        "salary_range": (170000, 650000),
        "work_life_balance": 3.5,
        "career_growth": 4.1,
        "benefits": 4.3,
        "culture": 3.9,
        "interview_difficulty": 4.5,
        "tags": ["电商", "云计算", "物流", "AI", "广告"],
        "recent_trends": "AWS持续扩张，生成式AI服务开发"
    },
    "Meta": {
        "rating": 4.3,
        "size": "大型",
        "industry": "社交媒体",
        "locations": ["美国", "英国", "新加坡", "爱尔兰"],
        "salary_range": (200000, 800000),
        "work_life_balance": 3.9,
        "career_growth": 4.2,
        "benefits": 4.5,
        "culture": 4.1,
        "interview_difficulty": 4.8,
        "tags": ["社交", "VR/AR", "AI", "广告", "元宇宙"],
        "recent_trends": "元宇宙投资减少，AI和效率工具成为重点"
    },
    
    # 中国科技公司
    "腾讯": {
        "rating": 4.4,
        "size": "大型",
        "industry": "互联网",
        "locations": ["中国", "新加坡", "美国"],
        "salary_range": (200000, 1000000),
        "work_life_balance": 3.6,
        "career_growth": 4.2,
        "benefits": 4.4,
        "culture": 4.0,
        "interview_difficulty": 4.5,
        "tags": ["游戏", "社交", "云计算", "AI", "金融科技"],
        "recent_trends": "游戏出海和AI应用，云计算业务扩张"
    },
    "阿里巴巴": {
        "rating": 4.3,
        "size": "大型",
        "industry": "电商/云计算",
        "locations": ["中国", "新加坡", "美国", "欧洲"],
        "salary_range": (180000, 800000),
        "work_life_balance": 3.4,
        "career_growth": 4.1,
        "benefits": 4.3,
        "culture": 3.9,
        "interview_difficulty": 4.4,
        "tags": ["电商", "云计算", "AI", "物流", "金融"],
        "recent_trends": "云计算国际化，AI大模型研发"
    },
    "字节跳动": {
        "rating": 4.5,
        "size": "大型",
        "industry": "短视频/AI",
        "locations": ["中国", "新加坡", "美国", "英国"],
        "salary_range": (220000, 1200000),
        "work_life_balance": 3.3,
        "career_growth": 4.4,
        "benefits": 4.5,
        "culture": 4.2,
        "interview_difficulty": 4.6,
        "tags": ["短视频", "AI推荐", "广告", "教育", "企业服务"],
        "recent_trends": "AI算法优化，海外市场扩张"
    },
    "百度": {
        "rating": 4.1,
        "size": "大型",
        "industry": "搜索/AI",
        "locations": ["中国"],
        "salary_range": (160000, 600000),
        "work_life_balance": 3.7,
        "career_growth": 3.9,
        "benefits": 4.2,
        "culture": 3.8,
        "interview_difficulty": 4.2,
        "tags": ["搜索", "AI", "自动驾驶", "云计算"],
        "recent_trends": "文心一言大模型，自动驾驶商业化"
    },
    
    # 新兴独角兽
    "OpenAI": {
        "rating": 4.9,
        "size": "中型",
        "industry": "AI",
        "locations": ["美国"],
        "salary_range": (250000, 1500000),
        "work_life_balance": 3.8,
        "career_growth": 4.8,
        "benefits": 4.6,
        "culture": 4.7,
        "interview_difficulty": 4.9,
        "tags": ["AGI", "大模型", "研究", "API"],
        "recent_trends": "GPT系列持续迭代，多模态AI发展"
    },
    "Anthropic": {
        "rating": 4.8,
        "size": "中型",
        "industry": "AI",
        "locations": ["美国"],
        "salary_range": (240000, 1200000),
        "work_life_balance": 4.0,
        "career_growth": 4.7,
        "benefits": 4.5,
        "culture": 4.6,
        "interview_difficulty": 4.8,
        "tags": ["AI安全", "大模型", "研究"],
        "recent_trends": "Claude模型优化，AI安全研究"
    },
    "Stripe": {
        "rating": 4.7,
        "size": "中型",
        "industry": "金融科技",
        "locations": ["美国", "爱尔兰", "新加坡"],
        "salary_range": (200000, 900000),
        "work_life_balance": 4.3,
        "career_growth": 4.5,
        "benefits": 4.6,
        "culture": 4.5,
        "interview_difficulty": 4.6,
        "tags": ["支付", "API", "金融基础设施"],
        "recent_trends": "全球支付网络扩张，加密货币支持"
    }
}

# ================================
# 📈 行业薪资数据
# ================================

INDUSTRY_SALARY_DATA = {
    "AI/机器学习": {
        "average_salary": 280000,
        "growth_rate": 0.25,
        "job_count": 15000,
        "competition_level": "极高",
        "top_skills": ["Python", "TensorFlow", "PyTorch", "LLM", "MLOps"],
        "salary_by_level": {
            "初级": (150000, 250000),
            "中级": (250000, 400000),
            "高级": (400000, 700000),
            "专家": (700000, 1500000)
        },
        "hot_companies": ["OpenAI", "Google", "Meta", "字节跳动"],
        "market_outlook": "极度火热，AGI发展推动需求爆发"
    },
    "区块链": {
        "average_salary": 260000,
        "growth_rate": 0.18,
        "job_count": 8000,
        "competition_level": "高",
        "top_skills": ["Solidity", "Web3", "DeFi", "智能合约", "Rust"],
        "salary_by_level": {
            "初级": (120000, 200000),
            "中级": (200000, 350000),
            "高级": (350000, 600000),
            "专家": (600000, 1200000)
        },
        "hot_companies": ["Coinbase", "Binance", "Polygon", "Chainlink"],
        "market_outlook": "波动较大，但长期看好"
    },
    "云计算": {
        "average_salary": 220000,
        "growth_rate": 0.15,
        "job_count": 25000,
        "competition_level": "高",
        "top_skills": ["AWS", "Kubernetes", "Docker", "Terraform", "微服务"],
        "salary_by_level": {
            "初级": (120000, 180000),
            "中级": (180000, 300000),
            "高级": (300000, 500000),
            "专家": (500000, 900000)
        },
        "hot_companies": ["AWS", "Microsoft", "Google Cloud", "阿里云"],
        "market_outlook": "稳定增长，企业数字化转型推动"
    },
    "前端开发": {
        "average_salary": 180000,
        "growth_rate": 0.08,
        "job_count": 40000,
        "competition_level": "中",
        "top_skills": ["React", "Vue", "TypeScript", "Next.js", "微前端"],
        "salary_by_level": {
            "初级": (80000, 140000),
            "中级": (140000, 220000),
            "高级": (220000, 350000),
            "专家": (350000, 600000)
        },
        "hot_companies": ["字节跳动", "腾讯", "阿里巴巴", "美团"],
        "market_outlook": "需求稳定，向全栈和移动端发展"
    },
    "后端开发": {
        "average_salary": 200000,
        "growth_rate": 0.10,
        "job_count": 50000,
        "competition_level": "中",
        "top_skills": ["Java", "Python", "Go", "微服务", "分布式"],
        "salary_by_level": {
            "初级": (90000, 150000),
            "中级": (150000, 250000),
            "高级": (250000, 400000),
            "专家": (400000, 700000)
        },
        "hot_companies": ["阿里巴巴", "腾讯", "字节跳动", "美团"],
        "market_outlook": "需求旺盛，向云原生和AI集成发展"
    }
}

# ================================
# 🔥 职位热度数据
# ================================

JOB_HOTNESS_INDEX = {
    "AI工程师": {"热度": 98, "增长率": 45, "竞争度": 95, "薪资指数": 95},
    "大模型工程师": {"热度": 99, "增长率": 60, "竞争度": 98, "薪资指数": 98},
    "区块链开发": {"热度": 85, "增长率": 25, "竞争度": 80, "薪资指数": 88},
    "云架构师": {"热度": 88, "增长率": 20, "竞争度": 75, "薪资指数": 85},
    "DevOps工程师": {"热度": 82, "增长率": 18, "竞争度": 70, "薪资指数": 80},
    "全栈工程师": {"热度": 75, "增长率": 12, "竞争度": 85, "薪资指数": 75},
    "前端工程师": {"热度": 70, "增长率": 8, "竞争度": 90, "薪资指数": 70},
    "后端工程师": {"热度": 78, "增长率": 10, "竞争度": 80, "薪资指数": 78},
    "数据科学家": {"热度": 85, "增长率": 15, "竞争度": 85, "薪资指数": 85},
    "产品经理": {"热度": 65, "增长率": 5, "竞争度": 95, "薪资指数": 70},
    "UI/UX设计师": {"热度": 60, "增长率": 3, "竞争度": 88, "薪资指数": 65},
    "测试工程师": {"热度": 55, "增长率": 2, "竞争度": 60, "薪资指数": 60}
}

# ================================
# 📊 大数据分析类
# ================================

class BigDataAnalyzer:
    def __init__(self):
        self.companies_db = GLOBAL_COMPANIES_DATABASE
        self.industry_data = INDUSTRY_SALARY_DATA
        self.job_hotness = JOB_HOTNESS_INDEX
    
    def get_company_analysis(self, company_name: str) -> Dict:
        """获取公司详细分析"""
        if company_name not in self.companies_db:
            return self._search_similar_companies(company_name)
        
        company = self.companies_db[company_name]
        
        # 计算综合评分
        overall_score = (
            company["rating"] * 0.3 +
            company["work_life_balance"] * 0.2 +
            company["career_growth"] * 0.2 +
            company["benefits"] * 0.15 +
            company["culture"] * 0.15
        )
        
        return {
            "company_name": company_name,
            "basic_info": {
                "评分": company["rating"],
                "规模": company["size"],
                "行业": company["industry"],
                "办公地点": company["locations"]
            },
            "详细评价": {
                "工作生活平衡": company["work_life_balance"],
                "职业发展": company["career_growth"],
                "福利待遇": company["benefits"],
                "公司文化": company["culture"],
                "面试难度": company["interview_difficulty"]
            },
            "薪资信息": {
                "薪资范围": company["salary_range"],
                "货币单位": "人民币/年"
            },
            "技术标签": company["tags"],
            "最新动态": company["recent_trends"],
            "综合评分": round(overall_score, 2),
            "推荐指数": self._calculate_recommendation_index(company)
        }
    
    def get_industry_report(self, industry: str) -> Dict:
        """获取行业报告"""
        if industry not in self.industry_data:
            return {"错误": f"暂不支持行业: {industry}"}
        
        data = self.industry_data[industry]
        
        # 生成趋势预测
        future_salary = data["average_salary"] * (1 + data["growth_rate"])
        
        return {
            "行业名称": industry,
            "市场概况": {
                "平均薪资": data["average_salary"],
                "年增长率": f"{data['growth_rate']*100:.1f}%",
                "职位数量": data["job_count"],
                "竞争程度": data["competition_level"]
            },
            "薪资分布": data["salary_by_level"],
            "核心技能": data["top_skills"],
            "热门公司": data["hot_companies"],
            "市场前景": data["market_outlook"],
            "趋势预测": {
                "明年预期薪资": int(future_salary),
                "增长趋势": "上升" if data["growth_rate"] > 0.1 else "稳定",
                "投资建议": self._generate_investment_advice(data)
            }
        }
    
    def analyze_job_hotness(self, job_titles: List[str] = None) -> Dict:
        """分析职位热度"""
        if job_titles is None:
            job_titles = list(self.job_hotness.keys())
        
        analysis = {
            "热度排行": [],
            "增长最快": [],
            "高薪职位": [],
            "竞争激烈": []
        }
        
        # 按热度排序
        sorted_by_hotness = sorted(
            [(job, data) for job, data in self.job_hotness.items() if job in job_titles],
            key=lambda x: x[1]["热度"],
            reverse=True
        )
        
        for job, data in sorted_by_hotness:
            analysis["热度排行"].append({
                "职位": job,
                "热度指数": data["热度"],
                "增长率": f"{data['增长率']}%",
                "薪资指数": data["薪资指数"]
            })
        
        # 增长最快的职位
        analysis["增长最快"] = sorted(
            [{"职位": job, "增长率": data["增长率"]} 
             for job, data in self.job_hotness.items() if job in job_titles],
            key=lambda x: x["增长率"],
            reverse=True
        )[:5]
        
        # 高薪职位
        analysis["高薪职位"] = sorted(
            [{"职位": job, "薪资指数": data["薪资指数"]} 
             for job, data in self.job_hotness.items() if job in job_titles],
            key=lambda x: x["薪资指数"],
            reverse=True
        )[:5]
        
        # 竞争激烈的职位
        analysis["竞争激烈"] = sorted(
            [{"职位": job, "竞争度": data["竞争度"]} 
             for job, data in self.job_hotness.items() if job in job_titles],
            key=lambda x: x["竞争度"],
            reverse=True
        )[:5]
        
        return analysis
    
    def get_skill_value_report(self, skills: List[str]) -> Dict:
        """技能价值报告"""
        from .ai_analyzer import SKILL_VALUE_DATABASE
        
        skill_analysis = {
            "技能评估": [],
            "价值排行": [],
            "趋势分析": {},
            "学习建议": []
        }
        
        total_value = 0
        for skill in skills:
            if skill in SKILL_VALUE_DATABASE:
                data = SKILL_VALUE_DATABASE[skill]
                skill_info = {
                    "技能": skill,
                    "基础价值": data["base_value"],
                    "增长趋势": data["growth_trend"],
                    "市场需求": data["demand_level"],
                    "技能类别": data["category"]
                }
                skill_analysis["技能评估"].append(skill_info)
                total_value += data["base_value"]
        
        # 按价值排序
        skill_analysis["价值排行"] = sorted(
            skill_analysis["技能评估"],
            key=lambda x: x["基础价值"],
            reverse=True
        )
        
        # 趋势分析
        skill_analysis["趋势分析"] = {
            "平均技能价值": total_value / len(skills) if skills else 0,
            "高价值技能数量": len([s for s in skill_analysis["技能评估"] if s["基础价值"] > 85]),
            "新兴技能数量": len([s for s in skill_analysis["技能评估"] if s["增长趋势"] > 15])
        }
        
        # 学习建议
        skill_analysis["学习建议"] = self._generate_skill_learning_advice(skill_analysis["技能评估"])
        
        return skill_analysis
    
    def generate_market_insights(self) -> Dict:
        """生成市场洞察报告"""
        insights = {
            "全球趋势": {
                "最热门技术": ["AI/机器学习", "区块链", "云计算"],
                "增长最快行业": ["AI", "新能源", "生物技术"],
                "薪资增长最快": ["AI工程师", "区块链开发", "云架构师"]
            },
            "地区分析": {
                "北美": "AI和云计算领先，薪资水平最高",
                "欧洲": "注重工作生活平衡，绿色技术发展快",
                "亚洲": "移动互联网和制造业强势，增长潜力大"
            },
            "投资建议": [
                "重点关注AI相关技能，未来5年将是黄金期",
                "云计算技能需求稳定，适合长期发展",
                "区块链虽有波动，但长期价值巨大",
                "全栈开发能力越来越重要"
            ],
            "风险提示": [
                "传统技能面临淘汰风险",
                "AI可能替代部分重复性工作",
                "技能更新速度加快，需要持续学习"
            ]
        }
        
        return insights
    
    def _search_similar_companies(self, company_name: str) -> Dict:
        """搜索相似公司"""
        # 简单的模糊匹配
        similar = []
        for name in self.companies_db.keys():
            if company_name.lower() in name.lower() or name.lower() in company_name.lower():
                similar.append(name)
        
        return {
            "错误": f"未找到公司 '{company_name}'",
            "建议": f"您是否要查找: {', '.join(similar[:3])}" if similar else "请检查公司名称"
        }
    
    def _calculate_recommendation_index(self, company: Dict) -> str:
        """计算推荐指数"""
        score = (
            company["rating"] * 0.25 +
            company["work_life_balance"] * 0.2 +
            company["career_growth"] * 0.2 +
            company["benefits"] * 0.15 +
            company["culture"] * 0.2
        )
        
        if score >= 4.5:
            return "强烈推荐"
        elif score >= 4.0:
            return "推荐"
        elif score >= 3.5:
            return "一般"
        else:
            return "不推荐"
    
    def _generate_investment_advice(self, industry_data: Dict) -> str:
        """生成投资建议"""
        growth_rate = industry_data["growth_rate"]
        
        if growth_rate > 0.2:
            return "强烈建议投入学习，高增长潜力"
        elif growth_rate > 0.1:
            return "建议关注，稳定增长机会"
        elif growth_rate > 0.05:
            return "可以考虑，但需谨慎评估"
        else:
            return "增长缓慢，建议观望"
    
    def _generate_skill_learning_advice(self, skills: List[Dict]) -> List[str]:
        """生成技能学习建议"""
        advice = []
        
        high_value_skills = [s for s in skills if s["基础价值"] > 85]
        if len(high_value_skills) < 2:
            advice.append("建议重点学习高价值技能，提升竞争力")
        
        trending_skills = [s for s in skills if s["增长趋势"] > 15]
        if len(trending_skills) < 1:
            advice.append("关注新兴技术趋势，提前布局未来")
        
        categories = set(s["技能类别"] for s in skills)
        if len(categories) < 3:
            advice.append("扩展技能领域，增加技术栈广度")
        
        return advice
    
    # ================================
    # 🆕 新增缺失的方法
    # ================================
    
    def generate_industry_report(self, industry: str, region: str = "全球") -> Dict:
        """生成行业分析报告"""
        return self.get_industry_report(industry)
    
    def get_global_salary_benchmark(self, position: str, country: str, experience_years: int = 3) -> Dict:
        """获取全球薪资基准"""
        # 基础薪资数据
        base_salaries = {
            "水质在线监测工程师": 180000,
            "AI工程师": 250000,
            "前端工程师": 150000,
            "后端工程师": 170000,
            "DevOps工程师": 200000,
            "数据分析师": 160000
        }
        
        # 国家系数
        country_multipliers = {
            "中国": 1.0,
            "美国": 2.5,
            "德国": 2.0,
            "日本": 1.8,
            "新加坡": 1.6,
            "英国": 2.2
        }
        
        base_salary = base_salaries.get(position, 150000)
        country_multiplier = country_multipliers.get(country, 1.0)
        experience_multiplier = 1 + (experience_years * 0.15)
        
        final_salary = base_salary * country_multiplier * experience_multiplier
        
        return {
            "职位": position,
            "国家": country,
            "经验年限": experience_years,
            "基础薪资": base_salary,
            "国家系数": country_multiplier,
            "经验系数": experience_multiplier,
            "预估薪资": int(final_salary),
            "薪资范围": {
                "最低": int(final_salary * 0.8),
                "最高": int(final_salary * 1.3)
            },
            "市场竞争力": self._get_market_competitiveness(final_salary),
            "建议": self._generate_salary_advice(final_salary, position, country)
        }
    
    def generate_skill_value_report(self, skills: List[str], industry: str = "") -> Dict:
        """生成技能价值分析报告"""
        return self.get_skill_value_report(skills)
    
    def get_market_insights(self, query: str, scope: str = "全球") -> Dict:
        """获取市场洞察"""
        insights = self.generate_market_insights()
        
        # 根据查询内容过滤相关信息
        filtered_insights = {
            "查询": query,
            "范围": scope,
            "相关洞察": []
        }
        
        # 简单的关键词匹配
        query_lower = query.lower()
        
        if "水质" in query_lower or "环保" in query_lower:
            filtered_insights["相关洞察"].extend([
                "环保行业受政策驱动，发展前景良好",
                "水质监测技术需求增长，特别是智能化监测",
                "环保工程师薪资稳步上升，技术型人才更受欢迎"
            ])
        
        if "ai" in query_lower or "人工智能" in query_lower:
            filtered_insights["相关洞察"].extend([
                "AI行业爆发式增长，人才缺口巨大",
                "机器学习和深度学习技能价值极高",
                "AI+传统行业成为新趋势"
            ])
        
        if "薪资" in query_lower or "工资" in query_lower:
            filtered_insights["相关洞察"].extend([
                "技术岗位薪资持续上涨",
                "AI相关职位薪资涨幅最大",
                "一线城市薪资优势明显但生活成本高"
            ])
        
        # 如果没有匹配到特定内容，返回通用洞察
        if not filtered_insights["相关洞察"]:
            filtered_insights["相关洞察"] = [
                "技术行业整体发展良好",
                "持续学习是职业发展的关键",
                "跨领域技能组合更有竞争力"
            ]
        
        # 添加全球趋势
        filtered_insights["全球趋势"] = insights["全球趋势"]
        filtered_insights["投资建议"] = insights["投资建议"][:3]
        
        return filtered_insights
    
    def _get_market_competitiveness(self, salary: float) -> str:
        """获取市场竞争力"""
        if salary > 400000:
            return "顶尖水平"
        elif salary > 250000:
            return "高级水平"
        elif salary > 150000:
            return "中级水平"
        else:
            return "初级水平"
    
    def _generate_salary_advice(self, salary: float, position: str, country: str) -> List[str]:
        """生成薪资建议"""
        advice = []
        
        if salary > 300000:
            advice.append("薪资水平优秀，建议关注职业发展和技能提升")
        elif salary > 200000:
            advice.append("薪资水平良好，可考虑向更高级职位发展")
        else:
            advice.append("建议提升技能水平，争取更好的薪资待遇")
        
        if country == "中国":
            advice.append("国内市场竞争激烈，建议关注新兴技术领域")
        else:
            advice.append("海外市场机会多，但需要考虑文化适应和语言能力")
        
        return advice

# ================================
# 🤖 智能通用职位分析引擎 (重新设计)
# ================================

class UniversalJobAnalyzer:
    """
    🌍 通用职位分析引擎
    支持全球任意职位的智能分析，包括薪资预测、技能要求、发展前景等
    """
    
    def __init__(self):
        """初始化通用职位分析引擎"""
        # 全球主要城市数据
        self.global_cities = {
            "北京": {"等级": "一线", "生活成本": 1.2, "薪资系数": 1.0},
            "上海": {"等级": "一线", "生活成本": 1.25, "薪资系数": 1.05},
            "深圳": {"等级": "一线", "生活成本": 1.18, "薪资系数": 1.02},
            "广州": {"等级": "一线", "生活成本": 1.1, "薪资系数": 0.95},
            "杭州": {"等级": "新一线", "生活成本": 1.0, "薪资系数": 0.9},
            "成都": {"等级": "新一线", "生活成本": 0.85, "薪资系数": 0.8},
            "纽约": {"等级": "国际", "生活成本": 1.8, "薪资系数": 2.5},
            "旧金山": {"等级": "国际", "生活成本": 2.0, "薪资系数": 2.8},
            "伦敦": {"等级": "国际", "生活成本": 1.6, "薪资系数": 2.2},
            "东京": {"等级": "国际", "生活成本": 1.4, "薪资系数": 1.8},
            "新加坡": {"等级": "国际", "生活成本": 1.3, "薪资系数": 1.6}
        }
        
        # 行业关键词映射
        self.industry_keywords = {
            "互联网": ["前端", "后端", "全栈", "产品", "运营", "UI", "UX"],
            "人工智能": ["AI", "机器学习", "深度学习", "算法", "数据科学"],
            "金融科技": ["量化", "风控", "支付", "区块链", "金融"],
            "游戏": ["游戏开发", "Unity", "Unreal", "游戏策划"],
            "电商": ["电商", "零售", "供应链", "物流"],
            "教育": ["在线教育", "教学", "培训", "知识付费"],
            "医疗": ["医疗", "生物", "制药", "健康"],
            "汽车": ["汽车", "自动驾驶", "新能源", "车联网"],
            "房地产": ["房地产", "建筑", "装修", "物业"],
            "制造业": ["制造", "工业", "自动化", "机械"],
            "能源": ["能源", "电力", "石油", "新能源"],
            "环保": ["环保", "水质", "监测", "治理", "节能"]
        }
    
    def analyze_any_job(self, job_title: str, city: str = "北京", experience_years: int = 3) -> Dict:
        """
        🎯 分析任意职位
        
        Args:
            job_title: 职位名称
            city: 城市
            experience_years: 工作经验年限
            
        Returns:
            完整的职位分析报告
        """
        # 识别行业
        industry = self._identify_industry(job_title)
        
        # 获取城市数据
        city_data = self._get_city_data(city)
        
        # 预测薪资
        salary_info = self._predict_salary(job_title, city_data, experience_years)
        
        # 生成技能要求
        skills = self._generate_skills(job_title, industry)
        
        # 分析发展前景
        prospects = self._analyze_prospects(industry, job_title)
        
        # 生成建议
        advice = self._generate_advice(salary_info, city_data, prospects)
        
        return {
            "职位信息": {
                "职位": job_title,
                "城市": city,
                "行业": industry,
                "经验要求": f"{experience_years}年"
            },
            "薪资分析": salary_info,
            "技能要求": skills,
            "发展前景": prospects,
            "城市分析": city_data,
            "综合建议": advice,
            "分析时间": "2024-01-01"
        }
    
    def _identify_industry(self, job_title: str) -> str:
        """识别职位所属行业"""
        job_lower = job_title.lower()
        
        for industry, keywords in self.industry_keywords.items():
            for keyword in keywords:
                if keyword.lower() in job_lower:
                    return industry
        
        # 默认返回互联网行业
        return "互联网"
    
    def _get_city_data(self, city: str) -> Dict:
        """获取城市数据"""
        if city in self.global_cities:
            return self.global_cities[city]
        else:
            # 对于未知城市，使用默认值
            return {"等级": "其他", "生活成本": 0.8, "薪资系数": 0.7}
    
    def _predict_salary(self, job_title: str, city_data: Dict, experience_years: int) -> Dict:
        """预测薪资"""
        # 基础薪资（以北京为基准）
        base_salaries = {
            "工程师": 180000,
            "经理": 250000,
            "总监": 400000,
            "专员": 120000,
            "主管": 200000,
            "架构师": 350000,
            "分析师": 160000,
            "顾问": 220000
        }
        
        # 根据职位名称匹配基础薪资
        base_salary = 150000  # 默认值
        for role, salary in base_salaries.items():
            if role in job_title:
                base_salary = salary
                break
        
        # 应用城市系数和经验系数
        city_multiplier = city_data["薪资系数"]
        experience_multiplier = 1 + (experience_years * 0.12)
        
        final_salary = base_salary * city_multiplier * experience_multiplier
        
        return {
            "基础薪资": base_salary,
            "城市系数": city_multiplier,
            "经验系数": experience_multiplier,
            "预估年薪": int(final_salary),
            "薪资区间": {
                "下限": int(final_salary * 0.8),
                "上限": int(final_salary * 1.3)
            },
            "月薪估算": int(final_salary / 12)
        }
    
    def _generate_skills(self, job_title: str, industry: str) -> List[str]:
        """生成技能要求"""
        # 通用技能
        common_skills = ["沟通能力", "团队协作", "问题解决", "学习能力"]
        
        # 行业特定技能
        industry_skills = {
            "互联网": ["Python", "JavaScript", "React", "Vue", "MySQL", "Redis"],
            "人工智能": ["Python", "TensorFlow", "PyTorch", "机器学习", "深度学习", "数据分析"],
            "金融科技": ["Python", "Java", "风险管理", "量化分析", "区块链"],
            "环保": ["环境监测", "数据分析", "传感器技术", "环保法规", "水质分析"]
        }
        
        # 职位特定技能
        if "前端" in job_title:
            specific_skills = ["HTML", "CSS", "JavaScript", "React", "Vue", "TypeScript"]
        elif "后端" in job_title:
            specific_skills = ["Python", "Java", "MySQL", "Redis", "微服务", "API设计"]
        elif "AI" in job_title or "算法" in job_title:
            specific_skills = ["机器学习", "深度学习", "Python", "TensorFlow", "数据挖掘"]
        elif "产品" in job_title:
            specific_skills = ["产品设计", "用户研究", "数据分析", "项目管理", "原型设计"]
        else:
            specific_skills = ["专业技能", "行业知识", "工具使用"]
        
        # 合并技能
        all_skills = common_skills + industry_skills.get(industry, []) + specific_skills
        
        # 去重并返回前10个
        return list(dict.fromkeys(all_skills))[:10]
    
    def _analyze_prospects(self, industry: str, job_title: str) -> Dict:
        """分析发展前景"""
        # 行业前景评分
        industry_scores = {
            "人工智能": 95,
            "互联网": 85,
            "金融科技": 80,
            "环保": 88,
            "医疗": 82,
            "教育": 75,
            "游戏": 70,
            "制造业": 65
        }
        
        score = industry_scores.get(industry, 70)
        
        if score >= 90:
            outlook = "极佳"
            description = "行业高速发展，人才需求旺盛"
        elif score >= 80:
            outlook = "良好"
            description = "行业稳定发展，就业机会较多"
        elif score >= 70:
            outlook = "一般"
            description = "行业发展平稳，需要提升竞争力"
        else:
            outlook = "谨慎"
            description = "行业面临挑战，建议关注转型机会"
        
        return {
            "行业评分": score,
            "发展前景": outlook,
            "前景描述": description,
            "建议关注": ["技能提升", "行业趋势", "职业规划"]
        }
    
    def _generate_advice(self, salary_info: Dict, city_data: Dict, prospects: Dict) -> List[str]:
        """生成综合建议"""
        advice = []
        
        # 薪资建议
        if salary_info["预估年薪"] > 300000:
            advice.append("💰 薪资水平优秀，建议关注职业发展和技能深度")
        elif salary_info["预估年薪"] > 200000:
            advice.append("💰 薪资水平良好，可考虑向高级职位发展")
        else:
            advice.append("💰 建议提升核心技能，争取更好的薪资待遇")
        
        # 城市建议
        if city_data["生活成本"] > 1.5:
            advice.append("🏙️ 生活成本较高，建议合理规划支出和投资")
        elif city_data["生活成本"] < 0.9:
            advice.append("🏙️ 生活成本较低，性价比不错，适合长期发展")
        
        # 前景建议
        if prospects["行业评分"] >= 85:
            advice.append("🚀 行业前景优秀，建议深耕专业领域")
        else:
            advice.append("📈 建议关注行业趋势，适时调整发展方向")
        
        return advice

# ================================
# 🔧 工具函数
# ================================

def create_big_data_analyzer() -> BigDataAnalyzer:
    """创建大数据分析器"""
    return BigDataAnalyzer()

def create_universal_job_analyzer() -> UniversalJobAnalyzer:
    """创建通用职位分析器"""
    return UniversalJobAnalyzer()

if __name__ == "__main__":
    # 测试代码
    print("📊 大数据分析测试")
    analyzer = create_big_data_analyzer()
    print("公司分析:", analyzer.get_company_analysis("Google"))
    print("行业报告:", analyzer.get_industry_report("AI/机器学习"))
    print("职位热度:", analyzer.analyze_job_hotness(["AI工程师", "前端工程师"]))
    
    print("\n🤖 通用职位分析测试")
    universal_analyzer = create_universal_job_analyzer()
    result = universal_analyzer.analyze_any_job("AI工程师", "深圳", 5)
    print("职位分析结果:", result)