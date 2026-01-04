(define (domain blocks-domain)
    (:requirements :adl :equality :typing)
    (:predicates (f1) (f13) (f2) (f3))
    (:action test_DETDUP_1
        :parameters ()
        :precondition (f13)
        :effect (when (f1) (f2))
    )
     (:action test_DETDUP_2
        :parameters ()
        :precondition (f13)
        :effect (f3)
    )
)