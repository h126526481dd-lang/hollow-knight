import pygame

class button(pygame.sprite.Sprite):
    def __init__ (self, color, font, text:str, width, height):
        pygame.sprite.Sprite.__init__(self)                         #初始化
        
        self.image = pygame.Surface([200, 100])                     #設定按鈕大小
        self.image.fill(color = "black")
        
        text.font = text                                            #設定
        font_style = pygame.font.SysFont(text, 50)



#    def show_UI():
