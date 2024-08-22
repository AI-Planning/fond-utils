
import argparse

from pddl import parse_domain
from pddl.formatter import domain_to_string

from fondutils.normalizer import normalize
from fondutils.determizer import determinize


def main():
    parser = argparse.ArgumentParser(description="Utilities to process FOND PDDL")

    parser.add_argument("command", choices=["check", "determinize", "normalize"])
    parser.add_argument("--input", required=True, help="Input domain file")
    parser.add_argument("--output", help="Output domain file")

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

    domain = parse_domain(args.input)

    if args.command == "check":
        print("\n  Checking domain file...\n")
        print(domain_to_string(domain))

    elif args.command == "determinize":
        new_domain = determinize(domain, args.prefix, args.suffix)

    elif args.command == "normalize":
        new_domain = normalize(domain)

    with open(args.output, "w") as f:
        f.write(domain_to_string(new_domain))

    if args.console:
        print(domain_to_string(new_domain))


if __name__ == '__main__':
    main()

