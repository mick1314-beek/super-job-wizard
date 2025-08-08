# -*- coding: utf-8 -*-
"""
🚀 超级求职向导 - 模块包初始化
Super Job Wizard - Modules Package Initialization

版本: 1.0.3
功能: AI分析、大数据分析、全局数据管理、平台集成、智能决策、数据接口标准、数据流管理、综合分析报告

作者: AI Assistant
创建时间: 2024年
"""

# 导入核心模块
from .ai_analyzer import AIJobAnalyzer
from .big_data import BigDataAnalyzer  
from .platform_integration import PlatformIntegrator
from .smart_decision import SmartDecisionEngine

# 导入数据接口标准
from .data_interface import (
    DataInterfaceManager,
    UserProfile,
    JobData,
    AnalysisResult,
    DataCache,
    DataValidator,
    DataConverter,
    PersonalityType,
    RiskLevel,
    JobStatus,
    AnalysisType
)

# 导入数据流管理器
from .data_flow_manager import DataFlowManager, ModuleCallProxy

# 导入综合分析报告系统
from .comprehensive_analyzer import (
    ComprehensiveAnalyzer,
    ComprehensiveReport,
    ComprehensiveInsight,
    DecisionMatrix,
    ReportType,
    InsightLevel
)

# 模块版本信息
__version__ = "1.0.3"
__author__ = "AI Assistant"

# 导出的公共接口
__all__ = [
    # 核心分析器
    "AIJobAnalyzer",
    "BigDataAnalyzer", 
    "PlatformIntegrator",
    "SmartDecisionEngine",
    
    # 数据接口标准
    "DataInterfaceManager",
    "UserProfile",
    "JobData", 
    "AnalysisResult",
    "DataCache",
    "DataValidator",
    "DataConverter",
    "PersonalityType",
    "RiskLevel",
    "JobStatus",
    "AnalysisType",
    
    # 数据流管理
    "DataFlowManager",
    "ModuleCallProxy",
    
    # 综合分析报告
    "ComprehensiveAnalyzer",
    "ComprehensiveReport",
    "ComprehensiveInsight", 
    "DecisionMatrix",
    "ReportType",
    "InsightLevel"
]