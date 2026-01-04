import argparse

from pddl.action import Action
from pddl.core import Domain
from pddl.logic.base import OneOf, And, Not
from pddl.logic.effects import When
from pddl.logic.predicates import Predicate
from pddl.requirements import Requirements


from .normalizer import normalize_operator

DEBUG = True


def determinize(domain: Domain, dom_suffix: str = "ALLOUT", op_prefix: str = "_DETDUP_", op_suffix: str = "") -> Domain:
    """Computes the all-outcome deterministic version of a FOND domain.

    Each non-deterministic operator is replaced by a set of deterministic operators, one for each possible outcome.

    The name of the new operators is the name of the original operator with a prefix, a counter, and a suffix; for example, the operator "move" with two possible outcomes will be replaced by two operators named "move<PREFIX>01<SUFFIX>" and "move<PREFIX>02<SUFFIX>".

    The name of the new domain is the name of the original domain with a suffix, for example, the domain "blocks" will be replaced by the domain "blocks_ALLOUT".

    Args:
        domain (Domain): the FOND domain to be determinized
        dom_suffix (str, optional): the suffix on the resulting domain name. Defaults to "ALLOUT".
        op_prefix (str, optional): the prefix for action name before the number. Defaults to "DETDUP".
        op_suffix (str, optional): the suffix for action name after the number. Defaults to no suffix.

    Returns:
        Domain: the all outcome determinized domain
    """
    new_actions = []

    # make sure original names of actions and domain name are separated with an underscore _
    if op_prefix == "":
        op_prefix = "_"
    if dom_suffix != "" and dom_suffix[0] != "_":
        dom_suffix = "_" + dom_suffix

    for act in domain.actions:
        if DEBUG:
            print(f"\nNormalizing action: {act.name}")

        new_act = normalize_operator(act)
        if isinstance(new_act.effect, OneOf):
            counter = 1
            for eff in new_act.effect.operands:
                assert isinstance(
                    eff, (And, Predicate, Not, When)
                ), f"Effect in OneOf is not an And effect: {eff}"
                new_actions.append(
                    Action(
                        name=f"{act.name}{op_prefix}{counter}{op_suffix}",
                        parameters=act.parameters,
                        precondition=act.precondition,
                        effect=eff,
                    )
                )
                counter += 1
        else:
            new_actions.append(new_act)

    return Domain(
        name=domain.name + dom_suffix,
        requirements=frozenset(
            [r for r in domain.requirements if r is not Requirements.NON_DETERMINISTIC]
        ),
        types=domain.types,
        constants=domain.constants,
        predicates=domain.predicates,
        actions=new_actions,
        functions=domain.functions,
        derived_predicates=domain.derived_predicates,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "domain",
        help="Input (non-deterministic) domain file",
    )
    parser.add_argument(
        "det_domain",
        help="Output (deterministic) domain file",
    )
    args = parser.parse_args()
    main(args.domain, args.det_domain)
