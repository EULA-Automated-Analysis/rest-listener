""" Contains the Formal category sum and the sub heuristics
"""

from models.category import Category
from models.heuristics import typeconventions, easeofnavigation, documentlength

class Formal(Category):
    
    @staticmethod
    def get_heuristics():
        return {
            typeconventions.TypeConventions: 1,
            easeofnavigation.EaseOfNavigation: 1,
            documentlength.DocumentLength: 1
        }