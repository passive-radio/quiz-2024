import csv
import pygame
from pygame.locals import*
from component import FourQuiz, QuizBox

def load_four_quiz(filepath: str) -> QuizBox:
    """Load quiz from CSV file.

    Args:
        filepath (str): filepath of CSV file

    Returns:
        int: id of QuizBox entity
    """
    
    quizes = []
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if i == 0:
                continue
            
            quiz = FourQuiz(
                question = row[0],
                correct = int(row[2]),
                answer = None,
                choices = row[3:],
            )
            quizes.append(quiz)
    
    quizbox = QuizBox(
        count_quiz = len(quizes),
        all_quizes = quizes,
    )
    
    return quizbox
