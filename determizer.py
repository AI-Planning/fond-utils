import argparse

from pddl import parse_domain
from pddl.action import Action
from pddl.core import Domain
from pddl.formatter import domain_to_string
from pddl.logic.base import OneOf
from pddl.logic.effects import AndEffect
from pddl.requirements import Requirements


from normalizer import normalize

DEBUG = False


def determinize(domain: Domain) -> Domain:
    new_actions = []

    for act in domain.actions:

        if DEBUG:
            print(f"\nNormalizing action: {act.name}")

        new_act = normalize(act)
        if isinstance(new_act.effect, OneOf):
            counter = 1
            for eff in new_act.effect.operands:
                assert isinstance(
                    eff, AndEffect
                ), f"Effect in OneOf is not an AndEffect: {eff}"
                new_actions.append(
                    Action(
                        name=f"{act.name}_DETDUP_{counter}",
                        parameters=act.parameters,
                        precondition=act.precondition,
                        effect=eff,
                    )
                )
                counter += 1
        else:
            new_actions.append(new_act)

    return Domain(
        name=domain.name,
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


def main(domain_in, domain_out):
    domain = parse_domain(domain_in)
    det_domain = determinize(domain)
    with open(domain_out, "w") as f:
        f.write(domain_to_string(det_domain))


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
