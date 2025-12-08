(define (domain blocks-domain_ALLOUT)
    (:requirements :equality :typing)
    (:types
        block - object
    )
    (:predicates (clear ?b - block)  (emptyhand) (holding ?b - block)  (on ?b1 - block ?b2 - block)  (on-table ?b - block))
    (:action pick-up_DETDUP_1
        :parameters (?b1 - block ?b2 - block)
        :precondition (and (not (= ?b1 ?b2)) (emptyhand) (clear ?b1) (on ?b1 ?b2))
        :effect (and (holding ?b1) (clear ?b2) (not (emptyhand)) (not (clear ?b1)) (not (on ?b1 ?b2)))
    )
     (:action pick-up_DETDUP_2
        :parameters (?b1 - block ?b2 - block)
        :precondition (and (not (= ?b1 ?b2)) (emptyhand) (clear ?b1) (on ?b1 ?b2))
        :effect (and (clear ?b2) (on-table ?b1) (not (on ?b1 ?b2)))
    )
     (:action pick-up_DETDUP_3
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