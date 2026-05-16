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

Start a guided financial assessment:

```bash
python -m financial_specialist_agent.cli --survey
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

Plan a savings goal:

```bash
python -m financial_specialist_agent.cli --task savings --params '{"goal_amount": 50000, "current_savings": 10000, "monthly_contribution": 750, "annual_return": 0.05}'
```

Summarize net worth:

```bash
python -m financial_specialist_agent.cli --task networth --params '{"assets": {"home": 250000, "investment": 40000}, "liabilities": {"mortgage": 180000, "car_loan": 12000}}'
```

Forecast cash flow:

```bash
python -m financial_specialist_agent.cli --task cashflow --params '{"monthly_income": 5500, "monthly_expenses": {"housing": 1600, "utilities": 300, "food": 600, "transportation": 350}, "months": 12}'
```

Assess insurance needs:

```bash
python -m financial_specialist_agent.cli --task insurance --params '{"annual_income": 90000, "dependents": 2, "assets_value": 150000, "has_life_insurance": false}'
```

Save a report locally:

```bash
python -m financial_specialist_agent.cli --task save_report --format text --output monthly_report.txt --params '{"report_data": {"summary": "Monthly plan", "surplus": 1500}}'
```

Schedule a report file:

```bash
python -m financial_specialist_agent.cli --task schedule --format json --output scheduled_report.json --frequency monthly --params '{"report_data": {"summary": "Monthly plan", "surplus": 1500}}'
```

Send a report email:

```bash
python -m financial_specialist_agent.cli --task email --format text --subject "Monthly Financial Report" --sender "sender@example.com" --recipient "recipient@example.com" --smtp-server "smtp.example.com" --smtp-port 587 --smtp-username "user" --smtp-password "pass" --params '{"report_data": {"summary": "Monthly plan", "surplus": 1500}}'
```

Build a financial goals plan:

```bash
python -m financial_specialist_agent.cli --task plan --params '{"monthly_income": 7000, "monthly_expenses": {"housing": 1800, "food": 700, "transportation": 350}, "goals": [{"name": "Emergency Fund", "amount": 12000, "target_months": 12, "priority": 1}, {"name": "Vacation", "amount": 5000, "target_months": 10, "priority": 2}]}'
```

Export a structured report:

```bash
python -m financial_specialist_agent.cli --task report --format text --params '{"report_data": {"summary": "Monthly plan", "monthly_surplus": 1500}}'
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
