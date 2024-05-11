from pigframe import Component
from dataclasses import dataclass, field
from typing import List, DefaultDict

@dataclass
class Status(Component):
    count_quiz: int
    total_time: int
    score: int = 0
    count_correct: int = 0
    count_answered: int = 0
    elapsed_time: int = 0
    
@dataclass
class FourQuiz(Component):
    question: str
    correct: int
    choices: List[str]
    answer: int = None
    
@dataclass
class QuizBox(Component):
    count_quiz: int
    all_quizes: List[FourQuiz]
    current_quiz: int = 0
    answered: List[FourQuiz] = field(default_factory=list)
    remaining: List[FourQuiz] = None