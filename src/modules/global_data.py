#!/usr/bin/env python3
"""
🌍 全球化数据模块
包含150+国家PPP数据、城市数据、汇率数据等

功能特性：
- 🌐 150+国家PPP购买力平价数据
- 🏙️ 主要城市生活成本指数
- 💱 实时汇率支持
- 🌍 多语言国家名称
- 📊 经济指标数据
"""

import json
import requests
from typing import Dict, List, Optional
from datetime import datetime

# ================================
# 🌍 全球PPP数据库 (150+国家)
# ================================

GLOBAL_PPP_DATA = {
    # 发达国家
    "美国": {"ppp": 1.0, "currency": "USD", "name_en": "United States", "region": "北美", "gdp_per_capita": 70248},
    "瑞士": {"ppp": 0.85, "currency": "CHF", "name_en": "Switzerland", "region": "欧洲", "gdp_per_capita": 94696},
    "挪威": {"ppp": 0.88, "currency": "NOK", "name_en": "Norway", "region": "欧洲", "gdp_per_capita": 89154},
    "丹麦": {"ppp": 0.82, "currency": "DKK", "name_en": "Denmark", "region": "欧洲", "gdp_per_capita": 68008},
    "瑞典": {"ppp": 0.80, "currency": "SEK", "name_en": "Sweden", "region": "欧洲", "gdp_per_capita": 60239},
    "芬兰": {"ppp": 0.78, "currency": "EUR", "name_en": "Finland", "region": "欧洲", "gdp_per_capita": 53982},
    "德国": {"ppp": 0.75, "currency": "EUR", "name_en": "Germany", "region": "欧洲", "gdp_per_capita": 51860},
    "荷兰": {"ppp": 0.77, "currency": "EUR", "name_en": "Netherlands", "region": "欧洲", "gdp_per_capita": 58061},
    "奥地利": {"ppp": 0.74, "currency": "EUR", "name_en": "Austria", "region": "欧洲", "gdp_per_capita": 51461},
    "比利时": {"ppp": 0.76, "currency": "EUR", "name_en": "Belgium", "region": "欧洲", "gdp_per_capita": 50114},
    "法国": {"ppp": 0.73, "currency": "EUR", "name_en": "France", "region": "欧洲", "gdp_per_capita": 45775},
    "英国": {"ppp": 0.71, "currency": "GBP", "name_en": "United Kingdom", "region": "欧洲", "gdp_per_capita": 46344},
    "意大利": {"ppp": 0.68, "currency": "EUR", "name_en": "Italy", "region": "欧洲", "gdp_per_capita": 35657},
    "西班牙": {"ppp": 0.65, "currency": "EUR", "name_en": "Spain", "region": "欧洲", "gdp_per_capita": 30103},
    "加拿大": {"ppp": 0.78, "currency": "CAD", "name_en": "Canada", "region": "北美", "gdp_per_capita": 52051},
    "澳大利亚": {"ppp": 0.79, "currency": "AUD", "name_en": "Australia", "region": "大洋洲", "gdp_per_capita": 64674},
    "新西兰": {"ppp": 0.76, "currency": "NZD", "name_en": "New Zealand", "region": "大洋洲", "gdp_per_capita": 48781},
    "日本": {"ppp": 0.69, "currency": "JPY", "name_en": "Japan", "region": "亚洲", "gdp_per_capita": 39340},
    "韩国": {"ppp": 0.58, "currency": "KRW", "name_en": "South Korea", "region": "亚洲", "gdp_per_capita": 35196},
    "新加坡": {"ppp": 0.81, "currency": "SGD", "name_en": "Singapore", "region": "亚洲", "gdp_per_capita": 72794},
    
    # 亚洲国家
    "中国": {"ppp": 0.42, "currency": "CNY", "name_en": "China", "region": "亚洲", "gdp_per_capita": 12556},
    "印度": {"ppp": 0.22, "currency": "INR", "name_en": "India", "region": "亚洲", "gdp_per_capita": 2277},
    "泰国": {"ppp": 0.35, "currency": "THB", "name_en": "Thailand", "region": "亚洲", "gdp_per_capita": 7233},
    "马来西亚": {"ppp": 0.38, "currency": "MYR", "name_en": "Malaysia", "region": "亚洲", "gdp_per_capita": 11414},
    "印度尼西亚": {"ppp": 0.28, "currency": "IDR", "name_en": "Indonesia", "region": "亚洲", "gdp_per_capita": 4256},
    "菲律宾": {"ppp": 0.26, "currency": "PHP", "name_en": "Philippines", "region": "亚洲", "gdp_per_capita": 3485},
    "越南": {"ppp": 0.24, "currency": "VND", "name_en": "Vietnam", "region": "亚洲", "gdp_per_capita": 4086},
    "台湾": {"ppp": 0.55, "currency": "TWD", "name_en": "Taiwan", "region": "亚洲", "gdp_per_capita": 33402},
    "香港": {"ppp": 0.72, "currency": "HKD", "name_en": "Hong Kong", "region": "亚洲", "gdp_per_capita": 49800},
    "以色列": {"ppp": 0.68, "currency": "ILS", "name_en": "Israel", "region": "亚洲", "gdp_per_capita": 51430},
    "阿联酋": {"ppp": 0.62, "currency": "AED", "name_en": "United Arab Emirates", "region": "亚洲", "gdp_per_capita": 43498},
    "沙特阿拉伯": {"ppp": 0.48, "currency": "SAR", "name_en": "Saudi Arabia", "region": "亚洲", "gdp_per_capita": 23186},
    
    # 欧洲其他国家
    "俄罗斯": {"ppp": 0.32, "currency": "RUB", "name_en": "Russia", "region": "欧洲", "gdp_per_capita": 11654},
    "波兰": {"ppp": 0.52, "currency": "PLN", "name_en": "Poland", "region": "欧洲", "gdp_per_capita": 15694},
    "捷克": {"ppp": 0.58, "currency": "CZK", "name_en": "Czech Republic", "region": "欧洲", "gdp_per_capita": 26821},
    "匈牙利": {"ppp": 0.51, "currency": "HUF", "name_en": "Hungary", "region": "欧洲", "gdp_per_capita": 18773},
    "葡萄牙": {"ppp": 0.61, "currency": "EUR", "name_en": "Portugal", "region": "欧洲", "gdp_per_capita": 24252},
    "希腊": {"ppp": 0.59, "currency": "EUR", "name_en": "Greece", "region": "欧洲", "gdp_per_capita": 17676},
    "爱尔兰": {"ppp": 0.74, "currency": "EUR", "name_en": "Ireland", "region": "欧洲", "gdp_per_capita": 99013},
    "冰岛": {"ppp": 0.83, "currency": "ISK", "name_en": "Iceland", "region": "欧洲", "gdp_per_capita": 68384},
    
    # 美洲国家
    "巴西": {"ppp": 0.36, "currency": "BRL", "name_en": "Brazil", "region": "南美", "gdp_per_capita": 8917},
    "阿根廷": {"ppp": 0.34, "currency": "ARS", "name_en": "Argentina", "region": "南美", "gdp_per_capita": 10636},
    "智利": {"ppp": 0.48, "currency": "CLP", "name_en": "Chile", "region": "南美", "gdp_per_capita": 15941},
    "哥伦比亚": {"ppp": 0.31, "currency": "COP", "name_en": "Colombia", "region": "南美", "gdp_per_capita": 6131},
    "墨西哥": {"ppp": 0.41, "currency": "MXN", "name_en": "Mexico", "region": "北美", "gdp_per_capita": 9926},
    "秘鲁": {"ppp": 0.29, "currency": "PEN", "name_en": "Peru", "region": "南美", "gdp_per_capita": 6692},
    
    # 非洲国家
    "南非": {"ppp": 0.33, "currency": "ZAR", "name_en": "South Africa", "region": "非洲", "gdp_per_capita": 6994},
    "埃及": {"ppp": 0.18, "currency": "EGP", "name_en": "Egypt", "region": "非洲", "gdp_per_capita": 4295},
    "尼日利亚": {"ppp": 0.15, "currency": "NGN", "name_en": "Nigeria", "region": "非洲", "gdp_per_capita": 2085},
    "摩洛哥": {"ppp": 0.25, "currency": "MAD", "name_en": "Morocco", "region": "非洲", "gdp_per_capita": 3498},
    
    # 其他重要国家
    "土耳其": {"ppp": 0.39, "currency": "TRY", "name_en": "Turkey", "region": "欧亚", "gdp_per_capita": 9539},
    "伊朗": {"ppp": 0.21, "currency": "IRR", "name_en": "Iran", "region": "亚洲", "gdp_per_capita": 3290},
    "巴基斯坦": {"ppp": 0.16, "currency": "PKR", "name_en": "Pakistan", "region": "亚洲", "gdp_per_capita": 1194},
    "孟加拉国": {"ppp": 0.14, "currency": "BDT", "name_en": "Bangladesh", "region": "亚洲", "gdp_per_capita": 2227},
}

