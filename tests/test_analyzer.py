"""
A股个股量化分析器 - 单元测试
"""

import unittest
from src.analyzer import (
    AStockQuantAnalyzer,
    MarketCondition,
    InvestmentRating,
    StockData
)


class TestAStockQuantAnalyzer(unittest.TestCase):
    """测试 AStockQuantAnalyzer 类"""
    
    def setUp(self):
        """测试前准备"""
        self.analyzer = AStockQuantAnalyzer(MarketCondition.OSCILLATION)
    
    def test_initialization(self):
        """测试初始化"""
        self.assertEqual(self.analyzer.market_condition, MarketCondition.OSCILLATION)
        self.assertEqual(self.analyzer.weights['fundamental'], 0.60)
        self.assertEqual(self.analyzer.weights['volume_price'], 0.25)
        self.assertEqual(self.analyzer.weights['risk'], 0.15)
    
    def test_set_market_condition(self):
        """测试市场环境切换"""
        self.analyzer.set_market_condition(MarketCondition.BULL)
        self.assertEqual(self.analyzer.weights['fundamental'], 0.50)
        self.assertEqual(self.analyzer.weights['volume_price'], 0.35)
        
        self.analyzer.set_market_condition(MarketCondition.BEAR)
        self.assertEqual(self.analyzer.weights['fundamental'], 0.70)
        self.assertEqual(self.analyzer.weights['volume_price'], 0.15)
    
    def test_fundamental_scoring(self):
        """测试基本面评分"""
        data = {
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
        
        score = self.analyzer.calculate_fundamental_score(data)
        
        self.assertIsNotNone(score)
        self.assertGreaterEqual(score.total_score, 0)
        self.assertLessEqual(score.total_score, 10)
        self.assertIn(score.rating, ['A+', 'A', 'B+', 'B', 'C', 'D'])
    
    def test_volume_price_scoring(self):
        """测试量价评分"""
        data = {
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
        
        score = self.analyzer.calculate_volume_price_score(data)
        
        self.assertIsNotNone(score)
        self.assertGreaterEqual(score.total_score, 0)
        self.assertLessEqual(score.total_score, 10)
        self.assertIn(score.stage, ['上升期', '下降期', '底部', '顶部', '震荡期'])
    
    def test_risk_scoring(self):
        """测试风险评分"""
        data = {
            'pe_percentile': 0.45,
            'avg_turnover': 80000000,
            'turnover_rate': 0.008,
            'max_drawdown': 0.15,
            'concentration_data': {'diversified': True}
        }
        
        score = self.analyzer.calculate_risk_score(data)
        
        self.assertIsNotNone(score)
        self.assertGreaterEqual(score.total_score, 0)
        self.assertLessEqual(score.total_score, 10)
        self.assertIn(score.warning_level, ['安全', '正常', '警告', '危险'])
    
    def test_signal_conflict_detection(self):
        """测试信号冲突检测"""
        # 双强
        conflict = self.analyzer.detect_signal_conflict(8.0, 8.0)
        self.assertIn('双强', conflict)
        
        # 双弱
        conflict = self.analyzer.detect_signal_conflict(3.0, 3.0)
        self.assertIn('双弱', conflict)
        
        # 基本面强+量价弱
        conflict = self.analyzer.detect_signal_conflict(8.0, 3.0)
        self.assertIn('量价弱', conflict)
        
        # 基本面弱+量价强
        conflict = self.analyzer.detect_signal_conflict(3.0, 8.0)
        self.assertIn('量价强', conflict)
        
        # 无冲突
        conflict = self.analyzer.detect_signal_conflict(6.0, 6.0)
        self.assertIsNone(conflict)
    
    def test_investment_rating(self):
        """测试投资评级"""
        # 强烈推荐
        rating, action, position = self.analyzer.get_investment_rating(9.0)
        self.assertEqual(rating, InvestmentRating.STRONG_BUY)
        
        # 推荐
        rating, action, position = self.analyzer.get_investment_rating(7.5)
        self.assertEqual(rating, InvestmentRating.BUY)
        
        # 中性
        rating, action, position = self.analyzer.get_investment_rating(6.0)
        self.assertEqual(rating, InvestmentRating.NEUTRAL)
        
        # 回避
        rating, action, position = self.analyzer.get_investment_rating(3.0)
        self.assertEqual(rating, InvestmentRating.AVOID)
    
    def test_framework_adaptation(self):
        """测试框架适配"""
        from src.analyzer import FundamentalScore, VolumePriceScore
        
        # 价值选股模型
        fundamental = FundamentalScore(
            F1_value=8.5, F2_growth=6.0, F3_quality=7.5,
            F4_momentum=6.0, F5_sentiment=6.0, F6_fund_flow=6.0,
            F7_esg=6.0, F8_alternative=6.0, total_score=7.0, rating='A'
        )
        vp = VolumePriceScore(
            V1_trend=6.0, V2_volume_price_fit=6.0, V3_key_position=6.0,
            V4_main_force=6.0, V5_volatility=6.0, V6_multi_period=6.0,
            total_score=6.0, stage='震荡期', adjustments=0
        )
        
        frameworks = self.analyzer.adapt_framework(fundamental, vp)
        self.assertIn('价值选股模型', frameworks)
    
    def test_composite_score_calculation(self):
        """测试综合得分计算"""
        from src.analyzer import FundamentalScore, VolumePriceScore, RiskScore
        
        fundamental = FundamentalScore(
            F1_value=7.0, F2_growth=7.0, F3_quality=7.0,
            F4_momentum=7.0, F5_sentiment=7.0, F6_fund_flow=7.0,
            F7_esg=7.0, F8_alternative=7.0, total_score=7.0, rating='A'
        )
        vp = VolumePriceScore(
            V1_trend=7.0, V2_volume_price_fit=7.0, V3_key_position=7.0,
            V4_main_force=7.0, V5_volatility=7.0, V6_multi_period=7.0,
            total_score=7.0, stage='震荡期', adjustments=0
        )
        risk = RiskScore(
            R1_valuation=7.0, R2_liquidity=7.0, R3_downside=7.0,
            R4_concentration=7.0, total_score=7.0, warning_level='正常'
        )
        
        composite = self.analyzer.calculate_composite_score(fundamental, vp, risk)
        
        # 震荡市权重：60% + 25% + 15%
        expected = 7.0 * 0.60 + 7.0 * 0.25 + 7.0 * 0.15
        self.assertAlmostEqual(composite, expected, places=2)


class TestConfig(unittest.TestCase):
    """测试配置文件"""
    
    def test_model_weights(self):
        """测试模型权重配置"""
        from src.config import MODEL_WEIGHTS
        
        for market, weights in MODEL_WEIGHTS.items():
            total = weights['fundamental'] + weights['volume_price'] + weights['risk']
            self.assertAlmostEqual(total, 1.0, places=2)
    
    def test_fundamental_factors(self):
        """测试基本面因子权重"""
        from src.config import FUNDAMENTAL_FACTORS
        
        total = sum(FUNDAMENTAL_FACTORS.values())
        self.assertAlmostEqual(total, 1.0, places=2)
    
    def test_volume_price_dimensions(self):
        """测试量价维度权重"""
        from src.config import VOLUME_PRICE_DIMENSIONS
        
        total = sum(VOLUME_PRICE_DIMENSIONS.values())
        self.assertAlmostEqual(total, 1.0, places=2)
    
    def test_risk_dimensions(self):
        """测试风险维度权重"""
        from src.config import RISK_DIMENSIONS
        
        total = sum(RISK_DIMENSIONS.values())
        self.assertAlmostEqual(total, 1.0, places=2)


if __name__ == '__main__':
    unittest.main()
