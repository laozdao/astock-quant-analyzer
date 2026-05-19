# astock-quant-analyzer

> 基于"双引擎四层"融合模型的 A股个股量化分析 Skill，一句话触发，3 分钟输出专业级投资分析报告。

[![SOLO Skill](https://img.shields.io/badge/SOLO-Skill-blue)](https://github.com/laozdao/astock-quant-analyzer/releases)
[![Python](https://img.shields.io/badge/Python-3.8+-green)]()
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Release](https://img.shields.io/badge/Release-v1.0.0-orange)](https://github.com/laozdao/astock-quant-analyzer/releases/tag/v1.0.0)

## ✨ 特性

- 🎯 **双引擎四层模型**：基本面(60%) + 量价(25%) + 风险(15%)，融合板块与消息面分析
- 📊 **八因子基本面评分**：价值、成长、质量、动量、情绪、资金流、ESG、另类数据
- 📈 **六维度量价分析**：趋势、量价配合、关键位置、主力行为、波动率、多周期共振
- 🛡️ **四维度风险控制**：估值、流动性、下行、集中度 + 信号冲突检测
- 🔄 **动态权重调整**：根据牛/熊/震荡市自动调整评分权重
- 🧩 **经典框架适配**：自动匹配价值选股、困境反转、成长股PEG、动量趋势模型
- 📋 **十大章节报告**：从基本信息到风险提示，结构化输出完整分析报告

## 📦 下载安装

### 方式一：从 Release 下载（推荐）

直接下载打包好的 Skill 文件，一键导入即可使用：

👉 **[下载 astock-quant-analyzer.skill](https://github.com/laozdao/astock-quant-analyzer/releases/download/v1.0.0/astock-quant-analyzer.skill)**

### 方式二：从源码安装

```bash
git clone https://github.com/laozdao/astock-quant-analyzer.git
cd astock-quant-analyzer
pip install -r requirements.txt
```

## 💻 支持的软件

本 Skill 可在以下 AI 助手软件中使用：

| 软件 | 说明 |
|------|------|
| **[SOLO](https://solo.trae.cn/)** | 通用 AI 助手，原生支持 Skill 导入 |
| **[Trae](https://trae.cn/)** | 字节跳动 AI 编程助手，原生支持 Skill 导入 |
| **[Claude Code](https://www.anthropic.com/claude)** | Anthropic 官方 AI 编程助手 |
| **[Codex](https://openai.com/index/introducing-codex/)** | OpenAI 代码生成模型 |
| **[Cursor](https://cursor.sh/)** | AI 编程助手，可通过 .cursorrules 适配 |
| **[Windsurf](https://codeium.com/windsurf)** | Codeium AI 编程助手 |
| **[Cline](https://github.com/cline/cline)** | VS Code AI 插件，支持自定义规则 |

> 💡 **提示**：SOLO 和 Trae 原生支持 `.skill` 文件导入，其他软件可能需要手动适配。

## 🚀 快速开始

### 前置条件

- Python 3.8+（使用源码方式时）
- 安装 [Trae](https://trae.cn/) 或 [SOLO](https://solo.trae.cn/) 客户端（推荐）

### 使用方法

#### 方式一：使用 Skill 文件（推荐）

1. 下载 [astock-quant-analyzer.skill](https://github.com/laozdao/astock-quant-analyzer/releases/download/v1.0.0/astock-quant-analyzer.skill)
2. 在 Trae/SOLO 中导入 Skill
3. 直接使用：`分析一下贵州茅台`

#### 方式二：使用 Python 源码

```python
from src.analyzer import AStockQuantAnalyzer, MarketCondition

# 创建分析器实例
analyzer = AStockQuantAnalyzer(MarketCondition.OSCILLATION)

# 准备数据
fundamental_data = {
    'ep': 0.06,
    'pb': 2.0,
    'revenue_growth': 0.15,
    'profit_growth': 0.12,
    'roe': 0.12,
    # ... 更多数据
}

# 计算评分
fundamental_score = analyzer.calculate_fundamental_score(fundamental_data)
print(f"基本面评分: {fundamental_score.total_score}")
```

## 📐 模型架构

```
综合得分 = 基本面 × 60% + 量价 × 25% + 风险 × 15%
```

## 📁 项目结构

```
astock-quant-analyzer/
├── src/                      # 源码目录
│   ├── config.py            # 模型配置
│   ├── analyzer.py          # 核心分析引擎
│   └── __init__.py
├── skill/                    # SOLO Skill 文件
│   └── SKILL.md             # Skill 定义文件
├── docs/                     # 文档目录
│   └── architecture.md      # 架构设计文档
├── examples/                 # 示例
│   └── sample_report.md     # 示例分析报告
├── tests/                    # 测试
│   └── test_analyzer.py
├── README.md                 # 本文件
├── LICENSE                   # MIT 协议
└── requirements.txt          # 依赖
```

## 📄 开源协议

[MIT](LICENSE)

---

> ⚠️ **免责声明**：本 Skill 仅供学习交流使用，不构成任何投资建议。股市有风险，投资需谨慎。
