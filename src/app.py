from pigframe import World
import pyxel

from entity import *
from component import *
from system import *
from screen import *
from action import *
from event import *

from text import BDFRenderer

class App(World):
    def __init__(self):
        super().__init__()
        self.init()
        
    def init(self):
        self.FPS = 60
        self.TITLE = "クイズゲーム"
        self.SCREEN_SIZE = (640, 480)
        self.BASE_BG_COLOR = 13
        pyxel.init(self.SCREEN_SIZE[0], self.SCREEN_SIZE[1],
                title = self.TITLE, fps = self.FPS)
        pyxel.colors[0] = 0x141414
        pyxel.load("assets/resource.pyxres")
        self.font_s = BDFRenderer("assets/b14.bdf")
        self.font_m = BDFRenderer("assets/b16.bdf")
        self.font_l = BDFRenderer("assets/b24.bdf")
        
        pyxel.mouse(True)
        
    def reset(self):
        pass
    
    def draw(self):
        pyxel.cls(self.BASE_BG_COLOR)
        self.process_screens()
        
    def update(self):
        self.frame_count = pyxel.frame_count
        self.scene_manager.update_scene()
        self.process_user_actions()
        self.scene_manager._SceneManager__process_events()
        self.process_events()
        self.process_systems()
        self.scene_manager._SceneManager__process_transitions()
    
    def run(self):
        pyxel.run(self.update, self.draw)
        
if __name__ == "__main__":
    app = App()
    app.add_scenes(["start", "answering", "answered", "result"])
    app.current_scene = "start"
    
    app.set_user_actions_map(Actions())

    app.add_system_to_scenes(SyElapse, "answering", 0)
    app.add_system_to_scenes(SyAnswer, "answering", 1)
    app.add_system_to_scenes(SyToResult, "answering", 2)
    app.add_system_to_scenes(SyReset, "result", 0)

    app.add_screen_to_scenes(ScStart, "start", 0)
    app.add_screen_to_scenes(ScStatusInAnswering, "answering", 0)
    app.add_screen_to_scenes(ScFourQuiz, "answering", 1)
    app.add_screen_to_scenes(ScResult, "result", 0)

    create_status(app, count_quiz = 29, remaining_time = 120)
    create_quizbox(app, "assets/four_quizes.csv")

    # シーン遷移の定義
    app.add_scene_transition("start", "answering", lambda: app.actions.mouse_left_p)
    app.add_scene_transition("result", "start", lambda: app.actions.mouse_left_p)
    app.run()