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

        self.HP = 10
        self.Max_HP = 10

        self.current_HP = 10
        self.Hurt_HP = 0


        self.ATK = 5
        self.endurance = 4
        self.Max_endurance = 4
        self.endurance_cd = 120

        self.Max_backup = 3
        self.backup = 3
        self.backup_cd = 1800
        self.drinking = 0

        self.hurt_flashing = 0
        self.death_cd = 0
        
        #角色圖片
        self.image = 0

        #角色速度
        self.vx = 0                                                   
        self.vy = 0
        self.pre_vx=0
        self.pre_vy=0

        #角色是否在地面上
        self.on_ground = 0             
        self.through = 0                         

        self.anime_time = 0

        self.flip = False

        #角色目前碰撞清單
        self.now_NT_Touch = []
        self.now_CT_Touch = []
        self.noe_Touch = []

        #attack字典用以紀錄attack動畫狀態
        self.attack_state = {}
        self.attack_state["playing"] = False
        self.atk_procedure = 0
        self.atk_next = 0


        

        #匯入Walk.png圖片並切分成動畫       



        #匯入3張Attack.png圖片並切分成動畫
        self.attack1 = "Image\Character\mainchacter\Attack_1.png"
        self.attack2 = "Image\Character\mainchacter\Attack_2.png" 
        self.attack3 = "Image\Character\mainchacter\Attack_3.png" 

        self.attack_sound = "Sound/blade.wav"
        self.dead_sound = "Sound\dead.wav"
        self.hurt_sound = "Sound\hurt.wav"
        self.dodge_sound = "Sound\dodge.wav"
        
        #匯入Jump.png圖片並切分成動畫
        self.jumping = "Image\Character\mainchacter\Jump.png"

        #匯入Hurt.png圖片並切分成動畫
        self.hurt = "Image\Character\mainchacter\Hurt.png"
        
        self.walk = "Image\Character\mainchacter\Walk.png"
        
        self.dead = "Image\Character\mainchacter\Dead.png"
        self.shield = "Image\Character\mainchacter\Shield.png"
        
        self.is_hurt = 0
        self.unhurtable_cd = 0

        #慣性
        self.inertia = 0
        
        #18招，0是未獲取，1是可發動，2是發動中
        self.skill_key = [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0]
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
        self.Attack1 = None
        self.Attack2 = None
        self.Attack3 = None
        
        #匯入Jump.png圖片並切分成動畫
        self.Jump = None

        #匯入Hurt.png圖片並切分成動畫
        self.Hurt = None

        #匯入格擋
        self.Shield = None
        self.block_state = {}
        self.block_state["playing"] = False

        
        self.Walk = None
        self.surface = None
        self.rect = None
        self.Attack_sound = None
        self.Dead_sound = None
        self.Hurt_sound = None

        #設定蹬牆跳方向(0是沒使用 1向右跳 2向左跳)
        self.Walljump_direct = 0
        self.Walljump_time = 0
        self.Wall_slip = 0

