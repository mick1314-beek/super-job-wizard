#!/usr/bin/env python3
"""
🤖 AI智能分析引擎
基于机器学习和自然语言处理的智能求职分析

功能特性：
- 🧠 AI简历智能分析和优化
- 📊 基于技能栈的薪资预测
- 🎯 职业路径智能规划
- 📈 市场趋势分析和预测
- 🔍 技能价值评估
- 💡 个性化建议生成
"""

import re
import json
import math
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from collections import Counter

# ================================
# 🎯 技能价值数据库
# ================================

SKILL_VALUE_DATABASE = {
    # 编程语言
    "Python": {"base_value": 85, "growth_trend": 15, "demand_level": "极高", "category": "编程语言"},
    "JavaScript": {"base_value": 80, "growth_trend": 12, "demand_level": "极高", "category": "编程语言"},
    "Java": {"base_value": 75, "growth_trend": 8, "demand_level": "高", "category": "编程语言"},
    "Go": {"base_value": 90, "growth_trend": 25, "demand_level": "极高", "category": "编程语言"},
    "Rust": {"base_value": 95, "growth_trend": 30, "demand_level": "高", "category": "编程语言"},
    "TypeScript": {"base_value": 88, "growth_trend": 20, "demand_level": "极高", "category": "编程语言"},
    "C++": {"base_value": 70, "growth_trend": 5, "demand_level": "中", "category": "编程语言"},
    "C#": {"base_value": 72, "growth_trend": 6, "demand_level": "中", "category": "编程语言"},
    "PHP": {"base_value": 60, "growth_trend": -5, "demand_level": "中", "category": "编程语言"},
    "Swift": {"base_value": 82, "growth_trend": 10, "demand_level": "高", "category": "编程语言"},
    "Kotlin": {"base_value": 85, "growth_trend": 18, "demand_level": "高", "category": "编程语言"},
    
    # 前端技术
    "React": {"base_value": 85, "growth_trend": 15, "demand_level": "极高", "category": "前端"},
    "Vue": {"base_value": 80, "growth_trend": 12, "demand_level": "高", "category": "前端"},
    "Angular": {"base_value": 75, "growth_trend": 5, "demand_level": "中", "category": "前端"},
    "Next.js": {"base_value": 88, "growth_trend": 22, "demand_level": "极高", "category": "前端"},
    "Svelte": {"base_value": 90, "growth_trend": 25, "demand_level": "中", "category": "前端"},
    
    # 后端技术
    "Node.js": {"base_value": 82, "growth_trend": 12, "demand_level": "极高", "category": "后端"},
    "Django": {"base_value": 78, "growth_trend": 8, "demand_level": "高", "category": "后端"},
    "Flask": {"base_value": 75, "growth_trend": 5, "demand_level": "中", "category": "后端"},
    "Spring": {"base_value": 73, "growth_trend": 3, "demand_level": "中", "category": "后端"},
    "Express": {"base_value": 80, "growth_trend": 10, "demand_level": "高", "category": "后端"},
    
    # 数据库
    "PostgreSQL": {"base_value": 85, "growth_trend": 15, "demand_level": "极高", "category": "数据库"},
    "MongoDB": {"base_value": 80, "growth_trend": 10, "demand_level": "高", "category": "数据库"},
    "Redis": {"base_value": 82, "growth_trend": 12, "demand_level": "高", "category": "数据库"},
    "MySQL": {"base_value": 70, "growth_trend": 2, "demand_level": "中", "category": "数据库"},
    "Elasticsearch": {"base_value": 88, "growth_trend": 18, "demand_level": "高", "category": "数据库"},
    
    # 云计算和DevOps
    "AWS": {"base_value": 90, "growth_trend": 20, "demand_level": "极高", "category": "云计算"},
    "Azure": {"base_value": 85, "growth_trend": 18, "demand_level": "极高", "category": "云计算"},
    "GCP": {"base_value": 88, "growth_trend": 22, "demand_level": "高", "category": "云计算"},
    "Docker": {"base_value": 85, "growth_trend": 15, "demand_level": "极高", "category": "DevOps"},
    "Kubernetes": {"base_value": 92, "growth_trend": 25, "demand_level": "极高", "category": "DevOps"},
    "Terraform": {"base_value": 90, "growth_trend": 20, "demand_level": "高", "category": "DevOps"},
    "Jenkins": {"base_value": 75, "growth_trend": 5, "demand_level": "中", "category": "DevOps"},
    
    # AI/ML
    "TensorFlow": {"base_value": 92, "growth_trend": 25, "demand_level": "极高", "category": "AI/ML"},
    "PyTorch": {"base_value": 95, "growth_trend": 30, "demand_level": "极高", "category": "AI/ML"},
    "Scikit-learn": {"base_value": 85, "growth_trend": 15, "demand_level": "高", "category": "AI/ML"},
    "OpenAI": {"base_value": 98, "growth_trend": 40, "demand_level": "极高", "category": "AI/ML"},
    "LangChain": {"base_value": 95, "growth_trend": 35, "demand_level": "极高", "category": "AI/ML"},
    
    # 区块链
    "Solidity": {"base_value": 95, "growth_trend": 30, "demand_level": "高", "category": "区块链"},
    "Web3": {"base_value": 92, "growth_trend": 25, "demand_level": "高", "category": "区块链"},
    "Ethereum": {"base_value": 90, "growth_trend": 20, "demand_level": "中", "category": "区块链"},
}

