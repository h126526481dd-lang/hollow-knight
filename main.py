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
        self.trans = 0
        self.R_edge = 0
        self.L_edge = 0
        self.B_edge = 1800
        self.T_edge = -1000
        self.init = 0
        self.back_cd = 0
        self.From = 0
        self.backpack = 0
        self.done = 0
        self.reset = 0
        

def Load(save):
    global Main
    global scene_ctrl
    Main = tool.load_p(save)
    scene_ctrl = tool.load_s(save,scene_ctrl)

#=======================================================================================================

pygame.init()   #初始化
pygame.mixer.init()  # 初始化音效系統 
Info = pygame.display.Info()                                      #偵測用戶顯示參數
screen_height = Info.current_h                                  #設定畫面大小成用戶螢幕大小
screen_width  = Info.current_w

trans=object_class.object(-1*screen_width,-0.5*screen_height,pygame.transform.scale(pygame.image.load("Image/Background/trans.png"), (screen_width*2, screen_height*2)),"trans",0,0,0,0,0,0)


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
            
            scene = []
            BUTTON.empty()

            button_start = button.Button(screen_width//2, screen_height//7*3, "Start", lambda:button.on_click(scene_ctrl,5))
            button_achievement = button.Button(screen_width//2, screen_height//8*7, "Achievement", lambda:button.on_click(scene_ctrl,2))
            button_menu = button.Button(screen_width//7, screen_height//8*7, "Menu", lambda:button.on_click(scene_ctrl,1))
            button_quit = button.Button(screen_width//7*6, screen_height//8*7, "Quit", button.quit_button)

            BUTTON.add(button_start,button_achievement,button_menu,button_quit)
            
            while scene_ctrl.num == 0: 
                
                scene.append(pygame.image.load("Image/Background/title_scene.png"))         # 導入背景圖片
                scene[0] = pygame.transform.scale(scene[0], (screen_width, screen_height))  # 調整大小

                screen.blit(scene[0], (0,0))                  #繪製背景圖片

                if scene_ctrl.button_cd > 0:
                    scene_ctrl.button_cd-=1                

                # 建立按鈕並加入群組
                BUTTON.update(scene_ctrl)
                BUTTON.draw(screen)
                pygame.display.update()


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
             
            button_back = button.Button(screen_width//4*3, screen_height//8*7, "Go back", lambda:button.on_click(scene_ctrl, scene_ctrl_temp))
            BUTTON.add(button_back)


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

            match scene_ctrl.reset:

                case 0:

                    BUTTON.empty()

                    text = font.render("Savings", True, (0,0,0))      #存檔標題
                    text_rect = text.get_rect(center=(screen_width//4, screen_height//6))

                    button_saving1 = button.Button(screen_width//4, screen_height//8*3, "Saving 1", lambda:Load(1))
                    button_saving2 = button.Button(screen_width//4, screen_height//8*4, "Saving 2", lambda:Load(2))
                    button_saving3 = button.Button(screen_width//4, screen_height//8*5, "Saving 3", lambda:Load(3))
                    button_saving4 = button.Button(screen_width//4, screen_height//8*6, "Saving 4", lambda:Load(4))
                    button_back = button.Button(screen_width//4*3, screen_height//8*7, "Go back", lambda:button.on_click(scene_ctrl, 0))
                    button_reset = button.Button(screen_width//4*3, screen_height//8*6, "reset saving", lambda:button.reset(scene_ctrl, 1))

                    BUTTON.add(button_back)
                    BUTTON.add(button_saving1, button_saving2, button_saving3, button_saving4, button_reset)

                    while scene_ctrl.num == 5 and scene_ctrl.reset == 0:

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

                case 1:                                                                #等待修復reset功能

                    BUTTON.empty()

                    button_reset1 = button.Button(screen_width//4, screen_height//8*3, "Reset 1", lambda:Load(1))
                    button_reset2 = button.Button(screen_width//4, screen_height//8*4, "Reset 2", lambda:Load(2))
                    button_reset3 = button.Button(screen_width//4, screen_height//8*5, "Reset 3", lambda:Load(3))
                    button_reset4 = button.Button(screen_width//4, screen_height//8*6, "Reset 4", lambda:Load(4))
                    button_reset_back = button.Button(screen_width//4*3, screen_height//8*7, "Go back", lambda:button.reset(scene_ctrl, 0))

                    BUTTON.add(button_reset1, button_reset2, button_reset3, button_reset4, button_reset_back)

                    while scene_ctrl.num == 5 and scene_ctrl.reset == 1:

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

        #case 6:                                                               

            #BUTTON.empty()
            
            
#=======================================================================================================

        case 10:                                                             #遊戲main loop
            
            match scene_ctrl.game:
                
                case -3:
                    Exit = [(3000,-1500)]
                    scene_ctrl.done = 0
                    if scene_ctrl.pre_game == -2:
                        (Main.x,Main.y) = Exit[scene_ctrl.From]
                        (Main.rect.x,Main.rect.y) = (Main.x+50,Main.y+50)
                        
                    scene = []
                    NT_object = []
                    CT_object = []
                    Enemy = []
                    ATKs_AL = []
                    ATKs_EN = []
                    strength_bar = []

                    BUTTON.empty()
                    
                    
                    scene_ctrl_temp = scene_ctrl.num                               #紀錄目前場景(用來使用back按鈕的)
                
                    scene_ctrl.R_edge = 2500 - screen_width//2
                    scene_ctrl.L_edge = -3200 + screen_width//2
                    scene_ctrl.T_edge = -2300 + screen_height //2
                    scene_ctrl.B_edge = 350

                    scene.append(pygame.image.load("Image/Background/background.png"))                                 #導入背景圖片
                    scene[0] = pygame.transform.scale(scene[0], (screen_width*5, screen_height*5))  # 調整大小
                    scene.append(pygame.image.load("Image/Background/white.jpg"))                                    #導入背景圖片
                    scene[1] = pygame.transform.scale(scene[1], (screen_width*5, screen_height*5))  # 調整大小
                    
                    NT_object.append(object_class.object(2500,-1400,tool.HRZ_combine("Image/Background/floor.png",8),"wall",0,0,0,0,0,0))
                    NT_object.append(object_class.object(-1720,-1400,tool.HRZ_combine("Image/Background/floor.png",33),"fake_wall",0,0,0,0,0,0))
                    
                    NT_object.append(object_class.object(-1100,700,tool.HRZ_combine("Image/Background/floor.png",15),"mirror_wall",0,0,0,0,0,0))
                    NT_object.append(object_class.object(-1300,250,tool.HRZ_combine("Image/Background/floor.png",3),"mirror_wall",0,0,0,0,0,0))
                    NT_object.append(object_class.object(650,250,tool.HRZ_combine("Image/Background/floor.png",3),"mirror_wall",0,0,0,0,0,0))

                    

                    Enemy.append(player_class.enemy("The_Second",-400,-300,450,"boss","The_Tank"))
                    #Enemy.append(player_class.enemy("The_Third",-400,-300,200,"boss","The_Sun"))


                    door = pygame.image.load("Image/Object/door.png")
                    door = pygame.transform.scale(door, (200, 700))  # 調整大小

                    save_point = pygame.image.load("Image/Object/save_point.png")
                    save_point = pygame.transform.scale(save_point, (350, 200))  # 調整大小

                    CT_object.append(object_class.object(3300,-1900,door,"path",0,0,0,0,0,[-2,1]))

                    CT_object.append(object_class.object(2500,-1600,save_point,"save_point",0,0,0,0,0,0))

                    strength_bar.append(pygame.image.load("Image/UI/strength_bar.png"))
                    strength_bar[0] = pygame.transform.scale(strength_bar[0], (screen_width/9, screen_height/12))
                    strength_bar.append(pygame.image.load("Image/UI/strength_bar_1.png"))
                    strength_bar[1] = pygame.transform.scale(strength_bar[1], (screen_width/9, screen_height/12))
                    strength_bar.append(pygame.image.load("Image/UI/strength_bar_2.png"))
                    strength_bar[2] = pygame.transform.scale(strength_bar[2], (screen_width/9, screen_height/12))
                    strength_bar.append(pygame.image.load("Image/UI/strength_bar_3.png"))
                    strength_bar[3] = pygame.transform.scale(strength_bar[3], (screen_width/9, screen_height/12))
                    strength_bar.append(pygame.image.load("Image/UI/strength_bar_4.png"))
                    strength_bar[4] = pygame.transform.scale(strength_bar[4], (screen_width/9, screen_height/12))

                    hint_backpack = pygame.image.load("Image/keys/keyboard_b.png")
                    hint_backpack = pygame.transform.scale(hint_backpack, (145,45))

                case -2:                                                    #場景控制區
                    Exit = [(-350,0),(-700,0)]
                    scene_ctrl.done = 0
                    if scene_ctrl.pre_game == -1:
                        (Main.x,Main.y) = Exit[scene_ctrl.From]
                        (Main.rect.x,Main.rect.y) = (Main.x+50,Main.y+50)
                        Main.vy = -20
                        Main.inertia = 30
                        Main.vx = 5   
                        
                    if scene_ctrl.pre_game == -3:
                        (Main.x,Main.y) = Exit[scene_ctrl.From]
                        (Main.rect.x,Main.rect.y) = (Main.x+50,Main.y+50)
                        
                    
                    scene = []
                    NT_object = []
                    CT_object = []
                    Enemy = []
                    ATKs_AL = []
                    ATKs_EN = []
                    strength_bar = []

                    BUTTON.empty()
                    
                    
                    scene_ctrl_temp = scene_ctrl.num                               #紀錄目前場景(用來使用back按鈕的)
                    
                    scene_ctrl.R_edge = 1800 - screen_width//2
                    scene_ctrl.L_edge = -1500 + screen_width//2
                    scene_ctrl.T_edge = -1900 + screen_height //2
                    scene_ctrl.B_edge = -250

                    scene.append(pygame.image.load("Image/Background/background.png"))                                 #導入背景圖片
                    scene[0] = pygame.transform.scale(scene[0], (screen_width*5, screen_height*5))  # 調整大小
                    scene.append(pygame.image.load("Image/Background/white.jpg"))                                    #導入背景圖片
                    scene[1] = pygame.transform.scale(scene[1], (screen_width*5, screen_height*5))  # 調整大小
                    
                    NT_object.append(object_class.object(-250,100,tool.HRZ_combine("Image/Background/floor.png",20),"wall",0,0,0,0,0,0))

                    NT_object.append(object_class.object(2300,-1500,pygame.transform.scale(tool.V_combine("Image/Background/floor.png",10),(600,2100)),"wall",0,0,0,0,0,0))

                    NT_object.append(object_class.object(-1300,100,tool.HRZ_combine("Image/Background/floor.png",6),"wall",0,0,0,0,0,0))
                    
                    
                    NT_object.append(object_class.object(400,-1500,tool.HRZ_combine("Image/Background/floor.png",15),"wall",0,0,0,0,0,0))


                    Enemy.append(player_class.enemy("The_Second",1200,-200,450,"boss","The_Tank"))
                    #Enemy.append(player_class.enemy("The_Third",1200,-600,200,"boss","The_Sun"))


                    door = pygame.image.load("Image/Object/door.png")
                    door = pygame.transform.scale(door, (350, 200))  # 調整大小

                    save_point = pygame.image.load("Image/Object/save_point.png")
                    save_point = pygame.transform.scale(save_point, (400, 200))  # 調整大小

                    CT_object.append(object_class.object(-550,200,door,"path",0,0,0,0,0,[-1,1]))
                    
                    
                    door = pygame.transform.scale(door, (200, 700))  # 調整大小

                    CT_object.append(object_class.object(-1000,-400,door,"path",0,0,0,0,0,[-3,0]))

                    CT_object.append(object_class.object(0,-100,save_point,"save_point",0,0,0,0,0,0))
                    CT_object.append(object_class.object(2000,500,pygame.image.load("Image/Object/skill.png"),"skill",0,0,0,5,0,0))

                    strength_bar.append(pygame.image.load("Image/UI/strength_bar.png"))
                    strength_bar[0] = pygame.transform.scale(strength_bar[0], (screen_width/9, screen_height/12))
                    strength_bar.append(pygame.image.load("Image/UI/strength_bar_1.png"))
                    strength_bar[1] = pygame.transform.scale(strength_bar[1], (screen_width/9, screen_height/12))
                    strength_bar.append(pygame.image.load("Image/UI/strength_bar_2.png"))
                    strength_bar[2] = pygame.transform.scale(strength_bar[2], (screen_width/9, screen_height/12))
                    strength_bar.append(pygame.image.load("Image/UI/strength_bar_3.png"))
                    strength_bar[3] = pygame.transform.scale(strength_bar[3], (screen_width/9, screen_height/12))
                    strength_bar.append(pygame.image.load("Image/UI/strength_bar_4.png"))
                    strength_bar[4] = pygame.transform.scale(strength_bar[4], (screen_width/9, screen_height/12))

                    hint_backpack = pygame.image.load("Image/keys/keyboard_b.png")
                    hint_backpack = pygame.transform.scale(hint_backpack, (145,45))


                
                
                case -1:
                    Exit = [(2400,600),(200,-1800)]
                    if scene_ctrl.pre_game == 0:
                        (Main.x,Main.y) = Exit[scene_ctrl.From]
                        (Main.rect.x,Main.rect.y) = (Main.x+50,Main.y+50)   
                    if scene_ctrl.pre_game == -2:
                        (Main.x,Main.y) = Exit[scene_ctrl.From]
                        (Main.rect.x,Main.rect.y) = (Main.x+50,Main.y+50)    


                    scene = []
                    NT_object = []
                    CT_object = []
                    Enemy = []
                    ATKs_AL = []
                    ATKs_EN = []
                    strength_bar = []
                    BUTTON.empty()
                    
                    
                    scene_ctrl_temp = scene_ctrl.num                               #紀錄目前場景(用來使用back按鈕的)
                    
                    scene_ctrl.R_edge = 1800 - screen_width//2
                    scene_ctrl.L_edge = -1500 + screen_width//2
                    scene_ctrl.T_edge = -2200 + screen_height //2
                    scene_ctrl.B_edge = 1300


                    scene.append(pygame.image.load("Image/Background/background.png"))                                 #導入背景圖片
                    scene[0] = pygame.transform.scale(scene[0], (screen_width*5, screen_height*5))  # 調整大小
                    scene.append(pygame.image.load("Image/Background/white.jpg"))                                    #導入背景圖片
                    scene[1] = pygame.transform.scale(scene[1], (screen_width*5, screen_height*5))  # 調整大小
                    
                    NT_object.append(object_class.object(1200,800,tool.HRZ_combine("Image/Background/floor.png",20),"wall",0,0,0,0,0,0))
                    NT_object.append(object_class.object(600,-1800,tool.V_combine("Image/Background/floor.png",25),"wall",0,0,0,0,0,0))

                    NT_object.append(object_class.object(-40,400,tool.HRZ_combine("Image/Background/floor.png",5),"wall",0,0,0,0,0,0))
                    NT_object.append(object_class.object(-1200,0,tool.HRZ_combine("Image/Background/floor.png",10),"wall",0,0,0,0,0,0))
                    NT_object.append(object_class.object(-40,-400,tool.HRZ_combine("Image/Background/floor.png",5),"wall",0,0,0,0,0,0))
                    NT_object.append(object_class.object(-1200,-800,tool.HRZ_combine("Image/Background/floor.png",10),"wall",0,0,0,0,0,0))

                    NT_object.append(object_class.object(400,-1800,tool.HRZ_combine("Image/Background/floor.png",10),"wall",0,0,0,0,0,0))
                    NT_object.append(object_class.object(-1200,-1800,tool.HRZ_combine("Image/Background/floor.png",10),"wall",0,0,0,0,0,0))



                    NT_object.append(object_class.object(-1200,800,tool.HRZ_combine("Image/Background/floor.png",10),"wall",0,0,0,0,0,0))

                    door = pygame.image.load("Image/Object/door.png")
                    door = pygame.transform.scale(door, (200, 1200))  # 調整大小

                    save_point = pygame.image.load("Image/Object/save_point.png")
                    save_point = pygame.transform.scale(save_point, (400, 200))  # 調整大小

                    CT_object.append(object_class.object(2000,500,pygame.image.load("Image/Object/skill.png"),"skill",0,0,0,4,0,0))
                    CT_object.append(object_class.object(2600,400,door,"path",0,0,0,0,0,[0,1]))

                    door = pygame.transform.scale(door, (600, 200))  # 調整大小

                    CT_object.append(object_class.object(-200,-2000,door,"path",0,0,0,0,0,[-2,0]))

                    CT_object.append(object_class.object(2000,600,save_point,"save_point",0,0,0,0,0,0))
                    CT_object.append(object_class.object(2000,500,pygame.image.load("Image/Object/skill.png"),"skill",0,0,0,5,0,0))

                    strength_bar.append(pygame.image.load("Image/UI/strength_bar.png"))
                    strength_bar[0] = pygame.transform.scale(strength_bar[0], (screen_width/9, screen_height/12))
                    strength_bar.append(pygame.image.load("Image/UI/strength_bar_1.png"))
                    strength_bar[1] = pygame.transform.scale(strength_bar[1], (screen_width/9, screen_height/12))
                    strength_bar.append(pygame.image.load("Image/UI/strength_bar_2.png"))
                    strength_bar[2] = pygame.transform.scale(strength_bar[2], (screen_width/9, screen_height/12))
                    strength_bar.append(pygame.image.load("Image/UI/strength_bar_3.png"))
                    strength_bar[3] = pygame.transform.scale(strength_bar[3], (screen_width/9, screen_height/12))
                    strength_bar.append(pygame.image.load("Image/UI/strength_bar_4.png"))
                    strength_bar[4] = pygame.transform.scale(strength_bar[4], (screen_width/9, screen_height/12))                
                
                    hint_backpack = pygame.image.load("Image/keys/keyboard_b.png")
                    hint_backpack = pygame.transform.scale(hint_backpack, (145,45))
                
                
                
                case 0:
            
                    Exit = [(2400,600),(-600,700)]
                    if scene_ctrl.pre_game == 1:
                        (Main.x,Main.y) = Exit[scene_ctrl.From]
                        (Main.rect.x,Main.rect.y) = (Main.x+50,Main.y+50)    
                    if scene_ctrl.pre_game == -1:
                        (Main.x,Main.y) = Exit[scene_ctrl.From]
                        (Main.rect.x,Main.rect.y) = (Main.x+50,Main.y+50)  

                    scene = []
                    NT_object = []
                    CT_object = []
                    Enemy = []
                    ATKs_AL = []
                    ATKs_EN = []
                    strength_bar = []
                    BUTTON.empty()

                    scene_ctrl_temp = scene_ctrl.num                               #紀錄目前場景(用來使用back按鈕的)
                    
                    scene_ctrl.R_edge = 2150 - screen_width//2
                    scene_ctrl.L_edge = -1500 + screen_width//2
                    scene_ctrl.B_edge = 1500


                    scene.append(pygame.image.load("Image/Background/background.png"))                                 #導入背景圖片
                    scene[0] = pygame.transform.scale(scene[0], (screen_width*5, screen_height*5))  # 調整大小
                    scene.append(pygame.image.load("Image/Background/white.jpg"))                                    #導入背景圖片
                    scene[1] = pygame.transform.scale(scene[1], (screen_width*5, screen_height*5))  # 調整大小
                    
                    NT_object.append(object_class.object(1200,800,tool.HRZ_combine("Image/Background/floor.png",20),"wall",0,0,0,0,0,0))
                    NT_object.append(object_class.object(-800,400,tool.HRZ_combine("Image/Background/floor.png",20),"wall",0,0,0,1,0,0))
                    NT_object.append(object_class.object(-950,-1300,tool.V_combine("Image/Background/floor.png",15),"wall",0,0,0,0,0,0))

                    
                    NT_object.append(object_class.object(-1400,800,tool.HRZ_combine("Image/Background/floor.png",10),"wall",0,0,0,0,0,0))

                    door = pygame.image.load("Image/Object/door.png")
                    door = pygame.transform.scale(door, (200, 1200))  # 調整大小

                    save_point = pygame.image.load("Image/Object/save_point.png")
                    save_point = pygame.transform.scale(save_point, (400, 200))  # 調整大小


                    CT_object.append(object_class.object(-1000,600,door,"path",0,0,0,0,0,[-1,0]))
                    CT_object.append(object_class.object(3000,-300,door,"path",0,0,0,0,0,[1,0]))
                    CT_object.append(object_class.object(2000,600,save_point,"save_point",0,0,0,0,0,0))
                    CT_object.append(object_class.object(2000,500,pygame.image.load("Image/Object/skill.png"),"skill",0,0,0,5,0,0))

                    Enemy.append(player_class.enemy("The_First",1200,0,100,"roadside",None))

                    strength_bar.append(pygame.image.load("Image/UI/strength_bar.png"))
                    strength_bar[0] = pygame.transform.scale(strength_bar[0], (screen_width/9, screen_height/12))
                    strength_bar.append(pygame.image.load("Image/UI/strength_bar_1.png"))
                    strength_bar[1] = pygame.transform.scale(strength_bar[1], (screen_width/9, screen_height/12))
                    strength_bar.append(pygame.image.load("Image/UI/strength_bar_2.png"))
                    strength_bar[2] = pygame.transform.scale(strength_bar[2], (screen_width/9, screen_height/12))
                    strength_bar.append(pygame.image.load("Image/UI/strength_bar_3.png"))
                    strength_bar[3] = pygame.transform.scale(strength_bar[3], (screen_width/9, screen_height/12))
                    strength_bar.append(pygame.image.load("Image/UI/strength_bar_4.png"))
                    strength_bar[4] = pygame.transform.scale(strength_bar[4], (screen_width/9, screen_height/12))

                    hint_backpack = pygame.image.load("Image/keys/keyboard_b.png")
                    hint_backpack = pygame.transform.scale(hint_backpack, (145,45))

                case 1:

                    Exit = [(-400,-700),(2700,1200),(2700,-1100)]
                    if scene_ctrl.pre_game == 0:
                        (Main.x,Main.y) = Exit[scene_ctrl.From]
                        (Main.rect.x,Main.rect.y) = (Main.x+50,Main.y+50)
                        
                    if scene_ctrl.pre_game == 2:
                        (Main.x,Main.y) = Exit[scene_ctrl.From]
                        (Main.rect.x,Main.rect.y) = (Main.x+50,Main.y+50)

                    scene = []
                    NT_object = []
                    CT_object = []
                    Enemy = []
                    ATKs_AL = []
                    ATKs_EN = []
                    strength_bar = []
                    BUTTON.empty()

                    scene_ctrl_temp = scene_ctrl.num                               #紀錄目前場景(用來使用back按鈕的)
                    scene_ctrl.R_edge = 2000 - screen_width//2
                    scene_ctrl.L_edge = -1300 + screen_width//2
                    scene_ctrl.B_edge = 2000
                    scene_ctrl.T_edge = -1800 + screen_height//2


                    scene.append(pygame.image.load("Image/Background/background.png"))                                 #導入背景圖片
                    scene[0] = pygame.transform.scale(scene[0], (screen_width*7, screen_height*7))  # 調整大小
                    scene.append(pygame.image.load("Image/Background/white.jpg"))                                    #導入背景圖片
                    scene[1] = pygame.transform.scale(scene[1], (screen_width*5, screen_height*5))  # 調整大小
                    
                    
                    NT_object.append(object_class.object(-1000,-600,tool.HRZ_combine("Image/Background/floor.png",8),"wall",0,0,0,0,0,0))
                    NT_object.append(object_class.object(500,400,tool.V_combine("Image/Background/floor.png",8),"wall",0,0,0,0,0,0))
                    NT_object.append(object_class.object(1000,700,tool.V_combine("Image/Background/floor.png",8),"wall",0,0,0,0,0,0))
                    NT_object.append(object_class.object(1500,1100,tool.V_combine("Image/Background/floor.png",12),"wall",0,0,0,0,0,0))
                    NT_object.append(object_class.object(1800,-1000,tool.HRZ_combine("Image/Background/floor.png",10),"wall",0,0,0,0,0,0))
                    NT_object.append(object_class.object(1800,1300,tool.HRZ_combine("Image/Background/floor.png",10),"wall",0,0,0,0,0,0))


                    door = pygame.image.load("Image/Object/door.png")
                    door = pygame.transform.scale(door, (200, 1200))  # 調整大小

                    save_point = pygame.image.load("Image/Object/save_point.png")
                    save_point = pygame.transform.scale(save_point, (400, 200))  # 調整大小


                    CT_object.append(object_class.object(3000,300,door,"path",0,0,0,0,0,[2,0]))
                    CT_object.append(object_class.object(-800,-900,door,"path",0,0,0,0,0,[0,0]))
                    CT_object.append(object_class.object(2000,1000,save_point,"save_point",0,0,0,0,0,0))
                    CT_object.append(object_class.object(1800,1700,pygame.image.load("Image/Object/skill.png"),"skill",0,0,0,6,0,0))

                    
                    strength_bar.append(pygame.image.load("Image/UI/strength_bar.png"))
                    strength_bar[0] = pygame.transform.scale(strength_bar[0], (screen_width/9, screen_height/12))
                    strength_bar.append(pygame.image.load("Image/UI/strength_bar_1.png"))
                    strength_bar[1] = pygame.transform.scale(strength_bar[1], (screen_width/9, screen_height/12))
                    strength_bar.append(pygame.image.load("Image/UI/strength_bar_2.png"))
                    strength_bar[2] = pygame.transform.scale(strength_bar[2], (screen_width/9, screen_height/12))
                    strength_bar.append(pygame.image.load("Image/UI/strength_bar_3.png"))
                    strength_bar[3] = pygame.transform.scale(strength_bar[3], (screen_width/9, screen_height/12))
                    strength_bar.append(pygame.image.load("Image/UI/strength_bar_4.png"))
                    strength_bar[4] = pygame.transform.scale(strength_bar[4], (screen_width/9, screen_height/12))

                    hint_backpack = pygame.image.load("Image/keys/keyboard_b.png")
                    hint_backpack = pygame.transform.scale(hint_backpack, (145,45))



                case 2:
                    Exit = [(-400,700),(2600,600)]
                    if scene_ctrl.pre_game == 1:
                        (Main.x,Main.y) = Exit[scene_ctrl.From]
                        (Main.rect.x,Main.rect.y) = (Main.x+50,Main.y+50)
                        
                    scene_ctrl_temp = scene_ctrl.num                               #紀錄目前場景(用來使用back按鈕的)
                    scene_ctrl.R_edge = 2000 - screen_width//2
                    scene_ctrl.L_edge = -1300 + screen_width//2
                    scene_ctrl.B_edge = 2000


                    scene = []
                    NT_object = []
                    CT_object = []
                    Enemy = []
                    ATKs_AL = []
                    ATKs_EN = []
                    strength_bar = []
                    BUTTON.empty()


                    scene.append(pygame.image.load("Image/Background/background.png"))                                 #導入背景圖片
                    scene[0] = pygame.transform.scale(scene[0], (screen_width*7, screen_height*7))  # 調整大小
                    scene.append(pygame.image.load("Image/Background/white.jpg"))                                    #導入背景圖片
                    scene[1] = pygame.transform.scale(scene[1], (screen_width*5, screen_height*5))  # 調整大小
                    
                    
                    NT_object.append(object_class.object(-1000,800,tool.HRZ_combine("Image/Background/floor.png",8),"wall",0,0,0,0,0,0))
                    
                    NT_object.append(object_class.object(500,-400,tool.V_combine("Image/Background/floor.png",15),"wall",0,0,0,0,0,0))
                    NT_object.append(object_class.object(-1000,-400,tool.HRZ_combine("Image/Background/floor.png",8),"wall",0,0,0,0,0,0))


                    
                    NT_object.append(object_class.object(1800,1300,tool.HRZ_combine("Image/Background/floor.png",10),"wall",0,0,0,0,0,0))


                    door = pygame.image.load("Image/Object/door.png")
                    door = pygame.transform.scale(door, (200, 1200))  # 調整大小

                    save_point = pygame.image.load("Image/Object/save_point.png")
                    save_point = pygame.transform.scale(save_point, (400, 200))  # 調整大小


                    CT_object.append(object_class.object(-800,-200,door,"path",0,0,0,0,0,[1,1]))

                    CT_object.append(object_class.object(-800,-1200,door,"path",0,0,0,0,0,[1,2]))
                    CT_object.append(object_class.object(2000,1000,save_point,"save_point",0,0,0,0,0,0))
                    
                    CT_object.append(object_class.object(1800,1700,pygame.image.load("Image/Object/skill.png"),"skill",0,0,0,6,0,0))

                    
                    strength_bar.append(pygame.image.load("Image/UI/strength_bar.png"))
                    strength_bar[0] = pygame.transform.scale(strength_bar[0], (screen_width/9, screen_height/12))
                    strength_bar.append(pygame.image.load("Image/UI/strength_bar_1.png"))
                    strength_bar[1] = pygame.transform.scale(strength_bar[1], (screen_width/9, screen_height/12))
                    strength_bar.append(pygame.image.load("Image/UI/strength_bar_2.png"))
                    strength_bar[2] = pygame.transform.scale(strength_bar[2], (screen_width/9, screen_height/12))
                    strength_bar.append(pygame.image.load("Image/UI/strength_bar_3.png"))
                    strength_bar[3] = pygame.transform.scale(strength_bar[3], (screen_width/9, screen_height/12))
                    strength_bar.append(pygame.image.load("Image/UI/strength_bar_4.png"))
                    strength_bar[4] = pygame.transform.scale(strength_bar[4], (screen_width/9, screen_height/12))

                    hint_backpack = pygame.image.load("Image/keys/keyboard_b.png")
                    hint_backpack = pygame.transform.scale(hint_backpack, (145,45))



                case "dead":                                                #死亡緩衝區
                    Main.HP=Main.Max_HP
                    Main.death_cd = 0
                    Load(1)
                    scene_ctrl.init = 1

#=========================================================================================================
                                                                            #轉場區(前半)
            if scene_ctrl.init == 0 :
                scene_ctrl.trans = 60
                trans.x = -1*screen_width
                trans.rect.x = -1*screen_width
                for i in range(30):
                    trans.x+=screen_width//30
                    trans.rect.x+=screen_width//30
                    scene_ctrl.trans -= 1
                    screen.blit(trans.surface, (trans.x, trans.y))
                    pygame.display.update()


            scene_ctrl.pre_game = scene_ctrl.game
#==========================================================================================================
            while scene_ctrl.num == 10 and scene_ctrl.game == scene_ctrl.pre_game :                                                     #遊戲主迴圈
                
     
                
                match scene_ctrl.game:
                    case -2:
                        if Main.rect.x >= 600 and scene_ctrl.done == 0:                     
                            NT_object.append(object_class.object(400,-1500,tool.V_combine("Image/Background/floor.png",20),"wall",0,0,0,0,0,0))
                            scene_ctrl.done = 1
                            
                    case -3:
                        if Main.rect.x <= 0 and scene_ctrl.done == 0:
                            for obj in NT_object:
                                if obj.type == "fake_wall":
                                    if tool.Touch(Main,obj):
                                        NT_object.remove(obj)
                                        del obj                     

     
     
     
     
                if scene_ctrl.init == 1:                                    #重返初始化(死亡回歸)
                    scene_ctrl.init = 0
                    break


                clock.tick(scene_ctrl.fps)                                  #控制每秒最多執行 FPS 次(固定每台電腦的執行速度)
                #print(clock.get_fps())

                if not get_current_input_lang() == 0x0409:
                    force_english_input()

            
                if Main.is_hurt > 20:
                    Main.is_hurt -= 1
                    continue



                keys = pygame.key.get_pressed()                             #偵測按鍵(把偵測按鍵拉出event.get()迴圈外，規避windows的按鍵延遲)

                                
                tool.tick_mission(screen, scene, Main, Enemy, ATKs_AL, ATKs_EN, NT_object, CT_object, keys, pre_keys, strength_bar, hint_backpack, trans, scene_ctrl)
                

                if keys[pygame.K_b] and not pre_keys[pygame.K_b]:

                    scene_ctrl.backpack = 1

                    while scene_ctrl.backpack > 0:

                        match   scene_ctrl.backpack:
                            
                            case 1:

                                BUTTON.empty()

                                while scene_ctrl.backpack == 1:

                                    if scene_ctrl.button_cd > 0:
                                        scene_ctrl.button_cd-=1

                                    if keys[pygame.K_b] and not pre_keys[pygame.K_b]:

                                        scene_ctrl.backpack = 0

                                    for event in pygame.event.get():                               #偵測事件
                                        if event.type == pygame.QUIT:
                                            pygame.quit()
                                            exit()

                if keys[pygame.K_b] and not pre_keys[pygame.K_b]:                                         

                    scene_ctrl.backpack = 1

                    while scene_ctrl.backpack > 0:

                        match scene_ctrl.backpack > 0:

                            case 1:       #背包

                                BUTTON.empty()

                                screen.blit(scene[2], (0,0))

                                

                if keys[pygame.K_ESCAPE] and not pre_keys[pygame.K_ESCAPE]:                               #按ESC後暫停

                    scene_ctrl.menu = 1
                    
                    while scene_ctrl.menu > 0:

                        match scene_ctrl.menu:

                            case 1:                            #暫停主介面

                                BUTTON.empty()

                                button_resume = button.Button(screen_width//2, screen_height//4, "Resume", lambda:button.resuming(scene_ctrl,0))
                                button_menu = button.Button(screen_width//2, screen_height//4*2, "Menu", lambda:button.resuming(scene_ctrl,2))
                                button_quit = button.Button(screen_width//2, screen_height//4*3, "Home", lambda:button.go_home(scene_ctrl))

                                BUTTON.add(button_resume, button_menu, button_quit)

                                while scene_ctrl.menu == 1 :

                                    pre_keys = keys
                                    keys = pygame.key.get_pressed()                             #偵測按鍵(把偵測按鍵拉出event.get()迴圈外，規避windows的按鍵延遲)


                                    screen.blit(scene[1], (0,0))                  #繪製背景圖片

                                    if scene_ctrl.button_cd > 0:
                                        scene_ctrl.button_cd-=1

                                    BUTTON.update(scene_ctrl)
                                    BUTTON.draw(screen)
                                    pygame.display.flip()
                                    
                                    if keys[pygame.K_ESCAPE] and not pre_keys[pygame.K_ESCAPE]:                               #按ESC後暫停
                                        scene_ctrl.menu = 0

                                    for event in pygame.event.get():                               #偵測事件
                                        if event.type == pygame.QUIT:
                                            pygame.quit()
                                            exit()



                            case 2:                      #暫停後的選單

                                BUTTON.empty()

                                button1 = button.Button(screen_width//2, screen_height//4, "Audio", lambda:button.resuming(scene_ctrl,3))
                                button2 = button.Button(screen_width//2, screen_height//4*2, "Video", lambda:button.resuming(scene_ctrl,4))  
                                button_back = button.Button(screen_width//2, screen_height//4*3, "Go back", lambda:button.resuming(scene_ctrl,1))

                                BUTTON.add(button1, button2, button_back)

                                while scene_ctrl.menu == 2:
                                    pre_keys = keys
                                    keys = pygame.key.get_pressed()                             #偵測按鍵(把偵測按鍵拉出event.get()迴圈外，規避windows的按鍵延遲)
                    
                                    screen.blit(scene[1], (0,0))                  #繪製背景圖片

                                    if scene_ctrl.button_cd > 0:
                                        scene_ctrl.button_cd-=1

                                    BUTTON.update(scene_ctrl)
                                    BUTTON.draw(screen)
                                    pygame.display.flip()
                                    
                                    if keys[pygame.K_ESCAPE] and not pre_keys[pygame.K_ESCAPE]:                               #按ESC後暫停
                                        scene_ctrl.menu = 1


                                    for event in pygame.event.get():                               #偵測事件
                                        if event.type == pygame.QUIT:
                                            pygame.quit()
                                            exit()

                            case 3:

                                BUTTON.empty()

                                while scene_ctrl.menu == 3:                                      #音訊調整
                                    
                                    pre_keys = keys
                                    keys = pygame.key.get_pressed()                             #偵測按鍵(把偵測按鍵拉出event.get()迴圈外，規避windows的按鍵延遲)

                                    pass
                                    
                                    if keys[pygame.K_ESCAPE] and not pre_keys[pygame.K_ESCAPE]:                               #按ESC後暫停
                                        scene_ctrl.menu = 2
                                        scene_ctrl.button_cd = 150


                                    for event in pygame.event.get():                               #偵測事件
                                        if event.type == pygame.QUIT:
                                            pygame.quit()
                                            exit()

                            case 4:                                           
                                            
                                BUTTON.empty()

                                button_back = button.Button(screen_width//2, screen_height//3*2, "Go back", lambda:button.resuming(scene_ctrl, 2))
                                BUTTON.add(button_back)
                                        
                                while scene_ctrl.menu == 4 :                                 #影像調整
                        
                                    pre_keys = keys
                                    keys = pygame.key.get_pressed()                             #偵測按鍵(把偵測按鍵拉出event.get()迴圈外，規避windows的按鍵延遲)

                                    screen.blit(scene[1], (0,0))                  #繪製背景圖片

                                    if scene_ctrl.button_cd > 0:
                                        scene_ctrl.button_cd-=1
                                            
                                    BUTTON.update(scene_ctrl)
                                    BUTTON.draw(screen)
                                    pygame.display.flip()
                                    
                                    if keys[pygame.K_ESCAPE] and not pre_keys[pygame.K_ESCAPE]:                               #按ESC後暫停
                                        scene_ctrl.menu = 2
                                        scene_ctrl.button_cd = 150


                                    for event in pygame.event.get():                               #偵測事件
                                        if event.type == pygame.QUIT:
                                            pygame.quit()
                                            exit()
                pre_keys = keys

#=======================================================================================================