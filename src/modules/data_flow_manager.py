# -*- coding: utf-8 -*-
"""
🔄 数据流管理器模块
Data Flow Manager Module

优化模块间调用链，实现单例模式、智能缓存和数据共享

功能：
🏗️ 单例模式管理所有模块实例
💾 智能缓存机制
🔗 数据传递链路追踪
📊 性能监控和优化
🎯 统一调用接口

作者: AI Assistant
版本: 1.0
"""

import time
import hashlib
import threading
from typing import Dict, List, Optional, Any, Union, Callable
from datetime import datetime, timedelta
from dataclasses import dataclass, field
import json

# 导入数据接口标准
try:
    from .data_interface import (
        DataInterfaceManager, UserProfile, JobData, AnalysisResult,
        DataCache, PersonalityType, RiskLevel, JobStatus, AnalysisType
    )
except ImportError:
    # 如果相对导入失败，尝试绝对导入
    import sys
    import os
    sys.path.append(os.path.dirname(__file__))
    from data_interface import (
        DataInterfaceManager, UserProfile, JobData, AnalysisResult,
        DataCache, PersonalityType, RiskLevel, JobStatus, AnalysisType
    )


# ================================
# 📊 性能监控数据结构
# ================================

@dataclass
class CallMetrics:
    """调用指标数据结构"""
    module_name: str
    method_name: str
    call_count: int = 0
    total_time: float = 0.0
    avg_time: float = 0.0
    last_called: Optional[datetime] = None
    cache_hits: int = 0
    cache_misses: int = 0
    
    def update_metrics(self, execution_time: float, cache_hit: bool = False):
        """更新调用指标"""
        self.call_count += 1
        self.total_time += execution_time
        self.avg_time = self.total_time / self.call_count
        self.last_called = datetime.now()
        
        if cache_hit:
            self.cache_hits += 1
        else:
            self.cache_misses += 1


# ================================
# 🏗️ 单例模式基类
# ================================

class SingletonMeta(type):
    """单例模式元类"""
    _instances = {}
    _lock = threading.Lock()
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


# ================================
# 💾 智能缓存管理器
# ================================

class SmartCacheManager:
    """智能缓存管理器"""
    
    def __init__(self, max_size: int = 1000, default_ttl: int = 3600):
        self.max_size = max_size
        self.default_ttl = default_ttl
        self.cache: Dict[str, DataCache] = {}
        self._lock = threading.Lock()
    
    def _generate_cache_key(self, module: str, method: str, args: tuple, kwargs: dict) -> str:
        """生成缓存键"""
        # 创建唯一标识符
        key_data = {
            "module": module,
            "method": method,
            "args": str(args),
            "kwargs": str(sorted(kwargs.items()))
        }
        key_string = json.dumps(key_data, sort_keys=True)
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def get(self, module: str, method: str, args: tuple, kwargs: dict) -> Optional[Any]:
        """获取缓存数据"""
        cache_key = self._generate_cache_key(module, method, args, kwargs)
        
        with self._lock:
            if cache_key in self.cache:
                cache_item = self.cache[cache_key]
                if not cache_item.is_expired():
                    return cache_item.data
                else:
                    # 删除过期缓存
                    del self.cache[cache_key]
        
        return None
    
    def set(self, module: str, method: str, args: tuple, kwargs: dict, data: Any, ttl: Optional[int] = None) -> None:
        """设置缓存数据"""
        cache_key = self._generate_cache_key(module, method, args, kwargs)
        ttl = ttl or self.default_ttl
        
        with self._lock:
            # 如果缓存已满，删除最旧的项
            if len(self.cache) >= self.max_size:
                oldest_key = min(self.cache.keys(), key=lambda k: self.cache[k].created_at)
                del self.cache[oldest_key]
            
            self.cache[cache_key] = DataCache(
                cache_key=cache_key,
                data=data,
                cache_type=f"{module}.{method}",
                ttl=ttl
            )
    
    def clear(self, module: Optional[str] = None) -> None:
        """清除缓存"""
        with self._lock:
            if module:
                # 清除特定模块的缓存
                keys_to_remove = [k for k, v in self.cache.items() if v.cache_type.startswith(module)]
                for key in keys_to_remove:
                    del self.cache[key]
            else:
                # 清除所有缓存
                self.cache.clear()
    
    def get_cache_stats(self) -> Dict:
        """获取缓存统计信息"""
        with self._lock:
            total_items = len(self.cache)
            expired_items = sum(1 for item in self.cache.values() if item.is_expired())
            
            return {
                "total_items": total_items,
                "active_items": total_items - expired_items,
                "expired_items": expired_items,
                "cache_types": list(set(item.cache_type for item in self.cache.values())),
                "memory_usage_estimate": total_items * 1024  # 粗略估计
            }


