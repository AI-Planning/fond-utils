# FOND Utilities

Utilities for parsing and manipulating the FOND planning language (those containing non-deterministic `oneof` effects). At this point the system can:

- _Check_ a file contains a legal FOND domain/problem.
- _Normalize_ a FOND planning domain (i.e., have a single top-level `oneof` clause in the effect).
- _Compute the all-outcome determinization_ of a FOND domain, where each non-deterministic action is replaced with a set of deterministic actions, each encoding one possible effect outcome of the action. A solution in the deterministic version amounts to a weak plan solution in the original FOND problem.
  - Note the determinizer produces another PDDL domain and does not deal with the problem itself, unlike the SAS-based determinizers used in other planners (like [PRP](https://github.com/QuMuLab/planner-for-relevant-policies), [FONDSAT](https://github.com/tomsons22/FOND-SAT), or [CFOND-ASP](https://github.com/ssardina-research/cfond-asp)) that are are based on the SAS translator in [Fast-Downard](https://github.com/aibasel/downward) classical planner and produce a SAS encoding of the determinization of a specific instance planning problem. For these determinizers that output SAS encodings, please refer to the individual planners or the [translator-fond](https://github.com/ssardina-research/translator-fond) repo.

> [!IMPORTANT]
> The system accepts effects that are an arbitrary nesting of `oneof`, conditional effects, and `and`. See section [Format allowed on effects](#format-allowed-on-effects) at the bottom about format accepted.

## Install

The fond-utils system can be installed (as a package) directly from its [PyPi](https://pypi.org/project/fond-utils/) repository:

```shell
$ pip install fond-utils
```

Alternatively, it can be installed directly from the repo:

```shell
$ pip install git+https://github.com/AI-Planning/fond-utils
```

or, clone the repository and install:

```shell
$ git clone https://github.com/AI-Planning/fond-utils
$ cd fond-utils
$ pip install .
```

The system already includes a CLI console application `fond-utils` that will generally be the tool to use. To check the installation was successful just run:

```shell
$ fond-utils -h
usage: fond-utils [-h] --input INPUT [--output OUTPUT] [--outproblem OUTPROBLEM] [--prefix PREFIX] [--suffix SUFFIX]
                  [--console]
                  {check,determinize,normalize}

Utilities to process FOND PDDL

positional arguments:
  {check,determinize,normalize}

options:
  -h, --help            show this help message and exit
  --input INPUT         Input domain file
  --output OUTPUT       Output domain file
  --outproblem OUTPROBLEM
                        Optional output problem file
  --prefix PREFIX       Prefix for determinized action outcome identifier (Default: _DETDUP_)
  --suffix SUFFIX       Suffix for determinized action outcome identifier
  --console             Print the domain after processing
```

> [!NOTE]
> The scripts on this system relies on the [pddl](https://github.com/AI-Planning/pddl) parser, which can be easily installed via [PyPi](https://pypi.org/project/pddl/) repository (`pip install pddl`). The pddl system relies itself on the [lark](https://lark-parser.readthedocs.io/en/stable/) parsing library. The fond-utils system, however, extends `pddl` to accept single files containing _both_ the domain and the problem instance, and will be extended further to accept labelled outcomes in the effects.

## Quickstart

You can use the fond-utils package in two ways: as a library, and as a CLI tool.

### As a CLI application tool

To just check that the PDDL input file is parsed well, use the command `check` and report to console:

```shell
$ fond-utils check --input https://raw.githubusercontent.com/AI-Planning/fond-utils/refs/heads/main/tests/domain_03.pddl
```

Since the system is provided as a module `fondutils`, this would be equivalent to:

```shell
$ python -m fondutils check --input https://raw.githubusercontent.com/AI-Planning/fond-utils/refs/heads/main/tests/domain_03.pddl
```

Note this would work if you have cloned the repo rather than installed the actual package; for example:

```shell
$ git clone https://github.com/AI-Planning/fond-utils
$ cd fond-utils
$ python -m fondutils check --input tests/domain_03.pddl
```

#### Normalize a domain

To simply perform normalization (i.e., have a single top-level `oneof` clause in the effect):

```shell
$ fond-utils normalize --input tests/domain_05.pddl --output normalized-domain.pddl
```

Example `test/domain_05.pddl` includes some complex (nested) `oneof` effects. The name of the normalized domain will be the original name with suffix `_NORM`.

#### All-outcome determinization

To perform the determinization, use the command `determinize`:

```shell
$ fond-utils determinize --input tests/domain_03.pddl --output determinized-domain.pddl
```

The name of the determinized domain will be the original name with a possible suffix separated with an underscore (default `_NEW`). Use `--suffix-domain ""` to use no suffix (same name as original domain).

The deterministic versions of a non-deterministic action are enumerated (starting from 1) with possible prefix and suffix on the number, each part separated with an underscore `_`. For example, the third deterministic action of operator `move` would be named `move_<PREFIX>_3_<SUFFIX>`; if no prefix or suffix is set, it would be just `move_3`.

> [!TIP]
> To change the default operator name prefix `DETDUP` use the options `--prefix`, and to add a suffix after the number, use `--suffix`. To set the suffix for the domain name use `--suffix-domain`. To get the resulting PDDL printed on console use `--console`:

```lisp
$ fond-utils  determinize --input tests/domain_03.pddl --prefix "PRE" --suffix "SUF"  --suffix-domain "NEW" --console
(define (domain blocks-domain_NEW)
    (:requirements :equality :typing)
    (:types block)
    (:predicates (clear ?b - block)  (emptyhand) (holding ?b - block)  (on ?b1 - block ?b2 - block)  (on-table ?b - block))
    (:action pick-up_PRE_1_SUF
        :parameters (?b1 - block ?b2 - block)
        :precondition (and (not (= ?b1 ?b2)) (emptyhand) (clear ?b1) (on ?b1 ?b2))
        :effect (and (holding ?b1) (clear ?b2) (not (emptyhand)) (not (clear ?b1)) (not (on ?b1 ?b2)))
    )
     (:action pick-up_PRE_2_SUF
        :parameters (?b1 - block ?b2 - block)
        :precondition (and (not (= ?b1 ?b2)) (emptyhand) (clear ?b1) (on ?b1 ?b2))
        :effect (and (clear ?b2) (on-table ?b1) (not (on ?b1 ?b2)))
    )
     (:action pick-up_PRE_3_SUF
        :parameters (?b1 - block ?b2 - block)
        :precondition (and (not (= ?b1 ?b2)) (emptyhand) (clear ?b1) (on ?b1 ?b2))
        :effect (and )
    )
     (:action put-down
        :parameters (?b - block)
        :precondition (holding ?b)
        :effect (and (on-table ?b) (emptyhand) (clear ?b) (not (holding ?b)))
    )
)
```

This resulting PDDL domain is now deterministic and can then be used as input to the original [Fast-Downward](https://github.com/aibasel/downward) SAS translator.

> [!WARNING]
> If the new domain is named with a suffix (as in the default case), existing problem instances may not be compatible with the new domain, as they will still refer to the original domain in the `:domain` section. If these problem instances will be used with the new PDDL encoding, either use no suffix for the domain name (so it will keep the same name as the original) or change the `:domain` section in the problem instances to match the new name that includes the suffix (by setting private property `_domain_name`). Note that if the file parsed included the problem as well, the CLI tool will do such update so that the resulting problem will have its domain name matching the new domain.

### As a library

This is an example of how we can normalize and determinize a PDDL non-deterministic domain programmatically:

```python
import io
import inspect
from pathlib import Path
import requests

from pddl import parse_domain
from pddl.formatter import domain_to_string
from fondutils.determizer import determinize
from fondutils.normalizer import normalize

# get a domain from AI-Planning/fond-domains repo
URL_DOMAIN = "https://raw.githubusercontent.com/AI-Planning/fond-domains/refs/heads/main/benchmarks/blocksworld-2/domain.pddl"
r = requests.get(URL_DOMAIN)
domain_file = io.StringIO(r.content.decode("utf-8"))

domain = parse_domain(domain_file)

# compute the normalization of the domain and print it on console
domain_norm = normalize(domain)
print(domain_to_string(domain_norm))

# compute the determinization of the domain and print it on console
domain_det = determinize(domain)
print(domain_to_string(domain_det))
```

To parse parse files that contain _both_ domain and problem together, we can use function `parse_domain_problem` in `fondutils.pddl`. Note how the following code also sets explicit domain suffix and operators prefixes and suffixes, and how we update the domain name in the problem to match the new one:

```python
import io
import inspect
from pathlib import Path
import requests

from pddl.formatter import domain_to_string, problem_to_string
from fondutils.pddl import parse_domain_problem
from fondutils.determizer import determinize
from fondutils.normalizer import normalize

# get a domain from AI-Planning/fond-domains repo
URL_DOMAIN = "https://raw.githubusercontent.com/AI-Planning/fond-utils/refs/heads/main/tests/domprob_03.pddl"
r = requests.get(URL_DOMAIN)
domain_file = io.StringIO(r.content.decode("utf-8"))

domain, problem = parse_domain_problem(domain_file)

# compute the determinization of the domain and print it on console
domain_det = determinize(domain, dom_suffix="XYZ", op_prefix="PRE", op_suffix="SUF")
print(domain_to_string(domain_det))

# update domain name in problem to match new domain name and print updated problem
problem._domain_name = domain_det.name
print(problem_to_string(problem))
```

## Format allowed on effects

The determinizer accepts effects that are an arbitrary nesting of `oneof`, conditional effects, and `and`.

If the effect is just one `oneof` clause, then it corresponds to the Unary Nondeterminism (1ND) Normal Form without conditionals in:

* Jussi Rintanen: [Expressive Equivalence of Formalisms for Planning with Sensing](https://gki.informatik.uni-freiburg.de/papers/Rintanen03expr.pdf). ICAPS 2003: 185-194

When there are many `oneof` clauses in a top-level `and` effect, the cross-product of all the `oneof` clauses will determine the deterministic actions.

## Authors

* **Sebastian Sardina** ([ssardina](https://github.com/ssardina)) - [RMIT University](https://www.rmit.edu.au)
* **Christian Muise** ([haz](https://github.com/haz)) - [Queen's University](https://www.queensu.ca)
