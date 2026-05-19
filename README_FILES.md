# 仓库文件说明

## 项目结构

```
astock-quant-analyzer/
├── src/                      # 核心源码
│   ├── __init__.py          # 包入口
│   ├── config.py            # 模型配置（评分标准/权重）
│   └── analyzer.py          # 分析引擎
├── skill/                    # SOLO Skill
│   └── SKILL.md             # 可导入 SOLO 的技能文件
├── docs/                     # 开发文档
│   └── architecture.md      # 架构设计文档
├── examples/                  # 使用示例
│   └── sample_report.md     # 完整分析报告示例
├── tests/                    # 单元测试
│   └── test_analyzer.py     # 测试用例
├── README.md                 # 项目主页
├── LICENSE                   # MIT 协议
└── requirements.txt         # 依赖清单
```

## 文件说明

### src/ - 核心源码

| 文件 | 说明 |
|------|------|
| `__init__.py` | 包入口，导出公开 API |
| `config.py` | 模型"参数配置表"，修改这里调整评分规则 |
| `analyzer.py` | 分析"执行者"，完成评分计算和报告生成 |

### skill/ - SOLO Skill

| 文件 | 说明 |
|------|------|
| `SKILL.md` | 可导入 SOLO 的技能文件，一句话触发分析 |

### docs/ - 开发文档

| 文件 | 说明 |
|------|------|
| `architecture.md` | 面向开发者的"技术蓝图" |

### examples/ - 使用示例

| 文件 | 说明 |
|------|------|
| `sample_report.md` | 以"贵州茅台"为案例的完整分析报告范本 |

### tests/ - 单元测试

| 文件 | 说明 |
|------|------|
| `test_analyzer.py` | 代码质量的"守护者"，确保评分逻辑正确 |

## 一句话总结

| 文件/目录 | 一句话描述 |
|-----------|-----------|
| `src/` | 量化分析引擎的"大脑"，包含所有评分算法 |
| `src/config.py` | 模型的"参数配置表" |
| `src/analyzer.py` | 量化分析的"执行者" |
| `skill/SKILL.md` | 一句话触发分析的技能文件 |
| `docs/architecture.md` | 面向开发者的"技术蓝图" |
| `examples/sample_report.md` | 茅台案例的"完整报告范本" |
| `tests/test_analyzer.py` | 代码质量的"守护者" |
| `README.md` | 仓库的"门面" |
| `LICENSE` | 法律保护的"盾牌" |
| `requirements.txt` | Python 依赖的"清单" |
