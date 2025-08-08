# -*- coding: utf-8 -*-
"""
📊 综合分析报告系统
Comprehensive Analysis Report System

整合所有模块的分析结果，生成多维度综合报告和决策建议矩阵

功能：
🔄 跨模块数据整合
📈 多维度综合分析
🎯 决策建议矩阵
📊 可视化报告生成
🧠 智能洞察提取
💡 个性化建议生成

作者: AI Assistant
版本: 1.0
"""

import json
import uuid
from typing import Dict, List, Optional, Any, Union, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum

# 导入数据接口和流管理器
try:
    from .data_interface import (
        DataInterfaceManager, UserProfile, JobData, AnalysisResult,
        PersonalityType, RiskLevel, JobStatus, AnalysisType
    )
    from .data_flow_manager import DataFlowManager, ModuleCallProxy
except ImportError:
    import sys
    import os
    sys.path.append(os.path.dirname(__file__))
    from data_interface import (
        DataInterfaceManager, UserProfile, JobData, AnalysisResult,
        PersonalityType, RiskLevel, JobStatus, AnalysisType
    )
    from data_flow_manager import DataFlowManager, ModuleCallProxy


# ================================
# 🎯 报告类型枚举
# ================================

class ReportType(Enum):
    """报告类型枚举"""
    COMPREHENSIVE_ANALYSIS = "综合分析报告"
    JOB_COMPARISON = "工作对比报告"
    CAREER_PLANNING = "职业规划报告"
    SKILL_ASSESSMENT = "技能评估报告"
    MARKET_INSIGHT = "市场洞察报告"
    DECISION_MATRIX = "决策矩阵报告"


class InsightLevel(Enum):
    """洞察级别枚举"""
    CRITICAL = "关键洞察"
    IMPORTANT = "重要发现"
    NOTABLE = "值得注意"
    INFORMATIONAL = "信息性"


# ================================
# 📊 综合分析数据结构
# ================================

@dataclass
class ComprehensiveInsight:
    """综合洞察数据结构"""
    insight_id: str
    level: InsightLevel
    category: str
    title: str
    description: str
    evidence: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    confidence: float = 0.0
    impact_score: float = 0.0
    source_modules: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            "insight_id": self.insight_id,
            "level": self.level.value,
            "category": self.category,
            "title": self.title,
            "description": self.description,
            "evidence": self.evidence,
            "recommendations": self.recommendations,
            "confidence": self.confidence,
            "impact_score": self.impact_score,
            "source_modules": self.source_modules
        }


@dataclass
class DecisionMatrix:
    """决策矩阵数据结构"""
    matrix_id: str
    options: List[str]
    criteria: List[str]
    scores: Dict[str, Dict[str, float]]  # {option: {criterion: score}}
    weights: Dict[str, float]  # {criterion: weight}
    final_scores: Dict[str, float]  # {option: weighted_score}
    recommendation: str
    confidence: float
    
    def to_dict(self) -> Dict:
        return {
            "matrix_id": self.matrix_id,
            "options": self.options,
            "criteria": self.criteria,
            "scores": self.scores,
            "weights": self.weights,
            "final_scores": self.final_scores,
            "recommendation": self.recommendation,
            "confidence": self.confidence
        }


@dataclass
class ComprehensiveReport:
    """综合报告数据结构"""
    report_id: str
    report_type: ReportType
    user_profile: UserProfile
    analysis_results: List[AnalysisResult]
    insights: List[ComprehensiveInsight]
    decision_matrix: Optional[DecisionMatrix]
    summary: Dict[str, Any]
    recommendations: List[str]
    next_steps: List[str]
    confidence_score: float
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict:
        return {
            "report_id": self.report_id,
            "report_type": self.report_type.value,
            "user_profile": self.user_profile.to_dict(),
            "analysis_results": [result.to_dict() for result in self.analysis_results],
            "insights": [insight.to_dict() for insight in self.insights],
            "decision_matrix": self.decision_matrix.to_dict() if self.decision_matrix else None,
            "summary": self.summary,
            "recommendations": self.recommendations,
            "next_steps": self.next_steps,
            "confidence_score": self.confidence_score,
            "created_at": self.created_at.isoformat()
        }


