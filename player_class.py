import random
import os
import pygame



def Touch(object1,object2):   #物件和物件  或  物件和玩家 的碰撞偵測
    
    T_rect = object2.surface.get_rect(topleft=(object2.x, object2.y))   #物件2的碰撞盒複製(調整用)

    
    if object1.rect.colliderect(object2.rect):
        T_rect.y+=(max(abs(object1.vy),32))
        if not object1.rect.colliderect(T_rect) :    #若當前有碰撞，則偵測物件二往下調整後是否還有碰撞  
                                            

            if object2.can_be_through == 0:          #若物件2是可穿越的，則不做調整
                object1.now_NT_Touch.append("1_D")      #若往下調沒碰撞，表示物件1的底部碰撞到了物件2(D=Down)，新增標籤到碰撞清單
                T_rect.y-=(max(abs(object1.vy),32))

                for i in range(max(abs(object1.vy),32)):       #把物件1往上調整，直到不碰撞為止
                    object1.y -= 1
                    object1.rect.y-=1    
                                                                                                    
                    
                    if not object1.rect.colliderect(T_rect) :    #若當前有碰撞，則偵測往上調整後是否還有碰撞  
                        object1.y += 1
                        object1.rect.y+=1
                        break

                object1.on_ground = True
            return True

        T_rect.y-=2*(max(abs(object1.vy),32))



        if not object1.rect.colliderect(T_rect) :    #若當前有碰撞，則偵測物件二往上調整後是否還有碰撞  


            if object2.can_be_through == 0:               #角色跟不可穿越物件 的上碰撞(上阻擋)偵測
                object1.now_NT_Touch.append("1_U")      #若往上調沒碰撞，表示物件1的頂部碰撞到了物件2(U=Up)，新增標籤到碰撞清單


                for i in range(max(abs(object1.vy),32)):                   #把物件1往下調整，直到不碰撞為止                                                                #把物件1往上調整，直到不碰撞為止
                    object1.y += 1
                    object1.rect.y+=1    

                    
                    if not object1.rect.colliderect(T_rect) :    
                        object1.y -= 1
                        object1.rect.y-=1
                        break

            return True

        T_rect.y+=(max(abs(object1.vy),32))
        T_rect.x+=(max(abs(object1.vx),11))
        
        if not object1.rect.colliderect(T_rect) :    #若當前有碰撞，則偵測物件2往右調整後是否還有碰撞  


            if object2.can_be_through == 0 :               #角色跟不可穿越物件 的右碰撞(右阻擋)偵測
                object1.now_NT_Touch.append("1_R")      #若往右調沒碰撞，表示物件1的右部碰撞到了物件2，新增標籤到碰撞清單
                object1.vx *= 0 
            return True


        T_rect.x-=2*(max(abs(object1.vx),11))
        if not object1.rect.colliderect(T_rect) :    #若當前有碰撞，則偵測物件2往左調整後是否還有碰撞  


            if object2.can_be_through == 0 :               #角色跟不可穿越物件 的左碰撞(左阻擋)偵測
                object1.now_NT_Touch.append("1_L")      #若往左調沒碰撞，表示物件1的左部碰撞到了物件2，新增標籤到碰撞清單
                object1.vx *= 0            
            return True

        return True
    else:
        return False




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



#播放動畫(物件, 幾偵動一下, 是否翻轉, 圖片數, 圖片清單)
def anime_update(object, change_time ,flip , image_num, image_list):
    object.anime_time += 1
    if object.anime_time >= change_time:
        object.image += 1
        object.anime_time = 0
        if object.image >= image_num:
            object.image = 0
    
    object.surface = image_list[object.image]
    if flip:
        object.surface = pygame.transform.flip(object.surface, True, False)
    object.mask = pygame.mask.from_surface(object.surface)                  #也許不需要？



def anime_update_click(object, change_time ,flip , image_num, image_list):
    delay_counter = 0
    image = 0
    for i in range(image_num):
        delay_counter += 1
        if delay_counter >= change_time:
            image+=1
            delay_counter = 0
        object.surface = image_list[image]
        if flip:
            object.surface = pygame.transform.flip(object.surface, True, False)
        object.mask = pygame.mask.from_surface(object.surface)
    '''for image in range(image_num):  
        object.surface = image_list[image]'''
    


class player():

             
    def __init__(self,name,x,y):                         #角色模型
        self.name = name                                              #角色名稱
        self.x = x                                                    #角色位置
        self.y = y
        
        self.HP = 5
        
        self.image = 0                                        #角色圖片
        self.vx = 0                                                   #角色速度
        self.vy = 0
        self.on_ground = False                                      #角色是否在地面上
        self.anime_time = 0
        self.flip = False

        self.now_NT_Touch = []                                      #角色目前碰撞清單


        #匯入Walk.png圖片並切分成動畫
        self.Walk = split("Character\mainchacter\Walk.png", 8)  
        self.surface = self.Walk[self.image]
        self.mask = pygame.mask.from_surface(self.surface)
        
        self.rect = self.surface.get_rect(topleft=(self.x, self.y+50))
        
        self.rect.x += 50
        
        self.rect.width -= 100
        self.rect.height -= 50

        #匯入Attack_1.png圖片並切分成動畫
        self.Attack1 = split("Character\mainchacter\Attack_1.png", 6) 
        self.Attack2 = split("Character\mainchacter\Attack_2.png", 4) 
        self.Attack3 = split("Character\mainchacter\Attack_3.png", 3) 
           
           
           
    def R_move(self):                                               #角色移動
        if not "1_R" in self.now_NT_Touch:   #若有右碰撞，則不移動
            self.vx = 10
            self.flip = False
            anime_update(self,5,False,8,self.Walk)



    def L_move(self):
        if not "1_L" in self.now_NT_Touch :   #若有左碰撞，則不移動

            self.vx = -10
            self.flip = True
            anime_update(self,5,True,8,self.Walk)



    def jump(self):
        if self.on_ground == True:
            self.vy = -20
    


    def idle(self):
        self.anime_time = 0
        self.image = 6
        self.surface = self.Walk[self.image]
        if self.flip:
            self.surface = pygame.transform.flip(self.surface, True, False)
        self.mask = pygame.mask.from_surface(self.surface)



    def attack(self):
        anime_update_click(self,2,False,6,self.Attack1)


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
        
        self.rect = self.surface.get_rect(topleft=(self.x, self.y))
        
    def Move(self,NT_object):
        
        match self.type:
            
            case 1:    
                pass
            
            
            case 2:    
                pass
            
            
            case 3:    
                pass
            
            
            case _:     
                for obj in NT_object:
                    Touch(self, obj)
                    if "1_D" in self.now_NT_Touch:
                        self.on_ground = True
                
                if self.on_ground :
                    self.vy = 0
                    self.vx = 5
                    self.x += self.vx
                    self.rect.x += self.vx
                else:
                    self.vy+=1
                    self.y += self.vy
                    self.rect.y += self.vy  