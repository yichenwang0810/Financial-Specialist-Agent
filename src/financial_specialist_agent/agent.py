import os
from typing import Optional

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
