import argparse
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

    if args.question:
        print(agent.ask(args.question))
        return

    print("Please provide --question or --interactive to use the financial agent.")


if __name__ == "__main__":
    main()
