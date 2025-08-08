# -*- coding: utf-8 -*-
"""
🔗 统一数据接口标准模块
Data Interface Standards Module

定义所有模块间数据交换的标准格式，确保数据一致性和兼容性

功能：
📋 标准数据结构定义
🔄 数据格式验证
🎯 类型安全保证
📊 数据转换工具

作者: AI Assistant
版本: 1.0
"""

from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum
import json


# ================================
# 🎯 枚举定义
# ================================

class PersonalityType(Enum):
    """性格类型枚举"""
    CONSERVATIVE = "稳健型"
    AGGRESSIVE = "进取型"
    BALANCED = "平衡型"
    INNOVATIVE = "创新型"


class RiskLevel(Enum):
    """风险等级枚举"""
    LOW = "低风险"
    MEDIUM = "中风险"
    HIGH = "高风险"
    VERY_HIGH = "极高风险"


class JobStatus(Enum):
    """求职状态枚举"""
    APPLIED = "已投递"
    INTERVIEW_SCHEDULED = "面试安排"
    INTERVIEWED = "已面试"
    OFFER_RECEIVED = "收到offer"
    REJECTED = "被拒绝"
    ACCEPTED = "已接受"
    WITHDRAWN = "已撤回"


class AnalysisType(Enum):
    """分析类型枚举"""
    RESUME_ANALYSIS = "简历分析"
    SALARY_PREDICTION = "薪资预测"
    CAREER_PLANNING = "职业规划"
    JOB_DECISION = "工作决策"
    MARKET_ANALYSIS = "市场分析"
    SKILL_ASSESSMENT = "技能评估"


# ================================
# 📋 核心数据结构
# ================================

