import pygame

class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, text, callback, color = (240,230,140), hover_color = (200, 200, 200)):
        super().__init__()                                  #sprite初始化
        self.font = pygame.font.SysFont(None, 80)           #字體
        self.text = text                                    #文字
        self.callback = callback                            #輸入按鈕按下所要執行的函式
        self.default_color = color                          #預設顏色
        self.hover_color = hover_color                      #觸碰顏色
        self.image = self.font.render(self.text, True, (0, 0, 0), self.default_color)  #建立surface
        self.rect = self.image.get_rect(center=(x, y))      #碰撞箱
        self.mouse_pre_pressed = 0                          #是否點擊
        self.mouse_pressed = 0


    def update(self,scene_ctrl):
        mouse_pos = pygame.mouse.get_pos()                       #拿鼠標座標
        self.mouse_pre_pressed = self.mouse_pressed
        self.mouse_pressed = pygame.mouse.get_pressed()[0]       #是否點擊

        # 滑鼠碰到就變顏色
        if self.rect.collidepoint(mouse_pos):
            self.image = self.font.render(self.text, True, (0, 0, 0), self.hover_color)
            if self.mouse_pressed and scene_ctrl.button_cd == 0 and not self.mouse_pre_pressed:
                scene_ctrl.button_cd = 60
                self.callback()
        else:
            self.image = self.font.render(self.text, True, (0, 0, 0), self.default_color)

def on_click(scene_ctrl,num):
    scene_ctrl.num = num
    print(scene_ctrl.num)

def resuming(scene_ctrl, num1):
    scene_ctrl.menu = num1

def backpack(scene_ctrl, num2):
    scene_ctrl.backpack = num2

def reset(scene_ctrl, num3):
    scene_ctrl.reset = num3

def go_home(scene_ctrl):
    scene_ctrl.num = 0
    scene_ctrl.menu = 0

def quit_button():
    pygame.quit()
    exit()