# ================================
# 🧠 综合分析引擎
# ================================

class ComprehensiveAnalyzer:
    """综合分析引擎 - 整合所有模块分析结果"""
    
    def __init__(self):
        """初始化综合分析引擎"""
        print("🧠 初始化综合分析引擎...")
        
        self.data_interface = DataInterfaceManager()
        self.data_flow_manager = DataFlowManager()
        self.module_proxy = ModuleCallProxy(self.data_flow_manager)
        
        # 分析权重配置
        self.analysis_weights = {
            "ai_analysis": 0.3,
            "big_data": 0.25,
            "smart_decision": 0.25,
            "platform_integration": 0.2
        }
        
        print("✅ 综合分析引擎初始化完成！")
    
    def generate_comprehensive_report(
        self, 
        user_profile: UserProfile, 
        job_data_list: List[JobData],
        analysis_context: Dict[str, Any] = None
    ) -> ComprehensiveReport:
        """生成综合分析报告"""
        print(f"📊 开始生成综合分析报告 - 用户: {user_profile.name}")
        
        analysis_context = analysis_context or {}
        report_id = str(uuid.uuid4())
        
        # 1. 收集所有模块的分析结果
        analysis_results = self._collect_all_analysis_results(user_profile, job_data_list, analysis_context)
        
        # 2. 提取综合洞察
        insights = self._extract_comprehensive_insights(analysis_results, user_profile)
        
        # 3. 生成决策矩阵
        decision_matrix = self._generate_decision_matrix(job_data_list, analysis_results, user_profile)
        
        # 4. 生成摘要和建议
        summary = self._generate_comprehensive_summary(analysis_results, insights, decision_matrix)
        recommendations = self._generate_comprehensive_recommendations(insights, decision_matrix, user_profile)
        next_steps = self._generate_next_steps(recommendations, user_profile)
        
        # 5. 计算整体信心分数
        confidence_score = self._calculate_overall_confidence(analysis_results, insights)
        
        # 创建综合报告
        report = ComprehensiveReport(
            report_id=report_id,
            report_type=ReportType.COMPREHENSIVE_ANALYSIS,
            user_profile=user_profile,
            analysis_results=analysis_results,
            insights=insights,
            decision_matrix=decision_matrix,
            summary=summary,
            recommendations=recommendations,
            next_steps=next_steps,
            confidence_score=confidence_score
        )
        
        print(f"✅ 综合分析报告生成完成 - 报告ID: {report_id}")
        return report
    
    def _collect_all_analysis_results(
        self, 
        user_profile: UserProfile, 
        job_data_list: List[JobData],
        context: Dict[str, Any]
    ) -> List[AnalysisResult]:
        """收集所有模块的分析结果"""
        print("🔄 收集各模块分析结果...")
        
        results = []
        
        try:
            # AI分析模块结果
            ai_results = self._get_ai_analysis_results(user_profile, job_data_list, context)
            results.extend(ai_results)
            
            # 大数据分析结果
            big_data_results = self._get_big_data_analysis_results(user_profile, job_data_list, context)
            results.extend(big_data_results)
            
            # 智能决策结果
            smart_decision_results = self._get_smart_decision_results(user_profile, job_data_list, context)
            results.extend(smart_decision_results)
            
            # 平台集成结果
            platform_results = self._get_platform_integration_results(user_profile, job_data_list, context)
            results.extend(platform_results)
            
        except Exception as e:
            print(f"⚠️ 收集分析结果时出现错误: {e}")
        
        print(f"✅ 收集到 {len(results)} 个分析结果")
        return results
    
    def _get_ai_analysis_results(self, user_profile: UserProfile, job_data_list: List[JobData], context: Dict) -> List[AnalysisResult]:
        """获取AI分析结果"""
        results = []
        
        # 模拟AI分析结果（实际应该调用真实的AI模块）
        for i, job_data in enumerate(job_data_list):
            result = AnalysisResult(
                analysis_id=f"ai_analysis_{i}",
                analysis_type=AnalysisType.JOB_DECISION,
                user_id=user_profile.user_id,
                score=85.0 + i * 2,
                confidence=0.9,
                recommendations=[
                    f"基于AI分析，{job_data.title}职位匹配度较高",
                    f"建议重点关注{job_data.company}的技术栈要求"
                ],
                insights={
                    "技能匹配度": 88.0,
                    "薪资合理性": 92.0,
                    "发展前景": 85.0
                },
                module_source="ai_analyzer"
            )
            results.append(result)
        
        return results
    
    def _get_big_data_analysis_results(self, user_profile: UserProfile, job_data_list: List[JobData], context: Dict) -> List[AnalysisResult]:
        """获取大数据分析结果"""
        results = []
        
        # 模拟大数据分析结果
        market_analysis = AnalysisResult(
            analysis_id="big_data_market",
            analysis_type=AnalysisType.MARKET_ANALYSIS,
            user_id=user_profile.user_id,
            score=78.0,
            confidence=0.85,
            recommendations=[
                "当前市场对Python开发者需求旺盛",
                "建议关注AI/机器学习相关技能提升"
            ],
            insights={
                "市场热度": 82.0,
                "薪资趋势": 75.0,
                "竞争激烈度": 70.0
            },
            module_source="big_data"
        )
        results.append(market_analysis)
        
        return results
    
    def _get_smart_decision_results(self, user_profile: UserProfile, job_data_list: List[JobData], context: Dict) -> List[AnalysisResult]:
        """获取智能决策结果"""
        results = []
        
        # 模拟智能决策结果
        decision_analysis = AnalysisResult(
            analysis_id="smart_decision_main",
            analysis_type=AnalysisType.JOB_DECISION,
            user_id=user_profile.user_id,
            score=91.0,
            confidence=0.95,
            recommendations=[
                "基于您的风险偏好，推荐选择稳定性较高的大公司",
                "建议优先考虑有明确晋升路径的职位"
            ],
            insights={
                "决策信心": 91.0,
                "风险评估": 25.0,
                "ROI预期": 88.0
            },
            module_source="smart_decision"
        )
        results.append(decision_analysis)
        
        return results
    
    def _get_platform_integration_results(self, user_profile: UserProfile, job_data_list: List[JobData], context: Dict) -> List[AnalysisResult]:
        """获取平台集成结果"""
        results = []
        
        # 模拟平台集成结果
        platform_analysis = AnalysisResult(
            analysis_id="platform_integration",
            analysis_type=AnalysisType.RESUME_ANALYSIS,
            user_id=user_profile.user_id,
            score=83.0,
            confidence=0.8,
            recommendations=[
                "LinkedIn档案完整度良好，建议增加项目展示",
                "简历关键词优化可提升匹配度"
            ],
            insights={
                "档案完整度": 85.0,
                "社交影响力": 78.0,
                "平台活跃度": 82.0
            },
            module_source="platform_integration"
        )
        results.append(platform_analysis)
        
        return results
    
    def _extract_comprehensive_insights(self, analysis_results: List[AnalysisResult], user_profile: UserProfile) -> List[ComprehensiveInsight]:
        """提取综合洞察"""
        print("🔍 提取综合洞察...")
        
        insights = []
        
        # 1. 技能匹配洞察
        skill_insight = self._analyze_skill_matching(analysis_results, user_profile)
        if skill_insight:
            insights.append(skill_insight)
        
        # 2. 市场趋势洞察
        market_insight = self._analyze_market_trends(analysis_results)
        if market_insight:
            insights.append(market_insight)
        
        # 3. 风险评估洞察
        risk_insight = self._analyze_risk_factors(analysis_results, user_profile)
        if risk_insight:
            insights.append(risk_insight)
        
        # 4. 职业发展洞察
        career_insight = self._analyze_career_development(analysis_results, user_profile)
        if career_insight:
            insights.append(career_insight)
        
        print(f"✅ 提取到 {len(insights)} 个综合洞察")
        return insights
    
    def _analyze_skill_matching(self, analysis_results: List[AnalysisResult], user_profile: UserProfile) -> Optional[ComprehensiveInsight]:
        """分析技能匹配情况"""
        skill_scores = []
        for result in analysis_results:
            if "技能匹配度" in result.insights:
                skill_scores.append(result.insights["技能匹配度"])
        
        if not skill_scores:
            return None
        
        avg_skill_score = sum(skill_scores) / len(skill_scores)
        
        if avg_skill_score >= 85:
            level = InsightLevel.IMPORTANT
            title = "技能匹配度优秀"
            description = f"您的技能与目标职位匹配度达到{avg_skill_score:.1f}%，处于优秀水平"
        elif avg_skill_score >= 70:
            level = InsightLevel.NOTABLE
            title = "技能匹配度良好"
            description = f"您的技能与目标职位匹配度为{avg_skill_score:.1f}%，有提升空间"
        else:
            level = InsightLevel.CRITICAL
            title = "技能匹配度需要提升"
            description = f"您的技能与目标职位匹配度仅为{avg_skill_score:.1f}%，建议重点提升"
        
        return ComprehensiveInsight(
            insight_id=str(uuid.uuid4()),
            level=level,
            category="技能分析",
            title=title,
            description=description,
            evidence=[f"平均技能匹配度: {avg_skill_score:.1f}%"],
            recommendations=["针对性学习缺失技能", "参与相关项目实践"],
            confidence=0.9,
            impact_score=avg_skill_score,
            source_modules=["ai_analyzer", "big_data"]
        )
    
    def _analyze_market_trends(self, analysis_results: List[AnalysisResult]) -> Optional[ComprehensiveInsight]:
        """分析市场趋势"""
        market_scores = []
        for result in analysis_results:
            if result.analysis_type == AnalysisType.MARKET_ANALYSIS:
                if "市场热度" in result.insights:
                    market_scores.append(result.insights["市场热度"])
        
        if not market_scores:
            return None
        
        avg_market_score = sum(market_scores) / len(market_scores)
        
        return ComprehensiveInsight(
            insight_id=str(uuid.uuid4()),
            level=InsightLevel.IMPORTANT,
            category="市场分析",
            title="市场需求分析",
            description=f"目标职位市场热度为{avg_market_score:.1f}%，市场需求{'旺盛' if avg_market_score >= 80 else '一般' if avg_market_score >= 60 else '较低'}",
            evidence=[f"市场热度评分: {avg_market_score:.1f}%"],
            recommendations=["关注市场动态", "提升核心竞争力"],
            confidence=0.85,
            impact_score=avg_market_score,
            source_modules=["big_data"]
        )
    
    def _analyze_risk_factors(self, analysis_results: List[AnalysisResult], user_profile: UserProfile) -> Optional[ComprehensiveInsight]:
        """分析风险因素"""
        risk_scores = []
        for result in analysis_results:
            if "风险评估" in result.insights:
                risk_scores.append(result.insights["风险评估"])
        
        if not risk_scores:
            return None
        
        avg_risk_score = sum(risk_scores) / len(risk_scores)
        
        if avg_risk_score <= 30:
            level = InsightLevel.INFORMATIONAL
            title = "风险水平较低"
        elif avg_risk_score <= 60:
            level = InsightLevel.NOTABLE
            title = "风险水平中等"
        else:
            level = InsightLevel.CRITICAL
            title = "风险水平较高"
        
        return ComprehensiveInsight(
            insight_id=str(uuid.uuid4()),
            level=level,
            category="风险评估",
            title=title,
            description=f"综合风险评估分数为{avg_risk_score:.1f}%，建议{'保持现状' if avg_risk_score <= 30 else '适度关注' if avg_risk_score <= 60 else '重点关注'}",
            evidence=[f"综合风险评分: {avg_risk_score:.1f}%"],
            recommendations=["制定风险缓解策略", "建立应急预案"],
            confidence=0.8,
            impact_score=100 - avg_risk_score,
            source_modules=["smart_decision"]
        )
    
    def _analyze_career_development(self, analysis_results: List[AnalysisResult], user_profile: UserProfile) -> Optional[ComprehensiveInsight]:
        """分析职业发展"""
        development_scores = []
        for result in analysis_results:
            if "发展前景" in result.insights:
                development_scores.append(result.insights["发展前景"])
        
        if not development_scores:
            return None
        
        avg_development_score = sum(development_scores) / len(development_scores)
        
        return ComprehensiveInsight(
            insight_id=str(uuid.uuid4()),
            level=InsightLevel.IMPORTANT,
            category="职业发展",
            title="职业发展前景分析",
            description=f"职业发展前景评分{avg_development_score:.1f}%，发展潜力{'优秀' if avg_development_score >= 85 else '良好' if avg_development_score >= 70 else '一般'}",
            evidence=[f"发展前景评分: {avg_development_score:.1f}%"],
            recommendations=["制定长期职业规划", "持续技能提升"],
            confidence=0.85,
            impact_score=avg_development_score,
            source_modules=["ai_analyzer", "smart_decision"]
        )
    
    def _generate_decision_matrix(self, job_data_list: List[JobData], analysis_results: List[AnalysisResult], user_profile: UserProfile) -> Optional[DecisionMatrix]:
        """生成决策矩阵"""
        if len(job_data_list) < 2:
            return None
        
        print("📊 生成决策矩阵...")
        
        # 决策标准
        criteria = ["薪资水平", "技能匹配", "发展前景", "工作环境", "风险评估"]
        
        # 根据用户性格调整权重
        if user_profile.personality_type == PersonalityType.CONSERVATIVE:
            weights = {"薪资水平": 0.25, "技能匹配": 0.25, "发展前景": 0.2, "工作环境": 0.2, "风险评估": 0.1}
        elif user_profile.personality_type == PersonalityType.AGGRESSIVE:
            weights = {"薪资水平": 0.3, "技能匹配": 0.2, "发展前景": 0.3, "工作环境": 0.1, "风险评估": 0.1}
        else:
            weights = {"薪资水平": 0.25, "技能匹配": 0.25, "发展前景": 0.25, "工作环境": 0.15, "风险评估": 0.1}
        
        # 计算各选项得分
        options = [f"{job.company} - {job.title}" for job in job_data_list]
        scores = {}
        
        for i, job in enumerate(job_data_list):
            option_name = options[i]
            scores[option_name] = {
                "薪资水平": min(90, (job.salary_max or 0) / 1000),  # 简化计算
                "技能匹配": 85 + i * 3,  # 模拟数据
                "发展前景": 80 + i * 2,
                "工作环境": 75 + i * 4,
                "风险评估": 70 + i * 5
            }
        
        # 计算加权总分
        final_scores = {}
        for option in options:
            final_scores[option] = sum(scores[option][criterion] * weights[criterion] for criterion in criteria)
        
        # 推荐最高分选项
        best_option = max(final_scores.keys(), key=lambda x: final_scores[x])
        confidence = final_scores[best_option] / 100.0
        
        return DecisionMatrix(
            matrix_id=str(uuid.uuid4()),
            options=options,
            criteria=criteria,
            scores=scores,
            weights=weights,
            final_scores=final_scores,
            recommendation=best_option,
            confidence=confidence
        )
    
    def _generate_comprehensive_summary(self, analysis_results: List[AnalysisResult], insights: List[ComprehensiveInsight], decision_matrix: Optional[DecisionMatrix]) -> Dict[str, Any]:
        """生成综合摘要"""
        summary = {
            "分析模块数": len(set(result.module_source for result in analysis_results)),
            "分析结果数": len(analysis_results),
            "洞察数量": len(insights),
            "平均信心度": sum(result.confidence for result in analysis_results) / len(analysis_results) if analysis_results else 0,
            "关键洞察": len([insight for insight in insights if insight.level == InsightLevel.CRITICAL]),
            "重要发现": len([insight for insight in insights if insight.level == InsightLevel.IMPORTANT]),
            "决策矩阵": decision_matrix is not None,
            "推荐选项": decision_matrix.recommendation if decision_matrix else None
        }
        
        return summary
    
    def _generate_comprehensive_recommendations(self, insights: List[ComprehensiveInsight], decision_matrix: Optional[DecisionMatrix], user_profile: UserProfile) -> List[str]:
        """生成综合建议"""
        recommendations = []
        
        # 基于洞察的建议
        for insight in insights:
            if insight.level in [InsightLevel.CRITICAL, InsightLevel.IMPORTANT]:
                recommendations.extend(insight.recommendations)
        
        # 基于决策矩阵的建议
        if decision_matrix:
            recommendations.append(f"基于综合评估，推荐选择: {decision_matrix.recommendation}")
        
        # 基于用户性格的建议
        if user_profile.personality_type == PersonalityType.CONSERVATIVE:
            recommendations.append("建议优先考虑稳定性和风险控制")
        elif user_profile.personality_type == PersonalityType.AGGRESSIVE:
            recommendations.append("建议重点关注发展前景和薪资增长")
        
        # 去重并限制数量
        unique_recommendations = list(set(recommendations))
        return unique_recommendations[:10]  # 最多10条建议
    
    def _generate_next_steps(self, recommendations: List[str], user_profile: UserProfile) -> List[str]:
        """生成下一步行动计划"""
        next_steps = [
            "1. 根据分析结果优化简历和求职策略",
            "2. 针对性提升关键技能和能力",
            "3. 制定详细的职业发展规划",
            "4. 建立行业人脉网络",
            "5. 持续关注市场动态和趋势变化"
        ]
        
        return next_steps
    
    def _calculate_overall_confidence(self, analysis_results: List[AnalysisResult], insights: List[ComprehensiveInsight]) -> float:
        """计算整体信心分数"""
        if not analysis_results:
            return 0.0
        
        # 基于分析结果的信心度
        analysis_confidence = sum(result.confidence for result in analysis_results) / len(analysis_results)
        
        # 基于洞察质量的调整
        insight_quality = sum(insight.confidence for insight in insights) / len(insights) if insights else 0.8
        
        # 综合信心度
        overall_confidence = (analysis_confidence * 0.7 + insight_quality * 0.3)
        
        return round(overall_confidence, 3)


