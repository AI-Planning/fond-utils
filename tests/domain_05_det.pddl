(define (domain blocks-domain_ALLOUT)
    (:requirements :equality :typing)
    (:types
        block - object
    )
    (:predicates (clear ?b - block)  (emptyhand) (emptyhead) (holding ?b - block)  (on ?b1 - block ?b2 - block)  (on-table ?b - block))
    (:action pick-up-complex01_DETDUP_1
        :parameters (?b1 - block ?b2 - block)
        :precondition (and (not (= ?b1 ?b2)) (emptyhand) (clear ?b1) (on ?b1 ?b2))
        :effect (and (clear ?b2) (clear ?b1) (holding ?b1) (not (emptyhand)) (not (clear ?b1)) (not (on ?b1 ?b2)))
    )
     (:action pick-up-complex01_DETDUP_2
        :parameters (?b1 - block ?b2 - block)
        :precondition (and (not (= ?b1 ?b2)) (emptyhand) (clear ?b1) (on ?b1 ?b2))
        :effect (and (clear ?b2) (clear ?b1) (on-table ?b1) (not (on ?b1 ?b2)))
    )
     (:action pick-up-empty_DETDUP_1
        :parameters (?b1 - block ?b2 - block)
        :precondition (and (not (= ?b1 ?b2)) (emptyhand) (clear ?b1) (on ?b1 ?b2))
        :effect (and )
    )
     (:action pick-up-empty_DETDUP_2
        :parameters (?b1 - block ?b2 - block)
        :precondition (and (not (= ?b1 ?b2)) (emptyhand) (clear ?b1) (on ?b1 ?b2))
        :effect (and (clear ?b2) (on-table ?b1) (not (on ?b1 ?b2)))
    )
     (:action pick-up-super-complex_DETDUP_1
        :parameters (?b1 - block ?b2 - block)
        :precondition (and (not (= ?b1 ?b2)) (emptyhand) (clear ?b1) (on ?b1 ?b2))
        :effect (and (emptyhead) (clear ?b2) (clear ?b1) (emptyhand) (holding ?b1))
    )
     (:action pick-up-super-complex_DETDUP_2
        :parameters (?b1 - block ?b2 - block)
        :precondition (and (not (= ?b1 ?b2)) (emptyhand) (clear ?b1) (on ?b1 ?b2))
        :effect (and (emptyhead) (clear ?b2) (clear ?b1) (emptyhand) (holding ?b2))
    )
     (:action pick-up-super-complex_DETDUP_3
        :parameters (?b1 - block ?b2 - block)
        :precondition (and (not (= ?b1 ?b2)) (emptyhand) (clear ?b1) (on ?b1 ?b2))
        :effect (and (emptyhead) (clear ?b2) (clear ?b1) (emptyhand) (on ?b1 ?b2))
    )
     (:action pick-up-super-complex_DETDUP_4
        :parameters (?b1 - block ?b2 - block)
        :precondition (and (not (= ?b1 ?b2)) (emptyhand) (clear ?b1) (on ?b1 ?b2))
        :effect (and (emptyhead) (holding ?b2) (holding ?b1) (emptyhand))
    )
     (:action pick-up-super-complex_DETDUP_5
        :parameters (?b1 - block ?b2 - block)
        :precondition (and (not (= ?b1 ?b2)) (emptyhand) (clear ?b1) (on ?b1 ?b2))
        :effect (and (emptyhead) (holding ?b2) (holding ?b1) (emptyhand))
    )
     (:action pick-up-super-complex_DETDUP_6
        :parameters (?b1 - block ?b2 - block)
        :precondition (and (not (= ?b1 ?b2)) (emptyhand) (clear ?b1) (on ?b1 ?b2))
        :effect (and (emptyhead) (holding ?b2) (holding ?b1) (emptyhand) (on ?b1 ?b2))
    )
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
)