# ================================
# 📊 行业薪资预测模型
# ================================

INDUSTRY_SALARY_MODELS = {
    "互联网": {
        "base_salary": 150000,
        "experience_multiplier": 1.25,
        "skill_bonus": 0.15,
        "location_factor": 1.2,
        "growth_rate": 0.12
    },
    "AI/机器学习": {
        "base_salary": 200000,
        "experience_multiplier": 1.35,
        "skill_bonus": 0.25,
        "location_factor": 1.3,
        "growth_rate": 0.18
    },
    "金融科技": {
        "base_salary": 180000,
        "experience_multiplier": 1.3,
        "skill_bonus": 0.2,
        "location_factor": 1.25,
        "growth_rate": 0.15
    },
    "区块链": {
        "base_salary": 220000,
        "experience_multiplier": 1.4,
        "skill_bonus": 0.3,
        "location_factor": 1.35,
        "growth_rate": 0.22
    },
    "云计算": {
        "base_salary": 170000,
        "experience_multiplier": 1.28,
        "skill_bonus": 0.18,
        "location_factor": 1.22,
        "growth_rate": 0.16
    },
    "游戏开发": {
        "base_salary": 140000,
        "experience_multiplier": 1.2,
        "skill_bonus": 0.12,
        "location_factor": 1.1,
        "growth_rate": 0.08
    },
    "电商": {
        "base_salary": 130000,
        "experience_multiplier": 1.18,
        "skill_bonus": 0.1,
        "location_factor": 1.15,
        "growth_rate": 0.1
    }
}

# ================================
# 🎯 职业发展路径
# ================================

CAREER_PATHS = {
    "前端工程师": {
        "初级": {"skills": ["HTML", "CSS", "JavaScript"], "salary_range": (80000, 120000)},
        "中级": {"skills": ["React", "Vue", "TypeScript", "Webpack"], "salary_range": (120000, 200000)},
        "高级": {"skills": ["Next.js", "微前端", "性能优化", "架构设计"], "salary_range": (200000, 350000)},
        "专家": {"skills": ["技术领导", "团队管理", "技术决策"], "salary_range": (350000, 600000)}
    },
    "后端工程师": {
        "初级": {"skills": ["Python", "Java", "数据库"], "salary_range": (90000, 140000)},
        "中级": {"skills": ["微服务", "Redis", "消息队列", "API设计"], "salary_range": (140000, 220000)},
        "高级": {"skills": ["分布式系统", "高并发", "系统架构"], "salary_range": (220000, 400000)},
        "专家": {"skills": ["技术架构", "团队领导", "技术战略"], "salary_range": (400000, 700000)}
    },
    "AI工程师": {
        "初级": {"skills": ["Python", "机器学习", "数据分析"], "salary_range": (120000, 180000)},
        "中级": {"skills": ["深度学习", "TensorFlow", "PyTorch"], "salary_range": (180000, 300000)},
        "高级": {"skills": ["模型优化", "MLOps", "算法研究"], "salary_range": (300000, 500000)},
        "专家": {"skills": ["AI架构", "研究领导", "产品化"], "salary_range": (500000, 1000000)}
    },
    "DevOps工程师": {
        "初级": {"skills": ["Linux", "Docker", "Git"], "salary_range": (100000, 150000)},
        "中级": {"skills": ["Kubernetes", "AWS", "CI/CD"], "salary_range": (150000, 250000)},
        "高级": {"skills": ["云架构", "自动化", "监控"], "salary_range": (250000, 400000)},
        "专家": {"skills": ["平台架构", "团队领导", "技术战略"], "salary_range": (400000, 650000)}
    }
}

