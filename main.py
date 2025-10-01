import random
import os
import pygame
import player_class
import object_class
import math
import tool



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
pre_keys=[]
#=======================================================================================================

while True:
    match scene_ctrl:
        
        case 0:                                                              #場景0
            scene = []
            scene.append(pygame.image.load("white.jpg"))                  #導入背景圖片
            scene[0] = pygame.transform.scale(scene[0], (screen_width*5, screen_height*5))  # 調整大小

            tool.show(screen,scene[0],0,0,0,0)
            pass
#=======================================================================================================

        case 10:                                                             #場景10

            scene = []
            NT_object = []
            CT_object = []
            Enemy = []
            ATKs_AL=[]
            ATKs_EN=[]

            scene.append(pygame.image.load("IMG_2794.jpg"))                  #導入背景圖片
            scene[0] = pygame.transform.scale(scene[0], (screen_width*5, screen_height*5))  # 調整大小
            
            NT_object.append(object_class.object(1200,800,tool.HRZ_combine("floor.png",10),"wall",0,0,0))
            NT_object.append(object_class.object(-50,400,tool.HRZ_combine("floor.png",10),"wall",0,0,0))


            door = pygame.image.load("door.png")
            door = pygame.transform.scale(door, (200, 200))  # 調整大小
            CT_object.append(object_class.object(1600,500,door,"door",0,0,0))

            Enemy.append(player_class.enemy("The_First",1200,0,100,"zombie"))
            
            
            while scene_ctrl == 10:                                                     #遊戲主迴圈
            
                clock.tick(FPS)                                             #控制每秒最多執行 FPS 次(固定每台電腦的執行速度)
                #print("FPS:", clock.get_fps())

                Main.now_NT_Touch = []                                      #角色目前碰撞清單

                for enemy in Enemy:
                    if enemy.unhurtable_cd > 0:
                        enemy.unhurtable_cd -= 3
                    enemy.now_CT_Touch = []
                    for atk_al in ATKs_AL:
                        if enemy.unhurtable_cd <= 0:
                            if tool.Touch(enemy,atk_al):
                                if atk_al.rect.x-enemy.rect.x < 0:
                                    enemy.HP-=atk_al.ATK
                                    enemy.x+=atk_al.KB
                                    enemy.unhurtable_cd = 30
                                else:
                                    enemy.HP-=atk_al.ATK
                                    enemy.x-=atk_al.KB
                                    enemy.unhurtable_cd = 30

                    if enemy.HP<=0:
                        Enemy.remove(enemy)

                for obj in NT_object:
                    tool.Touch(Main,obj)

                Main.unhurtable_cd -=1
                for enemy in Enemy:
                    player_class.enemy.Move(enemy,NT_object)

                    if tool.Touch(Main,enemy):
                        Main.get_hit()


                        
                if not "1_D" in Main.now_NT_Touch :                                           #若沒有站地上，則設為False
                    Main.on_ground = False
                    
                if "1_U" in Main.now_NT_Touch and Main.vy < 0:                                           #若沒有站地上，則設為False
                    Main.vy = 0 
                    
                if Main.on_ground == False and Main.vy <= 30:           #重力加速度(有設上限)
                    Main.vy += 1
            
                elif Main.on_ground == True:                            #觸地垂直速度歸零
                    Main.vy = 0

                keys = pygame.key.get_pressed()                             #偵測按鍵(把偵測按鍵拉出event.get()迴圈外，規避windows的按鍵延遲)
                
                if not Main.attack_state["playing"] or Main.atk_procedure != 2:     #如果不是第三段攻擊
                    if keys[pygame.K_d] and keys[pygame.K_a]:                #避免同時按兩個方向鍵
                        
                        pass
                    
                    else:
                    
                        if keys[pygame.K_d]:                                #按下d鍵右移
                            Main.R_move()

                        elif keys[pygame.K_a]:                                #按下a鍵左移
                            Main.L_move()

                        else:                                                   #不移動時水平速度歸零(沒有慣性)
                            Main.idle() 
                            Main.vx = 0
                elif abs(Main.vx) > 0:
                    if Main.flip:
                        Main.vx += 2
                    else:
                        Main.vx -= 2

                
                if keys[pygame.K_j] and not Main.attack_state["playing"] and not pre_keys[pygame.K_j]:
                    if Main.flip==0:
                        match Main.atk_procedure:
                            case 0:
                                ATKs_AL.append(object_class.object(Main.x+50,Main.y,pygame.image.load("Character\mainchacter\\blade1_start.png"),"dangerous",10,20,Main.blade1))
                            case 1:
                                pass
                            case 2:
                                pass
                        
                    else:
                        match Main.atk_procedure:
                            case 0:
                                pass
                            case 1:
                                pass
                            case 2:
                                pass
                    Main.attack()
                    print(Main.blade_state["playing"])

                for atk_AL in ATKs_AL:
                    tool.update_animation(atk_AL, Main.blade_state)
                    

                finished = tool.update_animation(Main, Main.attack_state)
                if finished and Main.atk_next == 0:
                    Main.atk_next = 20                              #此段攻擊結束需多久接下一段
                if Main.atk_next > 0:
                    Main.atk_next -= 1


                if keys[pygame.K_w]:                                #按下w進門
                    for obj in CT_object:
                        if obj.type=="door":
                            if tool.Touch(Main,obj):
                                scene_ctrl=11
                    

                if keys[pygame.K_SPACE] and not "1_U" in Main.now_NT_Touch :                                #按下空白鍵跳躍
                    Main.jump()

                pre_keys = keys

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
                
                if Main.HP <=0:
                    print("死")
                    pygame.quit()
                    exit()

                
                
                tool.show(screen,scene[0],NT_object,CT_object,Enemy,ATKs_AL,ATKs_EN,Main)
#=======================================================================================================

        case 11:                                                             #場景1
            while scene_ctrl == 11:                                                     #遊戲主迴圈
            
                print("go")
                pygame.quit()
                exit()