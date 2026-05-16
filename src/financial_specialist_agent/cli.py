import argparse
import json
from .agent import FinancialSpecialistAgent


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the Financial Specialist Agent from the command line."
    )
    parser.add_argument(
        "--question",
        help="Ask a single financial question and print the response.",
        type=str,
    )
    parser.add_argument(
        "--task",
        help="Run a specific financial analysis task: budget, retirement, debt, allocation, savings, networth, insurance, cashflow, plan, report, save_report, schedule, or email.",
        choices=["question", "budget", "retirement", "debt", "allocation", "savings", "networth", "insurance", "cashflow", "plan", "report", "save_report", "schedule", "email"],
        default="question",
    )
    parser.add_argument(
        "--format",
        help="Report export format for the report task: json or text.",
        choices=["json", "text"],
        default="json",
        type=str,
    )
    parser.add_argument(
        "--output",
        help="Path to write saved or scheduled report output.",
        type=str,
    )
    parser.add_argument(
        "--frequency",
        help="Reporting frequency when scheduling a report (e.g. monthly, weekly).",
        type=str,
        default="monthly",
    )
    parser.add_argument(
        "--subject",
        help="Email subject for the email task.",
        type=str,
    )
    parser.add_argument(
        "--sender",
        help="Sender email address for the email task.",
        type=str,
    )
    parser.add_argument(
        "--recipient",
        help="Recipient email address for the email task.",
        type=str,
    )
    parser.add_argument(
        "--smtp-server",
        help="SMTP server host for sending email.",
        type=str,
    )
    parser.add_argument(
        "--smtp-port",
        help="SMTP server port for sending email.",
        type=int,
    )
    parser.add_argument(
        "--smtp-username",
        help="SMTP username for sending email.",
        type=str,
    )
    parser.add_argument(
        "--smtp-password",
        help="SMTP password for sending email.",
        type=str,
    )
    parser.add_argument(
        "--params",
        help="JSON string with parameters for the chosen task.",
        type=str,
    )
    parser.add_argument(
        "--interactive",
        help="Start an interactive financial agent session.",
        action="store_true",
    )
    parser.add_argument(
        "--survey",
        help="Start an interactive financial assessment questionnaire.",
        action="store_true",
    )
    parser.add_argument(
        "--api-key",
        help="OpenAI API key to use for responses. If omitted, OPENAI_API_KEY is read from the environment.",
        type=str,
    )
    parser.add_argument(
        "--model",
        help="OpenAI model to use when API key is provided.",
        default="gpt-4o-mini",
        type=str,
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    agent = FinancialSpecialistAgent(api_key=args.api_key, model=args.model)

    if args.interactive:
        agent.interactive()
        return

    if args.survey:
        agent.interactive_assessment()
        return

    params = {}
    if args.params:
        try:
            params = json.loads(args.params)
        except json.JSONDecodeError:
            print("Unable to parse --params as JSON. Please provide valid JSON.")
            return

    if args.task == "question":
        if not args.question:
            print("Provide --question when using task 'question'.")
            return
        print(agent.ask(args.question))
        return

    if args.task == "budget":
        print(agent.analyze_budget(params.get("income", 0), params.get("expenses", {})))
        return

    if args.task == "retirement":
        print(agent.estimate_retirement_savings(
            params.get("current_age", 0),
            params.get("retirement_age", 0),
            params.get("current_savings", 0.0),
            params.get("monthly_contribution", 0.0),
            params.get("annual_return", 0.06),
        ))
        return

    if args.task == "debt":
        print(agent.debt_repayment_strategy(params.get("debts", []), params.get("extra_payment", 0.0)))
        return

    if args.task == "allocation":
        print(agent.generate_asset_allocation(params.get("risk_tolerance", "moderate"), params.get("investment_horizon_years", 10)))
        return

    if args.task == "savings":
        print(agent.plan_savings_goal(
            params.get("goal_amount", 0.0),
            params.get("current_savings", 0.0),
            params.get("monthly_contribution", 0.0),
            params.get("annual_return", 0.05),
            params.get("target_months"),
        ))
        return

    if args.task == "plan":
        print(agent.create_financial_plan(
            params.get("goals", []),
            params.get("monthly_income", 0.0),
            params.get("monthly_expenses", {}),
        ))
        return

    if args.task == "report":
        print(agent.export_report(params.get("report_data", {}), format=args.format))
        return

    if args.task == "save_report":
        output = args.output or params.get("output", "report.json")
        print(agent.save_report(params.get("report_data", {}), output, format=args.format))
        return

    if args.task == "schedule":
        output = args.output or params.get("output", "scheduled_report.json")
        print(agent.schedule_report(params.get("report_data", {}), output, frequency=args.frequency, format=args.format))
        return

    if args.task == "email":
        print(agent.send_email_report(
            params.get("report_data", {}),
            args.subject or params.get("subject", "Financial Report"),
            args.recipient or params.get("recipient", ""),
            args.sender or params.get("sender", ""),
            smtp_server=args.smtp_server or params.get("smtp_server"),
            smtp_port=args.smtp_port or params.get("smtp_port"),
            smtp_username=args.smtp_username or params.get("smtp_username"),
            smtp_password=args.smtp_password or params.get("smtp_password"),
            format=args.format,
        ))
        return

    if args.task == "networth":
        print(agent.summarize_net_worth(params.get("assets", {}), params.get("liabilities", {})))
        return

    if args.task == "cashflow":
        print(agent.forecast_cash_flow(
            params.get("monthly_income", 0.0),
            params.get("monthly_expenses", {}),
            params.get("months", 12),
        ))
        return

    if args.task == "insurance":
        print(agent.evaluate_insurance_needs(
            params.get("annual_income", 0.0),
            params.get("dependents", 0),
            params.get("assets_value", 0.0),
            params.get("has_life_insurance", False),
        ))
        return

    print("Please provide --question, --interactive, or a valid task to use the financial agent.")


if __name__ == "__main__":
    main()
