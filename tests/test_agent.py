import os
import tempfile
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

    def test_plan_savings_goal_with_target(self):
        agent = FinancialSpecialistAgent()
        result = agent.plan_savings_goal(50000, 10000, 750, 0.05, 60)
        self.assertIn("reach a $50,000.00 goal", result)

    def test_summarize_net_worth_positive(self):
        agent = FinancialSpecialistAgent()
        result = agent.summarize_net_worth({"home": 250000, "investments": 50000}, {"mortgage": 180000, "car": 10000})
        self.assertIn("net worth: $110,000.00", result.lower())

    def test_forecast_cash_flow_positive(self):
        agent = FinancialSpecialistAgent()
        result = agent.forecast_cash_flow(5000, {"housing": 1500, "food": 600}, 12)
        self.assertIn("projected surplus over 12 months", result.lower())

    def test_evaluate_insurance_needs(self):
        agent = FinancialSpecialistAgent()
        result = agent.evaluate_insurance_needs(85000, 2, 120000, False)
        self.assertIn("estimated life insurance coverage need", result.lower())

    def test_create_financial_plan_with_surplus(self):
        agent = FinancialSpecialistAgent()
        result = agent.create_financial_plan(
            [{"name": "Emergency Fund", "amount": 12000, "target_months": 12, "priority": 1}],
            7000,
            {"housing": 1800, "food": 600, "transportation": 400},
        )
        self.assertIn("monthly surplus available for goals", result.lower())

    def test_export_report_json(self):
        agent = FinancialSpecialistAgent()
        report = agent.export_report({"summary": "Test report", "value": 100}, format="json")
        self.assertIn('"summary": "Test report"', report)

    def test_export_report_text(self):
        agent = FinancialSpecialistAgent()
        report = agent.export_report({"summary": "Test report", "value": 100}, format="text")
        self.assertIn("summary: Test report", report)

    def test_interactive_assessment_is_callable(self):
        agent = FinancialSpecialistAgent()
        self.assertTrue(callable(agent.interactive_assessment))

    def test_save_report_writes_file(self):
        agent = FinancialSpecialistAgent()
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "report.txt")
            result = agent.save_report({"summary": "Save test"}, path, format="text")
            self.assertIn("Report saved", result)
            with open(path, "r", encoding="utf-8") as handle:
                self.assertIn("summary: Save test", handle.read())

    def test_schedule_report_writes_metadata(self):
        agent = FinancialSpecialistAgent()
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "scheduled_report.json")
            result = agent.schedule_report({"summary": "Scheduled test"}, path, frequency="weekly", format="json")
            self.assertIn("Scheduled report metadata written", result)
            self.assertTrue(os.path.exists(f"{path}.schedule.json"))

    def test_compose_email_report_contains_headers(self):
        agent = FinancialSpecialistAgent()
        raw_email = agent.compose_email_report(
            {"summary": "Email test"},
            "Report Subject",
            "recipient@example.com",
            "sender@example.com",
            format="text",
        )
        self.assertIn("Subject: Report Subject", raw_email)
        self.assertIn("To: recipient@example.com", raw_email)
        self.assertIn("summary: Email test", raw_email)
