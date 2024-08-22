
import argparse

from pddl.formatter import domain_to_string, problem_to_string

from fondutils.normalizer import normalize
from fondutils.determizer import determinize
from fondutils.pddl import parse_domain_problem


def main():
    parser = argparse.ArgumentParser(description="Utilities to process FOND PDDL")

    parser.add_argument("command", choices=["check", "determinize", "normalize"])
    parser.add_argument("--input", required=True, help="Input domain file")
    parser.add_argument("--output", help="Output domain file")
    parser.add_argument("--outproblem", help="Optional output problem file")

    parser.add_argument("--prefix",
                        default="_DETDUP_",
                        help="Prefix for determinized action outcome identifier")
    parser.add_argument("--suffix",
                        default="",
                        help="Suffix for determinized action outcome identifier")

    parser.add_argument("--console", action="store_true", help="Print the domain after processing")

    args = parser.parse_args()

    if args.command in ["determinize", "normalize"] and not args.output:
        parser.error("--output is required for determinize and normalize")

    fond_domain, fond_problem = parse_domain_problem(args.input)

    if (fond_problem is not None) and (not args.outproblem) and (not args.command == "check"):
        parser.error("--outproblem is required for domain+problem input")

    if args.command == "check":
        print("\n  Checking domain file...\n")
        print(domain_to_string(fond_domain))
        if fond_problem is not None:
            print(problem_to_string(fond_problem))
        return

    elif args.command == "determinize":
        new_domain = determinize(fond_domain, args.prefix, args.suffix)

    elif args.command == "normalize":
        new_domain = normalize(fond_domain)

    with open(args.output, "w") as f:
        f.write(domain_to_string(new_domain))

    if args.outproblem:
        with open(args.outproblem, "w") as f:
            f.write(problem_to_string(fond_problem))

    if args.console:
        print(domain_to_string(new_domain))


if __name__ == '__main__':
    main()

