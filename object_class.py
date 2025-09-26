import random
import os
import pygame
import player_class





class object():
             
    def __init__(self,x,y,IMG,can_be_through):                         #物件模型


        self.x = x                                                    #物件位置
        self.y = y
        self.surface=IMG                                        #物件圖片
        self.vx = 0                                                   #物件速
        self.vy = 0
        self.can_be_through = can_be_through                          #物件是否可通過(布林值)
        self.mask = pygame.mask.from_surface(self.surface)               #物件碰撞盒(不規則)

