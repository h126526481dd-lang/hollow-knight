import random
import os
import pygame
import player_class
import object_class
import button
import math
import tool
import sys
import json
import ctypes

def force_english_input():
    # 0x0409 是英文(美國)鍵盤代碼
    ctypes.windll.user32.PostMessageW(
        ctypes.windll.user32.GetForegroundWindow(),
        0x0050,  # WM_INPUTLANGCHANGEREQUEST
        0,
        0x0409  # 英文
    )

def get_current_input_lang():
    hwnd = ctypes.windll.user32.GetForegroundWindow()  # 取得目前視窗
    thread_id = ctypes.windll.user32.GetWindowThreadProcessId(hwnd, 0)
    layout_id = ctypes.windll.user32.GetKeyboardLayout(thread_id)
    lang_id = layout_id & 0xFFFF
    return lang_id


class scene_c():
    def __init__(self):
        self.num = 0
        self.menu = 0
        self.fps = 60
        self.button_cd = 0
        self.game = 0
        self.pre_game = 0

def Load(save,scene_ctrl):
    global Main
    Main = tool.load(1,scene_ctrl)

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
Main.read_surface()

font = pygame.font.Font(None, 60)
font_2 = pygame.font.Font(None, 80)
BUTTON = pygame.sprite.Group()

print(pygame.display.get_active())                              #確認是否正確開啟

scene_ctrl.num = 0
pre_keys = []


#=======================================================================================================

