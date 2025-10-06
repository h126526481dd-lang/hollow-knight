import pygame

class Button(pygame.sprite.Sprite):
    
    def __init__(self, x, y, text, callback, color = (100,100,100), hover_color = (200, 200, 200)):
        super().__init__()                                  #sprite初始化
        self.font = pygame.font.SysFont(None, 40)              #字體
        self.text = text                                    #文字
        self.callback = callback                            #輸入按鈕按下所要執行的函式
        self.default_color = color                #預設顏色
        self.hover_color = hover_color                  #觸碰顏色
        self.image = self.font.render(self.text, True, (0, 0, 0), self.default_color)  #建立surface
        self.rect = self.image.get_rect(center=(x, y))     #碰撞箱

    def update(self):
        mouse_pos = pygame.mouse.get_pos()                  #拿鼠標座標
        mouse_pressed = pygame.mouse.get_pressed()[0]       #是否點擊

        # 滑鼠碰到就變顏色
        if self.rect.collidepoint(mouse_pos):
            self.image = self.font.render(self.text, True, (0, 0, 0), self.hover_color)
            if mouse_pressed:
                self.callback()     #回傳上面寫的callback
        else:
            self.image = self.font.render(self.text, True, (0, 0, 0), self.default_color)

def on_click(scene_ctrl,num):
    scene_ctrl.num = num
    print(scene_ctrl.num)


def quit_button():
    pygame.quit()
    exit()

def change_FPS(FPS, changed_FPS):
    if(FPS == 60):
        changed_FPS == 30
        FPS = changed_FPS

    else:
        changed_FPS == 60
        FPS = changed_FPS