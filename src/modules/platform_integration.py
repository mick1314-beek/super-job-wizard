#!/usr/bin/env python3
"""
🔗 平台集成模块
整合各大求职平台和社交网络的数据和功能

功能特性：
- 💼 LinkedIn数据分析和优化
- 📱 多平台求职进度追踪
- 📧 智能邮件模板生成
- 📅 面试日程管理系统
- 🔍 职位信息聚合分析
- 📊 社交网络影响力评估
"""

import json
import re
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from collections import defaultdict

# ================================
# 💼 LinkedIn分析数据
# ================================

LINKEDIN_OPTIMIZATION_RULES = {
    "标题优化": {
        "关键词": ["AI", "机器学习", "云计算", "全栈", "DevOps", "区块链"],
        "格式": "{职位} | {核心技能} | {年限}年经验",
        "长度": (50, 120),
        "建议": [
            "包含核心技能关键词",
            "突出年限和专业领域",
            "使用行业术语",
            "避免过于通用的描述"
        ]
    },
    "摘要优化": {
        "结构": ["开场白", "核心技能", "工作经历亮点", "职业目标"],
        "长度": (200, 2000),
        "关键元素": [
            "量化成果",
            "技术栈列表",
            "行业经验",
            "个人特色"
        ]
    },
    "技能标签": {
        "热门技能": [
            "Python", "JavaScript", "React", "AWS", "Docker",
            "Kubernetes", "机器学习", "数据分析", "项目管理"
        ],
        "新兴技能": [
            "ChatGPT", "LangChain", "Stable Diffusion", "Web3",
            "Solidity", "Terraform", "GraphQL"
        ]
    }
}

# ================================
# 📱 求职平台数据
# ================================

JOB_PLATFORMS = {
    "LinkedIn": {
        "类型": "国际专业社交",
        "优势": ["全球职位", "专业网络", "行业洞察"],
        "适合人群": ["外企", "海外工作", "高级职位"],
        "使用技巧": [
            "完善个人资料",
            "主动建立连接",
            "发布专业内容",
            "参与行业讨论"
        ]
    },
    "BOSS直聘": {
        "类型": "直聊招聘",
        "优势": ["直接沟通", "响应快速", "职位丰富"],
        "适合人群": ["互联网", "快速求职", "中高级职位"],
        "使用技巧": [
            "优化简历关键词",
            "主动打招呼",
            "及时回复消息",
            "展示专业能力"
        ]
    },
    "拉勾网": {
        "类型": "互联网专业",
        "优势": ["互联网职位", "薪资透明", "公司详情"],
        "适合人群": ["互联网行业", "技术岗位"],
        "使用技巧": [
            "突出技术能力",
            "关注公司动态",
            "参与技术分享"
        ]
    },
    "智联招聘": {
        "类型": "综合招聘",
        "优势": ["职位全面", "传统企业多", "服务完善"],
        "适合人群": ["传统行业", "应届生", "全职位类型"],
        "使用技巧": [
            "详细填写简历",
            "使用求职意向",
            "关注企业宣讲"
        ]
    },
    "猎聘": {
        "类型": "中高端招聘",
        "优势": ["高端职位", "猎头服务", "薪资高"],
        "适合人群": ["管理岗位", "高级技术", "跳槽人群"],
        "使用技巧": [
            "展示管理经验",
            "突出核心成就",
            "保持简历更新"
        ]
    }
}

# ================================
# 📧 邮件模板库
# ================================