# ================================
# 🧪 测试函数
# ================================

def test_comprehensive_analyzer():
    """测试综合分析器"""
    print("🧪 测试综合分析器...")
    
    # 创建测试数据
    user_profile = UserProfile(
        user_id="test_user_001",
        name="张三",
        current_position="Python开发工程师",
        experience_years=3,
        skills=["Python", "Django", "MySQL"],
        personality_type=PersonalityType.BALANCED
    )
    
    job_data_list = [
        JobData(
            job_id="job_001",
            title="高级Python开发工程师",
            company="腾讯",
            location="深圳",
            salary_max=35000
        ),
        JobData(
            job_id="job_002", 
            title="Python后端工程师",
            company="字节跳动",
            location="北京",
            salary_max=40000
        )
    ]
    
    # 创建分析器并生成报告
    analyzer = ComprehensiveAnalyzer()
    report = analyzer.generate_comprehensive_report(user_profile, job_data_list)
    
    print(f"✅ 报告生成成功 - ID: {report.report_id}")
    print(f"✅ 洞察数量: {len(report.insights)}")
    print(f"✅ 建议数量: {len(report.recommendations)}")
    print(f"✅ 信心分数: {report.confidence_score}")
    
    print("🎉 综合分析器测试完成！")


if __name__ == "__main__":
    test_comprehensive_analyzer()