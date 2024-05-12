import pygame_gui
import Board
import pygame
import GameManager

class MainClass(object):
    def __init__(self) -> None:
        self.CurrentDisplay = StartMenu(self)

    def main(self):
        self.CurrentDisplay.Run()
        

class GameScreen(object):
    def __init__(self, difficulty, isDifficultyDisabled) -> None:
        self.difficulty = difficulty
        self.isDifficultyDisabled = isDifficultyDisabled
    def Run(self):
        pygame.init()
        screen = pygame.display.set_mode((600, 600))
        pygame.display.set_caption('Othello')
        pygame.display.flip()
        
        game_manager = GameManager.GameManager(screen, Board.Board(screen, 8),self.difficulty,self.isDifficultyDisabled)
        game_manager.RunGame()

class StartMenu(object):
    def __init__(self, mainClass) -> None:
        self.mainClass = mainClass
        self.difficulty_level = 1
        self.isDifficultyDisabled = True

    def Run(self):
        pygame.init()
        screen = pygame.display.set_mode((600, 600))
        pygame.display.set_caption('Othello')
        pygame.display.flip()
        manager = pygame_gui.UIManager((600, 600))
        background = pygame.Surface((800, 600))
        background.fill((4, 175, 112))
        self.DrawGUI(manager,screen, background)

    def DrawGUI(self, manager,screen,background):
        start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 200), (100, 50)), text='Start', manager=manager)
        
        dropDownList = pygame_gui.elements.UIDropDownMenu(options_list=["Player Vs Player", "Player Vs AI"],
                                                        starting_option="Player Vs Player",
                                                        relative_rect=pygame.Rect((300, 300), (200, 50)),
                                                        manager=manager)
        
        AIDifficultyList = pygame_gui.elements.UIDropDownMenu(options_list=["Easy", "Medium", "Hard"],
                                                            starting_option="Easy",
                                                            relative_rect=pygame.Rect((100, 300), (200, 50)),
                                                            manager=manager)

        AIDifficultyList.disable()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit(0)
                    
                manager.process_events(event)
                
                if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                    if event.ui_element == dropDownList:
                        selected_value = event.text
                        if selected_value == "Player Vs AI":
                            AIDifficultyList.enable()
                            self.isDifficultyDisabled = False
                        else:
                            AIDifficultyList.disable()
                            self.isDifficultyDisabled = True
                            
                    if event.ui_element == AIDifficultyList:
                        selected_difficulty = event.text
                        if selected_difficulty == "Easy":
                            self.difficulty_level = 1
                        elif selected_difficulty == "Medium":
                            self.difficulty_level = 3
                        elif selected_difficulty == "Hard":
                            self.difficulty_level = 5

                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == start_button:
                        self.StartGame()

            manager.update(1/60)
            screen.blit(background, (0, 0))
            manager.draw_ui(screen)
            pygame.display.flip()


    def StartGame(self):
        self.mainClass.CurrentDisplay = GameScreen(self.difficulty_level, self.isDifficultyDisabled)
        self.mainClass.CurrentDisplay.Run()

        
mainclass = MainClass() 
mainclass.main()
                

    