EMAIL_TEMPLATES = {
    "求职申请": {
        "主题": "应聘{职位名称} - {姓名}",
        "模板": """尊敬的HR/招聘负责人：

您好！我是{姓名}，对贵公司的{职位名称}职位非常感兴趣。

【个人背景】
我有{工作年限}年的{专业领域}经验，擅长{核心技能}。在之前的工作中，我{主要成就}。

【匹配度分析】
根据职位要求，我的优势包括：
{匹配点列表}

【期望】
希望能有机会进一步交流，我的联系方式：{联系方式}

期待您的回复！

此致
敬礼！

{姓名}
{日期}""",
        "变量": ["姓名", "职位名称", "工作年限", "专业领域", "核心技能", "主要成就", "匹配点列表", "联系方式", "日期"]
    },
    
    "面试感谢": {
        "主题": "感谢面试机会 - {职位名称} - {姓名}",
        "模板": """尊敬的{面试官姓名}：

您好！

感谢您今天抽出宝贵时间为我进行{职位名称}的面试。通过今天的交流，我对贵公司和这个职位有了更深入的了解。

【面试收获】
{面试收获内容}

【补充说明】
关于面试中提到的{技术问题}，我想补充说明：
{补充内容}

【再次表达兴趣】
我对加入贵公司团队非常期待，相信我的{核心优势}能为团队带来价值。

期待您的好消息！

此致
敬礼！

{姓名}
{联系方式}
{日期}""",
        "变量": ["面试官姓名", "职位名称", "姓名", "面试收获内容", "技术问题", "补充内容", "核心优势", "联系方式", "日期"]
    },
    
    "薪资谈判": {
        "主题": "关于{职位名称}薪资待遇的讨论 - {姓名}",
        "模板": """尊敬的{HR姓名}：

您好！

非常感谢贵公司对我的认可，我对{职位名称}这个机会非常珍惜。

【市场调研】
根据我的市场调研，{职位名称}在{城市}的薪资范围通常在{市场薪资范围}。

【个人价值】
基于我的{核心优势}，我相信能为公司创造{预期价值}。

【期望薪资】
综合考虑我的经验和市场情况，我的期望薪资是{期望薪资}。

【灵活性】
我也理解公司的预算考虑，我们可以在{其他福利}方面进行讨论。

期待进一步沟通！

此致
敬礼！

{姓名}
{联系方式}
{日期}""",
        "变量": ["HR姓名", "职位名称", "姓名", "城市", "市场薪资范围", "核心优势", "预期价值", "期望薪资", "其他福利", "联系方式", "日期"]
    }
}

# ================================
# 📅 面试管理数据
# ================================

INTERVIEW_TYPES = {
    "电话面试": {
        "时长": "30-45分钟",
        "准备要点": ["简历熟悉", "基础问题", "语言表达"],
        "常见问题": [
            "自我介绍",
            "为什么选择我们公司",
            "职业规划",
            "薪资期望"
        ]
    },
    "技术面试": {
        "时长": "60-90分钟",
        "准备要点": ["技术栈复习", "项目经验", "算法练习"],
        "常见问题": [
            "技术栈深度问题",
            "项目架构设计",
            "代码实现",
            "性能优化"
        ]
    },
    "HR面试": {
        "时长": "30-60分钟",
        "准备要点": ["公司了解", "文化匹配", "软技能"],
        "常见问题": [
            "团队合作经验",
            "压力处理能力",
            "学习能力",
            "职业稳定性"
        ]
    },
    "终面": {
        "时长": "45-90分钟",
        "准备要点": ["综合能力", "领导力", "战略思维"],
        "常见问题": [
            "管理经验",
            "决策能力",
            "创新思维",
            "长期规划"
        ]
    }
}

# ================================
# 🔗 平台集成分析类
# ================================

