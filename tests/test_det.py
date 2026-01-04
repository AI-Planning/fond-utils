import io
from fondutils.pddl import parse_domain_problem
from pddl.formatter import domain_to_string, problem_to_string

from pddl import parse_domain

from fondutils.determizer import determinize

import inspect
from pathlib import Path
import requests

_current_filepath = inspect.getframeinfo(inspect.currentframe()).filename  # type: ignore
TEST_DIRECTORY = Path(_current_filepath).absolute().parent

def test_01():
    domain = parse_domain(TEST_DIRECTORY / "domain_01.pddl")
    domain_det = determinize(domain)

    with open(TEST_DIRECTORY / "domain_01_det.pddl", "r") as file:
        domain_expected = file.read()

    assert domain_to_string(domain_det) == domain_expected


def test_02():
    domain = parse_domain(TEST_DIRECTORY / "domain_02.pddl")
    domain_det = determinize(domain)

    with open(TEST_DIRECTORY / "domain_02_det.pddl", "r") as file:
        domain_expected = file.read()

    assert domain_to_string(domain_det) == domain_expected


def test_03():
    domain = parse_domain(TEST_DIRECTORY / "domain_03.pddl")
    domain_det = determinize(domain)

    with open(TEST_DIRECTORY / "domain_03_det.pddl", "r") as file:
        domain_expected = file.read()

    assert domain_to_string(domain_det) == domain_expected


def test_04():
    domain = parse_domain(TEST_DIRECTORY / "domain_04.pddl")
    domain_det = determinize(domain)

    with open(TEST_DIRECTORY / "domain_04_det.pddl", "r") as file:
        domain_expected = file.read()

    assert domain_to_string(domain_det) == domain_expected


def test_05():
    domain = parse_domain(TEST_DIRECTORY / "domain_05.pddl")
    domain_det = determinize(domain)

    with open(TEST_DIRECTORY / "domain_05_det.pddl", "r") as file:
        domain_expected = file.read()

    assert domain_to_string(domain_det) == domain_expected


def test_06():
    """like 03 but with a problem also in the file"""
    domain, _ = parse_domain_problem(TEST_DIRECTORY / "domprob_03.pddl")
    domain_det = determinize(domain)

    with open(TEST_DIRECTORY / "domain_03_det.pddl", "r") as file:
        domain_expected = file.read()

    assert domain_to_string(domain_det) == domain_expected


def test_07():
    """like 05 but with a problem also in the file"""
    domain, _ = parse_domain_problem(TEST_DIRECTORY / "domprob_05.pddl")
    domain_det = determinize(domain)

    with open(TEST_DIRECTORY / "domain_05_det.pddl", "r") as file:
        domain_expected = file.read()

    assert domain_to_string(domain_det) == domain_expected


def test_08():
    """like 03 but domain is taken from URL and stored in memory file"""
    URL_DOMAIN = "https://raw.githubusercontent.com/AI-Planning/fond-domains/refs/heads/main/benchmarks/blocksworld-2/domain.pddl"
    URL_DOMAIN = "https://raw.githubusercontent.com/AI-Planning/fond-utils/refs/heads/main/tests/domain_03.pddl"

    r = requests.get(URL_DOMAIN)
    domain_file = io.StringIO(r.content.decode("utf-8"))

    domain, _ = parse_domain_problem(domain_file)
    domain_det = determinize(domain)

    with open(TEST_DIRECTORY / "domain_03_det.pddl", "r") as file:
        domain_expected = file.read()

    assert domain_to_string(domain_det) == domain_expected


def test_09():
    """like 03 but with a problem also in the file and no suffix in domain name"""
    domain, _ = parse_domain_problem(TEST_DIRECTORY / "domprob_03.pddl")
    domain_det = determinize(domain, dom_suffix="")

    with open(TEST_DIRECTORY / "domain_03_det_02.pddl", "r") as file:
        domain_expected = file.read()

    assert domain_to_string(domain_det) == domain_expected

def test_10():
    """tests if we have a basic condeff as an outcome"""
    domain = parse_domain(TEST_DIRECTORY / "domain_07.pddl")
    domain_det = determinize(domain, dom_suffix="")

    with open(TEST_DIRECTORY / "domain_07_det.pddl", "r") as file:
        domain_expected = file.read()

    assert domain_to_string(domain_det) == domain_expected


if __name__ == "__main__":
    test_01()
    test_02()
    test_03()
    test_04()
    test_05()
    test_06()
    test_07()
    test_08()
    test_09()
    test_10()