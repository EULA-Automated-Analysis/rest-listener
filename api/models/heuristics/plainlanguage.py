from models.heuristic import Heuristic
from readcalc import readcalc

class PlainLanguage(Heuristic):
    def score(self, input):

        text = input.text

        calc = readcalc.ReadCalc(text)
        grade = calc.get_flesch_kincaid_grade_level()

        if grade < 8:
            score = 4
        elif grade < 10:
            score = 3
        elif grade < 12:
            score = 2
        else:
            score = 0

        return {'score': score, 'max': 4}