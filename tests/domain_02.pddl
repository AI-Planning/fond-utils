;; multiple oneof cross product
(define (domain blocks-domain)
  (:requirements :non-deterministic :equality :typing)
  (:types block)
  (:predicates (holding ?b - block) (emptyhand) (on-table ?b - block) (on ?b1 ?b2 - block) (clear ?b - block))
  (:action pick-up
    :parameters (?b1 ?b2 - block)
    :precondition (and (not (= ?b1 ?b2)) (emptyhand) (clear ?b1) (on ?b1 ?b2))
    :effect
      (and (f1)
        (oneof (a1) (a2))
        (oneof (b1) (b2))
        (oneof (c1) (c2) (c3))
        (f3)
      )
  )
  (:action pick-up-from-table
    :parameters (?b - block)
    :precondition (and (emptyhand) (clear ?b) (on-table ?b))
    :effect ( and (holding ?b) (not (emptyhand)) (not (on-table ?b)))
  )
)
