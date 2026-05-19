"""
A股个股量化分析器 - 配置文件
双引擎四层融合模型配置
"""

# 模型权重配置
MODEL_WEIGHTS = {
    "bull_market": {      # 牛市
        "fundamental": 0.50,
        "volume_price": 0.35,
        "risk": 0.15
    },
    "oscillation_market": {  # 震荡市（默认）
        "fundamental": 0.60,
        "volume_price": 0.25,
        "risk": 0.15
    },
    "bear_market": {      # 熊市
        "fundamental": 0.70,
        "volume_price": 0.15,
        "risk": 0.15
    },
    "extreme_market": {   # 极端行情
        "fundamental": 0.40,
        "volume_price": 0.10,
        "risk": 0.50
    }
}

# 基本面八因子权重
FUNDAMENTAL_FACTORS = {
    "F1_value": 0.15,           # 价值因子
    "F2_growth": 0.15,          # 成长因子
    "F3_quality": 0.15,         # 质量因子
    "F4_momentum": 0.10,        # 动量因子
    "F5_sentiment": 0.10,       # 情绪因子
    "F6_fund_flow": 0.10,       # 资金流因子
    "F7_esg": 0.10,             # ESG因子
    "F8_alternative": 0.15      # 另类数据因子
}

# 量价六维度权重
VOLUME_PRICE_DIMENSIONS = {
    "V1_trend": 0.25,           # 趋势状态
    "V2_volume_price_fit": 0.20, # 量价配合度
    "V3_key_position": 0.20,    # 关键位置
    "V4_main_force": 0.15,      # 主力行为
    "V5_volatility": 0.10,      # 波动率
    "V6_multi_period": 0.10     # 多周期共振
}

# 风险四维度权重
RISK_DIMENSIONS = {
    "R1_valuation": 0.25,       # 估值风险
    "R2_liquidity": 0.25,       # 流动性风险
    "R3_downside": 0.25,        # 下行风险
    "R4_concentration": 0.25    # 集中度风险
}

# 评分标准 (0-10分制)
SCORING_CRITERIA = {
    "fundamental": {
        "F1_value": {
            "excellent": "EP>8% 或 PB<1.5 或 股息率>4%",
            "good": "EP 5-8%",
            "average": "EP 2-5%",
            "poor": "EP<2%"
        },
        "F2_growth": {
            "excellent": "营收+利润增速均>20%",
            "good": ">10%",
            "average": ">0%",
            "poor": "负增长"
        },
        "F3_quality": {
            "excellent": "ROE>15% + 毛利率>30% + FCF为正",
            "good": "ROE>10%",
            "average": "ROE>5%",
            "poor": "ROE<5%"
        },
        "F4_momentum": {
            "excellent": "多周期动量共振向上",
            "good": "中长周期向上",
            "average": "震荡",
            "poor": "多周期向下"
        },
        "F5_sentiment": {
            "excellent": "舆情正面 + 分析师上调 + 板块利好",
            "good": "偏正面",
            "average": "中性",
            "poor": "负面"
        },
        "F6_fund_flow": {
            "excellent": "主力持续净流入 + 北向增持",
            "good": "偏正面",
            "average": "中性",
            "poor": "持续流出"
        },
        "F7_esg": {
            "excellent": "AA以上",
            "good": "A",
            "average": "BBB",
            "poor": "BB以下"
        },
        "F8_alternative": {
            "excellent": "多维度正面信号 + 消息面催化",
            "good": "部分正面",
            "average": "中性",
            "poor": "负面"
        }
    },
    "volume_price": {
        "V1_trend": {
            "excellent": "多头排列 + ADX>25",
            "good": "多头排列",
            "average": "震荡",
            "poor": "空头排列"
        },
        "V2_volume_price_fit": {
            "excellent": "配合度>80%",
            "good": "60-80%",
            "average": "40-60%",
            "poor": "<40%"
        },
        "V3_key_position": {
            "excellent": "放量突破 + 量比>1.5",
            "good": "温和突破",
            "average": "位置中性",
            "poor": "破位下跌"
        },
        "V4_main_force": {
            "excellent": "吸筹/控盘 + 资金流入",
            "good": "偏正面",
            "average": "中性",
            "poor": "主力派发"
        },
        "V5_volatility": {
            "excellent": "低波动 + 趋势稳定",
            "good": "波动适中",
            "average": "波动偏高",
            "poor": "极端波动"
        },
        "V6_multi_period": {
            "excellent": "三周期共振",
            "good": "两周期间一致",
            "average": "单周期信号",
            "poor": "多周期矛盾"
        }
    },
    "risk": {
        "R1_valuation": {
            "excellent": "低于历史30分位",
            "good": "30-50分位",
            "average": "50-70分位",
            "poor": ">70分位"
        },
        "R2_liquidity": {
            "excellent": "日均成交额>1亿 + 换手率>0.5%",
            "good": ">5000万",
            "average": ">2000万",
            "poor": "<2000万"
        },
        "R3_downside": {
            "excellent": "最大回撤<10%",
            "good": "<20%",
            "average": "<30%",
            "poor": ">30%"
        },
        "R4_concentration": {
            "excellent": "分散度高 + 无极端暴露",
            "good": "适度集中",
            "average": "单一行业>40%",
            "poor": "极端集中"
        }
    }
}

