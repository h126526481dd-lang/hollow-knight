import random
import os
import pygame



class player():
             
    def __init__(self,name,x,y):                         #角色模型
        self.name = name                                              #角色名稱
        self.x = x                                                    #角色位置
        self.y = y
        self.image = 0                                        #角色圖片
        self.vx = 0                                                   #角色速度
        self.vy = 0
        self.on_ground = False                                      #角色是否在地面上
        sprite_sheet = pygame.image.load("Character\mainchacter\Walk.png").convert_alpha()
        frame_width = sprite_sheet.get_width() // 8
        frame_height = sprite_sheet.get_height()
        self.frames = []

        for i in range(8):
            frame = sprite_sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
            self.frames.append(frame)
            #導入圖片(八張合一起)，分割開後存進List    
       
        self.surface = self.frames[self.image]
        self.mask = pygame.mask.from_surface(self.surface)
           
           
           
    def R_move(self):                                               #角色移動
        self.vx = 10
        self.image += 1

        if self.image >= 8:
            self.image = 0
        self.surface = self.frames[self.image]
        self.mask = pygame.mask.from_surface(self.surface)



    def L_move(self):
        self.vx = -10
        self.image += 1
        if self.image >= 8:
            self.image = 0
        self.surface = self.frames[self.image]
        self.surface = pygame.transform.flip(self.surface, True, False)
        self.mask = pygame.mask.from_surface(self.surface)                  #也許不需要？



    def jump(self):
        if self.on_ground == True:
            self.vy = -30