# ================================
# 🔄 数据流管理器主类
# ================================

class DataFlowManager(metaclass=SingletonMeta):
    """数据流管理器 - 统一管理所有模块实例和数据流"""
    
    def __init__(self):
        """初始化数据流管理器"""
        print("🚀 初始化数据流管理器...")
        
        # 核心组件
        self.data_interface = DataInterfaceManager()
        self.cache_manager = SmartCacheManager()
        
        # 模块实例存储
        self._module_instances: Dict[str, Any] = {}
        self._module_lock = threading.Lock()
        
        # 性能监控
        self.call_metrics: Dict[str, CallMetrics] = {}
        self.metrics_lock = threading.Lock()
        
        # 数据共享存储
        self.shared_data: Dict[str, Any] = {}
        self.shared_data_lock = threading.Lock()
        
        print("✅ 数据流管理器初始化完成！")
    
    def get_module_instance(self, module_name: str, module_class: type) -> Any:
        """获取模块实例（单例模式）"""
        with self._module_lock:
            if module_name not in self._module_instances:
                print(f"🏗️ 创建新的模块实例: {module_name}")
                self._module_instances[module_name] = module_class()
            
            return self._module_instances[module_name]
    
    def call_module_method(
        self, 
        module_name: str, 
        method_name: str, 
        *args, 
        use_cache: bool = True,
        cache_ttl: Optional[int] = None,
        **kwargs
    ) -> Any:
        """调用模块方法（带缓存和性能监控）"""
        
        # 检查缓存
        if use_cache:
            cached_result = self.cache_manager.get(module_name, method_name, args, kwargs)
            if cached_result is not None:
                self._update_call_metrics(module_name, method_name, 0, cache_hit=True)
                return cached_result
        
        # 获取模块实例
        if module_name not in self._module_instances:
            raise ValueError(f"模块 {module_name} 未注册")
        
        module_instance = self._module_instances[module_name]
        
        # 检查方法是否存在
        if not hasattr(module_instance, method_name):
            raise AttributeError(f"模块 {module_name} 没有方法 {method_name}")
        
        # 执行方法并监控性能
        start_time = time.time()
        try:
            method = getattr(module_instance, method_name)
            result = method(*args, **kwargs)
            
            execution_time = time.time() - start_time
            
            # 缓存结果
            if use_cache:
                self.cache_manager.set(module_name, method_name, args, kwargs, result, cache_ttl)
            
            # 更新性能指标
            self._update_call_metrics(module_name, method_name, execution_time, cache_hit=False)
            
            return result
            
        except Exception as e:
            execution_time = time.time() - start_time
            self._update_call_metrics(module_name, method_name, execution_time, cache_hit=False)
            raise e
    
    def _update_call_metrics(self, module_name: str, method_name: str, execution_time: float, cache_hit: bool):
        """更新调用指标"""
        metric_key = f"{module_name}.{method_name}"
        
        with self.metrics_lock:
            if metric_key not in self.call_metrics:
                self.call_metrics[metric_key] = CallMetrics(module_name, method_name)
            
            self.call_metrics[metric_key].update_metrics(execution_time, cache_hit)
    
    def register_module(self, module_name: str, module_instance: Any) -> None:
        """注册模块实例"""
        with self._module_lock:
            self._module_instances[module_name] = module_instance
            print(f"📝 注册模块: {module_name}")
    
    def share_data(self, key: str, data: Any, ttl: Optional[int] = None) -> None:
        """共享数据到全局存储"""
        with self.shared_data_lock:
            self.shared_data[key] = {
                "data": data,
                "created_at": datetime.now(),
                "ttl": ttl
            }
    
    def get_shared_data(self, key: str) -> Optional[Any]:
        """获取共享数据"""
        with self.shared_data_lock:
            if key in self.shared_data:
                item = self.shared_data[key]
                
                # 检查是否过期
                if item["ttl"]:
                    if (datetime.now() - item["created_at"]).seconds > item["ttl"]:
                        del self.shared_data[key]
                        return None
                
                return item["data"]
        
        return None
    
    def get_performance_report(self) -> Dict:
        """获取性能报告"""
        with self.metrics_lock:
            report = {
                "总调用次数": sum(metric.call_count for metric in self.call_metrics.values()),
                "平均响应时间": sum(metric.avg_time for metric in self.call_metrics.values()) / len(self.call_metrics) if self.call_metrics else 0,
                "缓存命中率": self._calculate_cache_hit_rate(),
                "模块性能": {},
                "缓存统计": self.cache_manager.get_cache_stats(),
                "生成时间": datetime.now().isoformat()
            }
            
            # 详细模块性能
            for key, metric in self.call_metrics.items():
                report["模块性能"][key] = {
                    "调用次数": metric.call_count,
                    "平均时间": round(metric.avg_time, 4),
                    "总时间": round(metric.total_time, 4),
                    "缓存命中率": round(metric.cache_hits / (metric.cache_hits + metric.cache_misses) * 100, 2) if (metric.cache_hits + metric.cache_misses) > 0 else 0,
                    "最后调用": metric.last_called.isoformat() if metric.last_called else None
                }
            
            return report
    
    def _calculate_cache_hit_rate(self) -> float:
        """计算总体缓存命中率"""
        total_hits = sum(metric.cache_hits for metric in self.call_metrics.values())
        total_requests = sum(metric.cache_hits + metric.cache_misses for metric in self.call_metrics.values())
        
        return round(total_hits / total_requests * 100, 2) if total_requests > 0 else 0
    
    def clear_all_caches(self) -> None:
        """清除所有缓存"""
        self.cache_manager.clear()
        with self.shared_data_lock:
            self.shared_data.clear()
        print("🧹 所有缓存已清除")
    
    def reset_metrics(self) -> None:
        """重置性能指标"""
        with self.metrics_lock:
            self.call_metrics.clear()
        print("📊 性能指标已重置")