# 量价信号加减分
SIGNAL_ADJUSTMENTS = {
    "healthy": {
        "price_up_volume_up": 2,        # 价涨量增
        "huge_volume_breakout": 2,       # 巨量突破
        "low_volume_then_surge": 3,      # 地量后放量
        "wash_then_surge": 2,            # 缩量洗盘后再放量
        "multi_period_bull": 2           # 多周期多头
    },
    "dangerous": {
        "price_up_volume_down": -2,      # 价涨量缩
        "decline_volume_up": -3,         # 下跌放量
        "high_stagnation_volume": -3,    # 高位滞涨放量
        "top_divergence": -3,            # 顶背离
        "multi_period_bear": -2          # 多周期空头
    }
}

# 投资评级标准
INVESTMENT_RATINGS = {
    "strong_buy": {"min_score": 8.5, "max_score": 10.0, "action": "积极买入", "position": "80-100%"},
    "buy": {"min_score": 7.0, "max_score": 8.4, "action": "逢低买入", "position": "60-80%"},
    "neutral": {"min_score": 5.5, "max_score": 6.9, "action": "观望等待", "position": "20-40%"},
    "cautious": {"min_score": 4.0, "max_score": 5.4, "action": "回避", "position": "0-20%"},
    "avoid": {"min_score": 0.0, "max_score": 3.9, "action": "不参与", "position": "0%"}
}

# 信号冲突处理规则
SIGNAL_CONFLICT_RULES = {
    "strong_fundamental_weak_vp": {
        "condition": "基本面>=7.0 且 量价<=4.0",
        "action": "以基本面为准，等待量价改善",
        "position_limit": "50%"
    },
    "weak_fundamental_strong_vp": {
        "condition": "基本面<=4.0 且 量价>=7.0",
        "action": "警惕垃圾股反弹",
        "position_limit": "20%"
    },
    "double_weak": {
        "condition": "基本面<=4.0 且 量价<=4.0",
        "action": "回避，不参与",
        "position_limit": "0%"
    },
    "double_strong": {
        "condition": "基本面>=7.0 且 量价>=7.0",
        "action": "最佳机会，可满仓参与",
        "position_limit": "100%"
    }
}

# 个股特征调整
STOCK_CHARACTERISTICS_ADJUSTMENT = {
    "large_cap": {          # 大盘蓝筹 (>1000亿)
        "fundamental": 0.05,
        "volume_price": -0.05
    },
    "small_mid_cap": {      # 中小盘 (<200亿)
        "volume_price": 0.05,
        "risk": 0.05,
        "fundamental": -0.10
    },
    "high_volatility": {    # 高波动 (年化>40%)
        "risk": 0.10,
        "fundamental": -0.10
    }
}

# 经典框架适配规则
CLASSIC_FRAMEWORKS = {
    "value_stock_picking": {
        "name": "价值选股模型",
        "condition": "F1>=8.0 且 F3>=7.0"
    },
    "distressed_reversal": {
        "name": "困境反转模型",
        "condition": "F2边际改善 且 综合得分5.0-6.5"
    },
    "growth_peg": {
        "name": "成长股PEG模型",
        "condition": "F2>=8.0 且 F8>=7.0"
    },
    "momentum_trend": {
        "name": "动量趋势模型",
        "condition": "V1>=8.0 且 V6>=7.0"
    }
}

# 行业调整规则
INDUSTRY_ADJUSTMENTS = {
    "tech_gaming": {        # 科技股/游戏股
        "pe_tolerance": 1.30  # PE可上浮30%
    }
}

# 板块评分标准
SECTOR_SCORING = {
    "industry_prosperity": {
        "excellent": "行业处于上升周期+政策强力支持",
        "good": "行业稳定增长",
        "average": "行业成熟/增速放缓",
        "poor": "行业衰退/政策打压"
    },
    "concept_heat": {
        "excellent": "多个核心概念+高热度+有持续性",
        "good": "1-2个核心概念+中等热度",
        "average": "概念关联度一般",
        "poor": "纯蹭概念+短期炒作"
    }
}

# 消息面评分标准
NEWS_SCORING = {
    "excellent": "多条实质性利好叠加（业绩超预期+回购+政策支持），催化效应极强",
    "good": "有1-2条实质性利好，消息面整体偏正面",
    "average": "消息面中性，无明显利好或利空",
    "poor": "存在利空消息（减持、业绩下滑、诉讼等），需警惕",
    "dangerous": "重大利空（财务造假、监管处罚、实控人风险等），强烈回避"
}

# 消息类型分类
NEWS_CATEGORIES = [
    "业绩相关",      # 业绩预告/快报、年报/季报
    "资本运作",      # 定增、回购、减持、股权激励
    "产品/业务",     # 新产品发布、重大订单
    "政策相关",      # 行业政策、监管变化
    "管理层",        # 高管变动、股权变更
    "风险事件",      # 诉讼、处罚、监管函
    "机构动向",      # 机构调研、券商研报
    "市场热点"       # 概念炒作、板块轮动
]
