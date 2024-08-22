import argparse

from pddl.action import Action
from pddl.core import Domain
from pddl.logic.base import OneOf
from pddl.logic.effects import AndEffect
from pddl.requirements import Requirements


from fondutils.normalizer import normalize_operator

DEBUG = False


def determinize(domain: Domain) -> Domain:
    new_actions = []

    for act in domain.actions:

        if DEBUG:
            print(f"\nNormalizing action: {act.name}")

        new_act = normalize_operator(act)
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
