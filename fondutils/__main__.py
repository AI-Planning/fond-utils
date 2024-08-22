
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

    args = parser.parse_args()

    # --output is required for determinize and normalize
    if args.command in ["determinize", "normalize"] and not args.output:
        parser.error("--output is required for determinize and normalize")

    domain = parse_domain(args.input)

    if args.command == "check":
        print("\n  Checking domain file...\n")
        print(domain_to_string(domain))

    elif args.command == "determinize":
        det_domain = determinize(domain, args.prefix, args.suffix)
        with open(args.output, "w") as f:
            f.write(domain_to_string(det_domain))

    elif args.command == "normalize":
        norm_domain = normalize(domain)
        with open(args.output, "w") as f:
            f.write(domain_to_string(norm_domain))


if __name__ == '__main__':
    main()

