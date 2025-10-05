import random
import os
import pygame
import tool
import object_class



class player():

    #角色模型
    def __init__(self,name,x,y):

        #角色名稱
        self.name = name                                              

        #角色位置
        self.x = x
        self.y = y
        self.move_lock = 0

        self.HP = 5
        self.ATK = 5
        self.endurance = 4
        self.endurance_cd = 120
        self.hurt_flashing = 0
        
        #角色圖片
        self.image = 0                                        

        #角色速度
        self.vx = 0                                                   
        self.vy = 0

        #角色是否在地面上
        self.on_ground = False                                      

        self.anime_time = 0

        self.flip = False

        #角色目前碰撞清單
        self.now_NT_Touch = []
        self.now_CT_Touch = []

        #attack字典用以紀錄attack動畫狀態
        self.attack_state = {}
        self.attack_state["playing"] = False
        self.atk_procedure = 0
        self.atk_next = 0

        #匯入Walk.png圖片並切分成動畫       
        self.Walk = tool.split("Character\mainchacter\Walk.png", 8)
        self.surface = self.Walk[self.image]

        self.rect = self.surface.get_rect(topleft=(self.x, self.y+50))
        self.rect.x += 50

        self.rect.width -= 100
        self.rect.height -= 50

        #匯入3張Attack.png圖片並切分成動畫
        self.Attack1 = tool.split("Character\mainchacter\Attack_1.png", 6)
        self.Attack2 = tool.split("Character\mainchacter\Attack_2.png", 4) 
        self.Attack3 = tool.split("Character\mainchacter\Attack_3.png", 3) 
        
        #匯入Jump.png圖片並切分成動畫
        self.Jump = tool.split("Character\mainchacter\Jump.png", 12)

        #匯入Hurt.png圖片並切分成動畫
        self.Hurt = tool.split("Character\mainchacter\Hurt.png",2)
        
        self.is_hurt = 0
        self.unhurtable_cd = 0

        #慣性
        self.inertia = 0
        
        #18招，0是未獲取，1是可發動，2是發動中
        self.skill_key = [0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0]
        # [0]不須佩劍
        # [1]水上漂
        # [2]劍氣：長k
        self.skill2_time = 0
        # [3]瞬移路徑斬：a or d+ Lshift+t+ 長J
        self.skill3_time = 0
        # [4]二段跳：double space
        # [5]下劈重製跳躍並上彈+蹬牆跳+可在空中使用步法(閃避或疾跑)
        # [6]閃避：Lshift
        self.skill6_time = 0
        # [7]下衝：空中+s+長J
        self.skill7_time = 0
        # [8]上斬：w + 長J
        self.skill8_time = 0
        # [9]彈反：L
        self.skill9_time = 0
        #[10]砍半無敵幀：長J
        self.skill10_time = 0
        #[11]可裝備雙刀，改變普攻
        #[12]小怪不以你為目標
        #[13]疾跑：double a or d
        self.skill13_time = 0
        #[14]指定敵怪閃現貼臉：Tab選取+Lshift+長K
        self.skill14_time = 0
        #[15]強化普攻命中僵直：w+長K
        #[16]強化普攻命中觸發特殊對話(類似夢釘)：s+長K
        #[17]佩刀可切換刀背，傷害砍半斬擊不致死，敵怪剩餘1HP視作擊敗(劇情用)


#角色移動

    #向右移動
    def R_move(self):                                               
        if not "1_R" in self.now_NT_Touch:   #若有右碰撞，則不移動
            if self.attack_state["playing"]:
                self.vx = 3
            else:
                self.vx = 10
            self.flip = False
            tool.anime_update(self,5,False,8,self.Walk)



    #向左移動
    def L_move(self):
        if not "1_L" in self.now_NT_Touch :   #若有左碰撞，則不移動
            if self.attack_state["playing"]:
                self.vx = -3
            else:
                self.vx = -10
            self.flip = True
            tool.anime_update(self,5,True,8,self.Walk)



    #跳躍
    def jump(self):
        if self.on_ground == True or (not self.on_ground == True and self.skill_key[4] == 1) and not self.skill_key[6] == 2:
            self.vy = -20
            if self.on_ground == False:
                self.skill_key[4] = 2           
    


    def idle(self):
        self.anime_time = 0
        self.image = 6
        self.surface = self.Walk[self.image]
        if self.flip:
            self.surface = pygame.transform.flip(self.surface, True, False)


    def get_hit(self):
        if self.unhurtable_cd <=0:
            self.HP -= 1  
            if self.HP <=0:
                print("死")
                pygame.quit()
                exit()   
            self.unhurtable_cd = 120
            self.hurt_flashing = 120
            print(self.HP)


    def attack(self):
        if self.atk_next > 0:  # 在緩衝時間內
            if self.atk_procedure == 1:
                tool.start_animation(self.attack_state, self.Attack2, 5, self.flip, False)   #第二段攻擊
                self.atk_procedure = 2
            elif self.atk_procedure == 2:
                self.inertia = 21
                tool.start_animation(self.attack_state, self.Attack3, 7, self.flip, False)   #第三段攻擊會向前滑行
                if self.flip:
                    self.vx = -35
                else:
                    self.vx = 35
                self.atk_procedure = 0
                self.unhurtable_cd = 20
            else:
                # 已經是最後一段，回到第一段
                tool.start_animation(self.attack_state, self.Attack1, 3, self.flip, False)
                self.atk_procedure = 1
            self.atk_next = 0  # 用掉緩衝
        else:
            # 沒有緩衝 → 從頭開始
            tool.start_animation(self.attack_state, self.Attack1, 3, self.flip, False)
            self.atk_procedure = 1
        


class enemy():
             
    def __init__(self,name,x,y,HP,type):                                    #敵人模型
        self.name = name                                              #敵人名稱
        self.x = x                                                    #敵人位置
        self.y = y
        self.now_NT_Touch = []                                      #敵人目前碰撞清單
        self.now_CT_Touch = []                                   
        self.unhurtable_cd = 0

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

                self.Test_rect = pygame.rect.Rect(self.right_down_x,self.right_down_y,20,20)



    def Move(self,NT_object):

        match self.type:
            
            case 1:    
                pass
            
            
            case 2:    
                pass
            
            
            case 3:    
                pass
            
            
            case _: 
                
                self.back_check=0

                if self.back==1:
                    self.right_down_x = self.x+self.rect.width
                    self.right_down_y = self.y+self.rect.height
                    self.Test_rect.x = self.x+self.rect.width
                    self.Test_rect.y = self.y+self.rect.height
                else:
                    self.right_down_x = self.x
                    self.right_down_y = self.y+self.rect.height
                    self.Test_rect.x = self.x
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
                    
                    
                    
                    
class NPC():
    def __init__(self,x,y,who,IMG,phase,ani):
        self.x = x
        self.y = y
        self.who = who
        self.phase = phase        
        self.surface = IMG
        self.ani = ani
        self.is_talked = 0