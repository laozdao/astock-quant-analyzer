"""
A股个股量化分析器

基于"双引擎四层"融合模型的专业级量化分析工具
"""

from .analyzer import (
    AStockQuantAnalyzer,
    MarketCondition,
    InvestmentRating,
    StockData,
    FundamentalScore,
    VolumePriceScore,
    RiskScore,
    AnalysisResult
)

from .config import (
    MODEL_WEIGHTS,
    FUNDAMENTAL_FACTORS,
    VOLUME_PRICE_DIMENSIONS,
    RISK_DIMENSIONS,
    INVESTMENT_RATINGS,
    SIGNAL_CONFLICT_RULES,
    CLASSIC_FRAMEWORKS
)

__version__ = "1.0.0"
__author__ = "laozdao"
__license__ = "MIT"

__all__ = [
    "AStockQuantAnalyzer",
    "MarketCondition",
    "InvestmentRating",
    "StockData",
    "FundamentalScore",
    "VolumePriceScore",
    "RiskScore",
    "AnalysisResult",
    "MODEL_WEIGHTS",
    "FUNDAMENTAL_FACTORS",
    "VOLUME_PRICE_DIMENSIONS",
    "RISK_DIMENSIONS",
    "INVESTMENT_RATINGS",
    "SIGNAL_CONFLICT_RULES",
    "CLASSIC_FRAMEWORKS"
]
