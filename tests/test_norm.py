import io
from fondutils.pddl import parse_domain_problem
from pddl.formatter import domain_to_string, problem_to_string
from pddl import parse_domain

from fondutils.normalizer import normalize

import inspect
from pathlib import Path
import requests

_current_filepath = inspect.getframeinfo(inspect.currentframe()).filename  # type: ignore
TEST_DIRECTORY = Path(_current_filepath).absolute().parent

def check_normalize(file: Path, file_expected: Path):
    domain, _ = parse_domain_problem(TEST_DIRECTORY / file)
    domain_norm = normalize(domain, dom_suffix="NORM")

    # used to do this, but this will be very sensitive to syntax of expected file
    #  by parsing and then getting string we get the canonical form
    # with open(TEST_DIRECTORY / "domain_03_norm.pddl", "r") as file:
    #     domain_expected = file.read()
    # assert domain_to_string(domain_norm) == domain_expected

    domain_expected = parse_domain(TEST_DIRECTORY / file_expected)

    assert domain_to_string(domain_norm) == domain_to_string(domain_expected)


def test_01():
    # pytest tests/test_norm.py  -k test_01
    check_normalize("domain_01.pddl", "domain_01_norm.pddl")


def test_02():
    # pytest tests/test_norm.py  -k test_02
    check_normalize("domain_02.pddl", "domain_02_norm.pddl")


def test_03():
    # pytest tests/test_norm.py  -k test_03
    check_normalize("domain_03.pddl", "domain_03_norm.pddl")


def test_04():
    # pytest tests/test_norm.py  -k test_04
    check_normalize("domain_04.pddl", "domain_04_norm.pddl")


def test_05():
    # pytest tests/test_norm.py  -k test_05
    check_normalize("domain_05.pddl", "domain_05_norm.pddl")


def test_06():
    """like 03 but with a problem also in the file"""
    check_normalize("domprob_03.pddl", "domain_03_norm.pddl")


def test_07():
    """like 05 but with a problem also in the file"""
    check_normalize("domprob_05.pddl", "domain_05_norm.pddl")


def test_08():
    """like 03 but domain is taken from URL and stored in memory file"""
    URL_DOMAIN = "https://raw.githubusercontent.com/AI-Planning/fond-domains/refs/heads/main/benchmarks/blocksworld-2/domain.pddl"
    URL_DOMAIN = "https://raw.githubusercontent.com/AI-Planning/fond-utils/refs/heads/main/tests/domain_03.pddl"

    r = requests.get(URL_DOMAIN)
    domain_file = io.StringIO(r.content.decode("utf-8"))

    domain, _ = parse_domain_problem(domain_file)
    domain_norm = normalize(domain, dom_suffix="NORM")

    domain_expected = parse_domain(TEST_DIRECTORY / "domain_03_norm.pddl")

    assert domain_to_string(domain_norm) == domain_to_string(domain_expected)


if __name__ == "_main_":
    test_01()
    test_02()
    test_03()
    test_04()
    test_05()
    test_06()
    test_07()
    test_08()
