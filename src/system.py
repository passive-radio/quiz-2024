from pigframe import System
import pyxel
from copy import deepcopy
import random

from component import *

class SyElapse(System):
    def process(self):
        for ent, (status) in self.world.get_component(Status):
            fps = self.world.FPS
            if self.world.frame_count % fps == 0:
                status.elapsed_time += 1

class SyAnswer(System):
    def process(self):
        for ent, (quizbox) in self.world.get_component(QuizBox):
            quizbox: QuizBox
            if quizbox.remaining is None or len(quizbox.remaining) == 0:
                return
            
            quiz = quizbox.remaining[0]
            qa_dict = {
                1: self.world.actions.a_p,
                2: self.world.actions.f_p,
                3: self.world.actions.j_p,
                4: self.world.actions.l_p,
            }
            
            answer = None
            for key, action in qa_dict.items():
                if action is True:
                    answer = key
                    break
            
            # If no answer, return
            if answer is None:
                return
            
            for ent, (status) in self.world.get_component(Status):
                if answer == quiz.correct:
                    status.count_answered += 1
                    status.score += 1
                    status.count_correct += 1
                    print("correct")
                    pyxel.playm(0)
                else:
                    status.count_answered += 1
                    print("wrong")
                    pyxel.playm(1)
            
            quizbox.answered.append(quiz)
            quizbox.remaining.pop(0)
            quizbox.current_quiz += 1
            
class SyToResult(System):
    def process(self):
        ent_quizbox, quizbox = self.world.get_component(QuizBox)[0]
        ent_status, status = self.world.get_component(Status)[0]
        
        if status.count_answered == status.count_quiz:
            self.world.scene_manager.next_scene = "result"
            print("change scene to result 1")
            return
        
        if status.elapsed_time >= status.total_time:
            self.world.scene_manager.next_scene = "result"
            print("change scene to result 2")
            return
        
        if quizbox.remaining is None or len(quizbox.remaining) == 0:
            self.world.scene_manager.next_scene = "result"
            print("change scene to result 3")
            return
        
class SyReset(System):
    def process(self):
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
        
        # self.world.scene_manager.next_scene = "start"