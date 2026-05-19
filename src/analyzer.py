"""
A股个股量化分析器 - 核心分析引擎
双引擎四层融合模型实现
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import json

from config import (
    MODEL_WEIGHTS, FUNDAMENTAL_FACTORS, VOLUME_PRICE_DIMENSIONS, RISK_DIMENSIONS,
    SCORING_CRITERIA, SIGNAL_ADJUSTMENTS, INVESTMENT_RATINGS, SIGNAL_CONFLICT_RULES,
    STOCK_CHARACTERISTICS_ADJUSTMENT, CLASSIC_FRAMEWORKS, NEWS_CATEGORIES
)


class MarketCondition(Enum):
    """市场环境"""
    BULL = "bull_market"
    OSCILLATION = "oscillation_market"
    BEAR = "bear_market"
    EXTREME = "extreme_market"


class InvestmentRating(Enum):
    """投资评级"""
    STRONG_BUY = "strong_buy"
    BUY = "buy"
    NEUTRAL = "neutral"
    CAUTIOUS = "cautious"
    AVOID = "avoid"


@dataclass
class StockData:
    """股票基础数据"""
    name: str
    code: str
    price: float
    market_cap: float
    industry: str
    concept_sectors: List[str]
    week_52_high: float
    week_52_low: float


@dataclass
class FundamentalScore:
    """基本面评分"""
    F1_value: float
    F2_growth: float
    F3_quality: float
    F4_momentum: float
    F5_sentiment: float
    F6_fund_flow: float
    F7_esg: float
    F8_alternative: float
    total_score: float
    rating: str


@dataclass
class VolumePriceScore:
    """量价评分"""
    V1_trend: float
    V2_volume_price_fit: float
    V3_key_position: float
    V4_main_force: float
    V5_volatility: float
    V6_multi_period: float
    total_score: float
    stage: str
    adjustments: int


@dataclass
class RiskScore:
    """风险评分"""
    R1_valuation: float
    R2_liquidity: float
    R3_downside: float
    R4_concentration: float
    total_score: float
    warning_level: str


@dataclass
class AnalysisResult:
    """分析结果"""
    stock_data: StockData
    fundamental: FundamentalScore
    volume_price: VolumePriceScore
    risk: RiskScore
    composite_score: float
    investment_rating: InvestmentRating
    recommended_action: str
    position_suggestion: str
    adapted_framework: Optional[str]
    signal_conflict: Optional[str]
    buy_timing: str
    sell_timing: str
    stop_loss: float
    target_price: float
    catalyst_factors: List[str]


class AStockQuantAnalyzer:
    """
    A股个股量化分析器
    
    基于"双引擎四层"融合模型：
    - 基本面引擎（60%）：八因子评分
    - 量价引擎（25%）：六维度评分
    - 风险引擎（15%）：四维度评分
    """
    
    def __init__(self, market_condition: MarketCondition = MarketCondition.OSCILLATION):
        self.market_condition = market_condition
        self.weights = MODEL_WEIGHTS[market_condition.value]
    
    def set_market_condition(self, condition: MarketCondition):
        """设置市场环境"""
        self.market_condition = condition
        self.weights = MODEL_WEIGHTS[condition.value]
    
    def calculate_fundamental_score(self, data: Dict) -> FundamentalScore:
        """
        计算基本面八因子评分
        
        Args:
            data: 包含各因子原始数据的字典
            
        Returns:
            FundamentalScore: 基本面评分结果
        """
        scores = {}
        
        # F1 价值因子
        scores['F1'] = self._score_f1_value(data.get('ep'), data.get('pb'), data.get('dividend_yield'))
        
        # F2 成长因子
        scores['F2'] = self._score_f2_growth(data.get('revenue_growth'), data.get('profit_growth'))
        
        # F3 质量因子
        scores['F3'] = self._score_f3_quality(data.get('roe'), data.get('gross_margin'), data.get('fcf'))
        
        # F4 动量因子
        scores['F4'] = self._score_f4_momentum(data.get('momentum_signals'))
        
        # F5 情绪因子
        scores['F5'] = self._score_f5_sentiment(data.get('sentiment_data'))
        
        # F6 资金流因子
        scores['F6'] = self._score_f6_fund_flow(data.get('fund_flow_data'))
        
        # F7 ESG因子
        scores['F7'] = self._score_f7_esg(data.get('esg_rating'))
        
        # F8 另类数据因子
        scores['F8'] = self._score_f8_alternative(data.get('alternative_data'))
        
        # 计算加权总分
        total = sum(
            scores[f'F{i}'] * FUNDAMENTAL_FACTORS[f'F{i}_{self._get_factor_name(i)}']
            for i in range(1, 9)
        ) / 0.60  # 归一化到10分制
        
        # 确定评级
        rating = self._get_fundamental_rating(total)
        
        return FundamentalScore(
            F1_value=scores['F1'],
            F2_growth=scores['F2'],
            F3_quality=scores['F3'],
            F4_momentum=scores['F4'],
            F5_sentiment=scores['F5'],
            F6_fund_flow=scores['F6'],
            F7_esg=scores['F7'],
            F8_alternative=scores['F8'],
            total_score=round(total, 2),
            rating=rating
        )
    
    def calculate_volume_price_score(self, data: Dict) -> VolumePriceScore:
        """
        计算量价六维度评分
        
        Args:
            data: 包含量价数据的字典
            
        Returns:
            VolumePriceScore: 量价评分结果
        """
        scores = {}
        
        # V1 趋势状态
        scores['V1'] = self._score_v1_trend(data.get('ma_alignment'), data.get('adx'))
        
        # V2 量价配合度
        scores['V2'] = self._score_v2_fit(data.get('volume_price_correlation'))
        
        # V3 关键位置
        scores['V3'] = self._score_v3_position(data.get('breakout_status'), data.get('volume_ratio'))
        
        # V4 主力行为
        scores['V4'] = self._score_v4_main_force(data.get('main_force_behavior'))
        
        # V5 波动率
        scores['V5'] = self._score_v5_volatility(data.get('volatility'))
        
        # V6 多周期共振
        scores['V6'] = self._score_v6_multi_period(data.get('multi_period_signals'))
        
        # 计算基础分
        base_score = sum(
            scores[f'V{i}'] * VOLUME_PRICE_DIMENSIONS[f'V{i}_{self._get_vp_dimension_name(i)}']
            for i in range(1, 7)
        ) / 0.25  # 归一化到10分制
        
        # 信号加减分
        adjustments = self._calculate_signal_adjustments(data.get('signals', []))
        
        # 最终得分（限制在0-10）
        final_score = max(0, min(10, base_score + adjustments))
        
        # 识别量价阶段
        stage = self._identify_vp_stage(final_score, data)
        
        return VolumePriceScore(
            V1_trend=scores['V1'],
            V2_volume_price_fit=scores['V2'],
            V3_key_position=scores['V3'],
            V4_main_force=scores['V4'],
            V5_volatility=scores['V5'],
            V6_multi_period=scores['V6'],
            total_score=round(final_score, 2),
            stage=stage,
            adjustments=adjustments
        )
    
    def calculate_risk_score(self, data: Dict) -> RiskScore:
        """
        计算风险四维度评分
        
        Args:
            data: 包含风险数据的字典
            
        Returns:
            RiskScore: 风险评分结果
        """
        scores = {}
        
        # R1 估值风险
        scores['R1'] = self._score_r1_valuation(data.get('pe_percentile'))
        
        # R2 流动性风险
        scores['R2'] = self._score_r2_liquidity(data.get('avg_turnover'), data.get('turnover_rate'))
        
        # R3 下行风险
        scores['R3'] = self._score_r3_downside(data.get('max_drawdown'))
        
        # R4 集中度风险
        scores['R4'] = self._score_r4_concentration(data.get('concentration_data'))
        
        # 计算加权总分
        total = sum(
            scores[f'R{i}'] * RISK_DIMENSIONS[f'R{i}_{self._get_risk_dimension_name(i)}']
            for i in range(1, 5)
        ) / 0.15  # 归一化到10分制
        
        # 确定预警级别
        warning_level = self._get_risk_warning_level(total)
        
        return RiskScore(
            R1_valuation=scores['R1'],
            R2_liquidity=scores['R2'],
            R3_downside=scores['R3'],
            R4_concentration=scores['R4'],
            total_score=round(total, 2),
            warning_level=warning_level
        )
    
    def detect_signal_conflict(self, fundamental_score: float, vp_score: float) -> Optional[str]:
        """
        检测信号冲突
        
        Returns:
            冲突类型描述，无冲突返回None
        """
        if fundamental_score >= 7.0 and vp_score <= 4.0:
            return "基本面强+量价弱：可能是价值陷阱，等待量价改善"
        elif fundamental_score <= 4.0 and vp_score >= 7.0:
            return "基本面弱+量价强：警惕垃圾股反弹，严格止损"
        elif fundamental_score <= 4.0 and vp_score <= 4.0:
            return "双弱信号：坚决回避"
        elif fundamental_score >= 7.0 and vp_score >= 7.0:
            return "双强信号：最佳机会"
        return None
    
    def calculate_composite_score(
        self, 
        fundamental: FundamentalScore, 
        volume_price: VolumePriceScore, 
        risk: RiskScore
    ) -> float:
        """
        计算综合得分
        
        综合得分 = 基本面×权重 + 量价×权重 + 风险×权重
        """
        composite = (
            fundamental.total_score * self.weights['fundamental'] +
            volume_price.total_score * self.weights['volume_price'] +
            risk.total_score * self.weights['risk']
        )
        return round(composite, 2)
    
    def get_investment_rating(self, composite_score: float) -> Tuple[InvestmentRating, str, str]:
        """
        获取投资评级
        
        Returns:
            (评级枚举, 操作建议, 建议仓位)
        """
        for rating_key, rating_info in INVESTMENT_RATINGS.items():
            if rating_info['min_score'] <= composite_score <= rating_info['max_score']:
                rating_enum = InvestmentRating(rating_key)
                return rating_enum, rating_info['action'], rating_info['position']
        return InvestmentRating.AVOID, "不参与", "0%"
    
    def adapt_framework(self, fundamental: FundamentalScore, volume_price: VolumePriceScore) -> Optional[str]:
        """
        适配经典投资框架
        
        Returns:
            适配的框架名称，无适配返回None
        """
        frameworks = []
        
        # 价值选股模型
        if fundamental.F1_value >= 8.0 and fundamental.F3_quality >= 7.0:
            frameworks.append("价值选股模型")
        
        # 成长股PEG模型
        if fundamental.F2_growth >= 8.0 and fundamental.F8_alternative >= 7.0:
            frameworks.append("成长股PEG模型")
        
        # 动量趋势模型
        if volume_price.V1_trend >= 8.0 and volume_price.V6_multi_period >= 7.0:
            frameworks.append("动量趋势模型")
        
        # 困境反转模型
        if 5.0 <= fundamental.total_score <= 6.5:
            # 需要检查F2是否边际改善，这里简化处理
            frameworks.append("困境反转模型")
        
        return "、".join(frameworks) if frameworks else None
    
    def generate_trading_suggestions(
        self, 
        rating: InvestmentRating,
        conflict: Optional[str],
        stock_data: StockData
    ) -> Dict[str, str]:
        """生成交易建议"""
        suggestions = {
            'buy_timing': '',
            'sell_timing': '',
            'stop_loss': '',
            'target_price': '',
            'position': ''
        }
        
        # 根据评级生成建议
        if rating == InvestmentRating.STRONG_BUY:
            suggestions['buy_timing'] = '回调至支撑位附近积极买入'
            suggestions['sell_timing'] = '放量滞涨或跌破关键支撑位'
            suggestions['stop_loss'] = f"{stock_data.price * 0.92:.2f}元（-8%）"
            suggestions['target_price'] = f"{stock_data.price * 1.20:.2f}元（+20%）"
            suggestions['position'] = '80-100%'
        elif rating == InvestmentRating.BUY:
            suggestions['buy_timing'] = '回调至均线附近分批买入'
            suggestions['sell_timing'] = '放量滞涨或跌破止损位'
            suggestions['stop_loss'] = f"{stock_data.price * 0.90:.2f}元（-10%）"
            suggestions['target_price'] = f"{stock_data.price * 1.15:.2f}元（+15%）"
            suggestions['position'] = '60-80%'
        elif rating == InvestmentRating.NEUTRAL:
            suggestions['buy_timing'] = '观望，等待明确信号'
            suggestions['sell_timing'] = '持有或减仓'
            suggestions['stop_loss'] = f"{stock_data.price * 0.88:.2f}元（-12%）"
            suggestions['target_price'] = '待定'
            suggestions['position'] = '20-40%'
        else:
            suggestions['buy_timing'] = '不建议买入'
            suggestions['sell_timing'] = '如有持仓，考虑减仓'
            suggestions['stop_loss'] = 'N/A'
            suggestions['target_price'] = 'N/A'
            suggestions['position'] = '0-20%'
        
        # 根据信号冲突调整
        if conflict and '量价弱' in conflict:
            suggestions['position'] = '不超过50%'
        elif conflict and '量价强' in conflict:
            suggestions['position'] = '不超过20%，严格止损'
        
        return suggestions
    
    # ========== 私有辅助方法 ==========
    
    def _score_f1_value(self, ep: Optional[float], pb: Optional[float], dividend: Optional[float]) -> float:
        """F1 价值因子评分"""
        if ep and ep > 0.08:
            return 9.0
        elif pb and pb < 1.5:
            return 9.0
        elif dividend and dividend > 0.04:
            return 9.0
        elif ep and ep > 0.05:
            return 7.5
        elif ep and ep > 0.02:
            return 5.5
        else:
            return 3.0
    
    def _score_f2_growth(self, revenue_growth: Optional[float], profit_growth: Optional[float]) -> float:
        """F2 成长因子评分"""
        if revenue_growth and profit_growth:
            if revenue_growth > 0.20 and profit_growth > 0.20:
                return 9.0
            elif revenue_growth > 0.10 and profit_growth > 0.10:
                return 7.5
            elif revenue_growth > 0 and profit_growth > 0:
                return 5.5
        return 3.0
    
    def _score_f3_quality(self, roe: Optional[float], gross_margin: Optional[float], fcf: Optional[float]) -> float:
        """F3 质量因子评分"""
        score = 5.0
        if roe:
            if roe > 0.15:
                score += 2.0
            elif roe > 0.10:
                score += 1.0
            elif roe < 0.05:
                score -= 2.0
        
        if gross_margin and gross_margin > 0.30:
            score += 1.0
        
        if fcf and fcf > 0:
            score += 1.0
        
        return min(10.0, max(1.0, score))
    
    def _score_f4_momentum(self, momentum_signals: Optional[Dict]) -> float:
        """F4 动量因子评分"""
        if not momentum_signals:
            return 5.0
        # 简化实现
        return 7.0
    
    def _score_f5_sentiment(self, sentiment_data: Optional[Dict]) -> float:
        """F5 情绪因子评分"""
        if not sentiment_data:
            return 5.0
        # 简化实现
        return 6.0
    
    def _score_f6_fund_flow(self, fund_flow_data: Optional[Dict]) -> float:
        """F6 资金流因子评分"""
        if not fund_flow_data:
            return 5.0
        # 简化实现
        return 6.0
    
    def _score_f7_esg(self, esg_rating: Optional[str]) -> float:
        """F7 ESG因子评分"""
        rating_map = {'AA': 9.0, 'A': 7.5, 'BBB': 5.5, 'BB': 3.0}
        return rating_map.get(esg_rating, 5.0)
    
    def _score_f8_alternative(self, alternative_data: Optional[Dict]) -> float:
        """F8 另类数据因子评分"""
        if not alternative_data:
            return 5.0
        # 简化实现
        return 6.0
    
    def _score_v1_trend(self, ma_alignment: Optional[str], adx: Optional[float]) -> float:
        """V1 趋势状态评分"""
        if ma_alignment == 'bull' and adx and adx > 25:
            return 9.0
        elif ma_alignment == 'bull':
            return 7.5
        elif ma_alignment == 'bear':
            return 3.0
        return 5.0
    
    def _score_v2_fit(self, correlation: Optional[float]) -> float:
        """V2 量价配合度评分"""
        if correlation and correlation > 0.8:
            return 9.0
        elif correlation and correlation > 0.6:
            return 7.5
        elif correlation and correlation > 0.4:
            return 5.5
        return 3.0
    
    def _score_v3_position(self, breakout_status: Optional[str], volume_ratio: Optional[float]) -> float:
        """V3 关键位置评分"""
        if breakout_status == 'breakout' and volume_ratio and volume_ratio > 1.5:
            return 9.0
        elif breakout_status == 'breakout':
            return 7.5
        elif breakout_status == 'breakdown':
            return 3.0
        return 5.0
    
    def _score_v4_main_force(self, behavior: Optional[str]) -> float:
        """V4 主力行为评分"""
        if behavior == 'accumulating':
            return 8.0
        elif behavior == 'distributing':
            return 3.0
        return 5.0
    
    def _score_v5_volatility(self, volatility: Optional[float]) -> float:
        """V5 波动率评分"""
        if volatility and volatility < 0.20:
            return 8.0
        elif volatility and volatility < 0.30:
            return 6.0
        elif volatility and volatility > 0.50:
            return 3.0
        return 5.0
    
    def _score_v6_multi_period(self, signals: Optional[List]) -> float:
        """V6 多周期共振评分"""
        if not signals:
            return 5.0
        # 简化实现
        return 7.0
    
    def _score_r1_valuation(self, pe_percentile: Optional[float]) -> float:
        """R1 估值风险评分"""
        if pe_percentile and pe_percentile < 0.30:
            return 9.0
        elif pe_percentile and pe_percentile < 0.50:
            return 7.5
        elif pe_percentile and pe_percentile < 0.70:
            return 5.5
        return 3.0
    
    def _score_r2_liquidity(self, avg_turnover: Optional[float], turnover_rate: Optional[float]) -> float:
        """R2 流动性风险评分"""
        if avg_turnover and avg_turnover > 100000000 and turnover_rate and turnover_rate > 0.005:
            return 9.0
        elif avg_turnover and avg_turnover > 50000000:
            return 7.5
        elif avg_turnover and avg_turnover > 20000000:
            return 5.5
        return 3.0
    
    def _score_r3_downside(self, max_drawdown: Optional[float]) -> float:
        """R3 下行风险评分"""
        if max_drawdown and max_drawdown < 0.10:
            return 9.0
        elif max_drawdown and max_drawdown < 0.20:
            return 7.5
        elif max_drawdown and max_drawdown < 0.30:
            return 5.5
        return 3.0
    
    def _score_r4_concentration(self, concentration_data: Optional[Dict]) -> float:
        """R4 集中度风险评分"""
        if not concentration_data:
            return 5.0
        # 简化实现
        return 6.0
    
    def _calculate_signal_adjustments(self, signals: List[str]) -> int:
        """计算信号加减分"""
        adjustment = 0
        for signal in signals:
            if signal in SIGNAL_ADJUSTMENTS['healthy']:
                adjustment += SIGNAL_ADJUSTMENTS['healthy'][signal]
            elif signal in SIGNAL_ADJUSTMENTS['dangerous']:
                adjustment += SIGNAL_ADJUSTMENTS['dangerous'][signal]
        return adjustment
    
    def _identify_vp_stage(self, score: float, data: Dict) -> str:
        """识别量价阶段"""
        if score >= 8.0:
            return "上升期"
        elif score <= 3.0:
            return "下降期"
        elif data.get('volume') == 'low' and score > 5.0:
            return "底部"
        elif data.get('volume') == 'high' and score < 5.0:
            return "顶部"
        return "震荡期"
    
    def _get_fundamental_rating(self, score: float) -> str:
        """获取基本面评级"""
        if score >= 8.0:
            return "A+"
        elif score >= 7.0:
            return "A"
        elif score >= 6.0:
            return "B+"
        elif score >= 5.0:
            return "B"
        elif score >= 4.0:
            return "C"
        return "D"
    
    def _get_risk_warning_level(self, score: float) -> str:
        """获取风险预警级别"""
        if score >= 8.0:
            return "安全"
        elif score >= 6.0:
            return "正常"
        elif score >= 4.0:
            return "警告"
        return "危险"
    
    def _get_factor_name(self, index: int) -> str:
        """获取因子名称"""
        names = ['', 'value', 'growth', 'quality', 'momentum', 'sentiment', 'fund_flow', 'esg', 'alternative']
        return names[index]
    
    def _get_vp_dimension_name(self, index: int) -> str:
        """获取量价维度名称"""
        names = ['', 'trend', 'volume_price_fit', 'key_position', 'main_force', 'volatility', 'multi_period']
        return names[index]
    
    def _get_risk_dimension_name(self, index: int) -> str:
        """获取风险维度名称"""
        names = ['', 'valuation', 'liquidity', 'downside', 'concentration']
        return names[index]


# 使用示例
if __name__ == "__main__":
    # 创建分析器实例
    analyzer = AStockQuantAnalyzer(MarketCondition.OSCILLATION)
    
    # 示例数据
    fundamental_data = {
        'ep': 0.06,
        'pb': 2.0,
        'dividend_yield': 0.03,
        'revenue_growth': 0.15,
        'profit_growth': 0.12,
        'roe': 0.12,
        'gross_margin': 0.35,
        'fcf': 100000000,
        'momentum_signals': {'trend': 'up'},
        'sentiment_data': {'positive': True},
        'fund_flow_data': {'inflow': True},
        'esg_rating': 'A',
        'alternative_data': {'positive': True}
    }
    
    vp_data = {
        'ma_alignment': 'bull',
        'adx': 30,
        'volume_price_correlation': 0.75,
        'breakout_status': 'breakout',
        'volume_ratio': 1.8,
        'main_force_behavior': 'accumulating',
        'volatility': 0.25,
        'multi_period_signals': ['daily_up', 'weekly_up'],
        'signals': ['price_up_volume_up', 'huge_volume_breakout']
    }
    
    risk_data = {
        'pe_percentile': 0.45,
        'avg_turnover': 80000000,
        'turnover_rate': 0.008,
        'max_drawdown': 0.15,
        'concentration_data': {'diversified':