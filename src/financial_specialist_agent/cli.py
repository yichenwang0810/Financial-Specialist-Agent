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
        help="Run a specific financial analysis task: budget, retirement, debt, or allocation.",
        choices=["question", "budget", "retirement", "debt", "allocation"],
        default="question",
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

    print("Please provide --question, --interactive, or a valid task to use the financial agent.")


if __name__ == "__main__":
    main()