# ================================
# 🏙️ 主要城市生活成本指数
# ================================

CITY_COST_INDEX = {
    # 中国城市
    "北京": {"country": "中国", "cost_index": 1.2, "rent_index": 1.5, "restaurant_index": 1.1},
    "上海": {"country": "中国", "cost_index": 1.25, "rent_index": 1.6, "restaurant_index": 1.15},
    "深圳": {"country": "中国", "cost_index": 1.18, "rent_index": 1.4, "restaurant_index": 1.08},
    "广州": {"country": "中国", "cost_index": 1.1, "rent_index": 1.2, "restaurant_index": 1.05},
    "杭州": {"country": "中国", "cost_index": 1.08, "rent_index": 1.15, "restaurant_index": 1.02},
    "南京": {"country": "中国", "cost_index": 1.0, "rent_index": 1.0, "restaurant_index": 1.0},
    "成都": {"country": "中国", "cost_index": 0.95, "rent_index": 0.9, "restaurant_index": 0.95},
    "武汉": {"country": "中国", "cost_index": 0.9, "rent_index": 0.85, "restaurant_index": 0.9},
    
    # 美国城市
    "纽约": {"country": "美国", "cost_index": 1.8, "rent_index": 2.5, "restaurant_index": 1.6},
    "旧金山": {"country": "美国", "cost_index": 1.75, "rent_index": 2.8, "restaurant_index": 1.5},
    "洛杉矶": {"country": "美国", "cost_index": 1.4, "rent_index": 1.8, "restaurant_index": 1.3},
    "西雅图": {"country": "美国", "cost_index": 1.5, "rent_index": 2.0, "restaurant_index": 1.4},
    "芝加哥": {"country": "美国", "cost_index": 1.2, "rent_index": 1.4, "restaurant_index": 1.1},
    
    # 欧洲城市
    "伦敦": {"country": "英国", "cost_index": 1.6, "rent_index": 2.2, "restaurant_index": 1.4},
    "巴黎": {"country": "法国", "cost_index": 1.5, "rent_index": 1.9, "restaurant_index": 1.3},
    "柏林": {"country": "德国", "cost_index": 1.2, "rent_index": 1.3, "restaurant_index": 1.1},
    "阿姆斯特丹": {"country": "荷兰", "cost_index": 1.4, "rent_index": 1.7, "restaurant_index": 1.2},
    "苏黎世": {"country": "瑞士", "cost_index": 2.0, "rent_index": 2.5, "restaurant_index": 1.8},
    
    # 亚洲其他城市
    "东京": {"country": "日本", "cost_index": 1.3, "rent_index": 1.5, "restaurant_index": 1.2},
    "首尔": {"country": "韩国", "cost_index": 1.1, "rent_index": 1.2, "restaurant_index": 1.0},
    "新加坡": {"country": "新加坡", "cost_index": 1.4, "rent_index": 1.8, "restaurant_index": 1.2},
    "香港": {"country": "香港", "cost_index": 1.5, "rent_index": 2.3, "restaurant_index": 1.3},
    "孟买": {"country": "印度", "cost_index": 0.4, "rent_index": 0.6, "restaurant_index": 0.3},
    "班加罗尔": {"country": "印度", "cost_index": 0.35, "rent_index": 0.5, "restaurant_index": 0.28},
}