# ================================
# 🧠 AI分析引擎类
# ================================

class AIJobAnalyzer:
    def __init__(self):
        self.skill_database = SKILL_VALUE_DATABASE
        self.industry_models = INDUSTRY_SALARY_MODELS
        self.career_paths = CAREER_PATHS
    
    def extract_skills_from_resume(self, resume_text: str) -> List[Dict]:
        """从简历中提取技能"""
        found_skills = []
        resume_lower = resume_text.lower()
        
        for skill, data in self.skill_database.items():
            # 使用正则表达式匹配技能
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            if re.search(pattern, resume_lower):
                found_skills.append({
                    "skill": skill,
                    "value": data["base_value"],
                    "trend": data["growth_trend"],
                    "demand": data["demand_level"],
                    "category": data["category"]
                })
        
        return sorted(found_skills, key=lambda x: x["value"], reverse=True)
    
    def calculate_skill_score(self, skills: List[str]) -> Dict:
        """计算技能综合评分"""
        if not skills:
            return {"total_score": 0, "category_scores": {}, "recommendations": []}
        
        total_value = 0
        category_scores = {}
        skill_details = []
        
        for skill in skills:
            if skill in self.skill_database:
                data = self.skill_database[skill]
                total_value += data["base_value"]
                category = data["category"]
                
                if category not in category_scores:
                    category_scores[category] = []
                category_scores[category].append(data["base_value"])
                
                skill_details.append({
                    "skill": skill,
                    "value": data["base_value"],
                    "trend": data["growth_trend"]
                })
        
        # 计算各类别平均分
        for category in category_scores:
            category_scores[category] = sum(category_scores[category]) / len(category_scores[category])
        
        # 生成建议
        recommendations = self._generate_skill_recommendations(category_scores, skill_details)
        
        return {
            "total_score": total_value,
            "average_score": total_value / len(skills) if skills else 0,
            "category_scores": category_scores,
            "skill_details": skill_details,
            "recommendations": recommendations
        }
    
    def predict_salary_range(self, position: str, experience_years: int, 
                           skills: List[str], location: str, company_size: str = "medium") -> Dict:
        """预测薪资范围（新增函数）"""
        # 根据职位推断行业
        industry_mapping = {
            "前端": "互联网", "后端": "互联网", "全栈": "互联网",
            "AI": "AI/机器学习", "机器学习": "AI/机器学习", "算法": "AI/机器学习",
            "DevOps": "云计算", "运维": "云计算", "云计算": "云计算",
            "区块链": "区块链", "Web3": "区块链",
            "游戏": "游戏开发", "Unity": "游戏开发"
        }
        
        industry = "互联网"  # 默认
        for key, value in industry_mapping.items():
            if key in position:
                industry = value
                break
        
        # 公司规模调整系数
        size_factors = {
            "startup": 0.85,
            "medium": 1.0,
            "large": 1.15
        }
        size_factor = size_factors.get(company_size, 1.0)
        
        # 调用原有的predict_salary函数
        base_result = self.predict_salary(skills, experience_years, industry, location)
        
        # 应用公司规模调整
        adjusted_salary = base_result["predicted_salary"] * size_factor
        adjusted_range = (base_result["salary_range"][0] * size_factor, 
                         base_result["salary_range"][1] * size_factor)
        
        return {
            "position": position,
            "predicted_salary": adjusted_salary,
            "salary_range": adjusted_range,
            "location": location,
            "company_size": company_size,
            "industry": industry,
            "factors": {
                **base_result["factors"],
                "company_size_factor": size_factor
            },
            "confidence": base_result["confidence"],
            "market_position": base_result["market_position"],
            "recommendations": [
                f"基于{experience_years}年经验和技能栈，预测薪资范围为 ¥{adjusted_range[0]:,.0f} - ¥{adjusted_range[1]:,.0f}",
                f"在{location}的{company_size}公司，{position}职位的市场竞争力为{base_result['market_position']}",
                "建议关注技能提升和市场趋势变化"
            ]
        }
    
    def predict_salary(self, skills: List[str], experience_years: int, 
                      industry: str, location: str = "北京") -> Dict:
        """基于技能和经验预测薪资"""
        if industry not in self.industry_models:
            industry = "互联网"  # 默认行业
        
        model = self.industry_models[industry]
        
        # 基础薪资
        base_salary = model["base_salary"]
        
        # 经验加成
        experience_factor = min(model["experience_multiplier"] ** (experience_years / 3), 3.0)
        
        # 技能加成
        skill_score = self.calculate_skill_score(skills)
        skill_factor = 1 + (skill_score["average_score"] / 100) * model["skill_bonus"]
        
        # 地区加成
        location_factors = {
            "北京": 1.2, "上海": 1.25, "深圳": 1.18, "杭州": 1.08,
            "广州": 1.1, "成都": 0.95, "武汉": 0.9, "南京": 1.0
        }
        location_factor = location_factors.get(location, 1.0)
        
        # 计算预测薪资
        predicted_salary = base_salary * experience_factor * skill_factor * location_factor
        
        # 薪资范围（±20%）
        salary_range = (predicted_salary * 0.8, predicted_salary * 1.2)
        
        return {
            "predicted_salary": predicted_salary,
            "salary_range": salary_range,
            "factors": {
                "base_salary": base_salary,
                "experience_factor": experience_factor,
                "skill_factor": skill_factor,
                "location_factor": location_factor
            },
            "confidence": self._calculate_prediction_confidence(skills, experience_years),
            "market_position": self._get_market_position(predicted_salary, industry)
        }
    
    def generate_career_plan(self, current_skills: List[str], target_role: str, 
                           experience_years: int) -> Dict:
        """生成职业发展规划"""
        if target_role not in self.career_paths:
            return {"错误": f"不支持的职业路径: {target_role}"}
        
        path = self.career_paths[target_role]
        current_level = self._determine_current_level(current_skills, path, experience_years)
        
        plan = {
            "current_level": current_level,
            "career_path": target_role,
            "development_plan": []
        }
        
        # 生成发展计划
        levels = ["初级", "中级", "高级", "专家"]
        current_index = levels.index(current_level) if current_level in levels else 0
        
        for i in range(current_index, len(levels)):
            level = levels[i]
            level_data = path[level]
            
            missing_skills = [skill for skill in level_data["skills"] 
                            if skill not in current_skills]
            
            plan["development_plan"].append({
                "level": level,
                "target_skills": level_data["skills"],
                "missing_skills": missing_skills,
                "salary_range": level_data["salary_range"],
                "estimated_time": self._estimate_development_time(missing_skills, i - current_index),
                "learning_priority": self._prioritize_skills(missing_skills)
            })
        
        return plan
    
    def analyze_market_trends(self, industry: str, region: str = "全球") -> Dict:
        """分析行业市场趋势"""
        # 根据行业获取相关技能
        industry_skills = self._get_industry_skills(industry)
        
        trend_analysis = {
            "industry": industry,
            "region": region,
            "hot_skills": [],
            "declining_skills": [],
            "emerging_skills": [],
            "skill_trends": {},
            "market_outlook": "",
            "growth_rate": 0,
            "job_demand": ""
        }
        
        # 分析行业相关技能趋势
        for skill in industry_skills:
            if skill in self.skill_database:
                data = self.skill_database[skill]
                trend = data["growth_trend"]
                
                trend_analysis["skill_trends"][skill] = {
                    "trend": trend,
                    "status": "上升" if trend > 10 else "稳定" if trend > 0 else "下降",
                    "demand": data["demand_level"]
                }
                
                if trend > 20:
                    trend_analysis["hot_skills"].append(skill)
                elif trend < 0:
                    trend_analysis["declining_skills"].append(skill)
                elif trend > 15:
                    trend_analysis["emerging_skills"].append(skill)
        
        # 添加行业分析
        trend_analysis.update(self._analyze_industry_outlook(industry, region))
        
        # 添加市场建议
        trend_analysis["recommendations"] = self._generate_market_recommendations(trend_analysis)
        
        return trend_analysis
    
    def analyze_skill_gaps(self, current_skills: List[str], target_position: str) -> Dict:
        """分析技能差距"""
        # 获取目标职位所需技能
        required_skills = self._get_position_required_skills(target_position)
        
        # 计算技能差距
        missing_skills = [skill for skill in required_skills if skill not in current_skills]
        matching_skills = [skill for skill in current_skills if skill in required_skills]
        
        # 评估技能匹配度
        match_rate = len(matching_skills) / len(required_skills) if required_skills else 0
        
        # 生成学习建议
        learning_plan = self._generate_learning_plan(missing_skills, target_position)
        
        return {
            "target_position": target_position,
            "current_skills": current_skills,
            "required_skills": required_skills,
            "missing_skills": missing_skills,
            "matching_skills": matching_skills,
            "skill_match_rate": round(match_rate * 100, 1),
            "gap_analysis": {
                "critical_gaps": [s for s in missing_skills if self._is_critical_skill(s, target_position)],
                "nice_to_have": [s for s in missing_skills if not self._is_critical_skill(s, target_position)]
            },
            "learning_plan": learning_plan,
            "estimated_time": self._estimate_learning_time(missing_skills),
            "recommendations": self._generate_skill_gap_recommendations(missing_skills, match_rate)
        }
    
    def _get_industry_skills(self, industry: str) -> List[str]:
        """获取行业相关技能"""
        industry_skill_map = {
            "水质在线监测": ["Python", "数据分析", "传感器技术", "环境工程", "物联网", "数据库", "监控系统"],
            "环保": ["环境工程", "数据分析", "Python", "GIS", "传感器技术", "物联网", "监控系统"],
            "互联网": ["Python", "JavaScript", "React", "Node.js", "AWS", "Docker", "Kubernetes"],
            "AI": ["Python", "TensorFlow", "PyTorch", "机器学习", "深度学习", "数据科学"],
            "金融科技": ["Python", "Java", "区块链", "风控", "数据分析", "算法交易"],
            "云计算": ["AWS", "Azure", "GCP", "Docker", "Kubernetes", "Terraform", "DevOps"]
        }
        
        return industry_skill_map.get(industry, ["Python", "数据分析", "项目管理"])
    
    def _analyze_industry_outlook(self, industry: str, region: str) -> Dict:
        """分析行业前景"""
        industry_data = {
            "水质在线监测": {
                "market_outlook": "政策驱动下快速发展，环保要求日益严格",
                "growth_rate": 15,
                "job_demand": "高需求，特别是技术型人才"
            },
            "环保": {
                "market_outlook": "国家重点支持行业，长期发展前景良好",
                "growth_rate": 12,
                "job_demand": "持续增长，技术和管理人才都有需求"
            },
            "互联网": {
                "market_outlook": "成熟行业，竞争激烈但机会仍多",
                "growth_rate": 8,
                "job_demand": "中高需求，偏向高级人才"
            },
            "AI": {
                "market_outlook": "爆发式增长，是未来重点发展方向",
                "growth_rate": 25,
                "job_demand": "极高需求，人才缺口巨大"
            }
        }
        
        return industry_data.get(industry, {
            "market_outlook": "行业发展稳定",
            "growth_rate": 5,
            "job_demand": "中等需求"
        })
    
    def _get_position_required_skills(self, position: str) -> List[str]:
        """获取职位所需技能"""
        position_skills = {
            "水质在线监测工程师": ["Python", "数据分析", "传感器技术", "环境工程", "物联网", "SQL", "监控系统", "设备维护"],
            "高级水质在线监测工程师": ["Python", "数据分析", "传感器技术", "环境工程", "物联网", "SQL", "监控系统", "设备维护", "项目管理", "团队领导"],
            "前端工程师": ["HTML", "CSS", "JavaScript", "React", "Vue", "TypeScript"],
            "后端工程师": ["Python", "Java", "数据库", "API设计", "微服务", "Redis"],
            "AI工程师": ["Python", "机器学习", "深度学习", "TensorFlow", "PyTorch", "数据科学"],
            "DevOps工程师": ["Linux", "Docker", "Kubernetes", "AWS", "CI/CD", "监控"]
        }
        
        return position_skills.get(position, ["Python", "数据分析", "项目管理"])
    
    def _is_critical_skill(self, skill: str, position: str) -> bool:
        """判断是否为关键技能"""
        critical_skills = {
            "水质在线监测工程师": ["Python", "数据分析", "传感器技术", "环境工程"],
            "AI工程师": ["Python", "机器学习", "深度学习"],
            "前端工程师": ["JavaScript", "React", "HTML", "CSS"]
        }
        
        return skill in critical_skills.get(position, [])
    
    def _generate_learning_plan(self, missing_skills: List[str], position: str) -> Dict:
        """生成学习计划"""
        plan = {
            "phase_1": {"skills": [], "duration": "1-3个月", "priority": "高"},
            "phase_2": {"skills": [], "duration": "3-6个月", "priority": "中"},
            "phase_3": {"skills": [], "duration": "6-12个月", "priority": "低"}
        }
        
        for skill in missing_skills:
            if self._is_critical_skill(skill, position):
                plan["phase_1"]["skills"].append(skill)
            elif skill in self.skill_database and self.skill_database[skill]["base_value"] > 80:
                plan["phase_2"]["skills"].append(skill)
            else:
                plan["phase_3"]["skills"].append(skill)
        
        return plan
    
    def _estimate_learning_time(self, missing_skills: List[str]) -> str:
        """估算学习时间"""
        total_months = len(missing_skills) * 2  # 每个技能平均2个月
        
        if total_months <= 3:
            return "1-3个月"
        elif total_months <= 6:
            return "3-6个月"
        elif total_months <= 12:
            return "6-12个月"
        else:
            return "12个月以上"
    
    def _generate_skill_gap_recommendations(self, missing_skills: List[str], match_rate: float) -> List[str]:
        """生成技能差距建议"""
        recommendations = []
        
        if match_rate < 0.3:
            recommendations.append("🚨 技能匹配度较低，建议先学习核心技能再考虑申请")
        elif match_rate < 0.6:
            recommendations.append("⚠️ 需要补充关键技能，建议有针对性地学习")
        else:
            recommendations.append("✅ 技能匹配度良好，可以考虑申请并在工作中继续学习")
        
        if len(missing_skills) > 5:
            recommendations.append("📚 缺失技能较多，建议制定长期学习计划")
        
        return recommendations
    
    def _generate_skill_recommendations(self, category_scores: Dict, skill_details: List) -> List[str]:
        """生成技能建议"""
        recommendations = []
        
        # 检查技能平衡性
        if len(category_scores) < 3:
            recommendations.append("建议扩展技能栈，增加更多技术领域的技能")
        
        # 检查高价值技能
        high_value_skills = [s for s in skill_details if s["value"] > 85]
        if len(high_value_skills) < 2:
            recommendations.append("建议学习更多高价值技能，如AI/ML、云计算等")
        
        # 检查趋势技能
        trending_skills = [s for s in skill_details if s["trend"] > 15]
        if len(trending_skills) < 1:
            recommendations.append("建议关注新兴技术趋势，学习热门技能")
        
        return recommendations
    
    def _calculate_prediction_confidence(self, skills: List[str], experience_years: int) -> float:
        """计算预测置信度"""
        base_confidence = 0.7
        
        # 技能数量加成
        skill_bonus = min(len(skills) * 0.05, 0.2)
        
        # 经验加成
        experience_bonus = min(experience_years * 0.02, 0.1)
        
        return min(base_confidence + skill_bonus + experience_bonus, 0.95)
    
    def _get_market_position(self, salary: float, industry: str) -> str:
        """获取市场位置"""
        if salary > 400000:
            return "顶尖水平"
        elif salary > 250000:
            return "高级水平"
        elif salary > 150000:
            return "中级水平"
        else:
            return "初级水平"
    
    def _determine_current_level(self, skills: List[str], path: Dict, experience: int) -> str:
        """确定当前职业级别"""
        levels = ["初级", "中级", "高级", "专家"]
        
        for i, level in enumerate(levels):
            level_skills = path[level]["skills"]
            matching_skills = len([s for s in skills if s in level_skills])
            skill_coverage = matching_skills / len(level_skills)
            
            # 综合技能覆盖度和经验判断
            if skill_coverage < 0.5 or experience < i * 2:
                return levels[max(0, i - 1)] if i > 0 else "初级"
        
        return "专家"
    
    def _estimate_development_time(self, missing_skills: List[str], level_gap: int) -> str:
        """估算发展时间"""
        base_time = len(missing_skills) * 2 + level_gap * 6  # 月
        
        if base_time <= 6:
            return "3-6个月"
        elif base_time <= 12:
            return "6-12个月"
        elif base_time <= 24:
            return "1-2年"
        else:
            return "2年以上"
    
    def _prioritize_skills(self, skills: List[str]) -> List[str]:
        """技能学习优先级排序"""
        skill_priorities = []
        
        for skill in skills:
            if skill in self.skill_database:
                data = self.skill_database[skill]
                priority_score = data["base_value"] + data["growth_trend"]
                skill_priorities.append((skill, priority_score))
        
        # 按优先级排序
        skill_priorities.sort(key=lambda x: x[1], reverse=True)
        return [skill for skill, _ in skill_priorities]
    
    def _generate_market_recommendations(self, trend_analysis: Dict) -> List[str]:
        """生成市场建议"""
        recommendations = []
        
        if trend_analysis["hot_skills"]:
            recommendations.append(f"重点关注热门技能: {', '.join(trend_analysis['hot_skills'][:3])}")
        
        if trend_analysis["declining_skills"]:
            recommendations.append(f"考虑转型，避免过度依赖: {', '.join(trend_analysis['declining_skills'][:2])}")
        
        if trend_analysis["emerging_skills"]:
            recommendations.append(f"提前布局新兴技能: {', '.join(trend_analysis['emerging_skills'][:3])}")
        
        return recommendations

