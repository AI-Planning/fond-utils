
import sys
from lark import Lark

from typing import Any, Tuple

from pddl.core import Domain, Problem
from pddl.parser.base import BaseParser
from pddl.parser.domain import DomainTransformer
from pddl.parser.problem import ProblemTransformer
from pddl.formatter import domain_to_string, problem_to_string

from pddl.parser import GRAMMAR_FILE

from lark.visitors import Transformer

GRAMMAR = "domprob: [domain] [problem]\n" + GRAMMAR_FILE.read_text()


class DomainProblemTransformer(Transformer[Any, Tuple[Domain | None, Problem | None]]):
    """A transformer for domain + problems.
    Just delegates to the domain and problem transformers."""

    def __init__(self) -> None:
        super().__init__()
        self.domain_transformer = DomainTransformer()
        self.problem_transformer = ProblemTransformer()

    def domprob(self, children):
        """the start symbols"""
        domain = None
        problem = None
        if children:
            if len(children) == 1:
                if isinstance(children[0], Domain):
                    domain = children[0]
                else:
                    problem = children[0]
            else:
                domain, problem = children
        return domain, problem

    def domain(self, children) -> Domain:
        return self.domain_transformer.domain(children)

    def problem(self, children) -> Problem:
        return self.problem_transformer.problem(children)

    def transform(self, tree) -> Tuple[Domain | None, Problem | None]:
        domain = None
        problem = None
        for child in tree.children:
            if child is None:
                continue
            if child.data == "domain":
                domain = self.domain_transformer.transform(child)
            elif child.data == "problem":
                problem = self.problem_transformer.transform(child)
        return domain, problem


class DomainProblemParser(BaseParser[Tuple[Domain | None, Problem | None]]):
    """PDDL domain + problem parser class."""

    transformer_cls = DomainProblemTransformer
    start_symbol = "domprob"

    def __init__(self, *args, **kwargs) -> None:
        # need to change the parser to earley to be able to parse files with just problems (no left)
        #  "lalr" parser won't work (1 lookahead is not enough to know which rule to use)
        Transformer.__init__(self, *args, **kwargs)
        self._transformer = self.transformer_cls()
        self._parser = Lark(
            GRAMMAR,
            parser="earley",
            start=self.start_symbol,
        )

    def __call__(self, text: str) -> Tuple[Domain | None, Problem | None]:
        tree = self._parser.parse(text)
        return self._transformer.transform(tree)


if __name__ == "__main__":
    # we can use this for quick testing/debugging
    file = sys.argv[1]
    with open(file, "r") as f:
        ptext = f.read()

    domain, problem = DomainProblemParser()(ptext)
    if domain:
        domprob = print(domain_to_string(domain))
    if problem:
        domprob = print(problem_to_string(problem))
