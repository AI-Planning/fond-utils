
import argparse

from pddl import parse_domain


def main(din, dout):
    domain = parse_domain(din)

    print(domain.actions)
    # domain.determinize()
    # domain.write(dout)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # --input and --output
    parser.add_argument('--input', dest='din', required=True)
    parser.add_argument('--output', dest='dout', required=True)
    args = parser.parse_args()
    main(args.din, args.dout)
