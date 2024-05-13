from pigframe import Screen
import pyxel
from abc import ABCMeta, abstractmethod

from component import *
from text import BDFRenderer

class BaseScreen(Screen, metaclass=ABCMeta):
    def __init__(self, world, priority: int = 0, **kwargs) -> None:
        super().__init__(world, priority, **kwargs)
        self.font_s: BDFRenderer = self.world.font_s
        self.font_m: BDFRenderer = self.world.font_m
        self.font_l: BDFRenderer = self.world.font_l
        self.SCREEN_SIZE = self.world.SCREEN_SIZE
    
    @abstractmethod
    def draw(self):
        pass

class ScStart(BaseScreen):
    def draw(self):
        title = self.world.TITLE
        len_title = len(title)
        title_x = (self.SCREEN_SIZE[0] - len_title * 24) // 2
        title_y = 200
        self.font_l.draw_text(title_x, title_y, title, 1)
        
        guide_text = "画面をクリックでスタート"
        guide_x = (self.SCREEN_SIZE[0] - len(guide_text) * 16) // 2
        guide_y = 240
        self.font_m.draw_text(guide_x, guide_y, guide_text, 0)
        
class ScStatusInAnswering(BaseScreen):
    def draw(self):
        screen_size = self.SCREEN_SIZE
        base_x = screen_size[0] - 96
        base_y = 12
        font_s = self.font_s
        font_m = self.font_m
        font_l = self.font_l
        
        pyxel.rect(base_x, base_y, 90, 100, 7)
        for ent, (status) in self.world.get_component(Status):
            score_text = f"SCORE: {status.score}"
            font_m.draw_text(base_x, base_y, score_text, 0)
            
            correct_text = f"正解: {status.count_correct}"
            font_s.draw_text(base_x, base_y + 28, correct_text, 0)
            
            answered_text = f"回答: {status.count_answered}"
            font_s.draw_text(base_x, base_y + 48, answered_text, 0)
            
            remaining_time = status.total_time - status.elapsed_time
            remaining_text = f"経過時間:"
            font_s.draw_text(base_x, base_y + 68, remaining_text, 0)
            
            remaining_time_text = f"{remaining_time}/{status.total_time}"
            font_m.draw_text(base_x + 22, base_y + 84, remaining_time_text, 0)

class ScFourQuiz(BaseScreen):
    def draw(self):
        screen_size = self.SCREEN_SIZE
        base_x = 20
        base_y = 20
        font_s = self.font_s
        font_m = self.font_m
        font_l = self.font_l
        
        for ent, (quizbox) in self.world.get_component(QuizBox):
            quizbox: QuizBox
            if quizbox.remaining is None or len(quizbox.remaining) == 0:
                return
            
            quiz = quizbox.remaining[0]
            question = quiz.question
            
            guide = "問題"
            font_l.draw_text(base_x, base_y, guide, 0)
            pyxel.rect(base_x, base_y + 28, 480, 2, 0)
            # pyxel.rect(base_x, base_y + 32, 600, 100, 7)
            
            # font_l.draw_text(base_x, base_y + 36, question, 0)
            question_text_size = 24
            lines = self._draw_text_lines(question, question_text_size,
                                        base_x, base_y + 36, 4)
            
            choices_y = base_y + 52 + lines * question_text_size
            
            choice_keys = [
                "A", "F", "J", "L"
            ]
            
            for i, choice in enumerate(quiz.choices):
                choice_text = f"{choice_keys[i]}: {choice}"
                font_m.draw_text(base_x + 10, choices_y + i * 24, choice_text, 0)
                
    def _draw_text_lines(self, text: str, size: str, x: int, y: int, space_y: int = 2) -> int:
        """Draw text with line break if the text is too long.
        
        Args:
            text (str): text to draw
            size (int): font size
            x (int): x position
            y (int): y position
            space_y (int): space between lines
        
        Returns:
            int: number of lines
        """
        current_x = 0
        texts_to_draw = []
        remaining_text = text
        
        for i, letter in enumerate(text):
            current_x += 1
            if current_x * size >= 512:
                current_x = 0
                texts_to_draw.append(text[:i])
                remaining_text = text[i:]
                
        texts_to_draw.append(remaining_text)
        for i, text in enumerate(texts_to_draw):
            self.font_l.draw_text(x, y + i * (size + space_y) , text, 0)
            
        return len(texts_to_draw)
    
class ScResult(BaseScreen):
    def draw(self):
        screen_size = self.SCREEN_SIZE
        base_x = 20
        base_y = 20
        font_s = self.font_s
        font_m = self.font_m
        font_l = self.font_l
        
        ent, status = self.world.get_component(Status)[0]
        status: Status
        
        result_text = "クイズ終了！"
        result_text_x = (screen_size[0] - len(result_text) * 24) // 2
        font_l.draw_text(result_text_x, base_y + 12, result_text, 0)
        
        correct_text = f"全{status.count_answered}問中{status.count_correct}問正解でした"
        correct_text_x = (screen_size[0] - len(correct_text) * 24) // 2
        font_l.draw_text(correct_text_x, screen_size[1]//2 - 120, correct_text, 0)
        
        score_text = f"SCORE: {status.score}"
        score_text_x = correct_text_x
        font_l.draw_text(score_text_x, screen_size[1]//2 - 60, score_text, 0)
        
        remaining_time = status.total_time - status.elapsed_time
        remaining_time_text = f"(経過時間: {remaining_time}/{status.total_time}) [秒]"
        remaining_time_text_x = correct_text_x
        font_m.draw_text(remaining_time_text_x, screen_size[1]//2 - 20, remaining_time_text, 0)
        
        result_text = "画面をクリックで再挑戦！"
        font_l.draw_text(correct_text_x, screen_size[1]//2 + 20, result_text, (pyxel.frame_count * 3 //self.world.FPS) % 16)