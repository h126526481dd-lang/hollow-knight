import random
import os
import pygame
import math
import player_class
import object_class
import json


def cross(A, B):
    return A[0]*B[1] - A[1]*B[0]


def draw_line(screen, L,adj_x,adj_y, color=(255,0,0)):
    A, B, C = L
    W, H = screen.get_size()

    # vertical line (B = 0)
    if abs(B) < 1e-6:
        x = -C / A
        pygame.draw.line(screen, color, (x-adj_x, 0-adj_y), (x-adj_x, H-adj_y))
        return

    # otherwise compute y for x=0, x=W
    y1 = -(A*-1000 + C) / B
    y2 = -(A*W + C) / B

    pygame.draw.line(screen, color, (-1000-adj_x, y1-adj_y), (W-adj_x, y2-adj_y))



def save(player,scene_ctrl):

    match scene_ctrl.Save:
        
        case 1:
            p_path="save\save1\player.json"
            s_path="save\save1\scene.json"
        case 2:
            p_path="save\save2\player.json"
            s_path="save\save2\scene.json"
        case 3:
            p_path="save\save3\player.json"
            s_path="save\save3\scene.json"
        case 4:
            p_path="save\save4\player.json"
            s_path="save\save4\scene.json"




    with open(p_path,'w',encoding='utf-8') as f:
        json.dump(player.to_dict(),f)

    
    with open(s_path,'w',encoding='utf-8') as f:
        json.dump(scene_ctrl.__dict__,f)




def reset(save,scene_ctrl):


    match save:
        case 1:
            p_path="save\save1\player.json"
        case 2:
            p_path="save\save2\player.json"
        case 3:
            p_path="save\save3\player.json"
        case 4:
            p_path="save\save4\player.json"



    with open(p_path, 'w', encoding='utf-8') as f:
        with open("save\init\player.json", 'r', encoding='utf-8') as F:
            data = json.load(F)
            player=player_class.player.from_dict(data)
            player.read_surface()

            json.dump(player.to_dict(),f)






    match save:
        case 1:
            s_path="save\save1\scene.json"
        case 2:
            s_path="save\save2\scene.json"
        case 3:
            s_path="save\save3\scene.json"
        case 4:
            s_path="save\save4\scene.json"

    with open(s_path, 'w', encoding='utf-8') as f:
        with open("save\init\scene.json", 'r', encoding='utf-8') as F:
            data = json.load(F)

        scene_ctrl.menu = data["menu"]
        scene_ctrl.fps = data["fps"]
        scene_ctrl.button_cd = data["button_cd"]
        scene_ctrl.game = data["game"]
        scene_ctrl.pre_game = data["pre_game"]
        scene_ctrl.trans = data["trans"]
        scene_ctrl.R_edge = 0
        scene_ctrl.L_edge = 0
        scene_ctrl.From = 0
        scene_ctrl.done = 0
        scene_ctrl.minute = 0
        scene_ctrl.second = 0


        json.dump(scene_ctrl.__dict__,f)



            

    



