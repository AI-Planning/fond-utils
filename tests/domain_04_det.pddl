(define (domain blocks-domain_ALLOUT)
    (:requirements :equality :typing)
    (:types
        block - object
    )
    (:predicates (clear ?b - block)  (emptyhand) (holding ?b - block)  (on ?b1 - block ?b2 - block)  (on-table ?b - block))
    (:action pick-up-from-table
        :parameters (?b - block)
        :precondition (and (emptyhand) (clear ?b) (on-table ?b))
        :effect (and (holding ?b) (not (emptyhand)) (not (on-table ?b)))
    )
     (:action pick-up_DETDUP_1
        :parameters (?b1 - block ?b2 - block)
        :precondition (and (not (= ?b1 ?b2)) (emptyhand) (clear ?b1) (on ?b1 ?b2))
        :effect (and (f1) (a1) (b1) (f3))
    )
     (:action pick-up_DETDUP_10
        :parameters (?b1 - block ?b2 - block)
        :precondition (and (not (= ?b1 ?b2)) (emptyhand) (clear ?b1) (on ?b1 ?b2))
        :effect (and (f1) (a2) (c3) (f3))
    )
     (:action pick-up_DETDUP_2
        :parameters (?b1 - block ?b2 - block)
        :precondition (and (not (= ?b1 ?b2)) (emptyhand) (clear ?b1) (on ?b1 ?b2))
        :effect (and (f1) (a1) (b2) (f3))
    )
     (:action pick-up_DETDUP_3
        :parameters (?b1 - block ?b2 - block)
        :precondition (and (not (= ?b1 ?b2)) (emptyhand) (clear ?b1) (on ?b1 ?b2))
        :effect (and (f1) (a1) (c1) (f3))
    )
     (:action pick-up_DETDUP_4
        :parameters (?b1 - block ?b2 - block)
        :precondition (and (not (= ?b1 ?b2)) (emptyhand) (clear ?b1) (on ?b1 ?b2))
        :effect (and (f1) (a1) (c2) (f3))
    )
     (:action pick-up_DETDUP_5
        :parameters (?b1 - block ?b2 - block)
        :precondition (and (not (= ?b1 ?b2)) (emptyhand) (clear ?b1) (on ?b1 ?b2))
        :effect (and (f1) (a1) (c3) (f3))
    )
     (:action pick-up_DETDUP_6
        :parameters (?b1 - block ?b2 - block)
        :precondition (and (not (= ?b1 ?b2)) (emptyhand) (clear ?b1) (on ?b1 ?b2))
        :effect (and (f1) (a2) (b1) (f3))
    )
     (:action pick-up_DETDUP_7
        :parameters (?b1 - block ?b2 - block)
        :precondition (and (not (= ?b1 ?b2)) (emptyhand) (clear ?b1) (on ?b1 ?b2))
        :effect (and (f1) (a2) (b2) (f3))
    )
     (:action pick-up_DETDUP_8
        :parameters (?b1 - block ?b2 - block)
        :precondition (and (not (= ?b1 ?b2)) (emptyhand) (clear ?b1) (on ?b1 ?b2))
        :effect (and (f1) (a2) (c1) (f3))
    )
     (:action pick-up_DETDUP_9
        :parameters (?b1 - block ?b2 - block)
        :precondition (and (not (= ?b1 ?b2)) (emptyhand) (clear ?b1) (on ?b1 ?b2))
        :effect (and (f1) (a2) (c2) (f3))
    )
)