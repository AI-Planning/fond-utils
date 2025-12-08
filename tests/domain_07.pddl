;; multiple oneof cross product
(define (domain blocks-domain)
  (:requirements :non-deterministic :equality :typing :adl)
  (:predicates
    (f1) (f2) (f3) (f13)
  )

  (:action test
    :parameters ()
    :precondition (and (f13))
    :effect (oneof
      (when
        (f1)
        (f2))
      (f3)
    )
  )
)