def load_p(save):
    match save:
        case 1:
            p_path="save\save1\player.json"
        case 2:
            p_path="save\save2\player.json"
        case 3:
            p_path="save\save3\player.json"
        case 4:
            p_path="save\save4\player.json"

    with open(p_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        player=player_class.player.from_dict(data)
        player.read_surface()

    return player   

def load_s(save,scene_ctrl):
    match save:
        case 1:
            s_path="save\save1\scene.json"
        case 2:
            s_path="save\save2\scene.json"
        case 3:
            s_path="save\save3\scene.json"
        case 4:
            s_path="save\save4\scene.json"
    
    with open(s_path, 'r', encoding='utf-8') as f:

        data = json.load(f)

    scene_ctrl.num = 10
    scene_ctrl.menu = data["menu"]
    scene_ctrl.fps = data["fps"]
    scene_ctrl.button_cd = data["button_cd"]
    scene_ctrl.game = data["game"]
    scene_ctrl.pre_game = data["pre_game"]
    scene_ctrl.trans = data["trans"]
    scene_ctrl.R_edge = 0
    scene_ctrl.L_edge = 0
    scene_ctrl.From = 0
    scene_ctrl.done = 0

    return scene_ctrl

          

def show(screen,scene,NT_object,CT_object,Enemy,ATKs_AL,ATKs_EN,player,hint_backpack,trans,scene_ctrl):                          #繪製畫面(待修，以後應該是以場景為單位來繪製，要新增場景的class，裡面包含現在要輸入的東西)

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
            pygame.draw.rect(screen, (255, 0, 0),pygame.Rect(obj.rect.x - camera_x, obj.rect.y - camera_y, obj.rect.width, obj.rect.height),1) 
        
        #if obj.type == "mirror_wall":
         #   pygame.draw.rect(screen, (255, 255, 0),pygame.Rect(obj.outerect.x - camera_x, obj.outerect.y - camera_y, obj.outerect.width, obj.outerect.height),1) 
            
          #  pygame.draw.rect(screen, (0, 255, 0),pygame.Rect(obj.F_Px - camera_x, obj.F_Py - camera_y, 10, 10),0)
           # pygame.draw.rect(screen, (0, 0, 255),pygame.Rect(obj.S_Px - camera_x, obj.S_Py - camera_y, 10, 10),0)
            #pygame.draw.rect(screen, (30, 30, 30),pygame.Rect(obj.T_Px - camera_x, obj.T_Py - camera_y, 10, 10),0)
            



            
            
    for obj in CT_object:                                 #繪製物件    (若與camera有碰撞，物件位置=原位置-置中向量)
        if camera_rect.colliderect(obj.rect):
            screen.blit(obj.surface, (obj.x - camera_x, obj.y - camera_y))
            pygame.draw.rect(screen, (255, 0, 0),pygame.Rect(obj.x - camera_x, obj.y - camera_y, obj.rect.width, obj.rect.height),1)
    

    for enemy in Enemy:
        if camera_rect.colliderect(enemy.rect):
            screen.blit(enemy.surface, (enemy.x - camera_x, enemy.y - camera_y))
            pygame.draw.rect(screen, (255, 0, 0),pygame.Rect(enemy.rect.x - camera_x, enemy.rect.y - camera_y, enemy.rect.width, enemy.rect.height),1)
            pygame.draw.rect(screen, (255, 0, 0),pygame.Rect(enemy.right_down_x - enemy.Test_rect.width - camera_x,  enemy.right_down_y - camera_y, enemy.Test_rect.width, enemy.Test_rect.height),1)
    

    for atk in ATKs_AL:                                 #繪製物件    (若與camera有碰撞，物件位置=原位置-置中向量)
        if camera_rect.colliderect(atk.rect):
            screen.blit(atk.surface, (atk.x - camera_x, atk.y - camera_y))
            pygame.draw.rect(screen, (255, 0, 0),pygame.Rect(atk.x - camera_x, atk.y - camera_y, atk.rect.width,atk.rect.height),1)
    

    for atk in ATKs_EN:                                 #繪製物件    (若與camera有碰撞，物件位置=原位置-置中向量)
        if camera_rect.colliderect(atk.rect):
            screen.blit(atk.surface, (atk.x - camera_x, atk.y - camera_y))
            pygame.draw.rect(screen, (255, 0, 0),pygame.Rect(atk.x - camera_x, atk.y - camera_y, atk.rect.width,atk.rect.height),1)
            
        if atk.dif == "light":
            for enemy in Enemy:
                if enemy.dif == "The_Sun":
                    
                    if enemy.light_count == 3:
                        enemy.theta =math.pi*4/5
                        enemy.I = (16*math.cos(enemy.theta+0.01*enemy.skill_time),16*math.sin(enemy.theta+0.01*enemy.skill_time))
                        enemy.II =(16*math.cos(enemy.theta/4*3+0.01*enemy.skill_time),16*math.sin(enemy.theta/4*3+0.01*enemy.skill_time))
                        enemy.III =(16*math.cos(enemy.theta/4*2+0.01*enemy.skill_time),16*math.sin(enemy.theta/4*2+0.01*enemy.skill_time))
                        enemy.IV =(16*math.cos(enemy.theta/4+0.01*enemy.skill_time),16*math.sin(enemy.theta/4+0.01*enemy.skill_time))
                        enemy.V =(16,0)
                    
                    match atk.num:
                        case 1:
                            (atk.tag_x,atk.tag_y) = enemy.I 
                        case 2:
                            (atk.tag_x,atk.tag_y) = enemy.II
                        case 3:
                            (atk.tag_x,atk.tag_y) = enemy.III
                        case 4:
                            (atk.tag_x,atk.tag_y) = enemy.IV
                        case 5:
                            (atk.tag_x,atk.tag_y) = enemy.V
                        case 6:
                            (atk.tag_x,atk.tag_y) = enemy.VI


                        
                        
            for i in range(atk.dur):
                        #print(atk.tag_x,atk.tag_y)
                        
                atk.x += atk.tag_x
                atk.rect.x += atk.tag_x
                atk.y += atk.tag_y
                atk.rect.y += atk.tag_y
                                                    
                if atk.rect.colliderect(player.rect) and player.unhurtable_cd <= 0:
                    if player.unhurtable_cd <= 0 and player.HP > 1:
                        if player.rect.x-atk.rect.x -atk.rect.width//2 > 0:
                            player.vx = 10
                        else:
                            player.vx =- 10
                        player.y -= 10
                        player.rect.y -= 10
                        player.vy = -15
                        player.is_hurt = 30
                        player.get_hit()
                                    
                    elif player.unhurtable_cd <= 0 and player.HP == 1:
                        player.get_hit()                                  
                        
                    

                for obj in NT_object:
                    

                    if obj.type == "mirror_wall" and  not atk.L_mirror == obj:
                        
                        if atk.rect.colliderect(obj.outerect):
        
                            tem_x = atk.tag_x
                            tem_y = atk.tag_y
                            
                            atkF=[obj.F_Px - (atk.rect.x+atk.rect.width/2), obj.F_Py - (atk.rect.y+atk.rect.height/2)]
                            atkS=[obj.S_Px - (atk.rect.x+atk.rect.width/2), obj.S_Py - (atk.rect.y+atk.rect.height/2)]
                            atkT=[obj.T_Px - (atk.rect.x+atk.rect.width/2), obj.T_Py - (atk.rect.y+atk.rect.height/2)]
                            
                            cFS = cross(atkF, atkS)
                            cST = cross(atkS, atkT)
                            cTF = cross(atkT, atkF)
                            
                            if cFS > 0:
                                L_1 = True
                            else:
                                L_1 = False
                            
                            if cST > 0:
                                L_2 = True
                            else:
                                L_2 = False
                                
                            if cTF > 0:
                                L_3 = True
                            else:
                                L_3 = False
        
        
                            if (L_1 == L_2 == L_3):
                                atk.x -= atk.tag_x
                                atk.rect.x -= atk.tag_x
                                atk.y -= atk.tag_y
                                atk.rect.y -= atk.tag_y
                                
                                if atk.pre_test == 1:
                                    atk.tag_x = (math.cos(math.radians(obj.angle+90)*-2) * tem_x + math.sin(math.radians(obj.angle+90)*-2) * tem_y) *-1
                                    atk.tag_y = (math.sin(math.radians(obj.angle+90)*-2) * tem_x - math.cos(math.radians(obj.angle+90)*-2) * tem_y) * -1
                                    
                                elif atk.pre_test == 2:
                                    atk.tag_x = (math.cos(math.radians(obj.angle+120)*-2) * tem_x + math.sin(math.radians(obj.angle+120)*-2) * tem_y) *-1
                                    atk.tag_y = (math.sin(math.radians(obj.angle+120)*-2) * tem_x - math.cos(math.radians(obj.angle+120)*-2) * tem_y) * -1
                                    
                                elif atk.pre_test == 3:
                                    atk.tag_x = (math.cos(math.radians(obj.angle+60)*-2) * tem_x + math.sin(math.radians(obj.angle+60)*-2) * tem_y) *-1
                                    atk.tag_y = (math.sin(math.radians(obj.angle+60)*-2) * tem_x - math.cos(math.radians(obj.angle+60)*-2) * tem_y) * -1
                                
                                atk.L_mirror = obj  
                                atk.pre_test = 0        
                                

                            

                            
                            if L_1 == L_2:
                                atk.pre_test = 3
                            elif L_2 == L_3:
                                atk.pre_test = 1
                            elif L_3 == L_1:
                                atk.pre_test = 2
                            
                            
                            
                            
                                                       
                  
                    elif atk.rect.colliderect(obj.rect) and not atk.L_mirror == obj:
                        atk.delete =1
                            
                        
                        
                if camera_rect.colliderect(atk.rect):
                    screen.blit(atk.surface, (atk.x - camera_x, atk.y - camera_y))                

                    
                if atk.delete == 1:
                    break
                    
            ATKs_EN.remove(atk)
            del atk
                    
        elif atk.dif == "pre_light":
            for enemy in Enemy:
                if enemy.dif == "The_Sun":
                    
                    if enemy.light_count == 3:
                        enemy.theta =math.pi*4/5
                        enemy.I = (16*math.cos(enemy.theta),16*math.sin(enemy.theta))
                        enemy.II =(16*math.cos(enemy.theta/4*3),16*math.sin(enemy.theta/4*3))
                        enemy.III =(16*math.cos(enemy.theta/4*2),16*math.sin(enemy.theta/4*2))
                        enemy.IV =(16*math.cos(enemy.theta/4),16*math.sin(enemy.theta/4))
                        enemy.V =(16,0)
                    
                    match atk.num:
                        case 1:
                            (atk.tag_x,atk.tag_y) = enemy.I 
                        case 2:
                            (atk.tag_x,atk.tag_y) = enemy.II
                        case 3:
                            (atk.tag_x,atk.tag_y) = enemy.III
                        case 4:
                            (atk.tag_x,atk.tag_y) = enemy.IV
                        case 5:
                            (atk.tag_x,atk.tag_y) = enemy.V
                        case 6:
                            (atk.tag_x,atk.tag_y) = enemy.VI
                            
            for i in range(atk.dur):
                        #print(atk.tag_x,atk.tag_y)
                        
                atk.x += atk.tag_x
                atk.rect.x += atk.tag_x
                atk.y += atk.tag_y
                atk.rect.y += atk.tag_y
                                  
                
                    
                for obj in NT_object:
                    

                    if obj.type == "mirror_wall" and  not atk.L_mirror == obj:
                        
                        if atk.rect.colliderect(obj.outerect):
        
                            tem_x = atk.tag_x
                            tem_y = atk.tag_y
                            
                            atkF=[obj.F_Px - (atk.rect.x+atk.rect.width/2), obj.F_Py - (atk.rect.y+atk.rect.height/2)]
                            atkS=[obj.S_Px - (atk.rect.x+atk.rect.width/2), obj.S_Py - (atk.rect.y+atk.rect.height/2)]
                            atkT=[obj.T_Px - (atk.rect.x+atk.rect.width/2), obj.T_Py - (atk.rect.y+atk.rect.height/2)]
                            
                            cFS = cross(atkF, atkS)
                            cST = cross(atkS, atkT)
                            cTF = cross(atkT, atkF)
                            
                            if cFS > 0:
                                L_1 = True
                            else:
                                L_1 = False
                            
                            if cST > 0:
                                L_2 = True
                            else:
                                L_2 = False
                                
                            if cTF > 0:
                                L_3 = True
                            else:
                                L_3 = False
        
        
                            if (L_1 == L_2 == L_3):
                                atk.x -= atk.tag_x
                                atk.rect.x -= atk.tag_x
                                atk.y -= atk.tag_y
                                atk.rect.y -= atk.tag_y
                                
                                if atk.pre_test == 1:
                                    atk.tag_x = (math.cos(math.radians(obj.angle+90)*-2) * tem_x + math.sin(math.radians(obj.angle+90)*-2) * tem_y) *-1
                                    atk.tag_y = (math.sin(math.radians(obj.angle+90)*-2) * tem_x - math.cos(math.radians(obj.angle+90)*-2) * tem_y) * -1
                                    
                                elif atk.pre_test == 2:
                                    atk.tag_x = (math.cos(math.radians(obj.angle+120)*-2) * tem_x + math.sin(math.radians(obj.angle+120)*-2) * tem_y) *-1
                                    atk.tag_y = (math.sin(math.radians(obj.angle+120)*-2) * tem_x - math.cos(math.radians(obj.angle+120)*-2) * tem_y) * -1
                                    
                                elif atk.pre_test == 3:
                                    atk.tag_x = (math.cos(math.radians(obj.angle+60)*-2) * tem_x + math.sin(math.radians(obj.angle+60)*-2) * tem_y) *-1
                                    atk.tag_y = (math.sin(math.radians(obj.angle+60)*-2) * tem_x - math.cos(math.radians(obj.angle+60)*-2) * tem_y) * -1
                                
                                atk.L_mirror = obj  
                                atk.pre_test = 0        
                                

                            

                            
                            if L_1 == L_2:
                                atk.pre_test = 3
                            elif L_2 == L_3:
                                atk.pre_test = 1
                            elif L_3 == L_1:
                                atk.pre_test = 2

        
                            
                                                       
                  
                    elif atk.rect.colliderect(obj.rect) and not atk.L_mirror == obj:
                        atk.delete =1
                            
                        
                        
                if camera_rect.colliderect(atk.rect):
                    screen.blit(atk.surface, (atk.x - camera_x, atk.y - camera_y))                

                    
                if atk.delete == 1:
                    break
                    
            ATKs_EN.remove(atk)
            del atk
            
            
    
    if not player.hurt_flashing % 8 > 4:
        screen.blit(player.surface, ( player.x - camera_x,player.y - camera_y))#繪製角色    (角色位置=原位置-置中向量=螢幕中心)
    
    pygame.draw.rect(screen, (255, 0, 0),pygame.Rect(player.rect.x - camera_x,player.rect.y - camera_y, player.rect.width, player.rect.height),1)

    screen.blit(hint_backpack, (screen_width//100, screen_height//40*39))

    pygame.draw.rect(screen, (0,0,0), (screen_width//20-5, screen_height//8-5, player.Max_HP*50+10, screen_height//40+10))
    pygame.draw.rect(screen, (255,255,255), (screen_width//20, screen_height//8, player.Max_HP*50, screen_height//40))
    pygame.draw.rect(screen, (255,0,0), (screen_width//20, screen_height//8, player.HP*50, screen_height//40))
    
    pygame.draw.rect(screen, (0,0,0), (screen_width//20-5, screen_height//20+145, player.Max_endurance*50+10, screen_height//50+10))
    pygame.draw.rect(screen, (255,255,255), (screen_width//20, screen_height//20+150, player.Max_endurance*50, screen_height//50))
    pygame.draw.rect(screen, (135,206,235), (screen_width//20, screen_height//20+150, player.endurance*50, screen_height//50))
    
    
    
    if scene_ctrl.trans > 0:
        trans.x+=screen_width//30
        trans.rect.x+=screen_width//30
        scene_ctrl.trans -= 1
        screen.blit(trans.surface, (trans.x, trans.y))

    pygame.display.update()



def Touch(object1,object2):   #物件和物件  或  物件和玩家 的碰撞偵測
    
    T_rect = pygame.Rect(object2.rect.x,object2.rect.y,object2.rect.width,object2.rect.height)
  #物件2的碰撞盒複製(調整用)
    if not ("1_D" in object1.now_NT_Touch) and not ("1_DP" in object1.now_NT_Touch):
        object1.on_ground = 0

    
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

                object1.on_ground = 1
                object1.vy = 0
                return True
                        
            
            elif object2.can_be_through == 2 :
                if object1.vy >= 0 and object1.through == 0:
  
                    object1.now_NT_Touch.append("1_DP")      #若往下調沒碰撞，表示物件1的底部碰撞到了物件2(D=Down)，新增標籤到碰撞清單
                    T_rect.y-=(max(abs(object1.vy),32))

                    
                    for i in range(max(abs(object1.vy),32)):       #把物件1往上調整，直到不碰撞為止
                        object1.y -= 1
                        object1.rect.y -= 1    
                                                                                                        
                        
                        if not object1.rect.colliderect(T_rect) :    #若當前有碰撞，則偵測往上調整後是否還有碰撞  
                            object1.y += 1
                            object1.rect.y += 1
                            break


                    object1.vy = 0
                    object1.on_ground = 2
                    
                return True
            else :
                object1.now_CT_Touch.append("1_D")      
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
            
            elif object2.can_be_through == 2 :
                if object1.through == 0:
                    object1.now_NT_Touch.append("1_UP")      #若往下調沒碰撞，表示物件1的底部碰撞到了物件2(D=Down)，新增標籤到碰撞清單
                    
                return True
            else :
                object1.now_CT_Touch.append("1_U")      
                return True

        T_rect.y += (max(abs(object1.vy),32))
        T_rect.x += (max(abs(object1.vx),32))
        
        if not object1.rect.colliderect(T_rect) :    #若當前有碰撞，則偵測物件2往右調整後是否還有碰撞  

            if object2.can_be_through == 0 :               #角色跟不可穿越物件 的右碰撞(右阻擋)偵測
                
                object1.now_NT_Touch.append("1_R")      #若往右調沒碰撞，表示物件1的右部碰撞到了物件2，新增標籤到碰撞清單
                object1.inertia = 0
                T_rect.x -= (max(abs(object1.vx),32))

                    
                
                for i in range(max(abs(object1.vx),32)):       #把物件1往左調整，直到不碰撞為止
                    object1.x -= 1
                    object1.rect.x -= 1    
                    
                    if not object1.rect.colliderect(T_rect) :    #若當前有碰撞，則偵測往左調整後是否還有碰撞  
                        object1.x += 1
                        object1.rect.x += 1
                        break
                
                if object1.vx > 0:
                    object1.vx *= 0
                
                return True

            elif object2.can_be_through == 2 :               #角色跟不可穿越物件 的右碰撞(右阻擋)偵測
                if object1.through == 0:
                    object1.now_NT_Touch.append("1_RP")      #若往右調沒碰撞，表示物件1的右部碰撞到了物件2，新增標籤到碰撞清單
                return True

            else:
                object1.now_CT_Touch.append("1_R")      
                return True

        T_rect.x -= 2*(max(abs(object1.vx),32))
        if not object1.rect.colliderect(T_rect):    #若當前有碰撞，則偵測物件2往左調整後是否還有碰撞  


            if object2.can_be_through == 0:               #角色跟不可穿越物件 的左碰撞(左阻擋)偵測
                object1.now_NT_Touch.append("1_L")      #若往左調沒碰撞，表示物件1的左部碰撞到了物件2，新增標籤到碰撞清單
                object1.inertia = 0
                T_rect.x += (max(abs(object1.vx),32))
                

                
                for i in range(max(abs(object1.vx),32)):       #把物件1往右調整，直到不碰撞為止
                    object1.x += 1
                    object1.rect.x += 1    
                                                                                                    
                    
                    if not object1.rect.colliderect(T_rect) :    #若當前有碰撞，則偵測往右調整後是否還有碰撞  
                        object1.x -= 1
                        object1.rect.x -= 1

                        break

                if object1.vx < 0:
                    object1.vx *= 0 
                return True
                    
            elif object2.can_be_through == 2:               #角色跟不可穿越物件 的左碰撞(左阻擋)偵測
                if object1.through == 0:
                    object1.now_NT_Touch.append("1_LP")      #若往左調沒碰撞，表示物件1的左部碰撞到了物件2，新增標籤到碰撞清單
                return True
                
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
def anime_update(object, change_time ,flip , image_num, image_list, scale = None):
    object.anime_time += 1
    if object.anime_time >= change_time:
        object.image += 1
        object.anime_time = 0
        if object.image >= image_num:
            object.image = 0
    
    object.surface = image_list[object.image]
    if scale != None:
        object.surface = pygame.transform.scale(object.surface, scale)
    if flip:
        object.surface = pygame.transform.flip(object.surface, True, False)



#初始化動畫設定(物件字典(宣告時需加playing), 圖片清單, 幾偵換下一張, 是否循環, 大小(預設則不填))
def start_animation(state, image_list, change_time, flip, loop, scale = None): 
    state["playing"] = True
    state["current_frame"] = 0
    state["timer"] = 0
    state["image_list"] = image_list
    state["change_time"] = change_time
    state["flip"] = flip
    state["loop"] = loop
    state["scale"] = scale



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
    if state["scale"] != None:
        frame = pygame.transform.scale(frame, state["scale"])
    obj.surface = pygame.transform.flip(frame, True, False) if state["flip"] else frame
    return False



def tick_mission(screen,scene,Main,Enemy,ATKs_AL,ATKs_EN,NT_object,CT_object,keys,pre_keys,hint_backpack,trans,scene_ctrl):
    
    if Main.current_HP != Main.HP:
        
        Main.lost_HP = Main.HP-Main.current_HP
    
    Main.current_HP = Main.HP
    
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
        if Main.on_ground :
            Main.skill_key[4] = 1

#=====================================================================格擋

    update_animation(Main, Main.block_state)
    if keys[pygame.K_l] and Main.on_ground and not Main.attack_state["playing"] and not Main.block_state["playing"]:
        Main.block()
        
#===========================================================移動按鍵判定(動vx)(動角色圖片)

    if Main.is_hurt == 0:

        if (not Main.attack_state["playing"] and not Main.block_state["playing"]) or Main.atk_procedure != 0:     #如果不是第三段攻擊
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

        if keys[pygame.K_j] and not Main.attack_state["playing"] and not pre_keys[pygame.K_j] and Main.HP > 0 and not Main.block_state["playing"]:

            #如果未銜接攻擊，攻擊步驟歸零
            if Main.atk_next <= 0:
                Main.atk_procedure = 0
            
        #生成攻擊劍氣

            #確認角色朝向
            if not Main.flip:
                match Main.atk_procedure:
                    case 0:
                        ATKs_AL.append(object_class.object(Main.x + 100,Main.y + 30,pygame.image.load("Image\Character\mainchacter\\blade1_start.png"),"dangerous",Main.ATK,20,"blade1",0,0,0))
                    case 1:
                        ATKs_AL.append(object_class.object(Main.x + 100,Main.y + 30,pygame.image.load("Image\Character\mainchacter\\blade1_start.png"),"dangerous",Main.ATK,20,"blade2",0,0,0))
                    case 2:
                        ATKs_AL.append(object_class.object(Main.x,Main.y,pygame.image.load("Image\Character\mainchacter\\blade1_start.png"),"dangerous",Main.ATK,20,"blade3",0,0,0))
                            
            else:
                match Main.atk_procedure:
                    case 0:
                        ATKs_AL.append(object_class.object(Main.x - 70,Main.y + 30,pygame.image.load("Image\Character\mainchacter\\blade1_start.png"),"dangerous",Main.ATK,20,"blade1",0,1,0))
                    case 1:
                        ATKs_AL.append(object_class.object(Main.x - 70,Main.y + 30,pygame.image.load("Image\Character\mainchacter\\blade1_start.png"),"dangerous",Main.ATK,20,"blade2",0,1,0))
                    case 2:
                        ATKs_AL.append(object_class.object(Main.x,Main.y + 30,pygame.image.load("Image\Character\mainchacter\\blade1_start.png"),"dangerous",Main.ATK,20,"blade3",0,1,0))
            
            Main.attack()

#=====================================================================衝刺按鍵

        if keys[pygame.K_LSHIFT] and Main.skill_key[6]==1 and (Main.on_ground or (Main.on_ground==False and Main.skill_key[5]==1)) and Main.endurance > 0 and Main.HP > 0 and Main.move_lock == 0:
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

        if atk_al.dif == "blade1" or atk_al.dif == "blade2" or atk_al.dif == "blade3":
                
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
            else:
                Main.vy = 10

        elif Main.vy <= 30 and not Main.skill_key[6] == 2:           #重力加速度(有設上限)
            Main.vy += 1
    
    if "1_L" in Main.now_NT_Touch or "1_R" in Main.now_NT_Touch:
        Main.inertia = 0
#=================================================================w判定

    if keys[pygame.K_w]:
        for obj in CT_object:
            if Touch(Main,obj):
                
                if obj.type == "save_point":
                        

                        Main.HP=Main.Max_HP
                        save(Main,scene_ctrl)
                        Main.read_surface()


                if obj.type == "skill":
                        Main.skill_key[obj.num] = 1
                        CT_object.remove(obj)
                        del obj
                        



    for obj in CT_object:
        if Touch(Main,obj):

            if obj.type == "path":
                scene_ctrl.game = obj.goto[0]
                scene_ctrl.From = obj.goto[1]

#===============================================================敵人邏輯區

    for enemy in Enemy:

        if enemy.unhurtable_cd > 0:                             #無敵幀倒數
            enemy.unhurtable_cd -= 1
                    
        enemy.now_CT_Touch = []                                 #清空碰撞
        enemy.now_NT_Touch = []
       
        enemy.anime = update_animation(enemy, enemy.attack_state)#古老智慧(丁丁自行描述，拎北不管這個)
        enemy.attack_state["playing"]


        match enemy.type:                                       #分流 (波鼠 菁英 路邊) 

            case "boss":
                print("enemy=",enemy.type,"、",enemy.dif,",cd=",enemy.phase_cd,",wait=",enemy.wait,",found=",enemy.found,",phase=",enemy.phase,",skill_time=",enemy.skill_time,",back=",enemy.back,",HP=",enemy.HP,",broke=",enemy.broke)


                match enemy.dif:                                #分流不同波鼠

                    case "The_Tank":                            #牢坦克


                        if enemy.found and enemy.wait == 0:                                         #已發現玩家且停頓幀==0

                            if enemy.phase_cd > 0:                                                  #出招冷卻倒數
                                enemy.phase_cd -= 1
                                anime_update(enemy, 4 ,enemy.back-1 , 6, enemy.boss_walk, (320,300))#未出招播走路動畫

                            if enemy.phase_cd == 0 and not enemy.attack_state["playing"]:           #出招冷卻歸零播招式動畫 & 針對不同招式需求初始化
                                match enemy.phase:


                                    case 0: #零前搖衝刺
                                        if Main.rect.x - enemy.rect.x - enemy.rect.width//2 > 0:    #衝刺前轉向玩家
                                            enemy.back = 1
                                        else:
                                            enemy.back = -1
                                        start_animation(enemy.attack_state, enemy.boss_attack3, 10, enemy.back-1, False, (320,300))       
                            
                                    case 1: #射2子彈
                                        start_animation(enemy.attack_state, enemy.boss_attack2, 6, enemy.back-1, False, (320,300))

                                    case 2: #射3子彈
                                        start_animation(enemy.attack_state, enemy.boss_attack1, 6, enemy.back-1, False, (320,300))

                                    case 3:  #因果律起跳
                                        if Main.rect.x - enemy.rect.x - enemy.rect.width//2 > 0:    #起跳前轉向玩家
                                            enemy.back = 1
                                        else:
                                            enemy.back = -1
                                        start_animation(enemy.attack_state, enemy.boss_attack4, 3, enemy.back-1, False, (320,300))

                                        enemy.vy = -40                                              #播動畫時起跳
                                        enemy.vx = 0
                                                
                                        enemy.back_cd = 0                                           #避免起跳變陀螺
                                                
                                        enemy.y += enemy.vy
                                        enemy.rect.y += enemy.vy
                                                

                            elif enemy.attack_state["playing"]:         #動畫執行中，出招cd = -1
                                enemy.phase_cd = -1
                                if enemy.phase == 3:                    #若招為因果律起跳，補上重力加速度
                                    enemy.vy+=2

                            elif enemy.anime:                           #動畫播放完畢，出招cd = -2
                                enemy.phase_cd = -2

                            elif enemy.phase_cd == -2:                  #前搖完二次初始化

                                match enemy.phase:

                                    case 0:     #零前搖衝刺
                                        enemy.skill_time = 30           #技能時長30幀
                                        enemy.vx = 0                    #初始速度歸零
                                        enemy.vy = 0
                                                
                                        if Main.rect.x - enemy.rect.x - enemy.rect.width//2 > 0:    #轉向
                                            enemy.back = 1
                                        else:
                                            enemy.back = -1
                                                

                                    case 1:     #射2子彈
                                        enemy.skill_time = 0            #不需要技能時長

                                                                        #發子彈
                                        ATKs_EN.append(object_class.object(enemy.x,enemy.y-100,pygame.transform.scale(pygame.image.load("Image\Character\Enemy\Boss\Bullet.png"), (100, 100)),"dangerous",1,0,"bullet",None,None,None))
                                        ATKs_EN.append(object_class.object(enemy.x+100,enemy.y-150,pygame.transform.scale(pygame.image.load("Image\Character\Enemy\Boss\Bullet.png"), (100, 100)),"dangerous",1,0,"bullet",None,None,None))
                                    

                                    case 2:     #射3子彈
                                        enemy.skill_time = 0            #不需要技能時長

                                                                        #發子彈
                                        ATKs_EN.append(object_class.object(enemy.x-300,enemy.y-100,pygame.transform.scale(pygame.image.load("Image\Character\Enemy\Boss\Bullet.png"), (100, 100)),"dangerous",1,0,"bullet",None,None,None))
                                        ATKs_EN.append(object_class.object(enemy.x,enemy.y-200,pygame.transform.scale(pygame.image.load("Image\Character\Enemy\Boss\Bullet.png"), (100, 100)),"dangerous",1,0,"bullet",None,None,None))
                                        ATKs_EN.append(object_class.object(enemy.x+300,enemy.y-100,pygame.transform.scale(pygame.image.load("Image\Character\Enemy\Boss\Bullet.png"), (100, 100)),"dangerous",1,0,"bullet",None,None,None))
                                        
                                    case 3:     #因果律起跳
                                        enemy.skill_time = 15           #技能時長15幀
                                        enemy.wait = 10                 #空中停頓
                                        if Main.rect.x - enemy.rect.x - enemy.rect.width//2 > 0:    #轉向
                                            enemy.back = 1
                                        else:
                                            enemy.back = -1


                                enemy.phase_cd = -3                     #招式發動階段

                            elif enemy.phase_cd == -3 and enemy.skill_time > 0: #技能時長內觸發

                                for obj in NT_object:                           #讀碰撞(該狀態內不讀Move)
                                    Touch(enemy, obj)
                                    
                                enemy.skill_time -= 1                           #扣時

                                match enemy.phase:
                                    
                                    case 0:                                                 #衝刺
                                            
                                        if enemy.skill_time >= 15:                          #前半加速
                                                
                                            enemy.vx += 3 

                                        elif enemy.skill_time >= 0 and abs(enemy.vx) > 3:   #後半減速
                                            
                                            enemy.vx -= 3


                                        if enemy.skill_time == 0:                           #停止時轉向
                                            if Main.rect.x - enemy.rect.x - enemy.rect.width//2 > 0:
                                                enemy.back = 1
                                            else:
                                                enemy.back = -1
                                            
                                    case 3:                                                 #因果律起跳
                                    

                                        enemy.vy += 1                                       #補重力加速度

                                        if enemy.vy >= 0:                                   #最高點後給水平速度
                                            enemy.vx = 40

                                                
                                        if enemy.skill_time == 0:                                       #落地發子彈
                                            ATKs_EN.append(object_class.object(Main.x-200,Main.y-200,pygame.transform.scale(pygame.image.load("Image\Character\Enemy\Boss\Bullet.png"), (100, 100)),"dangerous",1,0,"bullet",None,None,None))
                                            ATKs_EN.append(object_class.object(Main.x,Main.y-300,pygame.transform.scale(pygame.image.load("Image\Character\Enemy\Boss\Bullet.png"), (100, 100)),"dangerous",1,0,"bullet",None,None,None))
                                            ATKs_EN.append(object_class.object(Main.x+200,Main.y-200,pygame.transform.scale(pygame.image.load("Image\Character\Enemy\Boss\Bullet.png"), (100, 100)),"dangerous",1,0,"bullet",None,None,None))
                                            
                                            if Main.rect.x - enemy.rect.x - enemy.rect.width//2 > 0:    #落地轉向
                                                enemy.back = 1
                                            else:
                                                enemy.back = -1

                            elif enemy.phase_cd == -3 and enemy.skill_time == 0:                        #放完技能
                                enemy.phase=random.randint(0,3)                                         #重骰招 & cd
                                enemy.phase_cd = random.randint(10,40)

                                if enemy.broke == 18 :                                                  #吃15刀癱瘓
                                    start_animation(enemy.attack_state, enemy.boss_break, 5, enemy.back-1, False, (320,300))
                                    enemy.wait = 450
                                    enemy.broke = 0
                        
                        
                        if enemy.wait == 31:                                                            #起身動畫
                            start_animation(enemy.attack_state, enemy.boss_up, 5, enemy.back-1, False, (320,300))







                    case "The_Sun":
                        if enemy.found and enemy.wait == 0:                                         #已發現玩家且停頓幀==0
                            
                            if enemy.phase_cd > 0:                                                  #出招冷卻倒數
                                enemy.phase_cd -= 1
                                
                            if  pow((Main.rect.x + Main.rect.width//2 - (enemy.rect.x+enemy.rect.width//2)),2) + pow((Main.rect.y + Main.rect.height//2 - (enemy.rect.y+enemy.rect.height//2)),2) <= pow(400,2) and enemy.sun_blaze ==0:
                                ATKs_EN.append(object_class.object(enemy.rect.x-175,enemy.rect.y-150,pygame.image.load("Image\Character\Enemy\Boss\sun_blaze.png"),"dangerous",1,1,"sun_blaze",0,0,0))    #太陽閃焰！
                                enemy.unhurtable_cd = 30
                                enemy.sun_blaze = 1
                            
                            if enemy.phase_cd == 0 and not enemy.attack_state["playing"]:           #出招冷卻歸零播招式動畫 & 針對不同招式需求初始化
                                match enemy.phase:


                                    case 0: #輻(射)光(線)
                                        start_animation(enemy.attack_state,enemy.boss_idle, 45, enemy.back, False) 

                                        if enemy.light_count < 3:
                                            enemy.theta =random.uniform(math.pi*5/6,math.pi*6/7)
                                            enemy.I = (16*math.cos(enemy.theta),16*math.sin(enemy.theta))
                                            enemy.theta =random.uniform(math.pi*3/6,math.pi*4/6)
                                            enemy.II =(16*math.cos(enemy.theta),16*math.sin(enemy.theta))
                                            enemy.theta =random.uniform(math.pi*2/6,math.pi*3/6)
                                            enemy.III =(16*math.cos(enemy.theta),16*math.sin(enemy.theta))
                                            enemy.theta =random.uniform(math.pi*1/7,math.pi*1/6)
                                            enemy.IV =(16*math.cos(enemy.theta),16*math.sin(enemy.theta))

                                        enemy.V =(16,0)
                                        
                                        
                                    case 1: #鏡反
                                        start_animation(enemy.attack_state,enemy.boss_idle, 45, enemy.back, False) 
                                        enemy.I = (0,16)


                                    case 2: #光球
                                        start_animation(enemy.attack_state,enemy.boss_idle, 60, enemy.back, False) 
                                        
                                        
                                    case 3: #絕滅劍殺
                                        start_animation(enemy.attack_state,enemy.boss_idle, 60, enemy.back, False) 


                                                

                            elif enemy.attack_state["playing"]:         #動畫執行中，出招cd = -1
                                
                                
                                match enemy.phase:
                                    case 0:
                                        
                                        ATKs_EN.append(object_class.object(enemy.rect.x+enemy.rect.width //2 ,enemy.rect.y+enemy.rect.height //2,pygame.image.load("Image\Object\pre_light.png"),"dangerous",1,0,"pre_light",1,None,None)) 
                                        ATKs_EN.append(object_class.object(enemy.rect.x+enemy.rect.width //2 ,enemy.rect.y+enemy.rect.height //2,pygame.image.load("Image\Object\pre_light.png"),"dangerous",1,0,"pre_light",2,None,None)) 
                                        ATKs_EN.append(object_class.object(enemy.rect.x+enemy.rect.width //2 ,enemy.rect.y+enemy.rect.height //2,pygame.image.load("Image\Object\pre_light.png"),"dangerous",1,0,"pre_light",3,None,None)) 
                                        ATKs_EN.append(object_class.object(enemy.rect.x+enemy.rect.width //2 ,enemy.rect.y+enemy.rect.height //2,pygame.image.load("Image\Object\pre_light.png"),"dangerous",1,0,"pre_light",4,None,None))
                                        ATKs_EN.append(object_class.object(-1500,650,pygame.image.load("Image\Object\pre_light.png"),"dangerous",1,0,"pre_light",5,None,None))
                                        
                                        for obj in NT_object:
                                            if obj.type == "mirror_wall":
                                                
                                                
                                                obj.center_x = obj.x + obj.rect.width /2
                                                obj.center_y = obj.y + obj.rect.height /2
                                                
                                                if obj.dif == 2 :
                                                    
                                                    obj.angle -= 1
                                                    obj.surface = pygame.transform.rotate(pygame.image.load("Image\Object\\triangle_gray.png"),obj.angle+180)
                                                    obj.rect = obj.surface.get_rect(center=(obj.org_x+obj.org_rect_w//2, obj.org_y+obj.org_rect_h//2))
                                                    print("angle=",obj.angle)
                                                
                                                if obj.dif == 1:
                                                    
                                                    obj.angle += 1
                                                    obj.surface = pygame.transform.rotate(pygame.image.load("Image\Object\\triangle_gray.png"),obj.angle+180)
                                                    obj.rect = obj.surface.get_rect(center=(obj.org_x+obj.org_rect_w//2, obj.org_y+obj.org_rect_h//2))
                                                    
                                                if obj.dif == 3:
                                                    
                                                    obj.angle -= 1
                                                    obj.surface = pygame.transform.rotate(pygame.image.load("Image\Object\\triangle_gray.png"),obj.angle+180)
                                                    obj.rect = obj.surface.get_rect(center=(obj.org_x+obj.org_rect_w//2, obj.org_y+obj.org_rect_h//2))
                                                
                                            
                                                obj.outerect = obj.rect.inflate(160,160)
                                                    
                                                obj.x = obj.rect.x
                                                obj.y = obj.rect.y
                                                    
                                                obj.S_Px = obj.center_x + math.sqrt(pow(obj.org_rect_w/2,2)+ pow(obj.org_rect_h/2,2)) * math.cos(math.radians(344 - obj.angle))
                                                obj.S_Py = obj.center_y + math.sqrt(pow(obj.org_rect_w/2,2)+ pow(obj.org_rect_h/2,2)) * math.sin(math.radians(344 - obj.angle))

                                                    
                                                    
                                                obj.F_Px = obj.S_Px - math.cos(math.radians(-obj.angle)) * obj.org_rect_w
                                                obj.F_Py = obj.S_Py - math.sin(math.radians(-obj.angle)) * obj.org_rect_w
                                                    
                                                obj.T_Px = obj.S_Px - math.cos(math.radians(-obj.angle-30)) * obj.org_rect_h *2
                                                obj.T_Py = obj.S_Py - math.sin(math.radians(-obj.angle-30)) * obj.org_rect_h *2 

                                                    
                                                if obj.angle >= 360:
                                                    obj.angle -= 360
                                                elif obj.angle < 0 :
                                                    obj.angle += 360
                                                    
                                                if obj.angle != 0:
                                                    obj.can_be_through = 1
                                            
                                            enemy.phase_cd = -1
                                                
                                    case 1:
                                        ATKs_EN.append(object_class.object(enemy.rect.x+enemy.rect.width //2 ,enemy.rect.y+enemy.rect.height //2,pygame.image.load("Image\Object\pre_light.png"),"dangerous",1,0,"pre_light",1,None,None,300)) 

                                        enemy.phase_cd = -1


                                    case 2:
                                        if enemy.summon_cd > 0:
                                            enemy.summon_cd -=1
                                        
                                        if enemy.summon % 2 != 0 and enemy.summon_cd == 0:
                                            ATKs_EN.append(object_class.object(enemy.rect.x+enemy.rect.width //2 - 570 ,enemy.rect.y+enemy.rect.height //2 + 200,pygame.image.load("Image\Character\Enemy\Boss\light_ball.png"),"dangerous",1,0,"light_ball",None,None,None))
                                            enemy.summon_cd = 15
                                            enemy.summon *= 2
                                        elif enemy.summon %3 != 0 and enemy.summon_cd == 0:
                                            ATKs_EN.append(object_class.object(enemy.rect.x+enemy.rect.width //2 - 370 ,enemy.rect.y+enemy.rect.height //2 ,pygame.image.load("Image\Character\Enemy\Boss\light_ball.png"),"dangerous",1,0,"light_ball",None,None,None))
                                            enemy.summon_cd = 15
                                            enemy.summon *= 3
                                        elif enemy.summon %5 != 0 and enemy.summon_cd == 0:
                                            ATKs_EN.append(object_class.object(enemy.rect.x+enemy.rect.width //2  ,enemy.rect.y+enemy.rect.height //2 - 100 ,pygame.image.load("Image\Character\Enemy\Boss\light_ball.png"),"dangerous",1,0,"light_ball",None,None,None))
                                            enemy.summon_cd = 15
                                            enemy.summon *= 5
                                        elif enemy.summon %7 != 0 and enemy.summon_cd == 0:
                                            ATKs_EN.append(object_class.object(enemy.rect.x+enemy.rect.width //2 + 330 ,enemy.rect.y+enemy.rect.height //2 ,pygame.image.load("Image\Character\Enemy\Boss\light_ball.png"),"dangerous",1,0,"light_ball",None,None,None))
                                            enemy.summon_cd = 15
                                            enemy.summon *= 7
                                        elif enemy.summon %11 != 0 and enemy.summon_cd == 0:
                                            ATKs_EN.append(object_class.object(enemy.rect.x+enemy.rect.width //2 + 530 ,enemy.rect.y+enemy.rect.height //2 + 200,pygame.image.load("Image\Character\Enemy\Boss\light_ball.png"),"dangerous",1,0,"light_ball",None,None,None))
                                            enemy.summon_cd = 15
                                            enemy.summon *= 11
                                            
                                        enemy.phase_cd = -1
                                        
                                    case 3:
                                        if enemy.summon_cd > 0:
                                            enemy.summon_cd -=1
                                        
                                        if enemy.summon % 2 != 0 and enemy.summon_cd == 0:
                                            ATKs_EN.append(object_class.object(enemy.rect.x+enemy.rect.width //2 - 370 ,enemy.rect.y+enemy.rect.height //2 + 200,pygame.image.load("Image\Character\Enemy\Boss\light_sword.png"),"dangerous",1,0,"light_sword",1,None,None,600))
                                            enemy.summon_cd = 20
                                            enemy.summon *= 2
                                        elif enemy.summon %3 != 0 and enemy.summon_cd == 0:
                                            ATKs_EN.append(object_class.object(enemy.rect.x+enemy.rect.width //2 - 170 ,enemy.rect.y+enemy.rect.height //2 + 150 ,pygame.image.load("Image\Character\Enemy\Boss\light_sword.png"),"dangerous",1,0,"light_sword",2,None,None,600))
                                            enemy.summon_cd = 20
                                            enemy.summon *= 3
                                        elif enemy.summon %5 != 0 and enemy.summon_cd == 0:
                                            ATKs_EN.append(object_class.object(enemy.rect.x+enemy.rect.width //2 - 270 ,enemy.rect.y+enemy.rect.height //2 + 100 ,pygame.image.load("Image\Character\Enemy\Boss\light_sword.png"),"dangerous",1,0,"light_sword",3,None,None,600))
                                            enemy.summon_cd = 20
                                            enemy.summon *= 5
                                        elif enemy.summon %7 != 0 and enemy.summon_cd == 0:
                                            ATKs_EN.append(object_class.object(enemy.rect.x+enemy.rect.width //2 + 270 ,enemy.rect.y+enemy.rect.height //2 + 100 ,pygame.image.load("Image\Character\Enemy\Boss\light_sword.png"),"dangerous",1,0,"light_sword",4,None,None,600))
                                            enemy.summon_cd = 20
                                            enemy.summon *= 7
                                        elif enemy.summon %11 != 0 and enemy.summon_cd == 0:
                                            ATKs_EN.append(object_class.object(enemy.rect.x+enemy.rect.width //2 + 170 ,enemy.rect.y+enemy.rect.height //2 + 150,pygame.image.load("Image\Character\Enemy\Boss\light_sword.png"),"dangerous",1,0,"light_sword",5,None,None,600))
                                            enemy.summon_cd = 20
                                            enemy.summon *= 11
                                        elif enemy.summon %13 != 0 and enemy.summon_cd == 0:
                                            ATKs_EN.append(object_class.object(enemy.rect.x+enemy.rect.width //2 + 370 ,enemy.rect.y+enemy.rect.height //2 + 200,pygame.image.load("Image\Character\Enemy\Boss\light_sword.png"),"dangerous",1,0,"light_sword",6,None,None,600))
                                            enemy.summon_cd = 20
                                            enemy.summon *= 13
                                            
                                            
                                        for obj in NT_object:
                                            if obj.type == "mirror_wall":
                                                if obj.dif == 1 or obj.dif == 2:
                                                    obj.y += 4
                                                    obj.rect.y += 4
                                                    
                                                    obj.outerect = obj.rect.inflate(160,160)
                                                    

                                                    obj.center_x = obj.x + obj.rect.width /2
                                                    obj.center_y = obj.y + obj.rect.height /2
                                                        
                                                    obj.S_Px = obj.center_x + math.sqrt(pow(obj.org_rect_w/2,2)+ pow(obj.org_rect_h/2,2)) * math.cos(math.radians(344 - obj.angle))
                                                    obj.S_Py = obj.center_y + math.sqrt(pow(obj.org_rect_w/2,2)+ pow(obj.org_rect_h/2,2)) * math.sin(math.radians(344 - obj.angle))

                                                        
                                                        
                                                    obj.F_Px = obj.S_Px - math.cos(math.radians(-obj.angle)) * obj.org_rect_w
                                                    obj.F_Py = obj.S_Py - math.sin(math.radians(-obj.angle)) * obj.org_rect_w
                                                        
                                                    obj.T_Px = obj.S_Px - math.cos(math.radians(-obj.angle-30)) * obj.org_rect_h *2
                                                    obj.T_Py = obj.S_Py - math.sin(math.radians(-obj.angle-30)) * obj.org_rect_h *2 
                                                    
                                                    
                                                                                                
                                        enemy.phase_cd = -1
                                        


                            elif enemy.anime:                           #動畫播放完畢，出招cd = -2
                                enemy.phase_cd = -2
                                
                                match enemy.phase:
                                    case 0:
                                        for obj in NT_object:
                                            if obj.type == "mirror_wall":
                                                
                                                obj.center_x = obj.x + obj.rect.width /2
                                                obj.center_y = obj.y + obj.rect.height /2
                                                
                                                if obj.dif == 2 :
                                                    
                                                    obj.angle -= 1
                                                    obj.surface = pygame.transform.rotate(pygame.image.load("Image\Object\\triangle_gray.png"),obj.angle+180)
                                                    obj.rect = obj.surface.get_rect(center=(obj.org_x+obj.org_rect_w//2, obj.org_y+obj.org_rect_h//2))
                                                    print("angle=",obj.angle)

                                                if obj.dif == 1:
                                                    
                                                    obj.angle += 1
                                                    obj.surface = pygame.transform.rotate(pygame.image.load("Image\Object\\triangle_gray.png"),obj.angle+180)
                                                    obj.rect = obj.surface.get_rect(center=(obj.org_x+obj.org_rect_w//2, obj.org_y+obj.org_rect_h//2))
                                                    
                                                if obj.dif == 3:
                                                    
                                                    obj.angle -= 1
                                                    obj.surface = pygame.transform.rotate(pygame.image.load("Image\Object\\triangle_gray.png"),obj.angle+180)
                                                    obj.rect = obj.surface.get_rect(center=(obj.org_x+obj.org_rect_w//2, obj.org_y+obj.org_rect_h//2))
                                                

                                                
                                                obj.x = obj.rect.x
                                                obj.y = obj.rect.y
                                                    
                                                obj.S_Px = obj.center_x + math.sqrt(pow(obj.org_rect_w/2,2)+ pow(obj.org_rect_h/2,2)) * math.cos(math.radians(344 - obj.angle))
                                                obj.S_Py = obj.center_y + math.sqrt(pow(obj.org_rect_w/2,2)+ pow(obj.org_rect_h/2,2)) * math.sin(math.radians(344 - obj.angle))

                                                    
                                                    
                                                obj.F_Px = obj.S_Px - math.cos(math.radians(-obj.angle)) * obj.org_rect_w
                                                obj.F_Py = obj.S_Py - math.sin(math.radians(-obj.angle)) * obj.org_rect_w
                                                    
                                                obj.T_Px = obj.S_Px - math.cos(math.radians(-obj.angle-30)) * obj.org_rect_h *2
                                                obj.T_Py = obj.S_Py - math.sin(math.radians(-obj.angle-30)) * obj.org_rect_h *2 
                                                    

                                                    
                                                if obj.angle == 0 or obj.angle == 360:
                                                    obj.can_be_through = 2
                                                    print(obj.dif,obj.can_be_through)
                                    case 1:
                                        enemy.phase_cd = -2
                                    case 2:
                                        enemy.phase_cd = -2
                                    case 3:
                                        enemy.phase_cd = -2


                            elif enemy.phase_cd == -2:                  #前搖完二次初始化

                                match enemy.phase:

                                    case 0:     #輻(射)光(線)
                                        enemy.skill_time = 60

                                                

                                    case 1:     #鏡反
                                        enemy.skill_time = 720
                                        
                                    case 2:     #光球
                                        enemy.skill_time = 450
                                    
                                    case 3:
                                        enemy.skill_time = 510


                                enemy.phase_cd = -3                     #招式發動階段



                            elif enemy.phase_cd == -3 and enemy.skill_time > 0: #技能時長內觸發

                                for obj in NT_object:                           #讀碰撞(該狀態內不讀Move)
                                    Touch(enemy, obj)
                                    
                                enemy.skill_time -= 1                           #扣時

                                match enemy.phase:
                                    
                                    case 0:                                                 #輻(射)光(線)
                                            
                                        
                                        ATKs_EN.append(object_class.object(enemy.rect.x+enemy.rect.width //2 ,enemy.rect.y+enemy.rect.height //2,pygame.image.load("Image\Object\skill.png"),"dangerous",1,0,"light",1,None,None)) 
                                        ATKs_EN.append(object_class.object(enemy.rect.x+enemy.rect.width //2 ,enemy.rect.y+enemy.rect.height //2,pygame.image.load("Image\Object\skill.png"),"dangerous",1,0,"light",2,None,None)) 
                                        ATKs_EN.append(object_class.object(enemy.rect.x+enemy.rect.width //2 ,enemy.rect.y+enemy.rect.height //2,pygame.image.load("Image\Object\skill.png"),"dangerous",1,0,"light",3,None,None)) 
                                        ATKs_EN.append(object_class.object(enemy.rect.x+enemy.rect.width //2 ,enemy.rect.y+enemy.rect.height //2,pygame.image.load("Image\Object\skill.png"),"dangerous",1,0,"light",4,None,None))
                                        ATKs_EN.append(object_class.object(-1500,650,pygame.image.load("Image\Object\skill.png"),"dangerous",1,0,"light",5,None,None))
                                    
                                    
                                    
                                    
                                    case 1:                                                 #鏡反
                                        
                                        O = [-(600*math.sin(math.pi/180 * (720-enemy.skill_time))),560]
                                        
                                        P = [600*math.sin(math.pi/180 * (720-enemy.skill_time)),560]




                                        V1 = [P[0] - (enemy.x + enemy.rect.width/2) , P[1] - (enemy.y + enemy.rect.height/2)]
                                        V2 = [O[0] - (enemy.x + enemy.rect.width/2) , O[1] - (enemy.y + enemy.rect.height/2)]
                                        
                                        enemy.I = ( 16 * V1[0] / math.sqrt(pow( V1[0] , 2 ) + pow( V1[1] , 2 )) , 16 * V1[1] / math.sqrt(pow( V1[0] , 2 ) + pow( V1[1] , 2 )) )

                                        enemy.II = ( 16 * V2[0] / math.sqrt(pow( V2[0] , 2 ) + pow( V2[1] , 2 )) , 16 * V2[1] / math.sqrt(pow( V2[0] , 2 ) + pow( V2[1] , 2 )) )

                                        if math.sin(math.pi/180 * (720-enemy.skill_time)) <= 0.5 and enemy.summon % 2 != 0 and math.sin(math.pi/180 * (720-enemy.skill_time)) > 0.1 :
                                            print("summon L")
                                            ATKs_EN.append(object_class.object(-1050 ,300,pygame.image.load("Image\Character\Enemy\Boss\light_sword.png"),"dangerous",1,0,"light_sword",1,None,None,300))
                                            ATKs_EN.append(object_class.object(-950 ,0,pygame.image.load("Image\Character\Enemy\Boss\light_sword.png"),"dangerous",1,0,"light_sword",1,None,None,300))
                                            ATKs_EN.append(object_class.object(-850 ,-200,pygame.image.load("Image\Character\Enemy\Boss\light_sword.png"),"dangerous",1,0,"light_sword",1,None,None,300))
                                            enemy.summon *= 2

                                        if math.sin(math.pi/180 * (720-enemy.skill_time)) >= -0.5 and enemy.summon % 3 !=0 and math.sin(math.pi/180 * (720-enemy.skill_time)) < -0.1:
                                            print("summon R")
                                            ATKs_EN.append(object_class.object(700 ,300,pygame.image.load("Image\Character\Enemy\Boss\light_sword.png"),"dangerous",1,0,"light_sword",1,None,None,300))
                                            ATKs_EN.append(object_class.object(600 ,0,pygame.image.load("Image\Character\Enemy\Boss\light_sword.png"),"dangerous",1,0,"light_sword",1,None,None,300))
                                            ATKs_EN.append(object_class.object(500 ,-200,pygame.image.load("Image\Character\Enemy\Boss\light_sword.png"),"dangerous",1,0,"light_sword",1,None,None,300)) 
                                            enemy.summon *= 3

                                        elif math.sin(math.pi/180 * (720-enemy.skill_time)) <= 0.1 and math.sin(math.pi/180 * (720-enemy.skill_time)) >= -0.1:
                                            for atk in ATKs_EN:
                                                if atk.dif == "light_sword":
                                                    atk.chase =1
                                                    enemy.summon = 1

                                        ATKs_EN.append(object_class.object(enemy.rect.x+enemy.rect.width //2 ,enemy.rect.y+enemy.rect.height //2,pygame.image.load("Image\Object\skill.png"),"dangerous",1,0,"light",1,None,None,300)) 
                                        ATKs_EN.append(object_class.object(enemy.rect.x+enemy.rect.width //2 ,enemy.rect.y+enemy.rect.height //2,pygame.image.load("Image\Object\skill.png"),"dangerous",1,0,"light",2,None,None,300)) 

                                        
                                        for obj in NT_object:
                                            if obj.type == "mirror_wall":

                                                obj.center_x = obj.x + obj.rect.width /2
                                                obj.center_y = obj.y + obj.rect.height /2



                                                obj.S_Px = obj.center_x + math.sqrt(pow(obj.org_rect_w/2,2)+ pow(obj.org_rect_h/2,2)) * math.cos(math.radians(344 - obj.angle))
                                                obj.S_Py = obj.center_y + math.sqrt(pow(obj.org_rect_w/2,2)+ pow(obj.org_rect_h/2,2)) * math.sin(math.radians(344 - obj.angle))

                                                    
                                                    
                                                obj.F_Px = obj.S_Px - math.cos(math.radians(-obj.angle)) * obj.org_rect_w
                                                obj.F_Py = obj.S_Py - math.sin(math.radians(-obj.angle)) * obj.org_rect_w
                                                    
                                                obj.T_Px = obj.S_Px - math.cos(math.radians(-obj.angle-30)) * obj.org_rect_h *2
                                                obj.T_Py = obj.S_Py - math.sin(math.radians(-obj.angle-30)) * obj.org_rect_h *2 

                                                if obj.dif == 1:
                                                    temx = 0 - (obj.x + obj.rect.width/2)
                                                    temy = 560 - (obj.y + obj.rect.height/2)
                                                    
                                                    
                                                    obj.tag_x = temy/115
                                                    obj.tag_y = -temx/115
                                                    
                                                    
                                                    if Main.rect.colliderect(obj.rect):
                                                        Main.rect.x += obj.tag_x
                                                        Main.rect.y += obj.tag_y
                                                        
                                                        Main.x = Main.rect.x-50
                                                        Main.y = Main.rect.y-50
                                                        
                                                    obj.rect.x += obj.tag_x
                                                    obj.rect.y += obj.tag_y

                                                    obj.outerect.x += obj.tag_x
                                                    obj.outerect.y += obj.tag_y
                                                        
                                                    obj.x = obj.rect.x
                                                    obj.y = obj.rect.y

                                                    
                                                elif obj.dif == 2:
                                                    temx = 0 - (obj.x + obj.rect.width/2)
                                                    temy = 560 - (obj.y + obj.rect.height/2)
                                                    
                                                    
                                                    obj.tag_x = temy/115
                                                    obj.tag_y = -temx/115
                                
                                                    if Main.rect.colliderect(obj.rect):
                                                        Main.rect.x += obj.tag_x
                                                        Main.rect.y += obj.tag_y
                                                        
                                                        Main.x = Main.rect.x-50
                                                        Main.y = Main.rect.y-50    
                                                    
                                                    obj.rect.x += obj.tag_x
                                                    obj.rect.y += obj.tag_y

                                                    obj.outerect.x += obj.tag_x
                                                    obj.outerect.y += obj.tag_y                                            
                                                    
                                                    obj.x = obj.rect.x
                                                    obj.y = obj.rect.y

                                    
                                    case 2:
                                        enemy.V = (16,0)
                                        print(enemy.skill_time)
                                        if (enemy.skill_time % 90)  ==0:
                                            ATKs_EN.append(object_class.object(-1500,450,pygame.image.load("Image\Character\Enemy\Boss\light_sword.png"),"dangerous",1,0,"light_sword",None,None,None))
                                            ATKs_EN.append(object_class.object(1000,450,pygame.image.load("Image\Character\Enemy\Boss\light_sword.png"),"dangerous",1,0,"light_sword",None,None,None))
                                            
                                            ATKs_EN.append(object_class.object(-1700,350,pygame.image.load("Image\Character\Enemy\Boss\light_sword.png"),"dangerous",1,0,"light_sword",None,None,None))
                                            ATKs_EN.append(object_class.object(1200,350,pygame.image.load("Image\Character\Enemy\Boss\light_sword.png"),"dangerous",1,0,"light_sword",None,None,None))
                                            
                                            ATKs_EN.append(object_class.object(-1900,250,pygame.image.load("Image\Character\Enemy\Boss\light_sword.png"),"dangerous",1,0,"light_sword",None,None,None))
                                            ATKs_EN.append(object_class.object(1400,250,pygame.image.load("Image\Character\Enemy\Boss\light_sword.png"),"dangerous",1,0,"light_sword",None,None,None))

                                        
                                        for atk in ATKs_EN:
                                            if atk.dif == "light_sword":
                                                atk.chase =1
                                                enemy.summon = 1
                        
                                        if enemy.skill_time % 90 == 0:
                                            for atk in ATKs_EN:
                                                if atk.dif == "light_ball":
                                                    if atk.chase == 0:
                                                        atk.chase = 1
                                                        break

                                    case 3:
                                        if enemy.skill_time == 480:
                                            for atk in ATKs_EN:
                                                if atk.dif == "light_sword":
                                                    if atk.num <= 3:
                                                        atk.chase = 1

                                                        tem_x = (Main.rect.x+Main.rect.width/2 - atk.rect.x- atk.rect.width/2 + 700)
                                                        tem_y = (Main.rect.y+Main.rect.height/2 - atk.rect.y- atk.rect.height/2 +400)             

                                                        atk.tag_x = tem_x / math.sqrt(pow(tem_x,2)+ pow(tem_y,2)) * 50
                                                        atk.tag_y = tem_y / math.sqrt(pow(tem_x,2)+ pow(tem_y,2)) * 50

                                                        atk.surface = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("Image\Character\Enemy\Boss\light_sword.png"),(50,150)),math.degrees(math.atan2(-atk.tag_y,atk.tag_x))+90)

                                        if enemy.skill_time == 450:
                                            for atk in ATKs_EN:
                                                if atk.dif == "light_sword":
                                                    if atk.num > 3:
                                                        atk.chase = 1

                                                        tem_x = (Main.rect.x+Main.rect.width/2 - atk.rect.x- atk.rect.width/2 - 700)
                                                        tem_y = (Main.rect.y+Main.rect.height/2 - atk.rect.y- atk.rect.height/2 +400)           

                                                        atk.tag_x = tem_x / math.sqrt(pow(tem_x,2)+ pow(tem_y,2)) * 50
                                                        atk.tag_y = tem_y / math.sqrt(pow(tem_x,2)+ pow(tem_y,2)) * 50

                                                        atk.surface = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("Image\Character\Enemy\Boss\light_sword.png"),(50,150)),math.degrees(math.atan2(-atk.tag_y,atk.tag_x))+90)
                                                        
                                        
                                            
                                                        
                                                        
                                        if enemy.skill_time < 420 and enemy.skill_time > 350:
                                            enemy.I = (16,0)
                                            enemy.II = (16,0)
                                            ATKs_EN.append(object_class.object(-1000,660,pygame.image.load("Image\Object\pre_light.png"),"dangerous",1,0,"pre_light",1,None,None)) 
                                            ATKs_EN.append(object_class.object(-1000,160,pygame.image.load("Image\Object\pre_light.png"),"dangerous",1,0,"pre_light",2,None,None)) 
                                        
                                        elif enemy.skill_time < 350 and enemy.skill_time >300:
                                            ATKs_EN.append(object_class.object(-1000,410-250*math.cos(math.pi/50 * (enemy.skill_time-350)),pygame.image.load("Image\Object\skill.png"),"dangerous",1,0,"light",1,None,None))
                                            ATKs_EN.append(object_class.object(-1000,410+250*math.cos(math.pi/50 * (enemy.skill_time-350)),pygame.image.load("Image\Object\skill.png"),"dangerous",1,0,"light",2,None,None))

                                            enemy.III = (0,16)
                                            enemy.IV = (0,16)
                                            ATKs_EN.append(object_class.object(-550,-560,pygame.image.load("Image\Object\pre_light.png"),"dangerous",1,0,"pre_light",3,None,None)) 
                                            ATKs_EN.append(object_class.object(550,-560,pygame.image.load("Image\Object\pre_light.png"),"dangerous",1,0,"pre_light",4,None,None)) 
                                            
                                            
                                        elif enemy.skill_time <300 and enemy.skill_time > 250:
                                            ATKs_EN.append(object_class.object(-1000,660,pygame.image.load("Image\Object\skill.png"),"dangerous",1,0,"light",1,None,None)) 
                                            ATKs_EN.append(object_class.object(-1000,160,pygame.image.load("Image\Object\skill.png"),"dangerous",1,0,"light",2,None,None)) 
                                            
                                            ATKs_EN.append(object_class.object(-550*math.cos(math.pi/50 * (enemy.skill_time-250)),-560,pygame.image.load("Image\Object\skill.png"),"dangerous",1,0,"light",3,None,None)) 
                                            ATKs_EN.append(object_class.object(550*math.cos(math.pi/50 * (enemy.skill_time-250)),-560,pygame.image.load("Image\Object\skill.png"),"dangerous",1,0,"light",4,None,None)) 
                                            
                                        elif enemy.skill_time < 250 and enemy.skill_time >215:
                                            ATKs_EN.append(object_class.object(-1000,660,pygame.image.load("Image\Object\skill.png"),"dangerous",1,0,"light",1,None,None)) 
                                            ATKs_EN.append(object_class.object(-1000,160,pygame.image.load("Image\Object\skill.png"),"dangerous",1,0,"light",2,None,None)) 
                                            
                                            ATKs_EN.append(object_class.object(-550,-560,pygame.image.load("Image\Object\skill.png"),"dangerous",1,0,"light",3,None,None)) 
                                            ATKs_EN.append(object_class.object(550,-560,pygame.image.load("Image\Object\skill.png"),"dangerous",1,0,"light",4,None,None)) 
                                            for atk in ATKs_EN:
                                                if atk.dif == "light_sword":
                                                    atk.L_mirror = None
                                                    atk.chase = 1
                                                    atk.dur = 120
                                        
                                        elif enemy.skill_time >160 and enemy.skill_time<215:
                                            for atk in ATKs_EN:
                                                if atk.dif == "light_sword":
                                                    atk.chase = 0
                                                    
                                            enemy.I=(0,0)
                                            enemy.II=(0,0)
                                            enemy.III=(0,0)
                                            enemy.IV=(0,0)
                                            enemy.V=(0,0)
                                            enemy.VI=(0,0)
                                        
                                        
                                        
                                        elif enemy.skill_time < 160 and enemy.skill_time > 120:
                                            for atk in ATKs_EN:
                                                if atk.dif == "light_sword":
                                                    
                                                    
                                                    
                                                    
                                                    V = [-(atk.rect.x - Main.rect.x) , -(atk.rect.y - Main.rect.y)]
 
                                                    if atk.num == 1 and enemy.I == (0,0):
                                                        enemy.I = ( 16 * V[0] / math.sqrt(pow( V[0] , 2 ) + pow( V[1] , 2 )) , 16 * V[1] / math.sqrt(pow( V[0] , 2 ) + pow( V[1] , 2 )) )
                                                    elif atk.num ==2 and enemy.II == (0,0):
                                                        enemy.II = ( 16 * V[0] / math.sqrt(pow( V[0] , 2 ) + pow( V[1] , 2 )) , 16 * V[1] / math.sqrt(pow( V[0] , 2 ) + pow( V[1] , 2 )) )

                                                    elif atk.num ==3 and enemy.III == (0,0):
                                                        enemy.III = ( 16 * V[0] / math.sqrt(pow( V[0] , 2 ) + pow( V[1] , 2 )) , 16 * V[1] / math.sqrt(pow( V[0] , 2 ) + pow( V[1] , 2 )) )
                                                        
                                                    elif atk.num ==4 and enemy.IV == (0,0):
                                                        enemy.IV = ( 16 * V[0] / math.sqrt(pow( V[0] , 2 ) + pow( V[1] , 2 )) , 16 * V[1] / math.sqrt(pow( V[0] , 2 ) + pow( V[1] , 2 )) )
                                                        
                                                    elif atk.num ==5 and enemy.V == (0,0):
                                                        enemy.V = ( 16 * V[0] / math.sqrt(pow( V[0] , 2 ) + pow( V[1] , 2 )) , 16 * V[1] / math.sqrt(pow( V[0] , 2 ) + pow( V[1] , 2 )) )
                                                        
                                                    elif atk.num ==6 and enemy.VI == (0,0):
                                                        enemy.VI = ( 16 * V[0] / math.sqrt(pow( V[0] , 2 ) + pow( V[1] , 2 )) , 16 * V[1] / math.sqrt(pow( V[0] , 2 ) + pow( V[1] , 2 )) )
                                                    
                                                    
                                                    ATKs_EN.append(object_class.object(atk.rect.x,atk.rect.y,pygame.image.load("Image\Object\skill.png"),"dangerous",1,0,"light",atk.num,None,None))
                                        
                                        elif enemy.skill_time == 120:
                                                
                                            for atk_en in ATKs_EN:
                                                if atk_en.dif == "light_sword":
                                                    atk_en.chase = 1
                                                    atk_en.tag_x = None
                                                    atk_en.tag_y = None
                                                    
                                        elif enemy.skill_time < 120:
                                            for obj in NT_object:
                                                if obj.type == "mirror_wall":
                                                    if obj.dif == 1 or obj.dif == 2:
                                                        obj.y -= 4
                                                        obj.rect.y -= 4
                                                        
                                                        obj.outerect = obj.rect.inflate(160,160)
                                                        

                                                        obj.center_x = obj.x + obj.rect.width /2
                                                        obj.center_y = obj.y + obj.rect.height /2
                                                            
                                                        obj.S_Px = obj.center_x + math.sqrt(pow(obj.org_rect_w/2,2)+ pow(obj.org_rect_h/2,2)) * math.cos(math.radians(344 - obj.angle))
                                                        obj.S_Py = obj.center_y + math.sqrt(pow(obj.org_rect_w/2,2)+ pow(obj.org_rect_h/2,2)) * math.sin(math.radians(344 - obj.angle))

                                                            
                                                            
                                                        obj.F_Px = obj.S_Px - math.cos(math.radians(-obj.angle)) * obj.org_rect_w
                                                        obj.F_Py = obj.S_Py - math.sin(math.radians(-obj.angle)) * obj.org_rect_w
                                                            
                                                        obj.T_Px = obj.S_Px - math.cos(math.radians(-obj.angle-30)) * obj.org_rect_h *2
                                                        obj.T_Py = obj.S_Py - math.sin(math.radians(-obj.angle-30)) * obj.org_rect_h *2 

                                        for atk_en in ATKs_EN:
                                            if atk_en.dif == "light_sword":
                                                    
                                                if pow(atk_en.rect.x+atk_en.rect.width/2   -   Main.rect.x-Main.rect.width/2,2)+pow(atk_en.rect.y+atk_en.rect.height/2   -   Main.rect.y-Main.rect.height/2,2) >= pow(850,2) and atk_en.L_mirror != None and not enemy.skill_time <=120:
                                                    atk_en.tag_x = None
                                                    atk_en.tag_y = None
                                                    atk_en.chase = 0
                                                    
                                                if atk_en.chase == 0:
                                                    atk_en.surface = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("Image\Character\Enemy\Boss\light_sword.png"),(50,150)),enemy.skill_time*5)
                                                        
                                                        
                                                        
                                                        
                                                        
                                                            
                                                    
                                                    
                                                    
                            elif enemy.phase_cd == -3 and enemy.skill_time == 0:                        #放完技能
                                
                            
                                
                                if enemy.phase == 0 and enemy.light_count < 3:                                         
                                    enemy.light_count += 1
                                    enemy.phase_cd = random.randint(60,90)


                                elif enemy.second_HP > 0:
                                    enemy.light_count = 0
                                    enemy.summon = 1
                                    enemy.phase=random.randint(0,2)                                         #重骰招 & cd
                                    enemy.phase_cd = random.randint(60,90)
                                    
                                else:
                                    enemy.summon = 1
                                    enemy.light_count = 0
                                    enemy.phase=random.randint(0,3)                                         #重骰招 & cd
                                    enemy.phase_cd = random.randint(60,90)

                                if enemy.broke == 10 :                                                  #吃18刀癱瘓
#                                    start_animation(enemy.attack_state, enemy.boss_break, 5, enemy.back-1, False, (320,300))
                                    enemy.wait = 450
                                    enemy.NoGravity = 0
                                    enemy.broke = 0
                        
                        
                        if enemy.wait <= 62 and enemy.wait != 0:                                                            #起身動畫
                            enemy.NoGravity = 1
                            enemy.y -= 12
                            enemy.rect.y -= 12


            case "elite":
                pass


            case "roadside":
                pass









#====================================================================碰撞清單清除、傷害判定

        if enemy.wait == 0:                                         #怪停頓無碰撞傷害
            if Touch(Main,enemy) and enemy.TDamage == 1:
                if Main.unhurtable_cd <= 0 and Main.HP > 1:         #碰撞傷害

                    if Main.rect.x-enemy.rect.x > 0:                #玩家受擊
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
            

        for atk_al in ATKs_AL:                                      #我方攻擊
            
            for atk_en in ATKs_EN:                                  #砍子彈
                if atk_en.delete != 1:
                        
                    if atk_en.dif == "bullet":
                        if atk_al.rect.colliderect(atk_en.rect):
                            atk_en.delete = 1
                                            
                    if atk_en.dif == "light_sword":
                        if atk_al.rect.colliderect(atk_en.rect):
                            atk_en.delete = 1
                            atk_en.tag_x = None
                            atk_en.ATK = Main.ATK
                            ATKs_AL.append(atk_en)
                
            
            
            if atk_al.dif == "light_sword":


                if atk_al.chase ==1:
                    if atk_al.tag_x == None:                            #飛行方向初始化 & 轉向

                        for enemy in Enemy:
                            enemy.distant =math.sqrt(pow(enemy.rect.x+enemy.rect.width/2   -   Main.rect.x-Main.rect.width/2,2)+pow(enemy.rect.y+enemy.rect.height/2   -   Main.rect.y-Main.rect.height/2,2))
                            
                        
                        Enemy.sort(key=lambda e: e.distant)             
                            
                            
                            
                            
                            
                        tem_x = (Enemy[0].rect.x+Enemy[0].rect.width/2 - atk_al.rect.x- atk_al.rect.width/2)
                        tem_y = (Enemy[0].rect.y+Enemy[0].rect.height/2 - atk_al.rect.y- atk_al.rect.height/2)           

                        atk_al.tag_x = tem_x / math.sqrt(pow(tem_x,2)+ pow(tem_y,2)) * 50
                        atk_al.tag_y = tem_y / math.sqrt(pow(tem_x,2)+ pow(tem_y,2)) * 50

                        atk_al.surface = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("Image\Character\Enemy\Boss\light_sword.png"),(50,150)),math.degrees(math.atan2(-atk_al.tag_y,atk_al.tag_x))+90)
                    
                    atk_al.surface = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("Image\Character\Enemy\Boss\light_sword.png"),(50,150)),math.degrees(math.atan2(-atk_al.tag_y,atk_al.tag_x))+90)

                    atk_al.rect.x += atk_al.tag_x                       #飛
                    atk_al.rect.y += atk_al.tag_y
                    atk_al.x = atk_al.rect.x
                    atk_al.y = atk_al.rect.y

                    if atk_al.rect.colliderect(Main.rect):              #打到玩家
                                
                        if Main.unhurtable_cd <= 0:
                                            
                            if Main.unhurtable_cd <= 0 and Main.HP > 1:
                                if Main.rect.x-atk_al.rect.x > 0:
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
                            atk_al.delete = 1


                    for obj in NT_object:                               #撞牆掰掰
                        if atk_al.rect.colliderect(obj.rect):
                            if obj.type == "mirror_wall":
                                
                                tem_x = atk_al.tag_x
                                tem_y = atk_al.tag_y
                                
                                atkF=[obj.F_Px - (atk_al.rect.x+atk_al.rect.width/2), obj.F_Py - (atk_al.rect.y+atk_al.rect.height/2)]
                                atkS=[obj.S_Px - (atk_al.rect.x+atk_al.rect.width/2), obj.S_Py - (atk_al.rect.y+atk_al.rect.height/2)]
                                atkT=[obj.T_Px - (atk_al.rect.x+atk_al.rect.width/2), obj.T_Py - (atk_al.rect.y+atk_al.rect.height/2)]
                                
                                cFS = cross(atkF, atkS)
                                cST = cross(atkS, atkT)
                                cTF = cross(atkT, atkF)
                                
                                if cFS > 0:
                                    L_1 = True
                                else:
                                    L_1 = False
                                
                                if cST > 0:
                                    L_2 = True
                                else:
                                    L_2 = False
                                    
                                if cTF > 0:
                                    L_3 = True
                                else:
                                    L_3 = False
            
            
                                if (L_1 == L_2 == L_3):
                                    atk_al.x -= atk_al.tag_x
                                    atk_al.rect.x -= atk_al.tag_x
                                    atk_al.y -= atk_al.tag_y
                                    atk_al.rect.y -= atk_al.tag_y
                                    
                                    if atk_al.pre_test == 1:
                                        atk_al.tag_x = (math.cos(math.radians(obj.angle+90)*-2) * tem_x + math.sin(math.radians(obj.angle+90)*-2) * tem_y) *-1
                                        atk_al.tag_y = (math.sin(math.radians(obj.angle+90)*-2) * tem_x - math.cos(math.radians(obj.angle+90)*-2) * tem_y) * -1

                                    elif atk_al.pre_test == 2:
                                        atk_al.tag_x = (math.cos(math.radians(obj.angle+120)*-2) * tem_x + math.sin(math.radians(obj.angle+120)*-2) * tem_y) *-1
                                        atk_al.tag_y = (math.sin(math.radians(obj.angle+120)*-2) * tem_x - math.cos(math.radians(obj.angle+120)*-2) * tem_y) * -1
                                        
                                    elif atk_al.pre_test == 3:
                                        atk_al.tag_x = (math.cos(math.radians(obj.angle+60)*-2) * tem_x + math.sin(math.radians(obj.angle+60)*-2) * tem_y) *-1
                                        atk_al.tag_y = (math.sin(math.radians(obj.angle+60)*-2) * tem_x - math.cos(math.radians(obj.angle+60)*-2) * tem_y) * -1
                                    

                                    atk_al.L_mirror = obj  
                                    atk_al.pre_test = 0        
                                
                                if L_1 == L_2:
                                    atk_al.pre_test = 3
                                elif L_2 == L_3:
                                    atk_al.pre_test = 1
                                elif L_3 == L_1:
                                    atk_al.pre_test = 2
                            else:
                                atk_al.delete = 1
                
                        
                        
                        
            for obj in NT_object:
                if obj.type == "mirror_wall":
                    if obj.dif != 0:
                        if atk_al.rect.colliderect(obj.rect) and atk_al.dif !=  "light_sword":       
                                                 
                            obj.center_x = obj.x + obj.rect.width /2
                            obj.center_y = obj.y + obj.rect.height /2
                                                
                            if obj.dif == 2 :
                                                    
                                obj.angle -= 3
                                obj.surface = pygame.transform.rotate(pygame.image.load("Image\Object\\triangle_gray.png"),obj.angle+180)
                                obj.rect = obj.surface.get_rect(center=(obj.org_x+obj.org_rect_w//2, obj.org_y+obj.org_rect_h//2))
                                print("angle=",obj.angle)
                                                
                            if obj.dif == 1:
                                                    
                                obj.angle += 3
                                obj.surface = pygame.transform.rotate(pygame.image.load("Image\Object\\triangle_gray.png"),obj.angle+180)
                                obj.rect = obj.surface.get_rect(center=(obj.org_x+obj.org_rect_w//2, obj.org_y+obj.org_rect_h//2))
                                                    
                                                
                                            
                            obj.outerect = obj.rect.inflate(160,160)
                                                    
                            obj.x = obj.rect.x
                            obj.y = obj.rect.y
                                                    
                            obj.S_Px = obj.center_x + math.sqrt(pow(obj.org_rect_w/2,2)+ pow(obj.org_rect_h/2,2)) * math.cos(math.radians(344 - obj.angle))
                            obj.S_Py = obj.center_y + math.sqrt(pow(obj.org_rect_w/2,2)+ pow(obj.org_rect_h/2,2)) * math.sin(math.radians(344 - obj.angle))

                                                    
                                                    
                            obj.F_Px = obj.S_Px - math.cos(math.radians(-obj.angle)) * obj.org_rect_w
                            obj.F_Py = obj.S_Py - math.sin(math.radians(-obj.angle)) * obj.org_rect_w
                                                    
                            obj.T_Px = obj.S_Px - math.cos(math.radians(-obj.angle-30)) * obj.org_rect_h *2
                            obj.T_Py = obj.S_Py - math.sin(math.radians(-obj.angle-30)) * obj.org_rect_h *2 

                                                    
                            if obj.angle >= 360:
                                obj.angle -= 360
                            elif obj.angle < 0 :
                                obj.angle += 360
                                                    
                            if obj.angle != 0 and not obj.angle == 360:
                                obj.can_be_through = 1
                                
                            if obj.angle == 0 or obj.angle == 360:
                                obj.can_be_through = 2
                                print(obj.dif,obj.can_be_through)
                    
                    
                    
                    
                    
                    
            if enemy.unhurtable_cd <= 0 :                           #怪受擊
                            
                if Touch(enemy,atk_al):
                    if not enemy.type == "boss":
                        
                        if atk_al.rect.x + atk_al.rect.width //2 - enemy.rect.x - enemy.rect.width//2 < 0 :
                            enemy.vx = atk_al.KB
                            
                        elif atk_al.rect.x + atk_al.rect.width //2 - enemy.rect.x - enemy.rect.width//2 > 0:
                            enemy.vx = atk_al.KB * -1
                    
                    enemy.HP -= atk_al.ATK
                    enemy.unhurtable_cd = 20


                    match enemy.type :

                        case "boss":

                            match enemy.dif:

                                case "The_Tank":                #坦克背刀轉身、直接發現玩家 、 癱瘓計數
                                    if not enemy.wait:
                                        if Main.rect.x - enemy.rect.x - enemy.rect.width//2 > 0:
                                            enemy.back = 1

                                        else:
                                            enemy.back = -1

                                    if enemy.found==0:    
                                        enemy.found = True
                                        enemy.wait=32

                                    if enemy.wait == 0 and enemy.broke < 18:
                                        enemy.broke+=1

                                case "The_Sun":
                                    
                                    if enemy.wait == 0 and enemy.broke < 10:
                                        enemy.broke+=1

                        case "elite":
                            pass

                        case "roadside" :
                            pass

       
        player_class.enemy.Move(enemy,NT_object,Main)           #怪移動(老規矩，碰撞放最後才不會卡進牆)


        if enemy.HP <= 0 :                                       #怪清除
            if enemy.type == "boss":
                if enemy.second_HP <= 0:
                    Enemy.remove(enemy)
                    del enemy
                    
                else:
                    enemy.unhurtable_cd = 300
                    print("二階段")
                    enemy.HP = enemy.second_HP
                    enemy.second_HP = 0
                    if enemy.dif == "The_Sun":
                        enemy.phase_cd = 30
                        enemy.phase = 3
                        for atk in ATKs_EN:
                            if atk.dif == "light_sword":
                                atk.delete = 1
                            if atk.dif == "light_ball":
                                atk.delete = 1                    
                    
                    
            else:
                Enemy.remove(enemy)
                del enemy

    Main.now_NT_Touch = []                                      #清除角色目前碰撞清單
    Main.now_CT_Touch = []
    Main.now_Touch = []



    for atk_en in ATKs_EN:                                      #敵方攻擊
        if atk_en.delete !=1:
            if atk_en.dif == "bullet":                              #子彈類邏輯
                    
                atk_en.dur -= 1                                     #扣時(存在時間)
                    
                if atk_en.dur == 0:                                 #超時刪除
                    atk_en.delete = 1
                    
                if atk_en.tag_x == None:                            #飛行方向初始化 & 轉向(Not yet)
                    atk_en.tag_x = (Main.rect.x - atk_en.rect.x)//30 
                    atk_en.tag_y = (Main.rect.y - atk_en.rect.y)//30
                    atk_en.surface = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("Image\Character\Enemy\Boss\Bullet.png"),(20,30)),math.degrees(math.atan2(-atk_en.tag_y,atk_en.tag_x))-30)
                
                    
                atk_en.rect.x += atk_en.tag_x                       #飛
                atk_en.rect.y += atk_en.tag_y
                atk_en.x = atk_en.rect.x
                atk_en.y = atk_en.rect.y
                    
                for obj in NT_object:                               #撞牆掰掰
                    if atk_en.rect.colliderect(obj.rect):
                        atk_en.delete = 1

                            
                if atk_en.rect.colliderect(Main.rect):              #打到玩家
                            
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
            


            elif atk_en.dif == "sun_blaze":                            
                atk_en.dur -= 1                                     #扣時(存在時間)
                    
                if atk_en.dur == 0:                                 #超時刪除
                    atk_en.delete = 1

                            
                if atk_en.rect.colliderect(Main.rect):              #打到玩家
                            
                    if Main.unhurtable_cd <= 0:
                                        
                        if Main.HP > 1:
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



            elif atk_en.dif == "light_sword":



                if atk_en.chase ==1:
                    if atk_en.tag_x == None:                            #飛行方向初始化 & 轉向
                        tem_x = (Main.rect.x+Main.rect.width/2 - atk_en.rect.x- atk_en.rect.width/2)
                        tem_y = (Main.rect.y+Main.rect.height/2 - atk_en.rect.y- atk_en.rect.height/2)           

                        atk_en.tag_x = tem_x / math.sqrt(pow(tem_x,2)+ pow(tem_y,2)) * 50
                        atk_en.tag_y = tem_y / math.sqrt(pow(tem_x,2)+ pow(tem_y,2)) * 50

                        atk_en.surface = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("Image\Character\Enemy\Boss\light_sword.png"),(50,150)),math.degrees(math.atan2(-atk_en.tag_y,atk_en.tag_x))+90)
                    
                    atk_en.surface = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("Image\Character\Enemy\Boss\light_sword.png"),(50,150)),math.degrees(math.atan2(-atk_en.tag_y,atk_en.tag_x))+90)

                    atk_en.rect.x += atk_en.tag_x                       #飛
                    atk_en.rect.y += atk_en.tag_y
                    atk_en.x = atk_en.rect.x
                    atk_en.y = atk_en.rect.y
                    

                    atk_en.dur -= 1                                     #扣時(存在時間)
                        
                    if atk_en.dur == 0:                                 #超時刪除
                        atk_en.delete = 1


                    if atk_en.rect.colliderect(Main.rect):              #打到玩家
                                
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


                    for obj in NT_object:                               #撞牆掰掰
                        if atk_en.rect.colliderect(obj.rect):
                            if obj.type == "mirror_wall":
                                
                                tem_x = atk_en.tag_x
                                tem_y = atk_en.tag_y
                                
                                atkF=[obj.F_Px - (atk_en.rect.x+atk_en.rect.width/2), obj.F_Py - (atk_en.rect.y+atk_en.rect.height/2)]
                                atkS=[obj.S_Px - (atk_en.rect.x+atk_en.rect.width/2), obj.S_Py - (atk_en.rect.y+atk_en.rect.height/2)]
                                atkT=[obj.T_Px - (atk_en.rect.x+atk_en.rect.width/2), obj.T_Py - (atk_en.rect.y+atk_en.rect.height/2)]
                                
                                cFS = cross(atkF, atkS)
                                cST = cross(atkS, atkT)
                                cTF = cross(atkT, atkF)
                                
                                if cFS > 0:
                                    L_1 = True
                                else:
                                    L_1 = False
                                
                                if cST > 0:
                                    L_2 = True
                                else:
                                    L_2 = False
                                    
                                if cTF > 0:
                                    L_3 = True
                                else:
                                    L_3 = False
            
            
                                if (L_1 == L_2 == L_3):
                                    atk_en.x -= atk_en.tag_x
                                    atk_en.rect.x -= atk_en.tag_x
                                    atk_en.y -= atk_en.tag_y
                                    atk_en.rect.y -= atk_en.tag_y
                                    
                                    if atk_en.pre_test == 1:
                                        atk_en.tag_x = (math.cos(math.radians(obj.angle+90)*-2) * tem_x + math.sin(math.radians(obj.angle+90)*-2) * tem_y) *-1
                                        atk_en.tag_y = (math.sin(math.radians(obj.angle+90)*-2) * tem_x - math.cos(math.radians(obj.angle+90)*-2) * tem_y) * -1

                                    elif atk_en.pre_test == 2:
                                        atk_en.tag_x = (math.cos(math.radians(obj.angle+120)*-2) * tem_x + math.sin(math.radians(obj.angle+120)*-2) * tem_y) *-1
                                        atk_en.tag_y = (math.sin(math.radians(obj.angle+120)*-2) * tem_x - math.cos(math.radians(obj.angle+120)*-2) * tem_y) * -1
                                        
                                    elif atk_en.pre_test == 3:
                                        atk_en.tag_x = (math.cos(math.radians(obj.angle+60)*-2) * tem_x + math.sin(math.radians(obj.angle+60)*-2) * tem_y) *-1
                                        atk_en.tag_y = (math.sin(math.radians(obj.angle+60)*-2) * tem_x - math.cos(math.radians(obj.angle+60)*-2) * tem_y) * -1
                                    

                                    atk_en.L_mirror = obj  
                                    atk_en.pre_test = 0        
                                
                                if L_1 == L_2:
                                    atk_en.pre_test = 3
                                elif L_2 == L_3:
                                    atk_en.pre_test = 1
                                elif L_3 == L_1:
                                    atk_en.pre_test = 2
                            else:
                                atk_en.delete = 1
                        
            elif atk_en.dif == "light_ball":

                
                if atk_en.chase == 1:
                    
                    atk_en.dur -= 1                                     #扣時(存在時間)
                        
                    if atk_en.dur == 0:                                 #超時刪除
                        atk_en.delete = 1
                        
                        
                    if atk_en.tag_x == None:                            #飛行方向初始化 & 轉向
                        tem_x = (Main.rect.x+Main.rect.width/2 + 30*Main.vx - atk_en.rect.x- atk.rect.width/2)
                        tem_y = (Main.rect.y+Main.rect.height/2 + 10*Main.vy - atk_en.rect.y- atk.rect.height/2)           

                        atk_en.tag_x = tem_x / math.sqrt(pow(tem_x,2)+ pow(tem_y,2)) * 35
                        atk_en.tag_y = tem_y / math.sqrt(pow(tem_x,2)+ pow(tem_y,2)) * 35
                        
                    atk_en.rect.x += atk_en.tag_x                       #飛
                    atk_en.rect.y += atk_en.tag_y
                    atk_en.x = atk_en.rect.x
                    atk_en.y = atk_en.rect.y
                        
                        
                    for obj in NT_object:                               #撞牆掰掰
                        if atk_en.rect.colliderect(obj.rect) or atk_en.rect.colliderect(Main.rect):
                            ATKs_EN.append(object_class.object(atk_en.rect.x-75,atk_en.rect.y-50,pygame.image.load("Image/Character/Enemy/Boss/eps1.png"),"dangerous",1,0,"explosion",None,None,None,39))

                            atk_en.delete = 1
                    
            elif atk_en.dif == "explosion":
                atk_en.dur -= 1                                     #扣時(存在時間)
                    
                if atk_en.dur == 0:                                 #超時刪除
                    atk_en.delete = 1

                atk_en.surface = atk_en.frames[atk_en.dur//5]
                if atk_en.rect.colliderect(Main.rect):              #打到玩家
                                
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
                

                
                
                
            
                        
        if atk_en.delete == 1:                                  #問斬
            if atk_en.dif == "sun_blaze":
                enemy.sun_blaze = 0
            ATKs_EN.remove(atk_en)
            del atk_en            







    for obj in NT_object:
        Main.now_Touch.append(Touch(Main,obj))
    if not any(Main.now_Touch):
        #print("?")
        Main.through = 0
            
            
    #print(Main.now_Touch)


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

#===================================================================跳躍和受傷動畫轉向
    #print(Main.through, Main.on_ground)



    #如果(按下空格, 在地上, 剛才沒按空格)
    if keys[pygame.K_SPACE] and keys[pygame.K_s] and "1_DP" in Main.now_NT_Touch and not pre_keys[pygame.K_SPACE] and Main.HP > 0 and Main.move_lock == 0:                      #按下空白鍵跳躍
        Main.through = 1
        Main.vy = 1

    elif keys[pygame.K_SPACE] and not "1_U" in Main.now_NT_Touch and not pre_keys[pygame.K_SPACE] and Main.HP > 0 and Main.move_lock == 0 and not Main.block_state["playing"]:                      #按下空白鍵跳躍
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

    if Main.y > scene_ctrl.B_edge + 500:
        Main.HP = 0
    
    
    
    if Main.HP<=0:
        if Main.death_cd == 0:
            Main.Dead_sound.play()
        Main.death_cd+=1
        Main.move_lock=1
        if Main.flip:
            Main.surface=pygame.transform.flip(Main.Dead[Main.death_cd//30],True,False)
        else:
            Main.surface=Main.Dead[Main.death_cd//30]
        if Main.death_cd == 89:
            scene_ctrl.game = "dead"

    
    
#=========================================================================刷新畫面

   
    show(screen,scene[0],NT_object,CT_object,Enemy,ATKs_AL,ATKs_EN,Main,hint_backpack,trans,scene_ctrl)    #最終印刷