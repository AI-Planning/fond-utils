
import sys
from lark import Lark

from pddl.parser.domain import DomainTransformer
from pddl.parser.problem import ProblemTransformer
from pddl.formatter import domain_to_string, problem_to_string


from lark.visitors import Transformer, merge_transformers

from pddl.parser import PARSERS_DIRECTORY as IMPORT_PARSERS_DIRECTORY


DOMPROB_GRAMMAR = """
    start: [domain_start] [problem_start]


    %ignore /\s+/
    %ignore COMMENT

    %import .domain.start -> domain_start
    %import .problem.start -> problem_start

    %import common.COMMENT -> COMMENT
    %import common.WS -> WS

"""

class DomainProblemTransformer(Transformer):
    """A transformer for domain + problems"""

    # def __init__(self, *args, **kwargs):
    #     """Initialize the domain transformer."""
    #     super().__init__(*args, **kwargs)

    def start(self, children):
        return children

    def domain_start(self, children):
        return children[0]

    def problem_start(self, children):
        return children[0]


class DomProbParser:
    """Domain and/or problem PDDL domain parser class."""

    def __init__(self):
        """Initialize."""
        self._transformer = merge_transformers(
            DomainProblemTransformer(),
            domain=DomainTransformer(),
            problem=ProblemTransformer(),
        )
        # need to use earley; lalr will not be able to recognise files with just problems (no left)
        # self._parser = Lark.open(DOMPROB_GRAMMAR_FILE, rel_to=__file__)
        self._parser = Lark(
            DOMPROB_GRAMMAR, parser="earley", import_paths=[IMPORT_PARSERS_DIRECTORY]
        )

    def __call__(self, text):
        """Call the object as a function
        Will return the object representing the parsed text/file which is an object
        of class pddl_parser.app_problem.APPProblem

        The call_parser() function is part of pddl package: will build a Tree from text and then an object pddl_parser.app_problem.APPProblem from the Tree
        """
        # TODO: this is OK when pddl.helpers.base provides call_parser API, but that is not in pip package 0.4.0 so we implement directly what is in that function
        # https://github.com/AI-Planning/pddl/blob/4ee8d63034a668072dd0656be1fe59d2f00804f8/pddl/helpers/base.py#L203
        # return call_parser(text, self._parser, self._transformer)

        # this was actually the code in call_parser() function
        sys.tracebacklimit = 0  # noqa
        tree = self._parser.parse(text)

        sys.tracebacklimit = None  # noqa
        result = self._transformer.transform(tree)
        return result


def domprob_to_string(domprob):
    """Convert a domain and problem to a string."""
    domain, problem = domprob

    domain_str = domain_to_string(domain) if domain is not None else None
    problem_str = problem_to_string(problem) if problem is not None else None

    return domain_str, problem_str



if __name__ == "__main__":
    file = sys.argv[1]
    with open(file, "r") as f:
        ptext = f.read()
    app = DomProbParser()(ptext)
    print(app)
