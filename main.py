import random
import os
import pygame
import player_class
import object_class
import math



def show(scene,NT_object,CT_object,Enemy,player):                          #繪製畫面(待修，以後應該是以場景為單位來繪製，要新增場景的class，裡面包含現在要輸入的東西)

    adjust_y = screen_height//2                                 #螢幕中心座標
    adjust_x = screen_width//2
    camera_x = player.x - adjust_x                              #把角色置中所需要的向量  
    camera_y = player.y - adjust_y
    
    camera_rect = pygame.Rect(camera_x,camera_y,screen_width,screen_height)  #攝影機碰撞盒(只顯示在螢幕中的物件)
    

    screen.blit(scene, (-500-camera_x, -500-camera_y))                  #繪製背景圖片(背景位置=原位置-置中向量)
   
    for obj in NT_object:                                 #繪製物件    (若與camera有碰撞，物件位置=原位置-置中向量)
        if camera_rect.colliderect(obj.rect):
            screen.blit(obj.surface, (obj.x-camera_x, obj.y-camera_y))
            pygame.draw.rect(screen, (255, 0, 0),pygame.Rect(obj.x - camera_x, obj.y - camera_y, obj.rect.width, obj.rect.height),1) 
            
    for obj in CT_object:                                 #繪製物件    (若與camera有碰撞，物件位置=原位置-置中向量)
        if camera_rect.colliderect(obj.rect):
            screen.blit(obj.surface, (obj.x-camera_x, obj.y-camera_y))
            pygame.draw.rect(screen, (255, 0, 0),pygame.Rect(obj.x - camera_x, obj.y - camera_y, obj.rect.width, obj.rect.height),1)
    
    for enemy in Enemy:
        if camera_rect.colliderect(enemy.rect):
            screen.blit(enemy.surface, (enemy.x-camera_x, enemy.y-camera_y))
            pygame.draw.rect(screen, (255, 0, 0),pygame.Rect(enemy.x - camera_x, enemy.y - camera_y, enemy.rect.width, enemy.rect.height),1)
            pygame.draw.rect(screen, (255, 0, 0),pygame.Rect(enemy.right_down_x-enemy.Test_rect.width-camera_x,  enemy.right_down_y-camera_y, enemy.Test_rect.width, enemy.Test_rect.height),1)

    screen.blit(player.surface, ( player.x-camera_x,player.y-camera_y))#繪製角色    (角色位置=原位置-置中向量=螢幕中心)
    pygame.draw.rect(screen, (255, 0, 0),pygame.Rect(player.rect.x - camera_x,player.rect.y - camera_y, player.rect.width, player.rect.height),1)
    
    
    pygame.display.update()



#=======================================================================================================



pygame.init()                                                   #初始化
Info = pygame.display.Info()                                      #偵測用戶顯示參數
screen_height = Info.current_h                                  #設定畫面大小成用戶螢幕大小
screen_width  = Info.current_w


screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME)

#導入背景，無邊框，螢幕大小

clock = pygame.time.Clock()                                     #建立時鐘物件(用來處理tick)
FPS = 60                                                     #設定每秒幀數

Main = player_class.player("BOBO",0,0)                #建立角色物件


print(pygame.display.get_active())                              #確認是否正確開啟

scene_ctrl = 10
#=======================================================================================================

while True:
    match scene_ctrl:
        
        case 10:                                                             #場景0

            scene = []
            NT_object = []
            CT_object = []
            Enemy = []

            scene.append(pygame.image.load("IMG_2794.jpg"))                  #導入背景圖片
            scene[0] = pygame.transform.scale(scene[0], (screen_width*5, screen_height*5))  # 調整大小
            
            NT_object.append(object_class.object(1200,800,player_class.HRZ_combine("floor.png",10),"wall"))
            NT_object.append(object_class.object(-50,400,player_class.HRZ_combine("floor.png",10),"wall"))


            door = pygame.image.load("door.png")
            door = pygame.transform.scale(door, (200, 200))  # 調整大小
            CT_object.append(object_class.object(1200,500,door,"door"))

            Enemy.append(player_class.enemy("The_First",1200,0,10,"zombie"))
            
            
            while scene_ctrl == 10:                                                     #遊戲主迴圈
            
                clock.tick(FPS)                                             #控制每秒最多執行 FPS 次(固定每台電腦的執行速度)

                Main.now_NT_Touch = []                                      #角色目前碰撞清單
                for obj in NT_object:
                    player_class.Touch(Main,obj)

                for enemy in Enemy:
                    player_class.enemy.Move(enemy,NT_object)
                    print(NT_object[0].x)
                    print(NT_object[0].y)
                    if player_class.Touch(Main,enemy):
                        Main.HP -= 1
                       # print(Main.HP)

                        
                if not "1_D" in Main.now_NT_Touch :                                           #若沒有站地上，則設為False
                    Main.on_ground = False
                    
                if "1_U" in Main.now_NT_Touch and Main.vy < 0:                                           #若沒有站地上，則設為False
                    Main.vy = 0 
                    
                if Main.on_ground == False and Main.vy <= 30:           #重力加速度(有設上限)
                    Main.vy += 1
            
                elif Main.on_ground == True:                            #觸地垂直速度歸零
                    Main.vy = 0

                keys = pygame.key.get_pressed()                             #偵測按鍵(把偵測按鍵拉出event.get()迴圈外，規避windows的按鍵延遲)
                

                if keys[pygame.K_d] and keys[pygame.K_a]:                #避免同時按兩個方向鍵
                    
                    pass
                
                else:
                
                    if keys[pygame.K_d]:                                #按下d鍵右移
                        Main.R_move()

                    elif keys[pygame.K_a]:                                #按下a鍵左移
                        Main.L_move()

                    else:                                                   #不移動時水平速度歸零(沒有慣性)
                        Main.idle() and not Main.attack_state["playing"]
                        Main.vx = 0
                    
                    if keys[pygame.K_j] and not Main.attack_state["playing"]:
                        Main.attack()

                    finished = player_class.update_animation(Main, Main.attack_state)
                    if finished and Main.atk_next == 0:
                        Main.atk_next = 20                              #此段攻擊結束需多久接下一段
                    if Main.atk_next > 0:
                        Main.atk_next -= 1


                    if keys[pygame.K_w]:                                #按下w進門
                        for obj in CT_object:
                            if obj.type=="door":
                                if player_class.Touch(Main,obj):
                                    scene_ctrl=11
                    

                if keys[pygame.K_SPACE] and not "1_U" in Main.now_NT_Touch :                                #按下空白鍵跳躍
                    Main.jump()

                Main.y += Main.vy                                       #更新角色位置
                Main.x += Main.vx

                Main.rect.x += Main.vx
                Main.rect.y += Main.vy


                for event in pygame.event.get():                               #偵測事件
                
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                if Main.y>1800:
                    Main.y=0
                    Main.rect.y=50
                
                
                
                

                

                
                
                show(scene[0],NT_object,CT_object,Enemy,Main)
#=======================================================================================================

        case 11:                                                             #場景1
            while scene_ctrl == 11:                                                     #遊戲主迴圈
            
                print("go")
                pygame.quit()
                exit()