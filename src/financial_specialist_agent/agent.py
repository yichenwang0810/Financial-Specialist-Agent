import json
import os
from typing import Any, Dict, List, Optional

try:
    import openai
except ImportError:  # pragma: no cover
    openai = None


class FinancialSpecialistAgent:
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self._use_openai = bool(self.api_key and openai)

        if self._use_openai:
            openai.api_key = self.api_key

    def _system_prompt(self) -> str:
        return (
            "You are a financial specialist agent. "
            "Provide clear, practical advice tailored to the user’s financial goals, risk tolerance, "
            "and personal finance context. Your expertise includes budgeting, investing, retirement planning, "
            "credit and debt management, insurance, tax strategy, and long-term financial wellness. "
            "Always include actionable suggestions and explain trade-offs when appropriate. "
            "If the user asks for something you cannot answer, acknowledge the limitation and encourage them to seek a licensed professional."
        )

    def analyze_budget(self, monthly_income: float, expense_breakdown: Dict[str, float]) -> str:
        if monthly_income <= 0:
            return "Monthly income must be a positive number."

        total_expenses = sum(expense_breakdown.values())
        savings_rate = max(0.0, (monthly_income - total_expenses) / monthly_income)
        savings_target = 0.2
        shortfall = total_expenses - monthly_income

        message_lines = [
            f"Total monthly income: ${monthly_income:,.2f}",
            f"Total monthly expenses: ${total_expenses:,.2f}",
            f"Current savings rate: {savings_rate * 100:.1f}%",
        ]

        if shortfall > 0:
            message_lines.append(
                "Your spending exceeds your income, so prioritize cutting discretionary expenses and increasing income where possible."
            )
        elif savings_rate < savings_target:
            message_lines.append(
                "Your savings rate is below recommended levels. Look for ways to increase savings by reducing nonessential spending and automating contributions."
            )
        else:
            message_lines.append(
                "Your savings rate is healthy. Continue monitoring recurring expenses and build toward larger goals like emergency savings and retirement."
            )

        categories = {
            "housing": 0.30,
            "transportation": 0.15,
            "food": 0.15,
            "insurance": 0.10,
            "savings": 0.20,
        }
        for category, threshold in categories.items():
            if expense_breakdown.get(category, 0) / monthly_income > threshold:
                message_lines.append(
                    f"Your {category} spending is more than {int(threshold * 100)}% of income; consider whether that category can be optimized."
                )

        return "\n".join(message_lines)

    def estimate_retirement_savings(
        self,
        current_age: int,
        retirement_age: int,
        current_savings: float,
        monthly_contribution: float,
        annual_return: float = 0.06,
    ) -> str:
        if retirement_age <= current_age:
            return "Retirement age must be greater than current age."
        if monthly_contribution < 0 or current_savings < 0:
            return "Savings and contribution values must be non-negative."

        months = (retirement_age - current_age) * 12
        monthly_rate = annual_return / 12

        if monthly_rate:
            future_value = current_savings * (1 + monthly_rate) ** months
            future_value += monthly_contribution * (((1 + monthly_rate) ** months - 1) / monthly_rate)
        else:
            future_value = current_savings + monthly_contribution * months

        guidance = (
            f"At age {current_age}, saving ${monthly_contribution:,.2f} per month until age {retirement_age} "
            f"with an assumed annual return of {annual_return * 100:.1f}% would grow to approximately ${future_value:,.2f}."
        )
        guidance += "\nA common rule of thumb is to target 25x your expected annual retirement expenses, but your personal goal should reflect your lifestyle and any guaranteed income sources."
        guidance += "\nReview contribution increases regularly and adjust when your income or goals change."
        return guidance

    def debt_repayment_strategy(self, debts: List[Dict[str, Any]], extra_payment: float = 0.0) -> str:
        if not debts:
            return "Provide at least one debt entry with balance and interest rate to generate a repayment strategy."

        sorted_debts = sorted(debts, key=lambda debt: debt.get("rate", 0), reverse=True)
        strategy = [
            "Use a high-interest first repayment strategy to minimize total interest paid. "
            "Make minimum payments on all debts, then apply extra cash toward the debt with the highest interest rate."
        ]

        for debt in sorted_debts:
            name = debt.get("name", "debt")
            balance = debt.get("balance", 0)
            rate = debt.get("rate", 0)
            strategy.append(
                f"- {name}: ${balance:,.2f} at {rate:.2f}% interest"
            )

        if extra_payment > 0:
            strategy.append(
                f"Add an extra ${extra_payment:,.2f} payment toward the highest-rate debt each month to accelerate payoff."
            )

        strategy.append(
            "Review your budget, consider refinancing only when fees are justified, and avoid adding new high-interest balances while you pay down debt."
        )
        return "\n".join(strategy)

    def generate_asset_allocation(self, risk_tolerance: str, investment_horizon_years: int) -> str:
        risk = risk_tolerance.strip().lower()
        allocation = {
            "conservative": "40% equities, 50% bonds, 10% cash or short-duration fixed income",
            "moderate": "60% equities, 30% bonds, 10% cash or short-duration fixed income",
            "aggressive": "80% equities, 15% bonds, 5% cash or short-duration fixed income",
        }
        recommendation = allocation.get(risk, allocation["moderate"])
        return (
            f"With a {risk_tolerance} risk tolerance and a {investment_horizon_years}-year horizon, a recommended starting allocation is {recommendation}. "
            "Adjust the mix over time, rebalance annually, and choose low-cost funds aligned with your goals."
        )

    def ask(self, question: str) -> str:
        question = question.strip()
        if not question:
            return "Please ask a specific financial question so I can help."

        if self._use_openai:
            return self._call_openai(question)
        return self._fallback_response(question)

    def _call_openai(self, question: str) -> str:
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self._system_prompt()},
                {"role": "user", "content": question},
            ],
            temperature=0.7,
            max_tokens=650,
        )
        return response.choices[0].message.content.strip()

    def _fallback_response(self, question: str) -> str:
        normalized = question.lower()
        if any(keyword in normalized for keyword in ["budget", "save", "expense", "cash flow"]):
            return (
                "Start with a simple budget that tracks income, fixed costs, and discretionary spending. "
                "Aim to save at least 10–20% of your income each month, reduce recurring subscriptions you no longer use, "
                "and prioritize an emergency fund that covers 3–6 months of essential expenses."
            )

        if any(keyword in normalized for keyword in ["invest", "investment", "stocks", "bonds", "portfolio"]):
            return (
                "Focus on diversification across asset classes and time horizons. "
                "Consider low-cost index funds, maintain an emergency fund before investing, "
                "and align allocations with your risk tolerance and investment horizon. "
                "Rebalance yearly and avoid timing the market."
            )

        if any(keyword in normalized for keyword in ["retire", "retirement", "401k", "ira", "pension"]):
            return (
                "Define your retirement goals, estimate your future expenses, and calculate how much you need to save. "
                "Maximize tax-advantaged accounts such as 401(k)s or IRAs, contribute enough to capture any employer match, "
                "and gradually shift toward more conservative investments as you near retirement."
            )

        if any(keyword in normalized for keyword in ["debt", "credit score", "credit", "loan", "mortgage"]):
            return (
                "Pay down high-interest debt first while staying current on all payments. "
                "Keep credit utilization low, review your credit report annually, and avoid opening unnecessary accounts. "
                "For mortgages or student loans, evaluate refinancing only when you can lock in a materially lower rate and the costs justify it."
            )

        if any(keyword in normalized for keyword in ["tax", "taxes", "deduction", "filing"]):
            return (
                "Use available tax-advantaged accounts, document deductions, and keep clear records throughout the year. "
                "A licensed tax professional can help you identify credits or deductions for your situation and minimize tax liability while staying compliant."
            )

        return (
            "I’m a financial specialist agent focused on budgeting, investing, retirement, credit, insurance, and tax guidance. "
            "Please provide a few details about your goals or the financial area you want help with so I can give actionable advice."
        )

    def interactive(self) -> None:
        print("Financial Specialist Agent Interactive Mode")
        print("Type 'exit' or 'quit' to leave.\n")
        while True:
            try:
                question = input("Ask your financial question: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nGoodbye.")
                break
            if question.lower() in {"exit", "quit"}:
                print("Goodbye.")
                break
            print("\n", self.ask(question), "\n")