while True:
    
    match scene_ctrl.num:
        
        case 0:                                                              #初始畫面
              
            BUTTON.empty()

            text = font_2.render("Welcome", True, (0,0,255))      #存檔標題
            text_rect = text.get_rect(center=(screen_width//2, screen_height//6))
            
            button1 = button.Button(screen_width//2, screen_height//7*3, "Start", lambda:button.on_click(scene_ctrl,10))
            button2 = button.Button(screen_width//2, screen_height//7*4, "Savings", lambda:button.on_click(scene_ctrl,5))
            button3 = button.Button(screen_width//2, screen_height//8*7, "Achievement", lambda:button.on_click(scene_ctrl,2))
            button4 = button.Button(screen_width//7, screen_height//8*7, "Menu", lambda:button.on_click(scene_ctrl,1))
            button5 = button.Button(screen_width//7*6, screen_height//8*7, "Quit", button.quit_button)

            BUTTON.add(button1,button2,button3,button4,button5)
            
            while scene_ctrl.num == 0: 
                
                
                if scene_ctrl.button_cd > 0:
                    scene_ctrl.button_cd-=1                

                # 建立按鈕並加入群組
                BUTTON.update(scene_ctrl)
                screen.fill((255,255,255))
                BUTTON.draw(screen)
                pygame.display.flip()


                for event in pygame.event.get():                               #偵測事件
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
            
#=======================================================================================================

        case 1:                                                                #選單
            
            
            
            BUTTON.empty()

            button1 = button.Button(screen_width//4, screen_height//4, "Audio", lambda:button.on_click(scene_ctrl,4))
            button2 = button.Button(screen_width//4, screen_height//2, "Video", lambda:button.on_click(scene_ctrl,4))  
            button_back = button.Button(screen_width//4*3, screen_height//8*7, "Go back", lambda:button.on_click(scene_ctrl, 0))

            BUTTON.add(button1, button2, button_back)

            while scene_ctrl.num == 1: 
            
                if scene_ctrl.button_cd > 0:
                    scene_ctrl.button_cd-=1
                

                scene_ctrl_temp = scene_ctrl.num                               #紀錄目前場景(用來使用back按鈕的)

                BUTTON.update(scene_ctrl)
                screen.fill((255,255,255))

                BUTTON.draw(screen)
                pygame.display.flip()

                for event in pygame.event.get():                               #偵測事件
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

#======================================================================================================
        case 2:                                                                #成就


            BUTTON.empty()

            scene_ctrl_temp = scene_ctrl.num                               #紀錄目前場景(用來使用back按鈕的)

            while scene_ctrl.num == 2: 

                if scene_ctrl.button_cd > 0:
                    scene_ctrl.button_cd-=1

                pygame.quit()
                exit()

                for event in pygame.event.get():                               #偵測事件
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

#=======================================================================================================

        case 3:                                                                #音量調整
            
            BUTTON.empty()
            
            button_back = button.Button(screen_width//4*3, screen_height//8*7, "Go back", lambda:button.on_click(scene_ctrl, scene_ctrl_temp))
            BUTTON.add(button_back)
            
            while scene_ctrl==5:
                
                pass
#=======================================================================================================

        case 4:                                                                #畫面設定
            
            
            BUTTON.empty()
            
            button_change_FPS = button.Button(screen_width//4, screen_height//4, "change FPS", lambda:button.change_FPS(scene_ctrl))   
            button_back = button.Button(screen_width//4*3, screen_height//8*7, "Go back", lambda:button.on_click(scene_ctrl, scene_ctrl_temp))
            BUTTON.add(button_back, button_change_FPS)


            while scene_ctrl.num == 4:
                if scene_ctrl.button_cd > 0:
                    scene_ctrl.button_cd-=1
        


                screen.fill((255,255,255))

                BUTTON.update(scene_ctrl)
                BUTTON.draw(screen)
                pygame.display.flip()
                

                for event in pygame.event.get():                               #偵測事件
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
#=======================================================================================================

        case 5:                                                                 #讀檔

            BUTTON.empty()

            scene_ctrl_temp = scene_ctrl.num                               #紀錄目前場景(用來使用back按鈕的)
            text = font.render("Savings", True, (0,0,0))      #存檔標題
            text_rect = text.get_rect(center=(screen_width//4, screen_height//6))

            button_saving1 = button.Button(screen_width//4, screen_height//8*3, "Saving 1", lambda:Load(1,scene_ctrl))
            button_saving2 = button.Button(screen_width//4, screen_height//8*4, "Saving 2", lambda:Load(2,scene_ctrl))
            button_saving3 = button.Button(screen_width//4, screen_height//8*5, "Saving 3", lambda:Load(3,scene_ctrl))
            button_saving4 = button.Button(screen_width//4, screen_height//8*6, "Saving 4", lambda:Load(4,scene_ctrl))
            button_back = button.Button(screen_width//4*3, screen_height//8*7, "Go back", lambda:button.on_click(scene_ctrl, 0))


            BUTTON.add(button_back)
            BUTTON.add(button_saving1, button_saving2, button_saving3, button_saving4)

            while scene_ctrl.num == 5:


                if scene_ctrl.button_cd > 0:
                    scene_ctrl.button_cd-=1


                screen.fill((255,255,255))
                screen.blit(text, text_rect)

                BUTTON.update(scene_ctrl)
                BUTTON.draw(screen)
                pygame.display.flip()

                for event in pygame.event.get():                               #偵測事件
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

#=======================================================================================================

        case 10:                                                             #遊戲main loop
            
            match scene_ctrl.game:
                
                
                
                case 0:
            
                    scene = []
                    NT_object = []
                    CT_object = []
                    Enemy = []
                    ATKs_AL = []
                    ATKs_EN = []
                    BUTTON.empty()

                    scene_ctrl_temp = scene_ctrl.num                               #紀錄目前場景(用來使用back按鈕的)

                    scene.append(pygame.image.load("IMG_2794.jpg"))                  #導入背景圖片
                    scene[0] = pygame.transform.scale(scene[0], (screen_width*5, screen_height*5))  # 調整大小
                    
                    NT_object.append(object_class.object(1200,800,tool.HRZ_combine("floor.png",10),"wall",0,0,0,0,0))
                    NT_object.append(object_class.object(-50,400,tool.HRZ_combine("floor.png",10),"wall",0,0,0,1,0))
                    
                    NT_object.append(object_class.object(1600,-500,tool.V_combine("floor.png",10),"wall",0,0,0,0,0))


                    door = pygame.image.load("door.png")
                    door = pygame.transform.scale(door, (200, 200))  # 調整大小

                    save_point=pygame.image.load("save_point.png")
                    save_point = pygame.transform.scale(save_point, (400, 200))  # 調整大小

                    CT_object.append(object_class.object(2400,600,door,"path",0,0,0,0,0))
                    CT_object.append(object_class.object(2000,600,save_point,"save_point",0,0,0,0,0))
                    CT_object.append(object_class.object(1600,500,door,"door",0,0,0,0,0))
                    CT_object.append(object_class.object(2000,300,pygame.image.load("skill.png"),"skill",0,0,0,6,0))

                    Enemy.append(player_class.enemy("The_First",1200,0,100,"zombie"))

                    # button_home = button.Button(200, 200, "Home", lambda:button.on_click(scene_ctrl,0))

                    # BUTTON.add(button_home)
                case 1:
                    pass
                
                case 2:
                    pass


            #while True:
             #   tool.show(screen,scene,NT_object,CT_object,Enemy,ATKs_AL,ATKs_EN,Main)
              #  scene_ctrl.pre_game = scene_ctrl.game


           
            while scene_ctrl.num == 10 and scene_ctrl.game == scene_ctrl.pre_game:                                                     #遊戲主迴圈

                clock.tick(scene_ctrl.fps)                                             #控制每秒最多執行 FPS 次(固定每台電腦的執行速度)

                if not get_current_input_lang() == 0x0409:
                    force_english_input()

            
                if Main.is_hurt > 20:
                    Main.is_hurt -= 1
                    continue
                
                # BUTTON.update()
                # BUTTON.draw(screen)
                # pygame.display.flip()

                #print("FPS:", clock.get_fps())
                
                keys = pygame.key.get_pressed()                             #偵測按鍵(把偵測按鍵拉出event.get()迴圈外，規避windows的按鍵延遲)

                for obj in CT_object:
                    if keys[pygame.K_w]:                                #按下w進門

                        if obj.type == "door":
                            if tool.Touch(Main,obj):
                                scene_ctrl.game = 11
                    if obj.type == "path":
                        if tool.Touch(Main,obj):
                            scene_ctrl.num = 0
                            print(0)
                    if obj.type == "save_point":
                        if keys[pygame.K_p]:
                            tool.save(Main,scene_ctrl)
                            Main.read_surface()
                                
                tool.tick_mission(screen, scene, Main, Enemy, ATKs_AL, ATKs_EN, NT_object, CT_object, keys, pre_keys)

                pre_keys = keys


                                
          
#=======================================================================================================