import random
import os
import pygame
import player_class





class object():
             
    def __init__(self,x,y,IMG,type,ATK,KB,dif,num,flip,goto,dur=200):                         #物件模型

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
                self.dif = dif     
                self.rect = self.surface.get_rect(topleft=(self.x, self.y))     #物件碰撞盒(規則)       
                self.angle = 0    
                     
                self.center_x = self.x + self.rect.width /2
                self.center_y = self.y + self.rect.height /2
                
                self.F_Px = self.rect.x
                self.F_Py = self.rect.y
                
                self.S_Px = self.rect.x + self.rect.width
                self.S_Py = self.rect.y
                
                self.T_Px = self.rect.x + self.rect.width //2
                self.T_Py = self.rect.y + self.rect.height
        
        
                
                self.left = self.rect.width - self.rect.height
                self.org_rect_w =self.rect.width        
                self.org_rect_h =self.rect.height
                self.org_x = self.x
                self.org_y = self.y
                
                self.FS = [self.S_Px - self.F_Px , (self.S_Py - self.F_Py)]
                self.ST = [self.T_Px - self.S_Px , (self.T_Py - self.S_Py)]
                self.TF = [self.F_Px - self.T_Px , (self.F_Py - self.T_Py)]
                
                self.L_FS = [self.FS[1] , self.FS[0]*-1]
                self.L_ST = [self.ST[1] , self.ST[0]*-1]
                self.L_TF = [self.TF[1] , self.TF[0]*-1]
        
                self.L_FS.append(-1*(self.L_FS[0]*self.F_Px + self.L_FS[1]*self.F_Py))
                self.L_ST.append(-1*(self.L_ST[0]*self.S_Px + self.L_ST[1]*self.S_Py))
                self.L_TF.append(-1*(self.L_TF[0]*self.T_Px + self.L_TF[1]*self.T_Py))        
        
                self.outerect = pygame.Rect(self.rect.x - 80, self.rect.y - 80, self.rect.width + 160, self.rect.height + 160)
        
                self.tag_x = None
                self.tag_y = None
                
                self.W = False
                
                self.play = False
        
        
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
                        self.num = num

                        self.rect = self.surface.get_rect(topleft=(self.x, self.y))     #物件碰撞盒(規則)
                        self.ATK=ATK
                        self.KB=KB
                        
                        self.index = 0
                        self.tag_x = None
                        self.tag_y = None
                        self.delete = 0
                        self.dur = 300


                    case "fire":
                        
                        self.vx = 0
                        self.vy = 0
                        self.can_be_through = 1                                         #物件是否可通過(布林值)
                        self.surface= pygame.transform.scale(self.surface,(100,100))

                        self.rect = self.surface.get_rect(topleft=(self.x, self.y))     #物件碰撞盒(規則)
                        self.ATK=ATK
                        self.KB=KB
                        
                        self.tag_x = None
                        self.tag_y = None
                        self.delete = 0
                        self.dur = 60

                    case "web":
                        
                        self.num = num
                        self.vx = 0
                        self.vy = 0
                        self.can_be_through = 1                                         #物件是否可通過(布林值)
                        self.surface= pygame.transform.scale(self.surface,(100,100))

                        self.rect = self.surface.get_rect(topleft=(self.x, self.y))     #物件碰撞盒(規則)
                        
                        self.tag_x = None
                        self.tag_y = None
                        self.delete = 0
                        self.dur = 180
                        
                        self.frames = [pygame.transform.scale(pygame.image.load("Image\Character\Enemy\Boss\web2.png"), (100, 100)),
                                        pygame.transform.scale(pygame.image.load("Image\Character\Enemy\Boss\web3.png"), (150, 100)),
                                        pygame.transform.scale(pygame.image.load("Image\Character\Enemy\Boss\web4.png"), (140, 140)),
                                        pygame.transform.scale(pygame.image.load("Image\Character\Enemy\Boss\web5.png"), (200, 220)),
                                        pygame.transform.scale(pygame.image.load("Image\Character\Enemy\Boss\web6.png"), (260, 260))]

                    case "light":
                        
                        self.num = num
                        
                        self.through = 1
                        
                        self.vx = 0
                        self.vy = 0
                        self.can_be_through = 1                                         #物件是否可通過(布林值)
                        self.surface= pygame.transform.scale(self.surface,(50,50))

                        self.rect = self.surface.get_rect(topleft=(self.x, self.y))     #物件碰撞盒(規則)
                        self.ATK=ATK
                        self.KB=KB
                        
                        self.tag_x = None
                        self.tag_y = None
                        
                        self.delete = 0
                        self.dur = dur
                        
                        self.pre_test = 0
                        
                        self.now_Touch =[]
                        self.L_mirror = None
                        
                    case "pre_light":
                        
                        self.num = num
                        
                        self.through = 1
                        
                        self.vx = 0
                        self.vy = 0
                        self.can_be_through = 1                                         #物件是否可通過(布林值)
                        self.surface= pygame.transform.scale(self.surface,(50,50))

                        self.rect = self.surface.get_rect(topleft=(self.x, self.y))     #物件碰撞盒(規則)

                        self.surface= pygame.transform.scale(self.surface,(10,10))

                        self.ATK=ATK
                        self.KB=KB
                        
                        self.tag_x = None
                        self.tag_y = None
                        self.delete = 0
                        self.dur = dur

                        self.pre_test = 0
                        self.now_Touch =[]
                        self.L_mirror = None
                        
                    case "sun_blaze":
                        self.vx = 0
                        self.vy = 0
                        self.can_be_through = 1                                         #物件是否可通過(布林值)  
                        self.dur = 60
                        self.surface= pygame.transform.scale(self.surface,(700,600))

                        self.delete = 0

                        self.rect = self.surface.get_rect(topleft=(self.x, self.y))     #物件碰撞盒(規則)
                        self.ATK=ATK
                        self.KB=KB
                        self.state={}
                        self.state["playing"]=False
                    
                    case "light_sword":
                        self.vx = 0
                        self.vy = 0
                        self.can_be_through = 1                                         #物件是否可通過(布林值)
                        self.dur = 300
                        
                        self.num = num

                        self.delete = 0
                        self.surface= pygame.transform.scale(self.surface,(50,150))

                        self.rect = self.surface.get_rect(topleft=(self.x, self.y))     #物件碰撞盒(規則)
                        self.ATK=ATK
                        self.KB=KB
                        self.state={}
                        self.state["playing"]=False

                        self.tag_x = None
                        self.tag_y = None

                        self.chase = 0
                        self.L_mirror = None
                        self.pre_test = 0

                    case "light_ball":
                        self.vx = 0
                        self.vy = 0
                        self.can_be_through = 1                                         #物件是否可通過(布林值)
                        self.dur = 300

                        self.delete = 0
                        self.surface= pygame.transform.scale(self.surface,(150,150))

                        self.rect = self.surface.get_rect(topleft=(self.x, self.y))     #物件碰撞盒(規則)
                        self.ATK=ATK
                        self.KB=KB
                        self.state={}
                        self.state["playing"]=False

                        self.chase = 0
                        self.tag_x = None
                        self.tag_y = None
                        
                    case "explosion":
                        self.can_be_through = 1                                         #物件是否可通過(布林值)
                        self.delete = 0
                        self.surface= pygame.transform.scale(self.surface,(350,350))
                        self.rect = self.surface.get_rect(topleft=(self.x, self.y))     #物件碰撞盒(規則)
                        self.ATK=ATK
                        self.KB=KB
                        self.dur = 39
                        
                        self.state={}
                        self.state["playing"]=False
                        
                        self.frames = [pygame.transform.scale(pygame.image.load("Image\Character\Enemy\Boss\eps1.png"), (350, 350)),
                                        pygame.transform.scale(pygame.image.load("Image\Character\Enemy\Boss\eps2.png"), (350, 350)),
                                        pygame.transform.scale(pygame.image.load("Image\Character\Enemy\Boss\eps3.png"), (350, 350)),
                                        pygame.transform.scale(pygame.image.load("Image\Character\Enemy\Boss\eps4.png"), (350, 350)),
                                        pygame.transform.scale(pygame.image.load("Image\Character\Enemy\Boss\eps5.png"), (350, 350)),
                                        pygame.transform.scale(pygame.image.load("Image\Character\Enemy\Boss\eps6.png"), (350, 350)),
                                        pygame.transform.scale(pygame.image.load("Image\Character\Enemy\Boss\eps7.png"), (350, 350)),
                                        pygame.transform.scale(pygame.image.load("Image\Character\Enemy\Boss\eps8.png"), (350, 350))]