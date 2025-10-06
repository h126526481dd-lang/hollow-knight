import pygame

class Button(pygame.sprite.Sprite):
    
    def __init__(self, x, y, text, callback):
        super().__init__()                                  #sprite初始化
        self.font = pygame.font.SysFont(None, 40)              #字體
        self.text = text                                    #文字
        self.callback = callback                            #輸入按鈕按下所要執行的函式
        self.default_color = (100, 100, 100)                #預設顏色
        self.hover_color = (200, 200, 200)                  #觸碰顏色
        self.image = self.font.render(self.text, True, (0, 0, 0), self.default_color)  #建立surface
        self.rect = self.image.get_rect(topleft=(x, y))     #碰撞箱

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

def on_click(num):
    import main
    main.scene_ctrl = num
    print(main.scene_ctrl)
