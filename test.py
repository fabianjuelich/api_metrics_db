import unittest
from src import indicator, fiscal, function, alphavantage

class TestIndicatorFunctions(unittest.TestCase):

    def test_dynamicReports(self):
        self.assertEqual(indicator.revenue_growth('IBM', fiscal.Fiscal.ANNUAL_REPORTS, '2022-12-31'), indicator.revenue_growth('IBM', fiscal.Fiscal.ANNUAL_REPORTS), indicator.revenue_growth('IBM'))
        self.assertEqual(indicator.revenue_growth('IBM', fiscal.Fiscal.QUARTERLY_REPORTS, '2022-12-31'), indicator.revenue_growth('IBM', fiscal.Fiscal.QUARTERLY_REPORTS))

class TestExceptions(unittest.TestCase):

    def test_invalidIndicator(self):
        self.assertRaises(Exception, alphavantage.alpha_vantage(function.Function.BALANCE_SHEET, "IBZ"))

    def test_invalidFiscalDateEnding(self):
        self.assertRaises(Exception, alphavantage.get_latest_report("IBM", function.Function.BALANCE_SHEET, fiscal.Fiscal.ANNUAL_REPORTS, fiscalDateEnding= '2022-08-31'))
