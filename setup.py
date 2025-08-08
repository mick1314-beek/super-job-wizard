#!/usr/bin/env python3
"""
Super Job Wizard - 超级求职神器 - Setup配置文件
"""

from setuptools import setup, find_packages
import os

# 读取README文件
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            return f.read()
    return "基于PPP和多维度因素的智能工作价值评估工具"

# 读取requirements
def read_requirements():
    requirements_path = os.path.join(os.path.dirname(__file__), "requirements.txt")
    if os.path.exists(requirements_path):
        with open(requirements_path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip() and not line.startswith("#")]
    return [
        "mcp>=1.0.0",
        "fastmcp>=2.0.0",
    ]

setup(
    name="super-job-wizard",
    version="2.0.0",
    author="Super Job Wizard Team",
    author_email="support@super-job-wizard.com",
    description="AI驱动的超级求职助手 - 集成全球化数据分析、智能决策支持、大数据洞察、平台集成和AI分析的终极求职工具",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/super-job-wizard",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Office/Business :: Financial",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "super-job-wizard=super_job_wizard:main",
        ],
    },
    keywords="job search, career planning, AI assistant, MCP, salary analysis, job wizard",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/super-job-wizard/issues",
        "Source": "https://github.com/yourusername/super-job-wizard",
        "Documentation": "https://github.com/yourusername/super-job-wizard#readme",
    },
    include_package_data=True,
    zip_safe=False,
)