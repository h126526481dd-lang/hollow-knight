import random
import os
import pygame
import player_class





class object():
             
    def __init__(self,x,y,IMG,type,ATK,KB,dif,num,flip,goto):                         #物件模型

        self.type=type
        self.x = x                                                    #物件位置
        self.y = y
        self.surface=IMG                                        #物件圖片
        self.now_NT_Touch = []                                      
        self.now_CT_Touch = []                   
        self.flip=flip
        self.dif=dif

        
        match type:
            case "wall":
                self.can_be_through = 0                                         #物件是否可通過      
                self.rect = self.surface.get_rect(topleft=(self.x, self.y))     #物件碰撞盒(規則)
                
                
            case "fake_wall":
                self.can_be_through = 0                                         #物件是否可通過     
                self.rect = self.surface.get_rect(topleft=(self.x, self.y))     #物件碰撞盒(規則)
                
                
            case "mirror_wall":
                self.can_be_through = 2                                         #物件是否可通過      
                self.rect = self.surface.get_rect(topleft=(self.x, self.y))     #物件碰撞盒(規則)                
                
        
            case "door":
                self.can_be_through = 1                                         #物件是否可通過      
                self.rect = self.surface.get_rect(topleft=(self.x, self.y))     #物件碰撞盒(規則)
            
            case "skill":
                self.can_be_through = 1
                self.rect = self.surface.get_rect(topleft=(self.x, self.y))
                self.num=num
            
            case "path":
                self.can_be_through = 1                                         #物件是否可通過(布林值)        
                self.goto = goto
                self.rect = self.surface.get_rect(topleft=(self.x, self.y))     #物件碰撞盒(規則)

            case "save_point":

                self.can_be_through = 1                                         #物件是否可通過(布林值)        
                self.rect = self.surface.get_rect(topleft=(self.x, self.y))     #物件碰撞盒(規則)

            case "trans":
                self.can_be_through = 1
                self.rect = self.surface.get_rect(topleft=(self.x, self.y))     #物件碰撞盒(規則)

            case "dangerous":
                
                
                match dif:
                    
                    case "blade1":
                        self.vx = 0
                        self.vy = 0
                        self.can_be_through = 1                                         #物件是否可通過(布林值)  
                        self.dur = 20 
                        self.surface= pygame.transform.scale(self.surface,(100,100))
                        self.frames = [pygame.transform.scale(pygame.image.load("Image\Character\mainchacter\\blade1_start.png"), (100, 100)),pygame.transform.scale(pygame.image.load("Image\Character\mainchacter\\blade1_end.png"), (100, 100))]

                        self.rect = self.surface.get_rect(topleft=(self.x, self.y))     #物件碰撞盒(規則)
                        self.ATK=ATK
                        self.KB=KB
                        self.state={}
                        self.state["playing"]=False
                    
                    case "blade2":
                        self.vx = 0
                        self.vy = 0
                        self.can_be_through = 1                                         #物件是否可通過(布林值)  
                        self.dur = 20 
                        self.surface= pygame.transform.scale(self.surface,(100,100))
                        self.frames = [pygame.transform.scale(pygame.image.load("Image\Character\mainchacter\\blade1_start.png"), (100, 100)),pygame.transform.scale(pygame.image.load("Image\Character\mainchacter\\blade1_end.png"), (100, 100))]

                        self.rect = self.surface.get_rect(topleft=(self.x, self.y))     #物件碰撞盒(規則)
                        self.ATK=ATK
                        self.KB=KB
                        self.state={}
                        self.state["playing"]=False

                    case "blade3":
                        self.vx = 0
                        self.vy = 0
                        self.can_be_through = 1                                         #物件是否可通過(布林值)  
                        self.dur = 20 
                        self.surface= pygame.transform.scale(self.surface,(100,100))
                        self.frames = [pygame.transform.scale(pygame.image.load("Image\Character\mainchacter\\blade1_start.png"), (100, 100)),pygame.transform.scale(pygame.image.load("Image\Character\mainchacter\\blade1_end.png"), (100, 100))]

                        self.rect = self.surface.get_rect(topleft=(self.x, self.y))     #物件碰撞盒(規則)
                        self.ATK=ATK
                        self.KB=KB
                        self.state={}
                        self.state["playing"]=False
                        
                    case "bullet":
                        
                        self.vx = 0
                        self.vy = 0
                        self.can_be_through = 1                                         #物件是否可通過(布林值)
                        self.surface= pygame.transform.scale(self.surface,(32,32))

                        self.rect = self.surface.get_rect(topleft=(self.x, self.y))     #物件碰撞盒(規則)
                        self.ATK=ATK
                        self.KB=KB
                        
                        self.index = 0
                        self.tag_x = None
                        self.tag_y = None
                        self.delete = 0
                        self.dur = 300
                