#角色移動

    #向右移動
    def R_move(self):                                               
        if not "1_R" in self.now_NT_Touch:   #若有右碰撞，則不移動
            if self.attack_state["playing"]:
                self.vx = 5
            else:
                self.vx = 10
            self.flip = False
            tool.anime_update(self,5,False,8,self.Walk)



    #向左移動
    def L_move(self):
        if not "1_L" in self.now_NT_Touch :   #若有左碰撞，則不移動
            if self.attack_state["playing"]:
                self.vx = -5
            else:
                self.vx = -10
            self.flip = True
            tool.anime_update(self,5,True,8,self.Walk)



    #四種跳躍模式
    def jump(self):
        #在地上跳
        if self.on_ground:
            self.vy = -20
        #蹬牆跳(左牆向右)
        elif  "1_L" in self.now_NT_Touch and self.skill_key[5] == 1:
            #print("wall jump")
            self.vy = -20
            self.Walljump_direct = 1
            self.Walljump_time = 10
        #蹬牆跳(右牆向左)
        elif  "1_R" in self.now_NT_Touch and self.skill_key[5] == 1:
            #print("wall jump")
            self.vy = -20
            self.Walljump_direct = 2
            self.Walljump_time = 10
        #二段跳
        elif(not self.on_ground == True and self.skill_key[4] == 1) and not self.skill_key[6] == 2:
            self.vy = -20
            self.skill_key[4] = 2  



    def idle(self):
        self.anime_time = 0
        self.image = 6
        self.surface = self.Walk[self.image]
        if self.flip:
            self.surface = pygame.transform.flip(self.surface, True, False)


    def get_hit(self):
        if self.unhurtable_cd <=0 and self.HP > 0:
            self.Hurt_sound.play()
            self.HP -= 1  
            self.unhurtable_cd = max(120,self.unhurtable_cd)
        if self.HP != 0 :
            self.hurt_flashing = 120


    def attack(self):
        self.Attack_sound.play()
        if self.atk_next > 0:  # 在緩衝時間內
            if self.atk_procedure == 1:
                tool.start_animation(self.attack_state, self.Attack2, 5, self.flip, False)   #第二段攻擊
                self.atk_procedure = 2
            elif self.atk_procedure == 2:
                tool.start_animation(self.attack_state, self.Attack3, 7, self.flip, False)   #第三段攻擊會向前滑行
                if self.move_lock == 0:
                    self.inertia = 21
                    if self.flip:
                        self.vx = -35
                    else:
                        self.vx = 35
                self.atk_procedure = 0
                self.unhurtable_cd = max(20,self.unhurtable_cd)
            else:
                # 已經是最後一段，回到第一段
                tool.start_animation(self.attack_state, self.Attack1, 3, self.flip, False)
                self.atk_procedure = 1
            self.atk_next = 0  # 用掉緩衝
        else:
            # 沒有緩衝 → 從頭開始
            tool.start_animation(self.attack_state, self.Attack1, 3, self.flip, False)
            self.atk_procedure = 1

    def block(self):
        self.vx = 0
        tool.start_animation(self.block_state, self.Shield, 60, self.flip, False)
            
    def to_dict(self):
        self.Attack1 = None
        self.Attack2 = None
        self.Attack3 = None
        self.Attack_sound = None
        self.Dead_sound = None
        
        #匯入Jump.png圖片並切分成動畫
        self.Jump = None
        self.Dead = None
        #匯入Hurt.png圖片並切分成動畫
        self.Hurt = None
        self.Hurt_sound = None
        self.Dodge_sound = None
        self.Walk = None
        self.surface = None
        self.rect = None
        self.Shield = None
        self.attack_state = {}
        self.attack_state["playing"] = False
        self.block_state = {}
        self.block_state["playing"] = False
        

        return self.__dict__
    
    @classmethod
    def from_dict(cls,data):
        # 建立一個空的 Player，不呼叫 __init__
        obj = cls.__new__(cls)

        # 回寫狀態
        for k, v in data.items():
            setattr(obj, k, v)

        return obj
    
    def read_surface(self):
        self.Attack1 = tool.split(self.attack1, 6)
        self.Attack2 = tool.split(self.attack2, 4) 
        self.Attack3 = tool.split(self.attack3, 3) 
        self.Attack_sound = pygame.mixer.Sound(self.attack_sound)
        self.Dead_sound = pygame.mixer.Sound(self.dead_sound)
        self.Hurt_sound = pygame.mixer.Sound(self.hurt_sound)
        self.Dodge_sound = pygame.mixer.Sound(self.dodge_sound)
        
        #匯入Jump.png圖片並切分成動畫
        self.Jump = tool.split(self.jumping, 12)

        #匯入Hurt.png圖片並切分成動畫
        self.Hurt = tool.split(self.hurt ,2)
        self.Dead = tool.split(self.dead, 3)

        self.Shield = tool.split(self.shield, 2)
        
        self.Walk = tool.split(self.walk, 8)
        self.surface = self.Walk[self.image]
        self.rect = self.surface.get_rect(topleft=(self.x, self.y+50))
        self.rect.x = self.x + 50

        self.rect.width -= 100
        self.rect.height -= 50
        self.attack_state = {}
        self.attack_state["playing"] = False
        self.block_state = {}
        self.block_state["playing"] = False