@dataclass
class UserProfile:
    """用户画像标准数据结构"""
    # 基本信息
    user_id: str
    name: str = ""
    age: Optional[int] = None
    location: str = ""
    
    # 职业信息
    current_position: str = ""
    experience_years: int = 0
    industry: str = ""
    education_level: str = ""
    
    # 技能和能力
    skills: List[str] = field(default_factory=list)
    certifications: List[str] = field(default_factory=list)
    languages: List[str] = field(default_factory=list)
    
    # 性格和偏好
    personality_type: PersonalityType = PersonalityType.BALANCED
    risk_tolerance: RiskLevel = RiskLevel.MEDIUM
    career_goals: Dict[str, Any] = field(default_factory=dict)
    
    # 薪资期望
    current_salary: Optional[float] = None
    expected_salary: Optional[float] = None
    salary_currency: str = "CNY"
    
    # 元数据
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict:
        """转换为字典格式"""
        return {
            "user_id": self.user_id,
            "name": self.name,
            "age": self.age,
            "location": self.location,
            "current_position": self.current_position,
            "experience_years": self.experience_years,
            "industry": self.industry,
            "education_level": self.education_level,
            "skills": self.skills,
            "certifications": self.certifications,
            "languages": self.languages,
            "personality_type": self.personality_type.value,
            "risk_tolerance": self.risk_tolerance.value,
            "career_goals": self.career_goals,
            "current_salary": self.current_salary,
            "expected_salary": self.expected_salary,
            "salary_currency": self.salary_currency,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


@dataclass
class JobData:
    """工作数据标准结构"""
    # 基本信息
    job_id: str
    title: str
    company: str
    location: str
    
    # 薪资信息
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    salary_currency: str = "CNY"
    
    # 工作详情
    description: str = ""
    requirements: List[str] = field(default_factory=list)
    benefits: List[str] = field(default_factory=list)
    work_type: str = "全职"  # 全职/兼职/实习/合同
    
    # 公司信息
    company_size: str = ""
    company_industry: str = ""
    company_stage: str = ""  # 创业/成长/成熟/上市
    
    # 申请状态
    application_status: JobStatus = JobStatus.APPLIED
    application_date: Optional[datetime] = None
    
    # 评估数据
    match_score: Optional[float] = None
    risk_score: Optional[float] = None
    
    # 元数据
    source_platform: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict:
        """转换为字典格式"""
        return {
            "job_id": self.job_id,
            "title": self.title,
            "company": self.company,
            "location": self.location,
            "salary_min": self.salary_min,
            "salary_max": self.salary_max,
            "salary_currency": self.salary_currency,
            "description": self.description,
            "requirements": self.requirements,
            "benefits": self.benefits,
            "work_type": self.work_type,
            "company_size": self.company_size,
            "company_industry": self.company_industry,
            "company_stage": self.company_stage,
            "application_status": self.application_status.value,
            "application_date": self.application_date.isoformat() if self.application_date else None,
            "match_score": self.match_score,
            "risk_score": self.risk_score,
            "source_platform": self.source_platform,
            "created_at": self.created_at.isoformat()
        }


@dataclass
class AnalysisResult:
    """分析结果标准结构"""
    # 基本信息
    analysis_id: str
    analysis_type: AnalysisType
    user_id: str
    
    # 分析结果
    score: Optional[float] = None
    confidence: Optional[float] = None
    recommendations: List[str] = field(default_factory=list)
    insights: Dict[str, Any] = field(default_factory=dict)
    
    # 详细数据
    detailed_scores: Dict[str, float] = field(default_factory=dict)
    risk_assessment: Dict[str, Any] = field(default_factory=dict)
    improvement_suggestions: List[str] = field(default_factory=list)
    
    # 元数据
    module_source: str = ""  # 来源模块
    processing_time: Optional[float] = None
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict:
        """转换为字典格式"""
        return {
            "analysis_id": self.analysis_id,
            "analysis_type": self.analysis_type.value,
            "user_id": self.user_id,
            "score": self.score,
            "confidence": self.confidence,
            "recommendations": self.recommendations,
            "insights": self.insights,
            "detailed_scores": self.detailed_scores,
            "risk_assessment": self.risk_assessment,
            "improvement_suggestions": self.improvement_suggestions,
            "module_source": self.module_source,
            "processing_time": self.processing_time,
            "created_at": self.created_at.isoformat()
        }


@dataclass
class DataCache:
    """数据缓存标准结构"""
    cache_key: str
    data: Any
    cache_type: str
    ttl: int = 3600  # 缓存时间（秒）
    created_at: datetime = field(default_factory=datetime.now)
    
    def is_expired(self) -> bool:
        """检查缓存是否过期"""
        return (datetime.now() - self.created_at).seconds > self.ttl
    
    def to_dict(self) -> Dict:
        """转换为字典格式"""
        return {
            "cache_key": self.cache_key,
            "data": self.data,
            "cache_type": self.cache_type,
            "ttl": self.ttl,
            "created_at": self.created_at.isoformat()
        }


# ================================
# 🔄 数据验证器
# ================================

class DataValidator:
    """数据验证器"""
    
    @staticmethod
    def validate_user_profile(data: Dict) -> bool:
        """验证用户画像数据"""
        required_fields = ["user_id"]
        
        for field in required_fields:
            if field not in data:
                return False
        
        # 验证枚举值
        if "personality_type" in data:
            valid_personalities = [p.value for p in PersonalityType]
            if data["personality_type"] not in valid_personalities:
                return False
        
        if "risk_tolerance" in data:
            valid_risks = [r.value for r in RiskLevel]
            if data["risk_tolerance"] not in valid_risks:
                return False
        
        return True
    
    @staticmethod
    def validate_job_data(data: Dict) -> bool:
        """验证工作数据"""
        required_fields = ["job_id", "title", "company"]
        
        for field in required_fields:
            if field not in data:
                return False
        
        # 验证状态枚举
        if "application_status" in data:
            valid_statuses = [s.value for s in JobStatus]
            if data["application_status"] not in valid_statuses:
                return False
        
        return True
    
    @staticmethod
    def validate_analysis_result(data: Dict) -> bool:
        """验证分析结果数据"""
        required_fields = ["analysis_id", "analysis_type", "user_id"]
        
        for field in required_fields:
            if field not in data:
                return False
        
        # 验证分析类型
        if "analysis_type" in data:
            valid_types = [t.value for t in AnalysisType]
            if data["analysis_type"] not in valid_types:
                return False
        
        return True


# ================================
# 🛠️ 数据转换工具
# ================================

class DataConverter:
    """数据转换工具"""
    
    @staticmethod
    def dict_to_user_profile(data: Dict) -> UserProfile:
        """字典转用户画像对象"""
        # 处理枚举类型
        if "personality_type" in data:
            for p_type in PersonalityType:
                if p_type.value == data["personality_type"]:
                    data["personality_type"] = p_type
                    break
        
        if "risk_tolerance" in data:
            for risk in RiskLevel:
                if risk.value == data["risk_tolerance"]:
                    data["risk_tolerance"] = risk
                    break
        
        # 处理日期时间
        if "created_at" in data and isinstance(data["created_at"], str):
            data["created_at"] = datetime.fromisoformat(data["created_at"])
        
        if "updated_at" in data and isinstance(data["updated_at"], str):
            data["updated_at"] = datetime.fromisoformat(data["updated_at"])
        
        return UserProfile(**data)
    
    @staticmethod
    def dict_to_job_data(data: Dict) -> JobData:
        """字典转工作数据对象"""
        # 处理状态枚举
        if "application_status" in data:
            for status in JobStatus:
                if status.value == data["application_status"]:
                    data["application_status"] = status
                    break
        
        # 处理日期时间
        if "application_date" in data and isinstance(data["application_date"], str):
            data["application_date"] = datetime.fromisoformat(data["application_date"])
        
        if "created_at" in data and isinstance(data["created_at"], str):
            data["created_at"] = datetime.fromisoformat(data["created_at"])
        
        return JobData(**data)
    
    @staticmethod
    def dict_to_analysis_result(data: Dict) -> AnalysisResult:
        """字典转分析结果对象"""
        # 处理分析类型枚举
        if "analysis_type" in data:
            for a_type in AnalysisType:
                if a_type.value == data["analysis_type"]:
                    data["analysis_type"] = a_type
                    break
        
        # 处理日期时间
        if "created_at" in data and isinstance(data["created_at"], str):
            data["created_at"] = datetime.fromisoformat(data["created_at"])
        
        return AnalysisResult(**data)


# ================================
# 📊 数据接口管理器
# ================================

class DataInterfaceManager:
    """数据接口管理器 - 统一数据操作入口"""
    
    def __init__(self):
        self.validator = DataValidator()
        self.converter = DataConverter()
    
    def create_user_profile(self, data: Dict) -> UserProfile:
        """创建用户画像"""
        if not self.validator.validate_user_profile(data):
            raise ValueError("用户画像数据验证失败")
        
        return self.converter.dict_to_user_profile(data)
    
    def create_job_data(self, data: Dict) -> JobData:
        """创建工作数据"""
        if not self.validator.validate_job_data(data):
            raise ValueError("工作数据验证失败")
        
        return self.converter.dict_to_job_data(data)
    
    def create_analysis_result(self, data: Dict) -> AnalysisResult:
        """创建分析结果"""
        if not self.validator.validate_analysis_result(data):
            raise ValueError("分析结果数据验证失败")
        
        return self.converter.dict_to_analysis_result(data)
    
    def standardize_module_output(self, module_name: str, raw_output: Dict) -> Dict:
        """标准化模块输出格式"""
        return {
            "module_source": module_name,
            "timestamp": datetime.now().isoformat(),
            "data": raw_output,
            "format_version": "1.0"
        }
    
    def merge_analysis_results(self, results: List[AnalysisResult]) -> Dict:
        """合并多个分析结果"""
        if not results:
            return {}
        
        merged = {
            "total_analyses": len(results),
            "analysis_types": [r.analysis_type.value for r in results],
            "average_score": sum(r.score for r in results if r.score) / len([r for r in results if r.score]),
            "combined_recommendations": [],
            "module_sources": list(set(r.module_source for r in results)),
            "created_at": datetime.now().isoformat()
        }
        
        # 合并推荐建议
        for result in results:
            merged["combined_recommendations"].extend(result.recommendations)
        
        # 去重推荐建议
        merged["combined_recommendations"] = list(set(merged["combined_recommendations"]))
        
        return merged


# ================================
# 🎯 导出接口
# ================================

# 导出主要类和枚举
__all__ = [
    # 枚举
    'PersonalityType',
    'RiskLevel', 
    'JobStatus',
    'AnalysisType',
    
    # 数据结构
    'UserProfile',
    'JobData',
    'AnalysisResult',
    'DataCache',
    
    # 工具类
    'DataValidator',
    'DataConverter',
    'DataInterfaceManager'
]


# ================================
# 🧪 测试函数
# ================================

def test_data_interface():
    """测试数据接口功能"""
    print("🧪 测试数据接口标准...")
    
    # 创建管理器
    manager = DataInterfaceManager()
    
    # 测试用户画像
    user_data = {
        "user_id": "test_user_001",
        "name": "张三",
        "current_position": "Python开发工程师",
        "experience_years": 3,
        "skills": ["Python", "Django", "MySQL"],
        "personality_type": "平衡型",
        "risk_tolerance": "中风险"
    }
    
    try:
        user_profile = manager.create_user_profile(user_data)
        print(f"✅ 用户画像创建成功: {user_profile.name}")
    except Exception as e:
        print(f"❌ 用户画像创建失败: {e}")
    
    # 测试工作数据
    job_data = {
        "job_id": "job_001",
        "title": "高级Python开发工程师",
        "company": "腾讯",
        "location": "深圳",
        "salary_min": 25000,
        "salary_max": 35000,
        "application_status": "已投递"
    }
    
    try:
        job = manager.create_job_data(job_data)
        print(f"✅ 工作数据创建成功: {job.title}")
    except Exception as e:
        print(f"❌ 工作数据创建失败: {e}")
    
    print("🎉 数据接口测试完成！")


if __name__ == "__main__":
    test_data_interface()