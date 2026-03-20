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


def test_01():
    # pytest tests/test_norm.py  -k test_01
    domain, _ = parse_domain_problem(TEST_DIRECTORY / "domain_01.pddl")
    domain_norm = normalize(domain, dom_suffix="NORM")

    domain_expected = parse_domain(TEST_DIRECTORY / "domain_01_norm.pddl")
    # with open(TEST_DIRECTORY / "domain_01_norm.pddl", "r") as file:
    #     domain_expected = file.read()

    assert domain_to_string(domain_norm) == domain_to_string(domain_expected)


def test_02():
    domain, _ = parse_domain_problem(TEST_DIRECTORY / "domain_02.pddl")
    domain_norm = normalize(domain, dom_suffix="NORM")

    domain_expected = parse_domain(TEST_DIRECTORY / "domain_02_norm.pddl")
    # with open(TEST_DIRECTORY / "domain_02_norm.pddl", "r") as file:
    #     domain_expected = file.read()

    assert domain_to_string(domain_norm) == domain_to_string(domain_expected)


def test_03():
    domain, _ = parse_domain_problem(TEST_DIRECTORY / "domain_03.pddl")
    domain_norm = normalize(domain, dom_suffix="NORM")

    with open(TEST_DIRECTORY / "domain_03_norm.pddl", "r") as file:
        domain_expected = file.read()

    assert domain_to_string(domain_norm) == domain_expected


def test_04():
    domain, _ = parse_domain_problem(TEST_DIRECTORY / "domain_04.pddl")
    domain_norm = normalize(domain, dom_suffix="NORM")

    with open(TEST_DIRECTORY / "domain_04_norm.pddl", "r") as file:
        domain_expected = file.read()

    assert domain_to_string(domain_norm) == domain_expected


def test_05():
    domain, _ = parse_domain_problem(TEST_DIRECTORY / "domain_05.pddl")
    domain_norm = normalize(domain, dom_suffix="NORM")

    with open(TEST_DIRECTORY / "domain_05_norm.pddl", "r") as file:
        domain_expected = file.read()

    assert domain_to_string(domain_norm) == domain_expected


def test_06():
    """like 03 but with a problem also in the file"""
    domain, _ = parse_domain_problem(TEST_DIRECTORY / "domprob_03.pddl")
    domain_norm = normalize(domain, dom_suffix="NORM")

    with open(TEST_DIRECTORY / "domain_03_norm.pddl", "r") as file:
        domain_expected = file.read()

    assert domain_to_string(domain_norm) == domain_expected


def test_07():
    """like 05 but with a problem also in the file"""
    domain, _ = parse_domain_problem(TEST_DIRECTORY / "domprob_05.pddl")
    domain_norm = normalize(domain, dom_suffix="NORM")

    with open(TEST_DIRECTORY / "domain_05_norm.pddl", "r") as file:
        domain_expected = file.read()

    assert domain_to_string(domain_norm) == domain_expected


def test_08():
    """like 03 but domain is taken from URL and stored in memory file"""
    URL_DOMAIN = "https://raw.githubusercontent.com/AI-Planning/fond-domains/refs/heads/main/benchmarks/blocksworld-2/domain.pddl"
    URL_DOMAIN = "https://raw.githubusercontent.com/AI-Planning/fond-utils/refs/heads/main/tests/domain_03.pddl"

    r = requests.get(URL_DOMAIN)
    domain_file = io.StringIO(r.content.decode("utf-8"))

    domain, _ = parse_domain_problem(domain_file)
    domain_norm = normalize(domain, dom_suffix="NORM")

    with open(TEST_DIRECTORY / "domain_03_norm.pddl", "r") as file:
        domain_expected = file.read()

    assert domain_to_string(domain_norm) == domain_expected


if __name__ == "_main_":
    test_01()
    test_02()
    test_03()
    test_04()
    test_05()
    test_06()
    test_07()
    test_08()
