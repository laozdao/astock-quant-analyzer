# tests/ 目录说明

## 单元测试目录

本目录包含自动化测试用例，确保代码质量。

## 文件说明

### `test_analyzer.py`
**作用**：自动化测试套件  
**框架**：Python unittest

**测试覆盖**：

#### TestAStockQuantAnalyzer 类
| 测试方法 | 测试内容 |
|----------|----------|
| `test_initialization` | 初始化和默认权重配置 |
| `test_set_market_condition` | 市场环境切换 |
| `test_fundamental_scoring` | 基本面八因子评分计算 |
| `test_volume_price_scoring` | 量价六维度评分计算 |
| `test_risk_scoring` | 风险四维度评分计算 |
| `test_signal_conflict_detection` | 信号冲突检测逻辑 |
| `test_investment_rating` | 投资评级生成 |
| `test_framework_adaptation` | 经典框架适配 |
| `test_composite_score_calculation` | 综合得分计算 |

#### TestConfig 类
| 测试方法 | 测试内容 |
|----------|----------|
| `test_model_weights` | 模型权重配置验证 |
| `test_fundamental_factors` | 基本面因子权重验证 |
| `test_volume_price_dimensions` | 量价维度权重验证 |
| `test_risk_dimensions` | 风险维度权重验证 |

**运行方式**：
```bash
cd tests
python -m pytest test_analyzer.py
# 或
python -m unittest test_analyzer
```

**质量保障**：
- 确保评分逻辑正确性
- 防止回归错误
- 验证配置参数有效性
