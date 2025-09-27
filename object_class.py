import random
import os
import pygame
import player_class





class object():
             
    def __init__(self,x,y,IMG,type):                         #物件模型

        self.type=type
        self.x = x                                                    #物件位置
        self.y = y
        self.surface=IMG                                        #物件圖片
        self.vx = 0                                                   #物件速
        self.vy = 0
        
        match type:
            case "wall":
                self.can_be_through = 0                                         #物件是否可通過(布林值)        
                self.rect = self.surface.get_rect(topleft=(self.x, self.y))     #物件碰撞盒(規則)
        
            case "door":
                self.can_be_through = 1                                         #物件是否可通過(布林值)        
                self.rect = self.surface.get_rect(topleft=(self.x, self.y))     #物件碰撞盒(規則)
                
                pass
            
            
            case "path":
                pass
            
            case _:
                pass

