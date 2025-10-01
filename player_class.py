import random
import os
import pygame
import tool
import object_class









class player():

             
    def __init__(self,name,x,y):                         #角色模型

        self.name = name                                              #角色名稱

        self.x = x                                                    #角色位置
        self.y = y

        self.HP = 5
        self.ATK=5

        self.image = 0                                        #角色圖片

        self.vx = 0                                                   #角色速度
        self.vy = 0

        self.on_ground = False                                      #角色是否在地面上

        self.anime_time = 0

        self.flip = False

        self.now_NT_Touch = []                                      #角色目前碰撞清單

        self.attack_state = {}                                      #attack字典用以紀錄attack動畫狀態
        self.attack_state["playing"] = False

        self.atk_procedure = 0
        self.atk_next = 0
                            
        self.Walk = tool.split("Character\mainchacter\Walk.png", 8)   #匯入Walk.png圖片並切分成動畫
        self.surface = self.Walk[self.image]
        
        self.rect = self.surface.get_rect(topleft=(self.x, self.y+50))
        
        self.rect.x += 50
        
        self.rect.width -= 100
        self.rect.height -= 50

        self.Attack1 = tool.split("Character\mainchacter\Attack_1.png", 6)         #匯入Attack_1.png圖片並切分成動畫
        self.Attack2 = tool.split("Character\mainchacter\Attack_2.png", 4) 
        self.Attack3 = tool.split("Character\mainchacter\Attack_3.png", 3) 
        
        self.blade1 = [pygame.image.load("Character\mainchacter\\blade1_start.png"),pygame.image.load("Character\mainchacter\\blade1_end.png")]
        self.blade_state={}
        self.blade_state["playing"]=False
        
        self.Jump = tool.split("Character\mainchacter\Jump.png", 12)
        
           
    def R_move(self):                                               #角色移動
        if not "1_R" in self.now_NT_Touch:   #若有右碰撞，則不移動
            if self.attack_state["playing"]:
                self.vx = 3
            else:
                self.vx = 10
            self.flip = False
            tool.anime_update(self,5,False,8,self.Walk)



    def L_move(self):
        if not "1_L" in self.now_NT_Touch :   #若有左碰撞，則不移動
            if self.attack_state["playing"]:
                self.vx = -3
            else:
                self.vx = -10
            self.flip = True
            tool.anime_update(self,5,True,8,self.Walk)



    def jump(self):
        if self.on_ground == True:
            self.vy = -30
            
    


    def idle(self):
        self.anime_time = 0
        self.image = 6
        self.surface = self.Walk[self.image]
        if self.flip:
            self.surface = pygame.transform.flip(self.surface, True, False)


    def attack(self):
        if self.atk_next > 0:  # 在緩衝時間內
            if self.atk_procedure == 0:
                tool.start_animation(self.attack_state, self.Attack2, 5, self.flip, False)   #第二段攻擊
                self.atk_procedure = 1
            elif self.atk_procedure == 1:
                tool.start_animation(self.attack_state, self.Attack3, 7, self.flip, False)   #第三段攻擊會向前滑行
                if self.flip:
                    self.vx = -35
                else:
                    self.vx = 35
                self.atk_procedure = 2
            else:
                # 已經是最後一段，回到第一段
                tool.start_animation(self.attack_state, self.Attack1, 3, self.flip, False)
                self.atk_procedure = 0
            self.atk_next = 0  # 用掉緩衝
        else:
            # 沒有緩衝 → 從頭開始
            tool.start_animation(self.attack_state, self.Attack1, 3, self.flip, False)
            tool.start_animation(self.blade_state, self.blade1, 2, self.flip, False)
            self.atk_procedure = 0
        


class enemy():
             
    def __init__(self,name,x,y,HP,type):                                    #敵人模型
        self.name = name                                              #敵人名稱
        self.x = x                                                    #敵人位置
        self.y = y
        self.now_NT_Touch = []                                      #敵人目前碰撞清單
        self.type = type
        self.image = 0                                        #敵人圖片
        self.vx = 0                                                   #敵人速度
        self.vy = 0
        self.on_ground = False                                      #敵人是否在地面上
        self.HP = HP
        self.can_be_through = 1
        self.back = 1
        self.back_check=0
        self.back_cd = 0

        match self.type:
            
            case 1:    
                pass
            
            
            case 2:    
                pass
            
            
            case 3:    
                pass
            
            
            case _: 
        

                self.surface =pygame.image.load("zombie.png")
                self.rect = self.surface.get_rect(topleft=(self.x, self.y))



                self.right_down_x = self.x+self.rect.width
                self.right_down_y = self.y+self.rect.height

                self.Test_rect = pygame.rect.Rect(self.right_down_x-20,self.right_down_y,20,20)








    def Move(self,NT_object):

        match self.type:
            
            case 1:    
                pass
            
            
            case 2:    
                pass
            
            
            case 3:    
                pass
            
            
            case _: 
                
                self.now_NT_Touch=[]
                self.back_check=0

                if self.back==1:
                    self.right_down_x = self.x+self.rect.width
                    self.right_down_y = self.y+self.rect.height
                    self.Test_rect.x = self.x+self.rect.width
                    self.Test_rect.y = self.y+self.rect.height
                else:
                    self.right_down_x = self.x-10
                    self.right_down_y = self.y+self.rect.height
                    self.Test_rect.x = self.x-10
                    self.Test_rect.y = self.y+self.rect.height



                for obj in NT_object:
                    tool.Touch(self, obj)
                    if self.Test_rect.colliderect(obj.rect):
                        self.back_check += 1

                if self.back_check == 0 and self.back_cd == 0:
                    self.back *= -1
                    self.back_check=0
                    self.back_cd =1
                    self.surface = pygame.transform.flip(self.surface, True, False)


                if self.back_check > 0:
                    self.back_cd =0


                if "1_D" in self.now_NT_Touch:
                    self.on_ground = True
                else:
                    self.on_ground =False
                
                if self.on_ground :
                    self.vy = 0
                    self.vx = 5*self.back
                    self.x += self.vx
                    self.rect.x += self.vx
                else:
                    
                    self.vy+=1
                    self.y += self.vy
                    self.rect.y += self.vy  

