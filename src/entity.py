from pigframe import World
from component import *
from utils import load_four_quiz
from copy import deepcopy
import random

def create_status(world: World, count_quiz: int = 20, remaining_time: int = 120) -> int:
    ent = world.create_entity()
    world.add_component_to_entity(ent, Status, 
            count_quiz = count_quiz,
            total_time = remaining_time,
            )
    return ent

def create_quizbox(world: World, quiz_path: str) -> int:
    ent = world.create_entity()
    quizbox = load_four_quiz(quiz_path)
    quizes = random.sample(quizbox.all_quizes, len(quizbox.all_quizes))
    world.add_component_to_entity(ent, QuizBox,
            count_quiz = quizbox.count_quiz,
            all_quizes = quizes,
            remaining = deepcopy(quizes),
        )
    return ent
