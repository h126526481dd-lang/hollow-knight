import random
import os
import pygame
import player_class
import object_class
import button
import math
import tool
import sys

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
pre_keys = []

#=======================================================================================================

while True:
    match scene_ctrl:
        
        case 0:                                                              #場景0
            
            while True: 
                screen.fill(color= "white")
                
                test=button.button("black",200,200)
                
                screen.blit(test.image,(400,400))
                
                pygame.display.update()

                for event in pygame.event.get():                               #偵測事件
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
            
#=======================================================================================================

        case 10:                                                             #場景10

            scene = []
            NT_object = []
            CT_object = []
            Enemy = []
            ATKs_AL = []
            ATKs_EN = []

            scene.append(pygame.image.load("IMG_2794.jpg"))                  #導入背景圖片
            scene[0] = pygame.transform.scale(scene[0], (screen_width*8, screen_height*8))  # 調整大小
            
            NT_object.append(object_class.object(1200,800,tool.HRZ_combine("floor.png",10),"wall",0,0,0,0,0))
            NT_object.append(object_class.object(-50,400,tool.HRZ_combine("floor.png",10),"wall",0,0,0,1,0))
            NT_object.append(object_class.object(1200,0,tool.HRZ_combine("floor.png",10),"wall",0,0,0,1,0))
            NT_object.append(object_class.object(-50,-400,tool.HRZ_combine("floor.png",10),"wall",0,0,0,1,0))
            NT_object.append(object_class.object(1200,-800,tool.HRZ_combine("floor.png",10),"wall",0,0,0,1,0))
            NT_object.append(object_class.object(-50,-1200,tool.HRZ_combine("floor.png",10),"wall",0,0,0,1,0))
            NT_object.append(object_class.object(1200,-1600,tool.HRZ_combine("floor.png",10),"wall",0,0,0,1,0))



            door = pygame.image.load("door.png")
            door = pygame.transform.scale(door, (200, 200))  # 調整大小
            
            CT_object.append(object_class.object(2400,600,door,"path",0,0,0,0,0))
            
            CT_object.append(object_class.object(1600,500,door,"door",0,0,0,0,0))
            CT_object.append(object_class.object(2000,-2000,pygame.image.load("skill.png"),"skill",0,0,0,6,0))
            CT_object.append(object_class.object(2000,600,pygame.image.load("skill.png"),"skill",0,0,0,4,0))


            Enemy.append(player_class.enemy("The_First",1200,0,100,"zombie"))
            
            while scene_ctrl == 10:                                                     #遊戲主迴圈

                clock.tick(FPS)                                             #控制每秒最多執行 FPS 次(固定每台電腦的執行速度)

                if Main.is_hurt > 20:
                    Main.is_hurt -= 1
                    continue
                    
                #print("FPS:", clock.get_fps())
                
                keys = pygame.key.get_pressed()                             #偵測按鍵(把偵測按鍵拉出event.get()迴圈外，規避windows的按鍵延遲)

                for obj in CT_object:
                    if keys[pygame.K_w]:                                #按下w進門

                        if obj.type == "door":
                            if tool.Touch(Main,obj):
                                scene_ctrl = 11
                    if obj.type == "path":
                        if tool.Touch(Main,obj):
                            scene_ctrl = 0

                                
                tool.tick_mission(screen, scene, Main, Enemy, ATKs_AL, ATKs_EN, NT_object, CT_object, keys, pre_keys)

                pre_keys = keys
                
#=======================================================================================================

        case 11:                                                             #場景1
            while scene_ctrl == 11:                                                     #遊戲主迴圈
            
                print("go")
                pygame.quit()
                exit()