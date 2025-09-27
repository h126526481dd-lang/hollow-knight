import random
import os
import pygame
import player_class
import object_class
import math



def show(scene,object,player):                          #繪製畫面(待修，以後應該是以場景為單位來繪製，要新增場景的class，裡面包含現在要輸入的東西)

    adjust_y = screen_height//2                                 #螢幕中心座標
    adjust_x = screen_width//2
    camera_x = player.x - adjust_x                              #把角色置中所需要的向量  
    camera_y = player.y - adjust_y

    screen.blit(scene, (-500-camera_x, -500-camera_y))                  #繪製背景圖片(背景位置=原位置-置中向量)
   
    for i in range(NT_object_num):                                 #繪製物件    (物件位置=原位置-置中向量)
        screen.blit(NT_object[i].surface, (NT_object[i].x-camera_x, NT_object[i].y-camera_y))

    for i in range(CT_object_num):                                 #繪製物件    (物件位置=原位置-置中向量)
        screen.blit(CT_object[i].surface, (CT_object[i].x-camera_x, CT_object[i].y-camera_y))
   
    screen.blit(player.surface, ( player.x-camera_x,player.y-camera_y))#繪製角色    (角色位置=原位置-置中向量=螢幕中心)

    pygame.display.update()



#=======================================================================================================



pygame.init()                                                   #初始化
Info = pygame.display.Info()                                      #偵測用戶顯示參數
screen_height = Info.current_h                                  #設定畫面大小成用戶螢幕大小
screen_width  = Info.current_w
NT_object_num = 0
CT_object_num = 0
object_num = NT_object_num + CT_object_num
player_num = 1
scene = []
NT_object = []
CT_object = []
object = NT_object + CT_object

scene.append(pygame.image.load("IMG_2794.jpg"))                  #導入背景圖片
scene[0] = pygame.transform.scale(scene[0], (screen_width*5, screen_height*5))  # 調整大小

screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME)

#導入背景，無邊框，螢幕大小

clock = pygame.time.Clock()                                     #建立時鐘物件(用來處理tick)
FPS = 60                                                        #設定每秒幀數

Main = player_class.player("BOBO",0,0)                #建立角色物件

for i in range(10):                                                                                          #建立物件(地板)
    NT_object.append(object_class.object(-50+120*i,500,pygame.image.load("floor2.png"),0))
    NT_object_num += 1
NT_object.append(object_class.object(300,300,pygame.image.load("floor.png"),0))
NT_object_num += 1


print(pygame.display.get_active())                              #確認是否正確開啟


#=======================================================================================================


attacking = False
while True:                                                     #遊戲主迴圈
   
    clock.tick(FPS)                                             #控制每秒最多執行 FPS 次(固定每台電腦的執行速度)

    Main.now_Touch = []                                      #角色目前碰撞清單
    keys = pygame.key.get_pressed()                             #偵測按鍵(把偵測按鍵拉出event.get()迴圈外，規避windows的按鍵延遲)

    if keys[pygame.K_d] and keys[pygame.K_a]:                #避免同時按兩個方向鍵
           
        pass
       
    else:
        if not attacking:
            if keys[pygame.K_d]:                                #按下d鍵右移
                Main.R_move()

            elif keys[pygame.K_a]:                              #按下a鍵左移
                Main.L_move()

            elif keys[pygame.K_j]:                              #按下j鍵攻擊
                Main.attack()

            else:                                                   #不移動時水平速度歸零(沒有慣性)
                Main.idle()
                Main.vx = 0
 


    for i in range(NT_object_num):                                 #偵測角色和不可穿越物件的碰撞
        player_class.Touch(Main,NT_object[i])
                                  


    if not "1_D" in Main.now_Touch :                                           #若沒有站地上，則設為False
        Main.on_ground = False

    if Main.on_ground == False and Main.vy <= 30:           #重力加速度(有設上限)
        Main.vy += 1
   
    elif Main.on_ground == True:                            #觸地垂直速度歸零
        Main.vy = 0



    if keys[pygame.K_SPACE] and not "1_U" in Main.now_Touch:                                #按下空白鍵跳躍
        Main.jump()

    Main.y += Main.vy                                       #更新角色位置
    Main.x += Main.vx

    for event in pygame.event.get():                               #偵測事件
       
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    if Main.y>1800:
        Main.y=0
    
    show(scene[0],object,Main)
