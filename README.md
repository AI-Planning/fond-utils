# FOND Utilities

Utilities for parsing and manipulating the FOND planning language.

In the _all-outcome determinization_, each non-deterministic action is replaced with a set of deterministic actions, each encoding one possible effect outcome of the action. A solution in the deterministic version amounts to a weak plan solution in the original FOND problem.

Note this determinizer produces another PDDL domain and does not deal with the problem itself, unlike the SAS-based determinizers used in other planners like [PRP](https://github.com/QuMuLab/planner-for-relevant-policies), [FONDSAT](https://github.com/tomsons22/FOND-SAT), or [CFOND-ASP](https://github.com/ssardina-research/cfond-asp) that produces a SAS encoding of the determinization of a specific instance planning problem and are based on the SAS translator in [Fast-Downard](https://github.com/aibasel/downward) classical planner. For these determinizers that output SAS encodings, please refer to the individual planners or the [translator-fond](https://github.com/ssardina-research/translator-fond) repo.

## Pre-requisites

The script relies on the [pddl](https://github.com/AI-Planning/pddl) parser, which can be easily installed via:

```shell
$ pip install pddl
```

The pddl system relies itself on the [lark](https://lark-parser.readthedocs.io/en/stable/) parsing library.

This repo extends `pddl` to accept single files containing both the domain and the problem instance, and will be extended further to accept labelled outcomes in the effects.

## Example runs

The system is provided as a module `fondutils`. To just check that the PDDL input file is parsed well, just issue the command `check` and report to console:

```shell
$ python -m fondutils check --input tests/domain_03.pddl
```

To perform the determinization:

```shell
$ python -m fondutils determinize --input tests/domain_03.pddl --output determinized-domain.pddl
```

To simply perform normalization (i.e., have a single top-level oneof clause in the effect):

```shell
$ python -m fondutils normalize --input tests/domain_03.pddl --output normalized-domain.pddl
```

Deterministic versions of non-deterministic actions will be indexed with term `__DETDUP_<n>_DETDUP__`, similar to [PRP](https://github.com/QuMuLab/planner-for-relevant-policies)'s original determinizer. The name of the determinized domain will be the original name with suffix `_ALLOUT`. The name of the normalized domain will be the original name with suffix `_NORM`.

To change the prefix `__DETDUP_` or suffix `_DETDUP__`, use the options `--prefix` and `--suffix`. To get the resulting PDDL printed on console use `--console`:

```lisp
$ python -m fondutils determinize --input tests/domain_03.pddl --console --suffix "VER" --output output.pddl
(define (domain blocks-domain_ALLOUT)
    (:requirements :equality :typing)
    (:types block)
    (:predicates (clear ?b - block)  (emptyhand) (holding ?b - block)  (on ?b1 - block ?b2 - block)  (on-table ?b - block))
    (:action pick-tower
        :parameters (?b1 - block ?b2 - block ?b3 - block)
        :precondition (and (emptyhand) (on ?b1 ?b2) (on ?b2 ?b3))
        :effect (and (holding ?b2) (clear ?b3) (not (emptyhand)) (not (on ?b2 ?b3)))
    )
     (:action pick-up-from-table
        :parameters (?b - block)
        :precondition (and (emptyhand) (clear ?b) (on-table ?b))
        :effect (and (holding ?b) (not (emptyhand)) (not (on-table ?b)))
    )
     (:action pick-up_VER_0
        :parameters (?b1 - block ?b2 - block)
        :precondition (and (not (= ?b1 ?b2)) (emptyhand) (clear ?b1) (on ?b1 ?b2))
        :effect (and (holding ?b1) (clear ?b2) (not (emptyhand)) (not (clear ?b1)) (not (on ?b1 ?b2)))
    )
     (:action pick-up_VER_1
        :parameters (?b1 - block ?b2 - block)
        :precondition (and (not (= ?b1 ?b2)) (emptyhand) (clear ?b1) (on ?b1 ?b2))
        :effect (and (clear ?b2) (on-table ?b1) (not (on ?b1 ?b2)))
    )
     (:action put-down
        :parameters (?b - block)
        :precondition (holding ?b)
        :effect (and (on-table ?b) (emptyhand) (clear ?b) (not (holding ?b)))
    )
...
```

Note this resulting PDDL domain is now deterministic and can then be used as input to the original [Fast-Downard](https://github.com/aibasel/downward) SAS translator.

## Format allowed on effects

The determinizer accepts effects that are an arbitrary nesting of `oneof`, conditional effects, and `and`.

If the effect is just one `oneof` clause, then it corresponds to the Unary Nondeterminism (1ND) Normal Form without conditionals in:

* Jussi Rintanen: [Expressive Equivalence of Formalisms for Planning with Sensing](https://gki.informatik.uni-freiburg.de/papers/Rintanen03expr.pdf). ICAPS 2003: 185-194

When there are many `oneof` clauses in a top-level `and` effect, the cross-product of all the `oneof` clauses will determine the deterministic actions.

## Authors

* **Sebastian Sardina** ([ssardina](https://github.com/ssardina)) - [RMIT University](https://www.rmit.edu.au)
* **Christian Muise** ([haz](https://github.com/haz)) - [Queen's University](https://www.queensu.ca)
