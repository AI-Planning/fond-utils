
_all__ = ['pddl']

"""Top-level package for extending pddl parser to APP."""

def parse_domain_problem(fn):
    from fondutils.pddl.domprob import DomProbParser

    with open(fn, "r") as f:
        ptext = f.read()
    return DomProbParser()(ptext)
