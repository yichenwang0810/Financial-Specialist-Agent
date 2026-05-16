import unittest
from financial_specialist_agent.agent import FinancialSpecialistAgent


class TestFinancialSpecialistAgent(unittest.TestCase):
    def test_fallback_response_budget(self):
        agent = FinancialSpecialistAgent()
        result = agent.ask("How can I reduce monthly expenses and save more?")
        self.assertIn("budget", result.lower())

    def test_fallback_response_investment(self):
        agent = FinancialSpecialistAgent()
        result = agent.ask("What should I know before investing in index funds?")
        self.assertIn("index funds", result.lower())

    def test_system_prompt_contains_expertise(self):
        agent = FinancialSpecialistAgent()
        self.assertIn("financial specialist", agent._system_prompt().lower())

    def test_analyze_budget_recommends_savings(self):
        agent = FinancialSpecialistAgent()
        result = agent.analyze_budget(5000, {"housing": 1500, "food": 600, "transportation": 300, "insurance": 300, "savings": 500})
        self.assertIn("savings rate", result.lower())
        self.assertIn("healthy", result.lower())

    def test_estimate_retirement_savings_returns_projection(self):
        agent = FinancialSpecialistAgent()
        result = agent.estimate_retirement_savings(30, 65, 25000, 800, 0.06)
        self.assertIn("would grow to approximately", result)

    def test_debt_repayment_strategy_prioritizes_high_interest(self):
        agent = FinancialSpecialistAgent()
        result = agent.debt_repayment_strategy([
            {"name": "Credit Card", "balance": 5000, "rate": 18.0},
            {"name": "Car Loan", "balance": 12000, "rate": 4.5},
        ], extra_payment=150)
        self.assertIn("credit card", result.lower())
        self.assertIn("extra $150.00", result)

    def test_generate_asset_allocation_returns_recommendation(self):
        agent = FinancialSpecialistAgent()
        result = agent.generate_asset_allocation("conservative", 5)
        self.assertIn("40% equities", result.lower())

    def test_interactive_assessment_is_callable(self):
        agent = FinancialSpecialistAgent()
        self.assertTrue(callable(agent.interactive_assessment))
