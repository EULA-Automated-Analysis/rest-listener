from models.heuristic import Heuristic


class EaseOfNavigation(Heuristic):
    def score(self, input):
        return {'score': 5, 'max': 5}