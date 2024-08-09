
from pddl.action import Action
from pddl.logic.base import OneOf, Not
from pddl.logic.effects import When, AndEffect
from pddl.logic.predicates import Predicate

from itertools import product, chain

DEBUG = False

def normalize(op):

    effs = flatten(op.effect)

    if len(effs) == 1:
        eff = effs[0]
    else:
        # Normalize to wrap every operand of an OneOf in an AndEffect
        for i in range(len(effs)):
            if not isinstance(effs[i], AndEffect):
                effs[i] = AndEffect(effs[i])
        
        # As an optimization, compress one level of nested AndEffects on the outcomes
        new_outcomes = []
        for outcome in effs:
            if isinstance(outcome, AndEffect):
                new_operands = []
                for operand in outcome.operands:
                    if isinstance(operand, AndEffect):
                        new_operands.extend(operand.operands)
                    else:
                        new_operands.append(operand)
                new_outcomes.append(AndEffect(*new_operands))
            else:
                new_outcomes.append(outcome)

        eff = OneOf(*new_outcomes)

    return Action(
        name=op.name,
        parameters=op.parameters,
        precondition=op.precondition,
        effect=eff)

def flatten(eff):
    return _flatten(eff)

def combine(eff_lists):
    combos = list(product(*eff_lists))
    combined_oneofs = [AndEffect(*[x for x in choice if x != AndEffect([])]) for choice in combos]
    if DEBUG:
        print ("\nCombining:\n%s" % '\n'.join(map(str, eff_lists)))
        print ("Result: %s\n" % combined_oneofs)
    return combined_oneofs

def _flatten(eff):

    if DEBUG:
        print ("Flattening %s" % str(eff))

    if isinstance(eff, AndEffect):
        if 0 == len(eff.operands):
            return [eff]
        else:
            return combine(list(map(_flatten, eff.operands)))

    elif isinstance(eff, OneOf):
        return list(chain(*(list(map(_flatten, eff.operands)))))

    elif isinstance(eff, When):
        return [When(eff.condition, res) for res in _flatten(eff.effect)]

    # Default cases
    elif isinstance(eff, Not):
        return [eff]

    elif isinstance(eff, Predicate):
        return [eff]
    
    else:
        if DEBUG:
            print ("Base: %s" % str(eff))
        raise ValueError("Unexpected effect type: %s" % type(eff))
        # return [eff]