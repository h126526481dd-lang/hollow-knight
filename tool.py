import random
import os
import pygame
import math
import player_class
import object_class
import json

def save(player,scene_ctrl):
    p_path="save\save1\player.json"

    with open(p_path,'w',encoding='utf-8') as f:
        json.dump(player.to_dict(),f)

    s_path="save\save1\scene.json"
    
    with open(s_path,'w',encoding='utf-8') as f:
        json.dump(scene_ctrl.__dict__,f)



def load_p(save):
    match save:
        case 1:
            with open("save\save1\player.json", 'r', encoding='utf-8') as f:
                data = json.load(f)
            player=player_class.player.from_dict(data)
            player.read_surface()

            with open("save\save1\scene.json", 'r', encoding='utf-8') as f:
                data = json.load(f)


        case 2:
            with open('save\save_2.json', 'r', encoding='utf-8') as f:
                data = json.load(f)

                # 現在 data 變數中包含了 JSON 檔案的內容
                print(data)


        case 3:
            with open('save\save_3.json', 'r', encoding='utf-8') as f:
                data = json.load(f)

                # 現在 data 變數中包含了 JSON 檔案的內容
                print(data)


        case 4:
            with open('save\save_4.json', 'r', encoding='utf-8') as f:
                data = json.load(f)

                # 現在 data 變數中包含了 JSON 檔案的內容
                print(data)  
    return player   

