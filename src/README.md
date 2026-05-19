# src/ 目录说明

## 核心源码目录

本目录包含 A股量化分析器的核心实现代码，是项目的"大脑"。

## 文件说明

### `__init__.py`
**作用**：Python 包初始化文件  
**功能**：
- 导出核心类和配置，方便外部调用
- 定义公开 API 接口
- 设置版本信息（当前 v1.0.0）

**使用示例**：
```python
from src import AStockQuantAnalyzer, MarketCondition
```

---

### `config.py`
**作用**：模型配置中心  
**功能**：
- 四种市场环境权重配置（牛市/震荡/熊市/极端）
- 基本面八因子评分标准（F1-F8）
- 量价六维度评分标准（V1-V6）
- 风险四维度评分标准（R1-R4）
- 信号加减分规则
- 投资评级阈值

**特点**：
> 修改此文件即可自定义评分规则，无需改动核心算法

---

### `analyzer.py`
**作用**：量化分析引擎  
**功能**：
- `AStockQuantAnalyzer` 类：主分析器
- 基本面八因子评分计算
- 量价六维度评分计算
- 风险四维度评分计算
- 信号冲突检测（基本面 vs 量价）
- 综合得分计算与评级生成
- 经典投资框架适配
- 买卖时机与仓位建议

**核心方法**：
- `calculate_fundamental_score()` - 基本面评分
- `calculate_volume_price_score()` - 量价评分
- `calculate_risk_score()` - 风险评分
- `detect_signal_conflict()` - 信号冲突检测
- `get_investment_rating()` - 投资评级

---

## 架构关系

```
config.py (配置) ← analyzer.py (引擎) ← __init__.py (入口)
     ↓                    ↓
  评分标准            计算逻辑
```