# ================================
# 🎯 便捷调用接口
# ================================

class ModuleCallProxy:
    """模块调用代理 - 提供便捷的调用接口"""
    
    def __init__(self, data_flow_manager: DataFlowManager):
        self.dfm = data_flow_manager
    
    def ai_analyzer(self, method: str, *args, **kwargs):
        """AI分析器调用代理"""
        return self.dfm.call_module_method("ai_analyzer", method, *args, **kwargs)
    
    def big_data(self, method: str, *args, **kwargs):
        """大数据分析器调用代理"""
        return self.dfm.call_module_method("big_data", method, *args, **kwargs)
    
    def platform_integration(self, method: str, *args, **kwargs):
        """平台集成调用代理"""
        return self.dfm.call_module_method("platform_integration", method, *args, **kwargs)
    
    def smart_decision(self, method: str, *args, **kwargs):
        """智能决策调用代理"""
        return self.dfm.call_module_method("smart_decision", method, *args, **kwargs)


# ================================
# 🧪 测试函数
# ================================

def test_data_flow_manager():
    """测试数据流管理器"""
    print("🧪 测试数据流管理器...")
    
    # 创建管理器实例
    dfm = DataFlowManager()
    
    # 测试单例模式
    dfm2 = DataFlowManager()
    assert dfm is dfm2, "单例模式测试失败"
    print("✅ 单例模式测试通过")
    
    # 测试数据共享
    dfm.share_data("test_key", {"message": "Hello World"})
    shared_data = dfm.get_shared_data("test_key")
    assert shared_data["message"] == "Hello World", "数据共享测试失败"
    print("✅ 数据共享测试通过")
    
    # 测试缓存
    cache_stats = dfm.cache_manager.get_cache_stats()
    print(f"✅ 缓存统计: {cache_stats}")
    
    # 测试性能报告
    performance_report = dfm.get_performance_report()
    print(f"✅ 性能报告生成成功")
    
    print("🎉 数据流管理器测试完成！")


if __name__ == "__main__":
    test_data_flow_manager()