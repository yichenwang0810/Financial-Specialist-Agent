# Financial Specialist Agent

A Python-based financial specialist agent designed to provide practical guidance on budgeting, investing, retirement planning, credit management, insurance, and tax strategy.

## Features

- Conversational assistant for personal finance questions
- Modular agent class with OpenAI integration
- Automatic fallback guidance when OpenAI credentials are unavailable
- Command-line interface for quick queries

## Setup

1. Create and activate a Python virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install the package in editable mode:

```bash
python -m pip install -e .
```

3. Optionally add your OpenAI API key:

```bash
export OPENAI_API_KEY="your_api_key_here"
```

## Usage

Ask a single financial question:

```bash
python -m financial_specialist_agent.cli --question "How should I start saving for retirement?"
```

Start an interactive session:

```bash
python -m financial_specialist_agent.cli --interactive
```

Run a budget analysis task:

```bash
python -m financial_specialist_agent.cli --task budget --params '{"income": 5000, "expenses": {"housing": 1500, "food": 600, "transportation": 300}}'
```

Calculate retirement savings projections:

```bash
python -m financial_specialist_agent.cli --task retirement --params '{"current_age": 35, "retirement_age": 65, "current_savings": 40000, "monthly_contribution": 800, "annual_return": 0.06}'
```

Develop a debt repayment strategy:

```bash
python -m financial_specialist_agent.cli --task debt --params '{"debts": [{"name": "Credit Card", "balance": 6500, "rate": 19.5}, {"name": "Student Loan", "balance": 18000, "rate": 4.2}], "extra_payment": 200}'
```

Create an asset allocation recommendation:

```bash
python -m financial_specialist_agent.cli --task allocation --params '{"risk_tolerance": "moderate", "investment_horizon_years": 20}'
```

## Package API

```python
from financial_specialist_agent import FinancialSpecialistAgent
agent = FinancialSpecialistAgent()
response = agent.ask("What is the best way to improve my credit score?")
print(response)
```

## Testing

Run the built-in tests:

```bash
python -m unittest discover tests
```
