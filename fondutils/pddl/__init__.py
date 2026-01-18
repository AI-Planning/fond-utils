_all__ = ['pddl']

"""Top-level package for extending pddl parser to APP."""
from io import StringIO

def parse_domain_problem(fn):
    # able to parse files containing only domain or only problem, or domain followed by problem
    from fondutils.pddl.domprob import DomainProblemParser

    if isinstance(fn, StringIO):
        ptext = fn.read()
    else:
        with open(fn, "r") as f:
            ptext = f.read()
    return DomainProblemParser()(ptext)
