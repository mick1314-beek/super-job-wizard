@echo off
chcp 65001 >nul
echo.
echo ========================================
echo 🚀 超级无敌宇宙级求职神器 v3.0
echo ========================================
echo.
echo 🌟 正在启动最强求职工具...
echo.

REM 切换到项目根目录
cd /d "%~dp0\.."

REM 检查虚拟环境
if not exist "super_job_env_313" (
    echo ❌ 虚拟环境不存在，请先创建虚拟环境！
    echo 💡 运行命令: python -m venv super_job_env_313
    pause
    exit /b 1
)

REM 激活虚拟环境
echo 🔧 激活虚拟环境...
call super_job_env_313\Scripts\activate.bat

REM 检查并安装依赖
echo 📦 检查依赖包...
pip install -r requirements.txt >nul 2>&1

echo.
echo ========================================
echo 🎉 启动超级求职神器！
echo ========================================
echo.
echo 🌍 全球化数据支持 - 150+国家PPP数据
echo 🤖 AI智能分析 - 简历优化、薪资预测
echo 📊 大数据支持 - 公司情报、行业报告  
echo 🔗 平台集成 - LinkedIn分析、多平台追踪
echo 🧠 智能决策 - 决策树分析、风险评估
echo 💰 工作价值计算 - 真实时薪、综合评估
echo 🎯 求职助手 - 简历分析、薪资谈判
echo 🎨 水质监测面试 - 专业PPT、题库、策略
echo.
echo 🔥 太牛逼了！准备征服全球求职市场！
echo.
echo ========================================

REM 启动超级求职神器
python src\super_job_wizard.py

echo.
echo 👋 超级求职神器已停止运行
pause