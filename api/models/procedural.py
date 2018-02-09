""" Contains the Procedural category sum and the sub heuristics
"""

from category import Category
from heuristic import Heuristic

from heuristics.mobileaccessibility import MobileAccessibility
from heuristics.mobilereadability import MobileReadability

class Procedural(Category):

    def evaluate(self, input):

        heuristics_to_eval = [MobileAccessibility, MobileReadability]

        weighted_score = 0
        heuristic_scores = dict((heur.__name__, heur().score(input)) for heur in heuristics_to_eval)

        return {
            'weighted_score': weighted_score,
            'heuristics': heuristic_scores
        }