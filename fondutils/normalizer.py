from pddl.action import Action
from pddl.core import Domain
from pddl.logic.base import OneOf, Not, And
from pddl.logic.effects import When, Forall
from pddl.logic.predicates import Predicate
from pddl.requirements import Requirements
from pddl.logic.functions import (
    Increase,
    Decrease,
    Divide,
    ScaleDown,
    ScaleUp,
    Plus,
    Minus,
    Times,
    Assign,
)

from itertools import product, chain

DEBUG = False


def normalize(domain: Domain, dom_suffix: str = "") -> Domain:
    new_actions = []

    # make sure the domain name is well-formed and suffix separated form original name with an underscore
    if dom_suffix != "" and dom_suffix[0] != "_":
        dom_suffix = "_" + dom_suffix

    for act in domain.actions:
        if DEBUG:
            print(f"\nNormalizing action: {act.name}")

        new_actions.append(normalize_operator(act))

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


def normalize_operator(op):

    effs = flatten(op.effect)

    if len(effs) == 1:
        eff = effs[0]
    else:
        # Normalize to wrap every operand of an OneOf in an And effect
        for i in range(len(effs)):
            if not isinstance(effs[i], And):
                effs[i] = And(effs[i])

        # As an optimization, compress one level of nested And effects on the outcomes
        new_outcomes = []
        for outcome in effs:
            if isinstance(outcome, And):
                new_operands = []
                for operand in outcome.operands:
                    if isinstance(operand, And):
                        new_operands.extend(operand.operands)
                    else:
                        new_operands.append(operand)
                new_outcomes.append(And(*new_operands))
            else:
                new_outcomes.append(outcome)

        eff = OneOf(*new_outcomes)

    return Action(
        name=op.name, parameters=op.parameters, precondition=op.precondition, effect=eff
    )


def flatten(eff):
    return _flatten(eff)


def combine(eff_lists):
    if DEBUG:
        print("\nCombining:\n%s" % "\n".join(map(str, eff_lists)))
    combos = list(product(*eff_lists))
    combined_oneofs = [And(*[x for x in choice if x != And()]) for choice in combos]
    if DEBUG:
        print("Result: %s\n" % combined_oneofs)
    return combined_oneofs


def _flatten(eff):

    if DEBUG:
        print("Flattening %s" % str(eff))

    if isinstance(eff, Forall):
        if (len(flatten(eff.effect)) > 1):
            raise ValueError("Oneof cannot be used within effect type: %s" % type(eff))
        return [eff]

    if isinstance(eff, And):
        if 0 == len(eff.operands):
            return [eff]
        else:
            return combine(list(map(_flatten, eff.operands)))

    elif isinstance(eff, OneOf):
        return list(chain(*(list(map(_flatten, eff.operands)))))

    elif isinstance(eff, When):
        return [When(eff.condition, res) for res in _flatten(eff.effect)]

    # Default cases
    # There's an assumption here that everything underneath doesn't need flattening; hence no recursive call.
    elif isinstance(eff, (Not, Predicate)):  # classical logical
        return [eff]
    elif isinstance(    # metric effects
        eff,
        (Increase, Decrease, Divide, ScaleDown, ScaleUp, Plus, Minus, Times, Assign),
    ):
        return [eff]

    else:
        if DEBUG:
            print("Base: %s" % str(eff))
        raise ValueError("Unexpected effect type: %s" % type(eff))
