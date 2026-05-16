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

    def plan_savings_goal(
        self,
        goal_amount: float,
        current_savings: float,
        monthly_contribution: float,
        annual_return: float = 0.05,
        target_months: Optional[int] = None,
    ) -> str:
        if goal_amount <= 0 or current_savings < 0 or monthly_contribution < 0:
            return "Goal amount and savings values must be non-negative, and goal amount must be positive."

        if target_months and target_months <= 0:
            return "Target months must be a positive integer."

        monthly_rate = annual_return / 12
        if target_months:
            needed = goal_amount - current_savings * (1 + monthly_rate) ** target_months
            if monthly_rate:
                required_payment = needed * monthly_rate / ((1 + monthly_rate) ** target_months - 1)
            else:
                required_payment = needed / target_months
            required_payment = max(required_payment, 0.0)
            return (
                f"To reach a ${goal_amount:,.2f} goal in {target_months} months with ${current_savings:,.2f} already saved, "
                f"you would need to save about ${required_payment:,.2f} per month at an assumed {annual_return * 100:.1f}% annual return."
            )

        months = 0
        balance = current_savings
        while balance < goal_amount and months < 1200:
            balance = balance * (1 + monthly_rate) + monthly_contribution
            months += 1

        if balance < goal_amount:
            return (
                "With the current monthly contribution and return assumptions, this savings goal would take longer than 100 years to reach. "
                "Consider increasing your monthly contribution or reviewing the target amount."
            )

        return (
            f"At ${monthly_contribution:,.2f} per month and an assumed {annual_return * 100:.1f}% annual return, "
            f"you can reach ${goal_amount:,.2f} in about {months} months (around {months // 12} years and {months % 12} months)."
        )

    def summarize_net_worth(self, assets: Dict[str, float], liabilities: Dict[str, float]) -> str:
        total_assets = sum(assets.values())
        total_liabilities = sum(liabilities.values())
        net_worth = total_assets - total_liabilities
        debt_ratio = total_liabilities / total_assets if total_assets else 0.0

        summary = [
            f"Total assets: ${total_assets:,.2f}",
            f"Total liabilities: ${total_liabilities:,.2f}",
            f"Net worth: ${net_worth:,.2f}",
            f"Debt-to-asset ratio: {debt_ratio * 100:.1f}%",
        ]

        if net_worth < 0:
            summary.append(
                "Your net worth is negative, which means liabilities exceed assets. Focus on reducing high-interest debt and building savings."
            )
        elif debt_ratio > 0.5:
            summary.append(
                "More than half of your assets are funded by liabilities. Consider paying down debt and strengthening savings."
            )
        else:
            summary.append(
                "Your net worth is positive, and your asset base is more than your liabilities. Continue growing assets while maintaining manageable debt levels."
            )

        return "\n".join(summary)

    def forecast_cash_flow(
        self,
        monthly_income: float,
        monthly_expenses: Dict[str, float],
        months: int = 12,
    ) -> str:
        if monthly_income < 0 or months <= 0:
            return "Monthly income must be non-negative and months must be a positive integer."

        total_expenses = sum(monthly_expenses.values())
        monthly_surplus = monthly_income - total_expenses
        forecast = monthly_surplus * months
        summary = [
            f"Monthly income: ${monthly_income:,.2f}",
            f"Monthly expenses: ${total_expenses:,.2f}",
            f"Monthly surplus (income minus expenses): ${monthly_surplus:,.2f}",
            f"Projected surplus over {months} months: ${forecast:,.2f}",
        ]

        if monthly_surplus < 0:
            summary.append(
                "Your expenses exceed income. Review discretionary spending and consider options to increase income to avoid cash flow pressure."
            )
        else:
            summary.append(
                "A positive monthly surplus gives you flexibility to save, invest, or pay down debt. Keep tracking expenses and adjust as needed."
            )

        return "\n".join(summary)

    def evaluate_insurance_needs(
        self,
        annual_income: float,
        dependents: int,
        assets_value: float,
        has_life_insurance: bool = False,
    ) -> str:
        if annual_income < 0 or dependents < 0 or assets_value < 0:
            return "Income, dependents, and asset values must be non-negative."

        needed_coverage = annual_income * max(10, dependents * 5)
        summary = [
            f"Estimated life insurance coverage need: ${needed_coverage:,.2f}",
            f"Current asset base: ${assets_value:,.2f}",
        ]

        if has_life_insurance:
            summary.append(
                "Since you already have life insurance coverage, review your policy annually to ensure it scales with your income and family needs."
            )
        else:
            summary.append(
                "Consider life insurance if you have dependents or debts that others would need to cover if your income were lost."
            )

        summary.append(
            "Also verify that you have sufficient property, disability, and health coverage for your situation, especially if you have major assets or dependents."
        )
        return "\n".join(summary)

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

    def _prompt_float(self, prompt: str, allow_zero: bool = True) -> float:
        while True:
            value = input(prompt).strip()
            if not value:
                return 0.0
            try:
                number = float(value)
                if number < 0 or (not allow_zero and number == 0):
                    print("Please enter a valid positive number.")
                    continue
                return number
            except ValueError:
                print("Please enter a valid number.")

    def _prompt_int(self, prompt: str, minimum: int = 0) -> int:
        while True:
            value = input(prompt).strip()
            if not value:
                return 0
            try:
                number = int(value)
                if number < minimum:
                    print(f"Please enter an integer greater than or equal to {minimum}.")
                    continue
                return number
            except ValueError:
                print("Please enter a valid integer.")

    def _prompt_expense_breakdown(self) -> Dict[str, float]:
        print("Enter monthly expenses by category. Leave the category blank when finished.")
        expenses: Dict[str, float] = {}
        while True:
            category = input("Category: ").strip()
            if not category:
                break
            amount = self._prompt_float(f"Amount for {category}: ", allow_zero=False)
            expenses[category.lower()] = amount
        return expenses

    def _prompt_debts(self) -> List[Dict[str, Any]]:
        print("Enter debts one at a time. Leave the debt name blank when finished.")
        debts: List[Dict[str, Any]] = []
        while True:
            name = input("Debt name: ").strip()
            if not name:
                break
            balance = self._prompt_float(f"Balance for {name}: ", allow_zero=False)
            rate = self._prompt_float(f"Interest rate (percent) for {name}: ", allow_zero=False)
            debts.append({"name": name, "balance": balance, "rate": rate})
        return debts

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

    def interactive_assessment(self) -> None:
        print("Financial Specialist Agent Assessment Mode")
        print("Choose a task to complete a guided financial assessment.\n")

        while True:
            print("1) Budget assessment")
            print("2) Retirement projection")
            print("3) Debt repayment strategy")
            print("4) Asset allocation recommendation")
            print("5) Plan a savings goal")
            print("6) Net worth summary")
            print("7) Cash flow forecast")
            print("8) Insurance needs assessment")
            print("9) Ask a general financial question")
            print("0) Exit\n")

            choice = input("Select an option: ").strip()
            if choice in {"0", "exit", "quit"}:
                print("Goodbye.")
                break

            if choice == "1":
                income = self._prompt_float("Monthly income: ", allow_zero=False)
                expenses = self._prompt_expense_breakdown()
                print("\n" + self.analyze_budget(income, expenses) + "\n")
                continue

            if choice == "2":
                current_age = self._prompt_int("Current age: ", minimum=0)
                retirement_age = self._prompt_int("Retirement age: ", minimum=0)
                current_savings = self._prompt_float("Current retirement savings: ")
                monthly_contribution = self._prompt_float("Planned monthly contribution: ")
                annual_return = self._prompt_float("Expected annual return (as decimal, e.g. 0.06): ")
                print(
                    "\n" +
                    self.estimate_retirement_savings(
                        current_age,
                        retirement_age,
                        current_savings,
                        monthly_contribution,
                        annual_return or 0.06,
                    ) +
                    "\n"
                )
                continue

            if choice == "3":
                debts = self._prompt_debts()
                extra_payment = self._prompt_float("Extra monthly payment amount: ")
                print("\n" + self.debt_repayment_strategy(debts, extra_payment) + "\n")
                continue

            if choice == "4":
                risk_tolerance = input("Risk tolerance (conservative/moderate/aggressive): ").strip() or "moderate"
                horizon = self._prompt_int("Investment horizon in years: ", minimum=0)
                print("\n" + self.generate_asset_allocation(risk_tolerance, horizon or 10) + "\n")
                continue

            if choice == "5":
                goal_amount = self._prompt_float("Savings goal amount: ", allow_zero=False)
                current_savings = self._prompt_float("Current savings: ")
                monthly_contribution = self._prompt_float("Monthly contribution: ")
                annual_return = self._prompt_float("Expected annual return (as decimal, e.g. 0.05): ")
                target_months = self._prompt_int("Target months (leave blank to calculate time to goal): ", minimum=0)
                print("\n" + self.plan_savings_goal(goal_amount, current_savings, monthly_contribution, annual_return or 0.05, target_months or None) + "\n")
                continue

            if choice == "6":
                print("Enter asset values. Leave the asset name blank when finished.")
                assets = {}
                while True:
                    name = input("Asset name: ").strip()
                    if not name:
                        break
                    assets[name.lower()] = self._prompt_float(f"Value for {name}: ", allow_zero=False)
                print("Enter liability values. Leave the liability name blank when finished.")
                liabilities = {}
                while True:
                    name = input("Liability name: ").strip()
                    if not name:
                        break
                    liabilities[name.lower()] = self._prompt_float(f"Value for {name}: ", allow_zero=False)
                print("\n" + self.summarize_net_worth(assets, liabilities) + "\n")
                continue

            if choice == "7":
                income = self._prompt_float("Monthly income: ", allow_zero=False)
                expenses = self._prompt_expense_breakdown()
                months = self._prompt_int("Forecast months: ", minimum=1)
                print("\n" + self.forecast_cash_flow(income, expenses, months or 12) + "\n")
                continue

            if choice == "8":
                annual_income = self._prompt_float("Annual income: ", allow_zero=False)
                dependents = self._prompt_int("Number of dependents: ", minimum=0)
                assets_value = self._prompt_float("Total asset value: ")
                has_life_insurance = input("Do you currently have life insurance? (yes/no): ").strip().lower() in {"yes", "y"}
                print("\n" + self.evaluate_insurance_needs(annual_income, dependents, assets_value, has_life_insurance) + "\n")
                continue

            if choice == "9":
                question = input("What do you want to know? ").strip()
                if question:
                    print("\n" + self.ask(question) + "\n")
                continue

            print("Please choose a valid option from the menu.\n")
