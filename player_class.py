import random
import os
import pygame



def split(picture, times):              #切割圖片(圖片, 切割次數)
    frames = []
    sprite_sheet = pygame.image.load(picture).convert_alpha()
    frame_width = sprite_sheet.get_width() // times
    frame_height = sprite_sheet.get_height()
    for i in range(times):
        frame = sprite_sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
        frames.append(frame)
    #導入圖片(八張合一起)，分割開後存進List  
    return frames  

class player():
             
    def __init__(self,name,x,y):                         #角色模型
        self.name = name                                              #角色名稱
        self.x = x                                                    #角色位置
        self.y = y
        self.image = 0                                        #角色圖片
        self.vx = 0                                                   #角色速度
        self.vy = 0
        self.on_ground = False                                      #角色是否在地面上
        self.anime_time = 0

        #匯入Walk.png圖片並切分成動畫
        self.Walk = split("Character\mainchacter\Walk.png", 8)  
        self.surface = self.Walk[self.image]
        self.mask = pygame.mask.from_surface(self.surface)

        #匯入Attack_1.png圖片並切分成動畫
        self.Attack1 = split("Character\mainchacter\Attack_1.png", 6) 
           
           
           
    def R_move(self):                                               #角色移動
        self.vx = 10
        '''self.anime_time += 1
        if self.anime_time >=5:
            self.image += 1
            self.anime_time = 0
            if self.image >= 8:
                self.image = 0'''
        self.image += 1
        if self.image >= 8:
            self.image = 0
        self.surface = self.Walk[self.image]
        self.mask = pygame.mask.from_surface(self.surface)



    def L_move(self):
        self.vx = -10
        self.anime_time += 1
        if self.anime_time >=5:
            self.image += 1
            self.anime_time = 0
            if self.image >= 8:
                self.image = 0
        '''self.image += 1
        if self.image >= 8:
            self.image = 0'''
        self.surface = self.Walk[self.image]
        self.surface = pygame.transform.flip(self.surface, True, False)
        self.mask = pygame.mask.from_surface(self.surface)                  #也許不需要？



    def jump(self):
        if self.on_ground == True:
            self.vy = -30
    
    def idle(self):
        self.anime_time = 0
        self.image = 6
        self.surface = self.Walk[self.image]
        self.mask = pygame.mask.from_surface(self.surface)

    #def attack(self):
