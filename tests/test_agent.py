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