# ================================
# 🔧 工具函数
# ================================

def create_ai_analyzer() -> AIJobAnalyzer:
    """创建AI分析器实例"""
    return AIJobAnalyzer()

def analyze_resume_with_ai(resume_text: str, target_position: str = "") -> Dict:
    """AI简历分析"""
    analyzer = create_ai_analyzer()
    
    # 提取技能
    skills = analyzer.extract_skills_from_resume(resume_text)
    skill_names = [s["skill"] for s in skills]
    
    # 计算技能评分
    skill_score = analyzer.calculate_skill_score(skill_names)
    
    # 分析市场趋势
    market_trends = analyzer.analyze_market_trends(skill_names)
    
    return {
        "extracted_skills": skills,
        "skill_analysis": skill_score,
        "market_trends": market_trends,
        "ai_recommendations": _generate_ai_recommendations(skills, skill_score, market_trends)
    }

def _generate_ai_recommendations(skills: List[Dict], skill_score: Dict, trends: Dict) -> List[str]:
    """生成AI建议"""
    recommendations = []
    
    # 基于技能分析的建议
    if skill_score["average_score"] < 70:
        recommendations.append("🎯 建议重点提升核心技能，学习高价值技术栈")
    
    # 基于市场趋势的建议
    if trends["hot_skills"]:
        recommendations.append(f"🔥 建议学习热门技能: {', '.join(trends['hot_skills'][:2])}")
    
    # 基于技能平衡性的建议
    categories = skill_score.get("category_scores", {})
    if len(categories) < 3:
        recommendations.append("📚 建议扩展技能领域，增加技术栈的广度")
    
    return recommendations

if __name__ == "__main__":
    # 测试代码
    analyzer = create_ai_analyzer()
    test_skills = ["Python", "React", "AWS", "Docker"]
    
    print("🤖 AI分析引擎测试")
    print("技能评分:", analyzer.calculate_skill_score(test_skills))
    print("薪资预测:", analyzer.predict_salary(test_skills, 3, "互联网"))
    print("市场趋势:", analyzer.analyze_market_trends(test_skills))