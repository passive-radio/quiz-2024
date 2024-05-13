import random
from copy import deepcopy

from pigframe import Event
from component import *

class EvReset(Event):
    def _Event__process(self):
        for ent, (status) in self.world.get_component(Status):
            status.score = 0
            status.count_correct = 0
            status.count_answered = 0
            status.elapsed_time = 0
            print("reset status")
        
        for ent, (quizbox) in self.world.get_component(QuizBox):
            quizbox.current_quiz = 0
            quizbox.answered = []
            quizbox.all_quizes = random.sample(quizbox.all_quizes, len(quizbox.all_quizes))
            quizbox.remaining = deepcopy(quizbox.all_quizes)
            print("reset quizbox")