import random
import os
import pygame
import player_class
import object_class
import button
import math
import tool
import sys

class scene_c():
    def __init__(self):
        self.num = 0
        self.menu = 0

#=======================================================================================================

pygame.init()                                                   #初始化
Info = pygame.display.Info()                                      #偵測用戶顯示參數
screen_height = Info.current_h                                  #設定畫面大小成用戶螢幕大小
screen_width  = Info.current_w

scene_ctrl=scene_c()

screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME)

#導入背景，無邊框，螢幕大小

clock = pygame.time.Clock()                                     #建立時鐘物件(用來處理tick)
FPS = 60                                                     #設定每秒幀數

Main = player_class.player("BOBO",0,0)                #建立角色物件

# font = pygame.font.Font(None, 50)

BUTTON = pygame.sprite.Group()

print(pygame.display.get_active())                              #確認是否正確開啟

scene_ctrl.num = 0
pre_keys = []


#=======================================================================================================

while True:
    match scene_ctrl.num:
        
        case 0:                                                              #初始畫面
            
                        
            BUTTON.empty()

            button1 = button.Button(screen_width//2, 300, "Start", lambda:button.on_click(scene_ctrl,10))
            button2 = button.Button(screen_width//2, 400, "Menu", lambda:button.on_click(scene_ctrl,1))
            button3 = button.Button(screen_width//2, 500, "Achievement", lambda:button.on_click(scene_ctrl,2))
            button4 = button.Button(screen_width//2, 900, "Quit", button.quit_button)

            BUTTON.add(button1)
            BUTTON.add(button2)
            BUTTON.add(button3)
            BUTTON.add(button4)

            
            
            while scene_ctrl.num == 0: 


                # 建立按鈕並加入群組
                BUTTON.update()
                screen.fill((50, 50, 50))
                BUTTON.draw(screen)
                pygame.display.flip()


                for event in pygame.event.get():                               #偵測事件
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
            
#=======================================================================================================

        case 1:                                                                #選單
            
            BUTTON.empty()

            button1 = button.Button(screen_width//2, 400, "Audio", lambda:button.on_click(scene_ctrl,10))
            button2 = button.Button(screen_width//2, 700, "Video", lambda:button.on_click(scene_ctrl,1))

            BUTTON.add(button1)
            BUTTON.add(button2)

            while scene_ctrl.num == 1: 

                BUTTON.update()
                screen.fill((50, 50, 50))

                BUTTON.draw(screen)
                pygame.display.flip()

                for event in pygame.event.get():                               #偵測事件
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

#======================================================================================================
        case 2:                                                                #成就

            BUTTON.empty()


            while scene_ctrl.num == 2: 



                pass


                for event in pygame.event.get():                               #偵測事件
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

#=======================================================================================================

        case 3:                                                                #音量調整
            pass
#=======================================================================================================

        case 4:                                                                #畫面設定
            pass

#=======================================================================================================

        case 10:                                                             #場景10

            Main.x = 0
            Main.y = 0
            Main.rect.x = 50
            Main.rect.y = 50
            scene = []
            NT_object = []
            CT_object = []
            Enemy = []
            ATKs_AL = []
            ATKs_EN = []

            scene.append(pygame.image.load("IMG_2794.jpg"))                  #導入背景圖片
            scene[0] = pygame.transform.scale(scene[0], (screen_width*5, screen_height*5))  # 調整大小
            
            NT_object.append(object_class.object(1200,800,tool.HRZ_combine("floor.png",10),"wall",0,0,0,0,0))
            NT_object.append(object_class.object(-50,400,tool.HRZ_combine("floor.png",10),"wall",0,0,0,1,0))


            door = pygame.image.load("door.png")
            door = pygame.transform.scale(door, (200, 200))  # 調整大小
            
            CT_object.append(object_class.object(2400,600,door,"path",0,0,0,0,0))
            
            CT_object.append(object_class.object(1600,500,door,"door",0,0,0,0,0))
            CT_object.append(object_class.object(2000,300,pygame.image.load("skill.png"),"skill",0,0,0,6,0))

            Enemy.append(player_class.enemy("The_First",1200,0,100,"zombie"))
            
            while scene_ctrl.num == 10:                                                     #遊戲主迴圈

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
                                scene_ctrl.num = 11
                    if obj.type == "path":
                        if tool.Touch(Main,obj):
                            scene_ctrl.num = 0

                                
                tool.tick_mission(screen, scene, Main, Enemy, ATKs_AL, ATKs_EN, NT_object, CT_object, keys, pre_keys)

                pre_keys = keys


                                
          
#=======================================================================================================

        case 11:                                                             #場景1
            while scene_ctrl.num == 11:                                                     #遊戲主迴圈
            
                print("go")
                pygame.quit()
                exit()