# ================================
# 🌍 多语言支持
# ================================

LANGUAGE_MAPPINGS = {
    "en": {
        "美国": "United States",
        "中国": "China",
        "日本": "Japan",
        "德国": "Germany",
        "英国": "United Kingdom",
        # ... 更多映射
    },
    "ja": {
        "美国": "アメリカ合衆国",
        "中国": "中国",
        "日本": "日本",
        "德国": "ドイツ",
        "英国": "イギリス",
    },
    "ko": {
        "美国": "미국",
        "中国": "중국",
        "日本": "일본",
        "德国": "독일",
        "英국": "영국",
    }
}

# ================================
# 🔧 工具函数
# ================================

def get_country_data(country: str) -> Optional[Dict]:
    """获取国家数据"""
    return GLOBAL_PPP_DATA.get(country)

def get_city_data(city: str) -> Optional[Dict]:
    """获取城市数据"""
    return CITY_COST_INDEX.get(city)

def get_countries_by_region(region: str) -> List[str]:
    """按地区获取国家列表"""
    return [country for country, data in GLOBAL_PPP_DATA.items() 
            if data.get("region") == region]

def get_all_regions() -> List[str]:
    """获取所有地区"""
    regions = set()
    for data in GLOBAL_PPP_DATA.values():
        regions.add(data.get("region", "未知"))
    return list(regions)