class PlatformIntegrator:
    def __init__(self):
        self.platforms = JOB_PLATFORMS
        self.email_templates = EMAIL_TEMPLATES
        self.interview_types = INTERVIEW_TYPES
        self.linkedin_rules = LINKEDIN_OPTIMIZATION_RULES
    
    def analyze_linkedin_profile(self, profile_data: Dict) -> Dict:
        """分析LinkedIn个人资料"""
        analysis = {
            "优化建议": [],
            "评分": {},
            "关键词分析": {},
            "改进方案": {}
        }
        
        # 分析标题
        headline = profile_data.get("headline", "")
        headline_score = self._analyze_headline(headline)
        analysis["评分"]["标题"] = headline_score
        
        # 分析摘要
        summary = profile_data.get("summary", "")
        summary_score = self._analyze_summary(summary)
        analysis["评分"]["摘要"] = summary_score
        
        # 分析技能
        skills = profile_data.get("skills", [])
        skills_analysis = self._analyze_skills(skills)
        analysis["关键词分析"] = skills_analysis
        
        # 生成优化建议
        analysis["优化建议"] = self._generate_linkedin_suggestions(
            headline_score, summary_score, skills_analysis
        )
        
        # 改进方案
        analysis["改进方案"] = self._create_improvement_plan(profile_data)
        
        return analysis
    
    def track_job_applications(self, applications: List[Dict]) -> Dict:
        """追踪求职申请进度"""
        tracking = {
            "总体统计": {},
            "平台分析": {},
            "状态分布": {},
            "时间线": [],
            "建议": []
        }
        
        # 总体统计
        total_apps = len(applications)
        platforms_used = set(app.get("platform", "未知") for app in applications)
        
        tracking["总体统计"] = {
            "总申请数": total_apps,
            "使用平台": list(platforms_used),
            "平均响应率": self._calculate_response_rate(applications),
            "面试转化率": self._calculate_interview_rate(applications)
        }
        
        # 平台分析
        platform_stats = defaultdict(list)
        for app in applications:
            platform = app.get("platform", "未知")
            platform_stats[platform].append(app)
        
        for platform, apps in platform_stats.items():
            tracking["平台分析"][platform] = {
                "申请数量": len(apps),
                "响应数量": len([a for a in apps if a.get("status") != "已投递"]),
                "面试数量": len([a for a in apps if "面试" in a.get("status", "")]),
                "成功率": self._calculate_platform_success_rate(apps)
            }
        
        # 状态分布
        status_count = defaultdict(int)
        for app in applications:
            status_count[app.get("status", "未知")] += 1
        tracking["状态分布"] = dict(status_count)
        
        # 生成建议
        tracking["建议"] = self._generate_tracking_suggestions(tracking)
        
        return tracking
    
    def generate_email(self, template_type: str, variables: Dict) -> Dict:
        """生成邮件内容"""
        if template_type not in self.email_templates:
            return {"错误": f"不支持的邮件类型: {template_type}"}
        
        template = self.email_templates[template_type]
        
        # 检查必需变量
        missing_vars = []
        for var in template["变量"]:
            if var not in variables:
                missing_vars.append(var)
        
        if missing_vars:
            return {
                "错误": "缺少必需变量",
                "缺少变量": missing_vars,
                "所需变量": template["变量"]
            }
        
        # 生成邮件内容
        subject = template["主题"].format(**variables)
        content = template["模板"].format(**variables)
        
        return {
            "邮件类型": template_type,
            "主题": subject,
            "内容": content,
            "优化建议": self._get_email_optimization_tips(template_type)
        }
    
    def manage_interview_schedule(self, interviews: List[Dict]) -> Dict:
        """管理面试日程"""
        schedule = {
            "即将面试": [],
            "面试准备": {},
            "时间冲突": [],
            "准备建议": []
        }
        
        now = datetime.now()
        
        for interview in interviews:
            interview_time = datetime.fromisoformat(interview.get("time", now.isoformat()))
            time_diff = interview_time - now
            
            # 即将面试（7天内）
            if 0 <= time_diff.days <= 7:
                schedule["即将面试"].append({
                    "公司": interview.get("company", ""),
                    "职位": interview.get("position", ""),
                    "时间": interview.get("time", ""),
                    "类型": interview.get("type", ""),
                    "剩余天数": time_diff.days
                })
        
        # 按时间排序
        schedule["即将面试"].sort(key=lambda x: x["剩余天数"])
        
        # 面试准备建议
        for interview in schedule["即将面试"]:
            interview_type = interview["类型"]
            if interview_type in self.interview_types:
                schedule["面试准备"][interview["公司"]] = {
                    "准备要点": self.interview_types[interview_type]["准备要点"],
                    "常见问题": self.interview_types[interview_type]["常见问题"],
                    "建议时长": self.interview_types[interview_type]["时长"]
                }
        
        # 检查时间冲突
        schedule["时间冲突"] = self._check_time_conflicts(interviews)
        
        # 生成准备建议
        schedule["准备建议"] = self._generate_interview_prep_advice(schedule["即将面试"])
        
        return schedule
    
    def analyze_job_market_trends(self, job_data: List[Dict]) -> Dict:
        """分析职位市场趋势"""
        trends = {
            "热门技能": {},
            "薪资趋势": {},
            "公司类型": {},
            "地区分布": {},
            "行业分析": {},
            "技能组合": {},
            "增长趋势": {}
        }
        
        # 技能统计
        skill_count = defaultdict(int)
        salary_by_skill = defaultdict(list)
        company_types = defaultdict(int)
        locations = defaultdict(int)
        industries = defaultdict(int)
        skill_combinations = defaultdict(int)
        
        for job in job_data:
            skills = job.get("required_skills", [])
            salary = job.get("salary", 0)
            company_type = job.get("company_type", "未知")
            location = job.get("location", "未知")
            industry = job.get("industry", "未知")
            
            # 技能统计
            for skill in skills:
                skill_count[skill] += 1
                if salary > 0:
                    salary_by_skill[skill].append(salary)
            
            # 技能组合分析（2-3个技能的组合）
            if len(skills) >= 2:
                for i in range(len(skills)):
                    for j in range(i+1, len(skills)):
                        combo = f"{skills[i]}+{skills[j]}"
                        skill_combinations[combo] += 1
            
            # 其他维度统计
            company_types[company_type] += 1
            locations[location] += 1
            industries[industry] += 1
        
        # 热门技能排行
        trends["热门技能"] = dict(sorted(skill_count.items(), key=lambda x: x[1], reverse=True)[:10])
        
        # 薪资趋势
        for skill, salaries in salary_by_skill.items():
            if len(salaries) >= 2:  # 降低门槛到2个数据点
                trends["薪资趋势"][skill] = {
                    "平均薪资": round(sum(salaries) / len(salaries), 0),
                    "最高薪资": max(salaries),
                    "最低薪资": min(salaries),
                    "职位数量": len(salaries),
                    "薪资中位数": sorted(salaries)[len(salaries)//2]
                }
        
        # 公司类型分布
        trends["公司类型"] = dict(sorted(company_types.items(), key=lambda x: x[1], reverse=True)[:5])
        
        # 地区分布
        trends["地区分布"] = dict(sorted(locations.items(), key=lambda x: x[1], reverse=True)[:5])
        
        # 行业分析
        trends["行业分析"] = dict(sorted(industries.items(), key=lambda x: x[1], reverse=True)[:5])
        
        # 技能组合分析
        trends["技能组合"] = dict(sorted(skill_combinations.items(), key=lambda x: x[1], reverse=True)[:5])
        
        # 增长趋势预测（基于技能热度）
        trends["增长趋势"] = self._predict_skill_growth(skill_count)
        
        return trends
    
    def generate_resume_optimization_report(self, resume_data: Dict, target_jobs: List[Dict]) -> Dict:
        """生成简历优化报告"""
        report = {
            "匹配度分析": {},
            "技能差距": {},
            "关键词优化": {},
            "结构建议": {},
            "行动计划": {}
        }
        
        # 提取简历技能
        resume_skills = set(resume_data.get("skills", []))
        
        # 分析目标职位要求
        required_skills = set()
        preferred_skills = set()
        
        for job in target_jobs:
            required_skills.update(job.get("required_skills", []))
            preferred_skills.update(job.get("preferred_skills", []))
        
        # 匹配度分析
        matched_skills = resume_skills & required_skills
        missing_skills = required_skills - resume_skills
        extra_skills = resume_skills - required_skills
        
        report["匹配度分析"] = {
            "总体匹配度": round(len(matched_skills) / len(required_skills) * 100, 1) if required_skills else 0,
            "匹配技能": list(matched_skills),
            "缺失技能": list(missing_skills),
            "额外技能": list(extra_skills),
            "优势技能": list(resume_skills & preferred_skills)
        }
        
        # 技能差距分析
        report["技能差距"] = self._analyze_skill_gaps(missing_skills, target_jobs)
        
        # 关键词优化
        report["关键词优化"] = self._generate_keyword_suggestions(resume_data, target_jobs)
        
        # 结构建议
        report["结构建议"] = self._analyze_resume_structure(resume_data)
        
        # 行动计划
        report["行动计划"] = self._create_resume_action_plan(report)
        
        return report
    
    def analyze_platform_effectiveness(self, application_history: List[Dict]) -> Dict:
        """分析各平台求职效果"""
        effectiveness = {
            "平台排名": {},
            "最佳投递时间": {},
            "成功模式": {},
            "优化建议": {}
        }
        
        platform_stats = defaultdict(lambda: {
            "总投递": 0,
            "查看率": 0,
            "回复率": 0,
            "面试率": 0,
            "成功率": 0,
            "平均响应时间": []
        })
        
        for app in application_history:
            platform = app.get("platform", "未知")
            status = app.get("status", "已投递")
            response_time = app.get("response_time_hours", 0)
            
            stats = platform_stats[platform]
            stats["总投递"] += 1
            
            if status != "已投递":
                stats["查看率"] += 1
                if response_time > 0:
                    stats["平均响应时间"].append(response_time)
            
            if status in ["已回复", "面试邀请", "技术面试", "HR面试", "终面"]:
                stats["回复率"] += 1
            
            if "面试" in status:
                stats["面试率"] += 1
            
            if status in ["已录用", "待入职"]:
                stats["成功率"] += 1
        
        # 计算各平台效果评分
        for platform, stats in platform_stats.items():
            if stats["总投递"] > 0:
                查看率 = stats["查看率"] / stats["总投递"]
                回复率 = stats["回复率"] / stats["总投递"]
                面试率 = stats["面试率"] / stats["总投递"]
                成功率 = stats["成功率"] / stats["总投递"]
                
                # 综合评分（权重：成功率40%，面试率30%，回复率20%，查看率10%）
                综合评分 = (成功率 * 0.4 + 面试率 * 0.3 + 回复率 * 0.2 + 查看率 * 0.1) * 100
                
                effectiveness["平台排名"][platform] = {
                    "综合评分": round(综合评分, 1),
                    "查看率": round(查看率 * 100, 1),
                    "回复率": round(回复率 * 100, 1),
                    "面试率": round(面试率 * 100, 1),
                    "成功率": round(成功率 * 100, 1),
                    "平均响应时间": round(sum(stats["平均响应时间"]) / len(stats["平均响应时间"]), 1) if stats["平均响应时间"] else 0
                }
        
        # 分析最佳投递时间
        effectiveness["最佳投递时间"] = self._analyze_best_application_time(application_history)
        
        # 识别成功模式
        effectiveness["成功模式"] = self._identify_success_patterns(application_history)
        
        # 生成优化建议
        effectiveness["优化建议"] = self._generate_platform_optimization_advice(effectiveness)
        
        return effectiveness
    
    def _analyze_headline(self, headline: str) -> Dict:
        """分析LinkedIn标题"""
        rules = self.linkedin_rules["标题优化"]
        score = 0
        feedback = []
        
        # 长度检查
        if rules["长度"][0] <= len(headline) <= rules["长度"][1]:
            score += 25
        else:
            feedback.append(f"标题长度建议在{rules['长度'][0]}-{rules['长度'][1]}字符之间")
        
        # 关键词检查
        keyword_count = sum(1 for keyword in rules["关键词"] if keyword.lower() in headline.lower())
        if keyword_count > 0:
            score += min(keyword_count * 15, 50)
        else:
            feedback.append("建议包含相关技术关键词")
        
        # 格式检查
        if "|" in headline or "·" in headline:
            score += 25
        else:
            feedback.append("建议使用分隔符组织内容结构")
        
        return {"评分": score, "反馈": feedback}
    
    def _analyze_summary(self, summary: str) -> Dict:
        """分析LinkedIn摘要"""
        rules = self.linkedin_rules["摘要优化"]
        score = 0
        feedback = []
        
        # 长度检查
        if rules["长度"][0] <= len(summary) <= rules["长度"][1]:
            score += 30
        else:
            feedback.append(f"摘要长度建议在{rules['长度'][0]}-{rules['长度'][1]}字符之间")
        
        # 关键元素检查
        elements_found = 0
        for element in rules["关键元素"]:
            if any(keyword in summary for keyword in [element, element.lower()]):
                elements_found += 1
        
        score += min(elements_found * 17, 70)
        
        if elements_found < len(rules["关键元素"]):
            feedback.append("建议包含更多关键元素：量化成果、技术栈、行业经验等")
        
        return {"评分": score, "反馈": feedback}
    
    def _analyze_skills(self, skills: List[str]) -> Dict:
        """分析技能标签"""
        rules = self.linkedin_rules["技能标签"]
        
        hot_skills = [s for s in skills if s in rules["热门技能"]]
        emerging_skills = [s for s in skills if s in rules["新兴技能"]]
        
        return {
            "总技能数": len(skills),
            "热门技能": hot_skills,
            "新兴技能": emerging_skills,
            "热门技能占比": len(hot_skills) / len(skills) if skills else 0,
            "建议添加": [s for s in rules["热门技能"] if s not in skills][:5]
        }
    
    def _generate_linkedin_suggestions(self, headline_score: Dict, summary_score: Dict, skills_analysis: Dict) -> List[str]:
        """生成LinkedIn优化建议"""
        suggestions = []
        
        if headline_score["评分"] < 70:
            suggestions.append("优化个人标题，增加关键词和专业描述")
        
        if summary_score["评分"] < 70:
            suggestions.append("完善个人摘要，突出核心技能和成就")
        
        if skills_analysis["热门技能占比"] < 0.3:
            suggestions.append("增加更多热门技能标签")
        
        if len(skills_analysis["新兴技能"]) == 0:
            suggestions.append("关注新兴技术，添加前沿技能")
        
        return suggestions
    
    def _create_improvement_plan(self, profile_data: Dict) -> Dict:
        """创建改进计划"""
        plan = {
            "短期目标（1周内）": [
                "优化个人标题",
                "更新技能标签",
                "完善联系信息"
            ],
            "中期目标（1个月内）": [
                "重写个人摘要",
                "添加项目经历",
                "发布专业内容"
            ],
            "长期目标（3个月内）": [
                "建立行业连接",
                "参与专业讨论",
                "获得技能认证"
            ]
        }
        
        return plan
    
    def _calculate_response_rate(self, applications: List[Dict]) -> float:
        """计算响应率"""
        total = len(applications)
        if total == 0:
            return 0.0
        
        responded = len([app for app in applications if app.get("status") != "已投递"])
        return round(responded / total * 100, 1)
    
    def _calculate_interview_rate(self, applications: List[Dict]) -> float:
        """计算面试转化率"""
        total = len(applications)
        if total == 0:
            return 0.0
        
        interviews = len([app for app in applications if "面试" in app.get("status", "")])
        return round(interviews / total * 100, 1)
    
    def _calculate_platform_success_rate(self, apps: List[Dict]) -> float:
        """计算平台成功率"""
        if not apps:
            return 0.0
        
        success = len([app for app in apps if app.get("status") in ["已录用", "待入职"]])
        return round(success / len(apps) * 100, 1)
    
    def _generate_tracking_suggestions(self, tracking: Dict) -> List[str]:
        """生成追踪建议"""
        suggestions = []
        
        response_rate = tracking["总体统计"]["平均响应率"]
        if response_rate < 20:
            suggestions.append("响应率较低，建议优化简历和求职信")
        
        interview_rate = tracking["总体统计"]["面试转化率"]
        if interview_rate < 10:
            suggestions.append("面试转化率偏低，建议提升个人技能展示")
        
        platforms_count = len(tracking["总体统计"]["使用平台"])
        if platforms_count < 3:
            suggestions.append("建议使用更多求职平台，增加机会")
        
        return suggestions
    
    def _get_email_optimization_tips(self, template_type: str) -> List[str]:
        """获取邮件优化建议"""
        tips = {
            "求职申请": [
                "主题行要简洁明了",
                "突出与职位的匹配度",
                "量化个人成就",
                "保持专业语调"
            ],
            "面试感谢": [
                "24小时内发送",
                "提及具体面试内容",
                "补充遗漏信息",
                "再次表达兴趣"
            ],
            "薪资谈判": [
                "基于市场数据",
                "强调个人价值",
                "保持灵活性",
                "专业礼貌"
            ]
        }
        
        return tips.get(template_type, ["保持专业", "内容简洁", "逻辑清晰"])
    
    def _check_time_conflicts(self, interviews: List[Dict]) -> List[Dict]:
        """检查时间冲突"""
        conflicts = []
        
        for i, interview1 in enumerate(interviews):
            for j, interview2 in enumerate(interviews[i+1:], i+1):
                time1 = datetime.fromisoformat(interview1.get("time", ""))
                time2 = datetime.fromisoformat(interview2.get("time", ""))
                
                # 检查是否在同一天的2小时内
                if abs((time1 - time2).total_seconds()) < 7200:  # 2小时
                    conflicts.append({
                        "冲突面试": [
                            f"{interview1.get('company')} - {interview1.get('time')}",
                            f"{interview2.get('company')} - {interview2.get('time')}"
                        ]
                    })
        
        return conflicts
    
    def _generate_interview_prep_advice(self, upcoming_interviews: List[Dict]) -> List[str]:
        """生成面试准备建议"""
        advice = []
        
        if not upcoming_interviews:
            return ["暂无即将到来的面试"]
        
        # 按剩余天数给建议
        for interview in upcoming_interviews[:3]:  # 只看最近3个
            days_left = interview["剩余天数"]
            company = interview["公司"]
            
            if days_left == 0:
                advice.append(f"今天面试{company}，确认时间地点，准备相关材料")
            elif days_left == 1:
                advice.append(f"明天面试{company}，最后检查简历，准备常见问题")
            elif days_left <= 3:
                advice.append(f"{days_left}天后面试{company}，深入了解公司和职位")
            else:
                advice.append(f"{days_left}天后面试{company}，开始准备技术复习")
        
        return advice
    
    def _predict_skill_growth(self, skill_count: Dict) -> Dict:
        """预测技能增长趋势"""
        # 基于当前热度和技术发展趋势预测
        growth_predictions = {}
        
        # 定义技术发展趋势权重
        tech_trends = {
            "AI": 1.5, "机器学习": 1.4, "深度学习": 1.3,
            "云计算": 1.3, "Docker": 1.2, "Kubernetes": 1.2,
            "React": 1.1, "Vue": 1.1, "TypeScript": 1.2,
            "Python": 1.1, "Go": 1.3, "Rust": 1.4,
            "区块链": 1.2, "Web3": 1.3
        }
        
        for skill, count in skill_count.items():
            trend_weight = tech_trends.get(skill, 1.0)
            predicted_growth = round((count * trend_weight - count) / count * 100, 1) if count > 0 else 0
            
            growth_predictions[skill] = {
                "当前热度": count,
                "预测增长率": f"{predicted_growth}%",
                "趋势": "上升" if predicted_growth > 10 else "稳定" if predicted_growth > -5 else "下降"
            }
        
        # 只返回有增长潜力的技能
        return {k: v for k, v in growth_predictions.items() if v["预测增长率"] != "0.0%"}
    
    def _analyze_skill_gaps(self, missing_skills: set, target_jobs: List[Dict]) -> Dict:
        """分析技能差距"""
        gap_analysis = {
            "关键技能": [],
            "可选技能": [],
            "学习优先级": {},
            "学习建议": {}
        }
        
        # 统计技能在目标职位中的出现频率
        skill_frequency = defaultdict(int)
        for job in target_jobs:
            for skill in job.get("required_skills", []):
                if skill in missing_skills:
                    skill_frequency[skill] += 1
        
        total_jobs = len(target_jobs)
        
        for skill, freq in skill_frequency.items():
            frequency_rate = freq / total_jobs
            
            if frequency_rate >= 0.7:  # 70%以上职位要求
                gap_analysis["关键技能"].append(skill)
                gap_analysis["学习优先级"][skill] = "高"
            elif frequency_rate >= 0.3:  # 30-70%职位要求
                gap_analysis["可选技能"].append(skill)
                gap_analysis["学习优先级"][skill] = "中"
            else:
                gap_analysis["学习优先级"][skill] = "低"
        
        # 生成学习建议
        for skill in gap_analysis["关键技能"]:
            gap_analysis["学习建议"][skill] = self._get_learning_suggestion(skill)
        
        return gap_analysis
    
    def _generate_keyword_suggestions(self, resume_data: Dict, target_jobs: List[Dict]) -> Dict:
        """生成关键词优化建议"""
        suggestions = {
            "缺失关键词": [],
            "优化建议": [],
            "行业术语": [],
            "技能关键词": []
        }
        
        # 收集目标职位的关键词
        job_keywords = set()
        for job in target_jobs:
            # 从职位描述中提取关键词
            description = job.get("description", "")
            requirements = job.get("requirements", [])
            
            # 简单的关键词提取（实际应用中可以使用更复杂的NLP）
            for req in requirements:
                job_keywords.update(req.split())
        
        # 分析简历中缺失的关键词
        resume_text = str(resume_data.get("summary", "")) + " " + " ".join(resume_data.get("skills", []))
        
        missing_keywords = []
        for keyword in job_keywords:
            if len(keyword) > 2 and keyword.lower() not in resume_text.lower():
                missing_keywords.append(keyword)
        
        suggestions["缺失关键词"] = missing_keywords[:10]  # 只显示前10个
        
        # 生成优化建议
        if missing_keywords:
            suggestions["优化建议"] = [
                "在技能部分添加相关技术关键词",
                "在工作经历中使用行业术语",
                "在项目描述中突出核心技能",
                "保持关键词密度适中，避免堆砌"
            ]
        
        return suggestions
    
    def _analyze_resume_structure(self, resume_data: Dict) -> Dict:
        """分析简历结构"""
        structure_analysis = {
            "完整性评分": 0,
            "缺失部分": [],
            "优化建议": [],
            "结构评估": {}
        }
        
        # 检查必要部分
        required_sections = {
            "个人信息": ["name", "contact"],
            "工作经历": ["experience"],
            "教育背景": ["education"],
            "技能": ["skills"],
            "项目经历": ["projects"]
        }
        
        score = 0
        for section, fields in required_sections.items():
            if any(field in resume_data for field in fields):
                score += 20
                structure_analysis["结构评估"][section] = "✅ 已包含"
            else:
                structure_analysis["缺失部分"].append(section)
                structure_analysis["结构评估"][section] = "❌ 缺失"
        
        structure_analysis["完整性评分"] = score
        
        # 生成优化建议
        if score < 100:
            structure_analysis["优化建议"] = [
                f"补充{section}部分" for section in structure_analysis["缺失部分"]
            ]
        else:
            structure_analysis["优化建议"] = [
                "简历结构完整，建议优化内容质量",
                "确保各部分内容详实且相关",
                "保持格式统一和排版美观"
            ]
        
        return structure_analysis
    
    def _create_resume_action_plan(self, report: Dict) -> Dict:
        """创建简历优化行动计划"""
        action_plan = {
            "立即行动（今天）": [],
            "短期目标（1周内）": [],
            "中期目标（1个月内）": [],
            "长期目标（3个月内）": []
        }
        
        # 基于分析结果生成行动计划
        match_rate = report["匹配度分析"]["总体匹配度"]
        
        if match_rate < 50:
            action_plan["立即行动（今天）"] = [
                "重新审视目标职位要求",
                "更新技能列表",
                "优化个人摘要"
            ]
        
        missing_skills = report["匹配度分析"]["缺失技能"]
        if missing_skills:
            action_plan["短期目标（1周内）"] = [
                f"学习关键技能：{', '.join(missing_skills[:3])}",
                "更新LinkedIn资料",
                "准备技能证明材料"
            ]
        
        return action_plan
    
    def _analyze_best_application_time(self, application_history: List[Dict]) -> Dict:
        """分析最佳投递时间"""
        time_analysis = {
            "最佳投递日": {},
            "最佳投递时间": {},
            "响应率统计": {}
        }
        
        # 这里可以基于历史数据分析，现在提供一般性建议
        time_analysis["最佳投递日"] = {
            "周二": "响应率最高",
            "周三": "HR查看率高", 
            "周四": "面试安排活跃"
        }
        
        time_analysis["最佳投递时间"] = {
            "上午9-11点": "HR刚上班，注意力集中",
            "下午2-4点": "午休后，精力充沛",
            "避免时间": "周一早上、周五下午"
        }
        
        return time_analysis
    
    def _identify_success_patterns(self, application_history: List[Dict]) -> Dict:
        """识别成功模式"""
        patterns = {
            "成功因素": [],
            "失败原因": [],
            "最佳实践": []
        }
        
        # 分析成功的申请
        successful_apps = [app for app in application_history if app.get("status") in ["已录用", "待入职"]]
        
        if successful_apps:
            patterns["成功因素"] = [
                "简历关键词匹配度高",
                "申请时间选择合适",
                "个人资料完整专业",
                "及时跟进和回复"
            ]
        
        patterns["最佳实践"] = [
            "投递前仔细研究公司和职位",
            "定制化简历和求职信",
            "保持专业的沟通态度",
            "及时更新求职状态"
        ]
        
        return patterns
    
    def _generate_platform_optimization_advice(self, effectiveness: Dict) -> List[str]:
        """生成平台优化建议"""
        advice = []
        
        # 基于平台排名给建议
        platform_ranking = effectiveness.get("平台排名", {})
        
        if platform_ranking:
            best_platform = max(platform_ranking.items(), key=lambda x: x[1]["综合评分"])
            advice.append(f"重点使用{best_platform[0]}平台，综合效果最佳")
            
            worst_platforms = [p for p, stats in platform_ranking.items() if stats["综合评分"] < 20]
            if worst_platforms:
                advice.append(f"考虑减少在{', '.join(worst_platforms)}的投入")
        
        advice.extend([
            "定期分析和调整平台策略",
            "关注平台特色功能和最新变化",
            "保持多平台并行，分散风险"
        ])
        
        return advice
    
    def _get_learning_suggestion(self, skill: str) -> str:
        """获取技能学习建议"""
        learning_suggestions = {
            "Python": "推荐通过实际项目学习，关注数据分析和Web开发方向",
            "JavaScript": "从基础语法开始，逐步学习ES6+和前端框架",
            "React": "先掌握JavaScript基础，然后学习组件化开发思想",
            "机器学习": "建议先学习Python和数学基础，再学习算法理论",
            "Docker": "从容器概念开始，通过实际部署项目来学习",
            "AWS": "考虑考取AWS认证，通过官方培训材料学习"
        }
        
        return learning_suggestions.get(skill, f"建议通过在线课程和实际项目来学习{skill}")

# ================================
# 🔧 工具函数
# ================================

def create_platform_integrator() -> PlatformIntegrator:
    """创建平台集成器"""
    return PlatformIntegrator()

if __name__ == "__main__":
    # 测试代码
    integrator = create_platform_integrator()
    
    print("🔗 平台集成测试")
    
    # 测试LinkedIn分析
    test_profile = {
        "headline": "Python开发工程师 | AI/机器学习 | 5年经验",
        "summary": "专注于AI和机器学习的Python开发工程师，有5年项目经验...",
        "skills": ["Python", "机器学习", "TensorFlow"]
    }
    print("LinkedIn分析:", integrator.analyze_linkedin_profile(test_profile))