def load_s(save,scene_ctrl):
    match save:
        case 1:
            with open("save\save1\scene.json", 'r', encoding='utf-8') as f:
                data = json.load(f)

            scene_ctrl.num = data["num"]
            scene_ctrl.menu = data["menu"]
            scene_ctrl.fps = data["fps"]
            scene_ctrl.button_cd = data["button_cd"]
            scene_ctrl.game = data["game"]
            scene_ctrl.pre_game = data["pre_game"]
            scene_ctrl.trans = data["trans"]
            scene_ctrl.R_edge = 0
            scene_ctrl.L_edge = 0
            scene_ctrl.From = 0

        case 2:
            with open('save\save_2.json', 'r', encoding='utf-8') as f:
                data = json.load(f)

            scene_ctrl.num = data["num"]
            scene_ctrl.menu = data["menu"]
            scene_ctrl.fps = data["fps"]
            scene_ctrl.button_cd = data["button_cd"]


        case 3:
            with open('save\save_3.json', 'r', encoding='utf-8') as f:
                data = json.load(f)

            scene_ctrl.num = data["num"]
            scene_ctrl.menu = data["menu"]
            scene_ctrl.fps = data["fps"]
            scene_ctrl.button_cd = data["button_cd"]

        case 4:
            with open('save\save_4.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            scene_ctrl.num = data["num"]
            scene_ctrl.menu = data["menu"]
            scene_ctrl.fps = data["fps"]
            scene_ctrl.button_cd = data["button_cd"]

    return scene_ctrl

          

def show(screen,scene,NT_object,CT_object,Enemy,ATKs_AL,ATKs_EN,player,strength_bar,trans,scene_ctrl):                          #繪製畫面(待修，以後應該是以場景為單位來繪製，要新增場景的class，裡面包含現在要輸入的東西)

    Info = pygame.display.Info()                                      #偵測用戶顯示參數
    screen_height = Info.current_h                                  #設定畫面大小成用戶螢幕大小
    screen_width  = Info.current_w

    adjust_y = screen_height//2                                 #螢幕中心座標
    adjust_x = screen_width//2
    camera_x = player.x - adjust_x                              #把角色置中所需要的向量  
    camera_y = player.y - adjust_y
    camera_x = max(camera_x, scene_ctrl.L_edge)
    camera_x = min(camera_x, scene_ctrl.R_edge)
    camera_y = max(camera_y, scene_ctrl.T_edge)
    camera_y = min(camera_y, scene_ctrl.B_edge - screen_height//2)
    #print(camera_x, camera_y)
    
    camera_rect = pygame.Rect(camera_x,camera_y,screen_width,screen_height)  #攝影機碰撞盒(只顯示在螢幕中的物件)
    

    screen.blit(scene, (-2000-camera_x, -2500 - camera_y))                  #繪製背景圖片(背景位置=原位置-置中向量)
   
    for obj in NT_object:                                 #繪製物件    (若與camera有碰撞，物件位置=原位置-置中向量)
        if camera_rect.colliderect(obj.rect):
            screen.blit(obj.surface, (obj.x - camera_x, obj.y - camera_y))
            pygame.draw.rect(screen, (255, 0, 0),pygame.Rect(obj.x - camera_x, obj.y - camera_y, obj.rect.width, obj.rect.height),1) 
            
            
    for obj in CT_object:                                 #繪製物件    (若與camera有碰撞，物件位置=原位置-置中向量)
        if camera_rect.colliderect(obj.rect):
            screen.blit(obj.surface, (obj.x - camera_x, obj.y - camera_y))
            pygame.draw.rect(screen, (255, 0, 0),pygame.Rect(obj.x - camera_x, obj.y - camera_y, obj.rect.width, obj.rect.height),1)
    

    for enemy in Enemy:
        if camera_rect.colliderect(enemy.rect):
            screen.blit(enemy.surface, (enemy.x - camera_x, enemy.y - camera_y))
            pygame.draw.rect(screen, (255, 0, 0),pygame.Rect(enemy.x - camera_x, enemy.y - camera_y, enemy.rect.width, enemy.rect.height),1)
            pygame.draw.rect(screen, (255, 0, 0),pygame.Rect(enemy.right_down_x - enemy.Test_rect.width - camera_x,  enemy.right_down_y - camera_y, enemy.Test_rect.width, enemy.Test_rect.height),1)
    

    for atk in ATKs_AL:                                 #繪製物件    (若與camera有碰撞，物件位置=原位置-置中向量)
        if camera_rect.colliderect(atk.rect):
            screen.blit(atk.surface, (atk.x - camera_x, atk.y - camera_y))
            pygame.draw.rect(screen, (255, 0, 0),pygame.Rect(atk.x - camera_x, atk.y - camera_y, atk.rect.width,atk.rect.height),1)
    

    for atk in ATKs_EN:                                 #繪製物件    (若與camera有碰撞，物件位置=原位置-置中向量)
        if camera_rect.colliderect(atk.rect):
            screen.blit(atk.surface, (atk.x - camera_x, atk.y - camera_y))
            pygame.draw.rect(screen, (255, 0, 0),pygame.Rect(atk.x - camera_x, atk.y - camera_y, atk.rect.width,atk.rect.height),1)
    
    if not player.hurt_flashing % 8 > 4:
        screen.blit(player.surface, ( player.x - camera_x,player.y - camera_y))#繪製角色    (角色位置=原位置-置中向量=螢幕中心)
    
    pygame.draw.rect(screen, (255, 0, 0),pygame.Rect(player.rect.x - camera_x,player.rect.y - camera_y, player.rect.width, player.rect.height),1)

    screen.blit(strength_bar, (screen_width//25, screen_height//6))

    pygame.draw.rect(screen, (255,255,255), (screen_width//20-5, screen_height//8-5, (screen_width//20+(player.Max_HP-5)*10)+10, screen_height//50+10))
    pygame.draw.rect(screen, (255,0,0), (screen_width//20, screen_height//8, (screen_width//20+((player.Max_HP-5)*10))-(screen_width//20+((player.Max_HP-5)*10))*((player.Max_HP-player.HP)/player.Max_HP), screen_height//50))
    
    if scene_ctrl.trans > 0:
        trans.x+=screen_width//30
        trans.rect.x+=screen_width//30
        scene_ctrl.trans -= 1
        screen.blit(trans.surface, (trans.x, trans.y))

    pygame.display.update()



def Touch(object1,object2):   #物件和物件  或  物件和玩家 的碰撞偵測
    
    T_rect = object2.surface.get_rect(topleft = (object2.x, object2.y))
  #物件2的碰撞盒複製(調整用)
    if not "1_D" in object1.now_NT_Touch:
        object1.on_ground = False

    
    if object1.rect.colliderect(object2.rect):
        T_rect.y += (max(abs(object1.vy),32))
        if not object1.rect.colliderect(T_rect) :    #若當前有碰撞，則偵測物件二往下調整後是否還有碰撞  
                                            

            if object2.can_be_through == 0:          #若物件2是可穿越的，則不做調整
                object1.now_NT_Touch.append("1_D")      #若往下調沒碰撞，表示物件1的底部碰撞到了物件2(D=Down)，新增標籤到碰撞清單
                T_rect.y-=(max(abs(object1.vy),32))

                for i in range(max(abs(object1.vy),32)):       #把物件1往上調整，直到不碰撞為止
                    object1.y -= 1
                    object1.rect.y -= 1    
                                                                                                    
                    
                    if not object1.rect.colliderect(T_rect) :    #若當前有碰撞，則偵測往上調整後是否還有碰撞  
                        object1.y += 1
                        object1.rect.y += 1
                        break

                object1.on_ground = True
                object1.vy = 0

            
                return True

        T_rect.y-=2*(max(abs(object1.vy),32))



        if not object1.rect.colliderect(T_rect) :    #若當前有碰撞，則偵測物件二往上調整後是否還有碰撞  


            if object2.can_be_through == 0:               #角色跟不可穿越物件 的上碰撞(上阻擋)偵測
                object1.now_NT_Touch.append("1_U")      #若往上調沒碰撞，表示物件1的頂部碰撞到了物件2(U=Up)，新增標籤到碰撞清單
                T_rect.y+=(max(abs(object1.vy),32))


                for i in range(max(abs(object1.vy),32)):                   #把物件1往下調整，直到不碰撞為止                                                                #把物件1往上調整，直到不碰撞為止
                    object1.y += 1
                    object1.rect.y += 1    

                    
                    if not object1.rect.colliderect(T_rect) :    
                        object1.y -= 1
                        object1.rect.y -= 1
                        break

                return True

        T_rect.y += (max(abs(object1.vy),32))
        T_rect.x += (max(abs(object1.vx),11))
        
        if not object1.rect.colliderect(T_rect) :    #若當前有碰撞，則偵測物件2往右調整後是否還有碰撞  

            if object2.can_be_through == 0 :               #角色跟不可穿越物件 的右碰撞(右阻擋)偵測
                object1.now_NT_Touch.append("1_R")      #若往右調沒碰撞，表示物件1的右部碰撞到了物件2，新增標籤到碰撞清單
                object1.inertia = 0
                T_rect.x -= (max(abs(object1.vx),11))

                    
                
                for i in range(max(abs(object1.vx),11)):       #把物件1往左調整，直到不碰撞為止
                    object1.x -= 1
                    object1.rect.x -= 1    
                    
                    if not object1.rect.colliderect(T_rect) :    #若當前有碰撞，則偵測往左調整後是否還有碰撞  
                        object1.x += 1
                        object1.rect.x += 1
                        break
                
                if object1.vx > 0:
                    object1.vx *= 0


            else:
                object1.now_CT_Touch.append("1_R")      
            return True

        T_rect.x -= 2*(max(abs(object1.vx),11))
        if not object1.rect.colliderect(T_rect):    #若當前有碰撞，則偵測物件2往左調整後是否還有碰撞  


            if object2.can_be_through == 0:               #角色跟不可穿越物件 的左碰撞(左阻擋)偵測
                object1.now_NT_Touch.append("1_L")      #若往左調沒碰撞，表示物件1的左部碰撞到了物件2，新增標籤到碰撞清單
                object1.inertia = 0
                T_rect.x += (max(abs(object1.vx),11))
                

                
                for i in range(max(abs(object1.vx),11)):       #把物件1往右調整，直到不碰撞為止
                    object1.x += 1
                    object1.rect.x += 1    
                                                                                                    
                    
                    if not object1.rect.colliderect(T_rect) :    #若當前有碰撞，則偵測往右調整後是否還有碰撞  
                        object1.x -= 1
                        object1.rect.x -= 1

                        break
                    
                if object1.vx < 0:
                    object1.vx *= 0 
                    
                    
            else:
                object1.now_CT_Touch.append("1_L")                
            return True
        
        if object2.can_be_through == 0:
            object1.vx = object1.pre_vx*-1
            object1.vy = object1.pre_vy*-1

        return True
    
    else:
        return False



#切割圖片(圖片, 切割次數)
def split(picture, times):
    frames = []
    sprite_sheet = pygame.image.load(picture).convert_alpha()
    frame_width = sprite_sheet.get_width() // times
    frame_height = sprite_sheet.get_height()

    #導入圖片，分割開後存進List  
    for i in range(times):
        frame = sprite_sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
        frames.append(frame)
    return frames  



def HRZ_combine(picture, times):
    sprite_sheet = pygame.image.load(picture).convert_alpha()
    w , h = sprite_sheet.get_size()
    big_surface = pygame.Surface((w*times, h), pygame.SRCALPHA)         #導入圖片(八張合一起)，分割開後存進List 

    for i in range(times):
        big_surface.blit(sprite_sheet, (w*i, 0))

    return   big_surface


def V_combine(picture, times):
    sprite_sheet = pygame.image.load(picture).convert_alpha()
    w , h = sprite_sheet.get_size()
    big_surface = pygame.Surface((w, h*times), pygame.SRCALPHA)         #導入圖片(八張合一起)，分割開後存進List 

    for i in range(times):
        big_surface.blit(sprite_sheet, (0, h*i))

    return   big_surface


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



#初始化動畫設定
def start_animation(state, image_list, change_time, flip, loop): 
    state["playing"] = True
    state["current_frame"] = 0
    state["timer"] = 0
    state["image_list"] = image_list
    state["change_time"] = change_time
    state["flip"] = flip
    state["loop"] = loop



#每偵更新動畫
def update_animation(obj, state):
    if not state.get("playing", False):
        return False

    state["timer"] += 1
    if state["timer"] >= state["change_time"]:
        state["timer"] = 0
        state["current_frame"] += 1

        # 播放結束判斷
        if state["current_frame"] >= len(state["image_list"]):
            if state["loop"]:
                state["current_frame"] = 0
            else:
                state["current_frame"] = len(state["image_list"]) - 1
                state["playing"] = False
                return True

    # 更新圖片
    frame = state["image_list"][state["current_frame"]]
    obj.surface = pygame.transform.flip(frame, True, False) if state["flip"] else frame
    return False



def tick_mission(screen,scene,Main,Enemy,ATKs_AL,ATKs_EN,NT_object,CT_object,keys,pre_keys,strength_bar,trans,scene_ctrl):

    if Main.endurance < 4:
        Main.endurance_cd -= 1
        if Main.endurance_cd == 0:
            Main.endurance += 1
            Main.endurance_cd = 120

    if Main.hurt_flashing > 0:
        Main.hurt_flashing -= 1
    
    Main.unhurtable_cd -= 1
    if Main.inertia > 0:
        Main.inertia -= 1

#=======================================================角色技能區

    if Main.skill_key[6] == 2:

        if Main.skill6_time >= 10:
            if Main.flip == False:
                Main.vx += 3
            else:
                Main.vx -= 3

        elif Main.skill6_time > 0 and abs(Main.vx) > 3:
            if Main.flip == False:
                Main.vx -= 3
            else:
                Main.vx += 3

        elif Main.skill6_time == 0:
            Main.skill_key[6] = 1
            Main.move_lock = 0

        Main.skill6_time -= 1
        Main.vy = 0
        
        
        
    if Main.skill_key[4] == 2:
        if Main.on_ground == True:
            Main.skill_key[4] = 1
        
#===========================================================移動按鍵判定(動vx)(動角色圖片)

    if Main.is_hurt == 0:

        if not Main.attack_state["playing"] or Main.atk_procedure != 0 :     #如果不是第三段攻擊
            if keys[pygame.K_d] and keys[pygame.K_a] and Main.move_lock == 0:                       #避免同時按兩個方向鍵
                if  Main.inertia == 0:
                    Main.idle() 
                    Main.vx = 0
                        
            else:
                        
                if keys[pygame.K_d] and Main.move_lock == 0:                                        #按下d鍵右移
                    Main.R_move()

                elif keys[pygame.K_a] and Main.move_lock == 0:                                      #按下a鍵左移
                    Main.L_move()

                else:                                                       #不移動時水平速度歸零(沒有慣性)
                    if  Main.inertia == 0:
                        Main.idle() 
                        Main.vx = 0
                                
        elif abs(Main.vx) > 0:
            if Main.flip:
                Main.vx += 2
            else:
                Main.vx -= 2

#====================================================================滯空動畫
        if not Main.on_ground:
            if Main.vy >= 0:
                Main.surface = pygame.transform.flip(Main.Jump[7], Main.flip, False)
            elif Main.vy < 0:
                Main.surface = pygame.transform.flip(Main.Jump[6], Main.flip, False)

#=================================================偵測角色攻擊按鍵(是否按下j鍵, 是否在撥放攻擊動畫, 前一偵是否按著j鍵)

        if keys[pygame.K_j] and not Main.attack_state["playing"] and not pre_keys[pygame.K_j] and Main.HP > 0 :

            #如果未銜接攻擊，攻擊步驟歸零
            if Main.atk_next <= 0:
                Main.atk_procedure = 0
            
        #生成攻擊劍氣

            #確認角色朝向
            if not Main.flip:
                match Main.atk_procedure:
                    case 0:
                        ATKs_AL.append(object_class.object(Main.x + 100,Main.y + 30,pygame.image.load("Image\Character\mainchacter\\blade1_start.png"),"dangerous",10,20,"blade1",0,0,0))
                    case 1:
                        ATKs_AL.append(object_class.object(Main.x + 100,Main.y + 30,pygame.image.load("Image\Character\mainchacter\\blade1_start.png"),"dangerous",10,20,"blade2",0,0,0))
                    case 2:
                        ATKs_AL.append(object_class.object(Main.x,Main.y,pygame.image.load("Image\Character\mainchacter\\blade1_start.png"),"dangerous",10,20,"blade3",0,0,0))
                            
            else:
                match Main.atk_procedure:
                    case 0:
                        ATKs_AL.append(object_class.object(Main.x - 70,Main.y + 30,pygame.image.load("Image\Character\mainchacter\\blade1_start.png"),"dangerous",10,20,"blade1",0,1,0))
                    case 1:
                        ATKs_AL.append(object_class.object(Main.x - 70,Main.y + 30,pygame.image.load("Image\Character\mainchacter\\blade1_start.png"),"dangerous",10,20,"blade2",0,1,0))
                    case 2:
                        ATKs_AL.append(object_class.object(Main.x,Main.y + 30,pygame.image.load("Image\Character\mainchacter\\blade1_start.png"),"dangerous",10,20,"blade3",0,1,0))
            
            Main.attack()

#=====================================================================衝刺按鍵

        if keys[pygame.K_LSHIFT] and Main.skill_key[6]==1 and (Main.on_ground==True or (Main.on_ground==False and Main.skill_key[5]==1)) and Main.endurance > 0 and Main.HP > 0:
            if Main.inertia == 0:
                Main.vx = 0
            Main.unhurtable_cd = max(22,Main.unhurtable_cd)
            Main.skill_key[6] = 2
            Main.skill6_time = 20
            Main.inertia = max(Main.inertia,20)
            Main.move_lock = 1
            Main.endurance -= 1



    else:
        Main.is_hurt-=1

#==================================================================斬擊朝向(動vx)

    for atk_al in ATKs_AL:
        if atk_al.dif == "blade1":
            if atk_al.flip == False:
                atk_al.x = Main.x + 100
                atk_al.y = Main.y + 30
                atk_al.rect.x = atk_al.x
                atk_al.rect.y = atk_al.y
            else:
                atk_al.x = Main.x - 70
                atk_al.y = Main.y + 30
                atk_al.rect.x = atk_al.x
                atk_al.rect.y = atk_al.y
        
        elif atk_al.dif == "blade2":
            if atk_al.flip == False:
                atk_al.x = Main.x + 100
                atk_al.y = Main.y + 30
                atk_al.rect.x = atk_al.x
                atk_al.rect.y = atk_al.y
            else:
                atk_al.x = Main.x - 70
                atk_al.y = Main.y + 30
                atk_al.rect.x = atk_al.x
                atk_al.rect.y = atk_al.y

        elif atk_al.dif == "blade3":
            atk_al.x = Main.x
            atk_al.y = Main.y + 30
            atk_al.rect.x = atk_al.x
            atk_al.rect.y = atk_al.y

        if atk_al.state["playing"] == False:
            start_animation(atk_al.state, atk_al.frames, 15, atk_al.flip, False)
            
        if atk_al.dur <= 0:
            ATKs_AL.remove(atk_al)
        atk_al.dur -= 1    
        update_animation(atk_al, atk_al.state)

#==================================================================攻擊動畫(動角色圖片)

    finished = update_animation(Main, Main.attack_state)

    if finished and Main.atk_next == 0:
        Main.atk_next = 20                              #此段攻擊結束需多久接下一段
    
    if Main.atk_next > 0:
        Main.atk_next -= 1

#==================================================================頂頭+下墜判定(動vy)
                    
    if "1_U" in Main.now_NT_Touch and Main.vy < 0:                          
        Main.vy = 0 

    if Main.on_ground == False:
        if ("1_L" in Main.now_NT_Touch or "1_R" in Main.now_NT_Touch) and Main.skill_key[5] == 1:   #如果碰牆就緩速下滑
            if Main.vy < 0 and Main.vy > -18:
                Main.vy = 0
            if Main.skill_key[4] >= 1:
                Main.skill_key[4] = 1
            if Main.vy <= 10:
                if Main.Wall_slip == 1:
                    Main.vy += 1
                    Main.Wall_slip = 0
                else:
                    Main.Wall_slip = 1

        elif Main.vy <= 30 and not Main.skill_key[6] == 2:           #重力加速度(有設上限)
            Main.vy += 1
    
    if "1_L" in Main.now_NT_Touch or "1_R" in Main.now_NT_Touch:
        Main.inertia = 0
#=================================================================撿技能球判定

    if keys[pygame.K_w]:
        for obj in CT_object:
            if obj.type == "skill":
                if Touch(Main,obj):
                    Main.skill_key[obj.num] = 1
                    CT_object.remove(obj)
                    del obj

#===============================================================碰撞清單清除、傷害判定以及敵人區

    for enemy in Enemy:
                    
        if enemy.unhurtable_cd > 0:
            enemy.unhurtable_cd -= 3
                        
        enemy.now_CT_Touch = []
        enemy.now_NT_Touch = []
    
    
    
    
    
            
        if enemy.type == 1 and enemy.found == 1 and enemy.phase_cd == 0:
            match enemy.phase:
                case 0:
                    pass
                case 1:
                    pass
                case 2:
                    pass
                case 3:
                    pass
                case 4:
                    ATKs_EN.append(object_class.object(enemy.x,enemy.y-100,pygame.transform.scale(pygame.image.load("Image\Object\\1.png"), (100, 100)),"dangerous",1,0,"bullet",None,None,None))
                    ATKs_EN.append(object_class.object(enemy.x+100,enemy.y-150,pygame.transform.scale(pygame.image.load("Image\Object\\1.png"), (100, 100)),"dangerous",1,0,"bullet",None,None,None))
                case 5:
                    ATKs_EN.append(object_class.object(enemy.x-300,enemy.y-100,pygame.transform.scale(pygame.image.load("Image\Object\\1.png"), (100, 100)),"dangerous",1,0,"bullet",None,None,None))
                    ATKs_EN.append(object_class.object(enemy.x,enemy.y-200,pygame.transform.scale(pygame.image.load("Image\Object\\1.png"), (100, 100)),"dangerous",1,0,"bullet",None,None,None))
                    ATKs_EN.append(object_class.object(enemy.x+300,enemy.y-100,pygame.transform.scale(pygame.image.load("Image\Object\\1.png"), (100, 100)),"dangerous",1,0,"bullet",None,None,None))
                                    
        
    
      
        player_class.enemy.Move(enemy,NT_object,Main)

        if Touch(Main,enemy):
            if Main.unhurtable_cd <= 0 and Main.HP > 1:

                if Main.rect.x-enemy.rect.x > 0:
                    Main.vx = 10
                    
                else:
                    Main.vx =- 10
                Main.y -= 10
                Main.rect.y -= 10
                Main.vy = -15
                Main.is_hurt = 30
                Main.get_hit()
                
            elif Main.unhurtable_cd <= 0 and Main.HP == 1:
                Main.get_hit()

        
        

            
            
                        
        for atk_al in ATKs_AL:
            
            if enemy.unhurtable_cd <= 0:
                            
                if Touch(enemy,atk_al):
                    if atk_al.rect.x - enemy.rect.x < 0:
                        enemy.HP -= atk_al.ATK
                        enemy.x += atk_al.KB
                        enemy.rect.x += atk_al.KB
                        enemy.unhurtable_cd = 60
                    else:
                        enemy.HP -= atk_al.ATK
                        enemy.x -= atk_al.KB
                        enemy.rect.x -= atk_al.KB
                        enemy.unhurtable_cd = 60

        for atk_en in ATKs_EN:
            
            if atk_en.dif == "bullet":
                
                atk_en.surface = atk_en.frames[atk_en.index//5]
                atk_en.index += 1
                if atk_en.index > 29:
                    atk_en.index = 0
                
                if atk_en.tag_x == None:
                    atk_en.tag_x = (Main.rect.x - atk_en.rect.x)//30 
                if atk_en.tag_y == None:
                    atk_en.tag_y = (Main.rect.y - atk_en.rect.y)//30
                
                atk_en.rect.x += atk_en.tag_x
                atk_en.rect.y += atk_en.tag_y
                atk_en.x = atk_en.rect.x
                atk_en.y = atk_en.rect.y
                
                for obj in NT_object:
                    if atk_en.rect.colliderect(obj.rect):
                        atk_en.delete = 1
                        
                if atk_en.rect.colliderect(Main.rect):
        
                    if Main.unhurtable_cd <= 0:
                                    
                        if Main.unhurtable_cd <= 0 and Main.HP > 1:
                            if Main.rect.x-atk_en.rect.x > 0:
                                Main.vx = 10
                                        
                            else:
                                Main.vx =- 10
                                Main.y -= 10
                                Main.rect.y -= 10
                                Main.vy = -15
                                Main.is_hurt = 30
                                Main.get_hit()
                                    
                        elif Main.unhurtable_cd <= 0 and Main.HP == 1:
                            Main.get_hit()
                        atk_en.delete = 1
                    
            if atk_en.delete == 1:        
                ATKs_EN.remove(atk_en)
                del atk_en            


        if enemy.HP <= 0:
            Enemy.remove(enemy)
            del enemy

    Main.now_NT_Touch = []                                      #角色目前碰撞清單

    for obj in NT_object:
        Touch(Main,obj)

#==================================================================蹬牆跳後的位移(動vx)

    if Main.Walljump_direct == 1:
        Main.vx = 7
        Main.flip = False
        Main.Walljump_time -= 1
        if Main.Walljump_time == 0:
            Main.Walljump_direct = 0
    
    elif Main.Walljump_direct == 2:
        Main.vx = -7
        Main.flip = True
        Main.Walljump_time -= 1
        if Main.Walljump_time == 0:
            Main.Walljump_direct = 0

#===================================================================跳躍和受傷判定

    #如果(按下空格, 在地上, 剛才沒按空格)
    if keys[pygame.K_SPACE] and not "1_U" in Main.now_NT_Touch and not pre_keys[pygame.K_SPACE] and Main.HP > 0:                                #按下空白鍵跳躍
        Main.jump()
    
    if Main.is_hurt > 0:
        Main.surface = pygame.transform.flip(Main.Hurt[0], Main.flip, False)

#===================================================================最終更新判定區
    Main.y += Main.vy                                       #更新角色位置
    Main.x += Main.vx

    Main.rect.x += Main.vx
    Main.rect.y += Main.vy

    Main.pre_vx = Main.vx
    Main.pre_vy = Main.vy

    for event in pygame.event.get():                               #偵測事件
                
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    if Main.y > scene_ctrl.B_edge + 500:
        Main.HP = 0
    
    
    
    if Main.HP<=0:
        Main.death_cd+=1
        Main.move_lock=1
        if Main.flip:
            Main.surface=pygame.transform.flip(Main.Dead[Main.death_cd//30],True,False)
        else:
            Main.surface=Main.Dead[Main.death_cd//30]
        if Main.death_cd == 89:
            scene_ctrl.game = "dead"

    
    
#=========================================================================刷新畫面

   
    show(screen,scene[0],NT_object,CT_object,Enemy,ATKs_AL,ATKs_EN,Main,strength_bar[Main.endurance],trans,scene_ctrl)    #最終印刷