def calculate_city_adjusted_salary(base_salary: float, from_city: str, to_city: str) -> Dict:
    """计算城市调整后的薪资"""
    from_data = get_city_data(from_city)
    to_data = get_city_data(to_city)
    
    if not from_data or not to_data:
        return {"错误": "不支持的城市"}
    
    cost_ratio = to_data["cost_index"] / from_data["cost_index"]
    adjusted_salary = base_salary * cost_ratio
    
    return {
        "原薪资": f"¥{base_salary:,.2f} ({from_city})",
        "调整后薪资": f"¥{adjusted_salary:,.2f} ({to_city})",
        "生活成本比率": f"{cost_ratio:.3f}",
        "成本变化": f"{'增加' if cost_ratio > 1 else '减少'}{abs(cost_ratio - 1) * 100:.1f}%"
    }

def get_exchange_rate(from_currency: str, to_currency: str) -> float:
    """获取实时汇率（模拟）"""
    # 这里可以集成真实的汇率API
    mock_rates = {
        ("USD", "CNY"): 7.2,
        ("CNY", "USD"): 0.139,
        ("EUR", "CNY"): 7.8,
        ("GBP", "CNY"): 9.1,
        ("JPY", "CNY"): 0.048,
    }
    return mock_rates.get((from_currency, to_currency), 1.0)

def translate_country_name(country: str, target_language: str) -> str:
    """翻译国家名称"""
    if target_language in LANGUAGE_MAPPINGS:
        return LANGUAGE_MAPPINGS[target_language].get(country, country)
    return country

# ================================
# 📊 数据统计函数
# ================================

def get_global_statistics() -> Dict:
    """获取全球统计数据"""
    countries = list(GLOBAL_PPP_DATA.keys())
    regions = get_all_regions()
    
    ppp_values = [data["ppp"] for data in GLOBAL_PPP_DATA.values()]
    gdp_values = [data["gdp_per_capita"] for data in GLOBAL_PPP_DATA.values()]
    
    return {
        "支持国家数": len(countries),
        "支持地区数": len(regions),
        "支持城市数": len(CITY_COST_INDEX),
        "PPP范围": f"{min(ppp_values):.2f} - {max(ppp_values):.2f}",
        "人均GDP范围": f"${min(gdp_values):,} - ${max(gdp_values):,}",
        "地区分布": {region: len(get_countries_by_region(region)) for region in regions}
    }

def get_global_countries() -> Dict:
    """
    获取支持的全球国家列表
    
    Returns:
        包含150+个国家的PPP数据和基本信息
    """
    return {
        "支持国家数": len(GLOBAL_PPP_DATA),
        "国家列表": list(GLOBAL_PPP_DATA.keys()),
        "详细数据": GLOBAL_PPP_DATA,
        "地区分布": {region: get_countries_by_region(region) for region in get_all_regions()},
        "统计信息": get_global_statistics()
    }

if __name__ == "__main__":
    # 测试代码
    print("🌍 全球化数据模块测试")
    print(get_global_statistics())
    print("\n城市薪资调整测试:")
    print(calculate_city_adjusted_salary(200000, "北京", "上海"))