class enemy():
             
    def __init__(self,name,x,y,HP,type,dif):                                    #敵人模型
        
        self.name = name                                              #敵人名稱
        self.x = x                                                    #敵人位置
        self.y = y
        self.now_NT_Touch = []                                      #敵人目前碰撞清單
        self.now_CT_Touch = []                                   
        self.unhurtable_cd = 0
        self.wait = 0

        self.type = type
        self.dif  = dif
        self.distant = None

        self.image = 0                                        #敵人圖片
        self.is_hit = 0
        self.vx = 0                                                   #敵人速度
        self.vy = 0
        self.through = 0
        self.on_ground = 0                                      #敵人是否在地面上
        self.HP = HP
        self.can_be_through = 1
        self.back = 1
        self.back_check=0
        self.back_cd = 0
        
        self.TDamage = 1
        self.NoGravity = 0
        self.inertia = 0
        self.pre_vx = 0
        self.pre_vy = 0

        self.found = False
        self.attack_state = {}
        self.attack_state["playing"] = False
        self.anime = False
        self.image = 0
        self.anime_time = 0        

        match self.type:
            
            case "boss":


                match self.dif :
                    
                    case "The_Tank":


                        self.boss_idle = tool.split("Image\Character\Enemy\Boss\Idle.png",4)
                        self.boss_walk = tool.split("Image\Character\Enemy\Boss\Walk.png",6)
                        self.boss_attack1 = tool.split("Image\Character\Enemy\Boss\Attack1.png",8)
                        self.boss_attack2 = tool.split("Image\Character\Enemy\Boss\Attack2.png",6)
                        self.boss_attack3 = tool.split("Image\Character\Enemy\Boss\Attack4.png",6)
                        del self.boss_attack3[4:6]
                        self.boss_attack4 = tool.split("Image\Character\Enemy\Boss\Attack4.png",6)
                        del self.boss_attack4[4:6]
                        self.boss_break = tool.split("Image\Character\Enemy\Boss\Death.png", 6)
                        self.boss_up = list(reversed(self.boss_break))


                        self.surface = pygame.transform.scale(self.boss_idle[0],(320,300))        #pygame.image.load("Image\Character\Enemy\zombie.png")
                        self.rect = self.surface.get_rect(topleft=(self.x, self.y))

                        self.broke = 0

                        self.rect.x = self.x + 21
                        self.rect.y = self.y + 80

                        self.rect.width -= 41
                        self.rect.height -= 80

                        self.second_HP = 0

                        self.skill_time = -1

                        self.phase = 6
                        self.phase_cd = 0

                        self.right_down_x = self.rect.x+self.rect.width +20
                        self.right_down_y = self.rect.y+self.rect.height

                        self.Test_rect = pygame.rect.Rect(self.right_down_x,self.right_down_y,20,20)     


                    case "The_Sun":
                        self.surface = pygame.transform.scale(pygame.image.load("Image\Character\Enemy\Boss\sun1.png"),(320,300))        #
                        
                        self.boss_idle = [pygame.transform.scale(pygame.image.load("Image\Character\Enemy\Boss\sun1.png"),(320,300)), 
                                          pygame.transform.scale(pygame.image.load("Image\Character\Enemy\Boss\sun2.png"),(320,300))]
                        self.rect = self.surface.get_rect(topleft=(self.x, self.y))


                        
                        self.I = (0,0)
                        self.II =(0,0)
                        self.III =(0,0)
                        self.IV = (0,0)
                        self.V =(0,0)
                        self.VI =(0,0)
                        
                        self.sun_blaze = 0
                        self.light_count = 0
                        self.theta = 0
                        
                        self.broke = 0

                        self.TDamage = 0
                        self.NoGravity = 1
                        self.skill_time = 0

                        self.phase = 2
                        self.phase_cd = 0

                        self.right_down_x = self.rect.x+self.rect.width +20
                        self.right_down_y = self.rect.y+self.rect.height

                        self.Test_rect = pygame.rect.Rect(self.right_down_x,self.right_down_y,20,20)     
                        self.summon = 1
                        self.summon_cd = 0
                        

                        self.second_HP = 200





            
            case "elite":    
                pass
            
            
            case "roadside":    
        

                self.surface =pygame.image.load("Image\Character\Enemy\zombie.png")
                self.rect = self.surface.get_rect(topleft=(self.x, self.y))



                self.right_down_x = self.x+self.rect.width
                self.right_down_y = self.y+self.rect.height

                self.Test_rect = pygame.rect.Rect(self.right_down_x,self.right_down_y,20,20)




    def Find(self,player,NT_object):

        RAY = F_RAY(self.x,self.y)
            
        for i in range(10):
            RAY.rect.x += (player.x - self.x)//10
            RAY.rect.y += (player.y - self.y)//10
            print (RAY.rect.x,RAY.rect.y)
            for obj in NT_object:
                if RAY.rect.colliderect(obj.rect):
                    del RAY
                    print("walled")
                    return False
            if RAY.rect.colliderect(player.rect):
                del RAY
                print("found!")
                return True
        del RAY
        return False

    def Move(self,NT_object,player):

        if self.wait > 0:
            self.wait -= 1
            for obj in NT_object:
                tool.Touch(self, obj)
            if "1_D" in self.now_NT_Touch:
                self.on_ground = 1
            elif "1_DP" in self.now_NT_Touch:
                self.on_ground = 2
            else:
                self.on_ground = 0
            
            if self.on_ground :
                self.vy = 0
                if abs(self.vx) > 0:
                    self.x += self.vx
                    self.rect.x += self.vx

                    self.vx = 0

            elif self.on_ground == 0 and self.NoGravity == 0:
                self.vx = 0
                self.vy+=1
                self.y += self.vy
                self.rect.y += self.vy  
            
        
        else:

            match self.type:
                
                case "boss":


                    match self.dif:


                        case "The_Tank":    
                    

                            if not self.found:
                                
                                self.surface = pygame.transform.scale(self.boss_break[5], (320, 300))
                                
                                if player.rect.x - (self.rect.x+self.rect.width//2) < 0 and self.back == -1:
                                    
                                    if  pow((player.rect.x - (self.rect.x+self.rect.width//2)),2) + pow((player.rect.y - (self.rect.y+self.rect.height//2)),2) <= pow(1000,2):
                                        print("found_Test_left")

                                        if self.Find(player,NT_object):
                                            self.wait = 32
                                            self.found = True
                                            
                                            
                                if player.rect.x - (self.rect.x+self.rect.width//2) > 0 and self.back == 1:
                                    
                                    if  pow((player.rect.x - (self.rect.x+self.rect.width//2)),2) + pow((player.rect.y - (self.rect.y+self.rect.height//2)),2) <= pow(1000,2):
                                        print("found_Test_right")
                                        
                                        if self.Find(player,NT_object):
                                            self.wait = 32
                                            self.found = True                        

                            
                            else:
                                
                                self.pre_vx = self.vx
                                self.pre_vy = self.vy
                                
                                self.back_check=0

                                if self.back==1:
                                    self.right_down_x = self.rect.x+self.rect.width + 20
                                    self.right_down_y = self.rect.y+self.rect.height
                                    self.Test_rect.x = self.rect.x+self.rect.width
                                    self.Test_rect.y = self.rect.y+self.rect.height
                                    
                                else:
                                    self.right_down_x = self.rect.x
                                    self.right_down_y = self.rect.y+self.rect.height
                                    self.Test_rect.x = self.rect.x
                                    self.Test_rect.y = self.rect.y+self.rect.height


                                for obj in NT_object:
                                    if not (self.phase_cd == -3 and self.skill_time > 0 and self.wait == 0):
                                        tool.Touch(self, obj)

                                    if self.Test_rect.colliderect(obj.rect):
                                        self.back_check += 1                    #碰到一個物件+1

                                if "1_L" in self.now_NT_Touch or "1_R" in self.now_NT_Touch and self.back_cd == 0:  #觸邊反彈
                                    if self.phase == 3:
                                        if player.rect.x - self.rect.x - self.rect.width//2 > 0:    #起跳前轉向玩家
                                            self.back = 1
                                        else:
                                            self.back = -1
                                    else:
                                        self.back_cd =-1
                                                        



                                if self.back_cd == -1:
                                    
                                    self.back *= -1
                                    self.back_check = 0
                                    self.back_cd = 2
                                    self.surface = pygame.transform.flip(self.surface, True, False)
                                    
                                if self.back_cd > 0:
                                    self.back_cd -= 1


                                if "1_D" in self.now_NT_Touch:
                                    self.on_ground = 1
                                elif "1_DP" in self.now_NT_Touch:
                                    self.on_ground = 2
                                else:
                                    self.on_ground = 0
                                


                                if (self.phase == 0 or self.phase == 2 or self.phase == 3 or self.phase == 5 or self.phase == 6) and self.skill_time > 0:

                                    if self.on_ground :
                                        if not self.phase == 6:
                                            self.vy = 0    
                                        self.x += self.vx * self.back
                                        self.rect.x += self.vx * self.back
                                        self.y += self.vy
                                        self.rect.y += self.vy        

                                    else:
                                        self.vy+=1
                                        self.x += self.vx * self.back
                                        self.rect.x += self.vx * self.back
                                        self.y += self.vy
                                        self.rect.y += self.vy                       

                                else:    
                                    if self.on_ground :


                                        self.vy = 0
                                        self.vx = 0
                                        if self.attack_state["playing"]:
                                            self.vx = 0
                                        self.x += self.vx
                                        self.rect.x += self.vx
                                    else:
                                        
                                        self.vy+=1
                                        self.y += self.vy
                                        self.rect.y += self.vy
                                        
                                        
                        case "The_Sun":
                            if not self.found:

                                if  pow((player.rect.x - (self.rect.x+self.rect.width//2)),2) + pow((player.rect.y - (self.rect.y+self.rect.height//2)),2) <= pow(1000,2) and player.on_ground:
                                    print("found_Test_right")
                                        
                                    if self.Find(player,NT_object):
                                        self.wait = 240
                                        self.found = True     
                                        
                            else:

                                self.pre_vx = self.vx
                                self.pre_vy = self.vy
                                
                                self.back_check=0

                                if self.back==1:
                                    self.right_down_x = self.rect.x+self.rect.width + 20
                                    self.right_down_y = self.rect.y+self.rect.height
                                    self.Test_rect.x = self.rect.x+self.rect.width
                                    self.Test_rect.y = self.rect.y+self.rect.height
                                    
                                else:
                                    self.right_down_x = self.rect.x
                                    self.right_down_y = self.rect.y+self.rect.height
                                    self.Test_rect.x = self.rect.x
                                    self.Test_rect.y = self.rect.y+self.rect.height


                                for obj in NT_object:
                                    if not (self.phase_cd == -3 and self.skill_time > 0 and self.wait == 0):
                                        tool.Touch(self, obj)




                                if "1_D" in self.now_NT_Touch:
                                    self.on_ground = 1
                                elif "1_DP" in self.now_NT_Touch:
                                    self.on_ground = 2
                                else:
                                    self.on_ground = 0
                                
                        
                                if self.on_ground :
                                    self.vy = 0    
                                    self.x += self.vx * self.back
                                    self.rect.x += self.vx * self.back
                                    self.y += self.vy
                                    self.rect.y += self.vy  
                                
                                
                                elif not self.on_ground and not self.NoGravity:
                                    self.vy+=1
                                    self.x += self.vx * self.back
                                    self.rect.x += self.vx * self.back
                                    self.y += self.vy
                                    self.rect.y += self.vy                      
                                    
                                else :
                                    self.x += self.vx * self.back
                                    self.rect.x += self.vx * self.back
                                    self.y += self.vy
                                    self.rect.y += self.vy     
                                    self.vx = 0
                            
                        
                            
                            
                case _:
                    self.pre_vx = self.vx
                    self.pre_vy = self.vy
                        
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
                                
                    if "1_L" in self.now_NT_Touch or "1_R" in self.now_NT_Touch and self.back_cd == 0:  #觸邊反彈
                        self.back_cd =-1
                                                        
                    if self.back_check == 0 and self.back_cd == 0:  #觸界反彈
                        self.back_cd =-1


                    if self.back_cd == -1:
                        self.back *= -1
                        self.back_check = 0
                        self.back_cd = 10
                        self.surface = pygame.transform.flip(self.surface, True, False)
                                        
                    if self.back_cd > 0:
                        self.back_cd -= 1


                    if "1_D" in self.now_NT_Touch:
                        self.on_ground = 1
                    elif "1_DP" in self.now_NT_Touch:
                        self.on_ground = 2
                    else:
                        self.on_ground = 0
                        
                    if self.on_ground :
                        self.vy = 0
                        self.vx = 5*self.back
                        self.x += self.vx
                        self.rect.x += self.vx
                    else:
                        
                        self.vy+=1
                        self.y += self.vy
                        self.rect.y += self.vy  

                    
                    

                        
class F_RAY():
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.vx=0
        self.vy=0
        self.inertia=0
        self.pre_vx=0
        self.pre_vy=0
        self.rect = pygame.Rect(self.x,self.y,200,200)
        self.rect.center = (self.x,self.y)
        self.now_NT_Touch = []
        self.now_CT_Touch = []
        self.on_ground = False

            
                    
class NPC():
    def __init__(self,x,y,who,IMG,phase,ani):
        self.x = x
        self.y = y
        self.who = who
        self.phase = phase        
        self.surface = IMG
        self.ani = ani
        self.is_talked = 0
        