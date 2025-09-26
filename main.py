import random
import os
import pygame
import player_class
import object_class
import math



def Touch(object1,object2):   #物件和物件  或  物件和玩家 的碰撞偵測

    offset = (object2.x - object1.x, object2.y - object1.y)                             #計算兩個物件的相對位置
    T_status = []

    if object1.mask.overlap(object2.mask,offset):                                                 #偵測"當把mask2放在offset的位置時有無覆蓋
        if not object1.mask.overlap(object2.mask,    (object2.x - object1.x, (object2.y + max(abs(object1.vy),50    )) - object1.y) ) :    #若當前有碰撞，則偵測往上調整後是否還有碰撞  
            T_status.append ("1_D")                                                                                                    #若往上調沒碰撞，表示物件1的底部碰撞到了物件2(D=Down)，新增標籤到碰撞清單
            f_NT_Test.append("1_D")
            for i in range(max(abs(object1.vy),50)):                                                                                   #把物件1往上調整，直到不碰撞為止
                object1.y -= 1                                                                                                         
                offset = (object2.x - object1.x, object2.y - object1.y)                                                               #重新計算兩個物件的相對位置
                if not object1.mask.overlap(object2.mask,offset):                                                                     #若不再碰撞，跳出迴圈
                    object1.y += 1
                    break
        #這行待修，很容易扎土豆

        if not object1.mask.overlap(object2.mask,    (object2.x - object1.x, (object2.y - max(abs(object1.vy),31)) - object1.y) ) :     #同理
            T_status.append ("1_U")
            f_NT_Test.append("1_U")

        if not object1.mask.overlap(object2.mask,    ((object2.x+abs(object1.vx)
                                                       ) - object1.x, object2.y - object1.y) ) :               #同理
            T_status.append ("1_R") 
            f_NT_Test.append("1_R")

        if not object1.mask.overlap(object2.mask,    ((object2.x-abs(object1.vx)) - object1.x, object2.y - object1.y) ) :               #同理
            T_status.append ("1_L")
            f_NT_Test.append("1_L")                
    return T_status                                                                                                                     #迴船碰撞清單



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

for i in range(5):                                                                                          #建立物件(地板)
    NT_object.append(object_class.object(-50+120*i,500,pygame.image.load("floor.png"),0))
    NT_object_num += 1

print(pygame.display.get_active())                              #確認是否正確開啟

while True:                                                     #遊戲主迴圈
   
    clock.tick(FPS)                                             #控制每秒最多執行 FPS 次(固定每台電腦的執行速度)


    keys = pygame.key.get_pressed()                             #偵測按鍵(把偵測按鍵拉出event.get()迴圈外，規避windows的按鍵延遲)
   
    for i in range(1):                                          #避免同時按兩個方向鍵
        if keys[pygame.K_d] and keys[pygame.K_a]:
           
            continue
       
        else:
       
            if keys[pygame.K_d]:                                #按下d鍵右移
                Main.R_move()

            elif keys[pygame.K_a]:                              #按下a鍵左移
                Main.L_move()

            else:                                                   #不移動時水平速度歸零(沒有慣性)
                Main.idle()
                Main.vx = 0



    NT_Test = []                                             #不可穿越物件 碰撞總清單
    f_NT_Test=[]
    up=0

    for i in range(NT_object_num):                                 #偵測角色和不可穿越物件的碰撞
        NT_Test.append(Touch(Main,NT_object[i]))


    if f_NT_Test.count("1_D") > 0 :                                           #角色跟不可穿越物件的下碰撞偵測(檢測是否站地上)
        Main.on_ground = True

            
    else:
        Main.on_ground = False



    if Main.on_ground == False and Main.vy <= 30:           #重力加速度(有設上限)
        Main.vy += 1
   
    elif Main.on_ground == True:                            #觸地垂直速度歸零
        Main.vy = 0



    if keys[pygame.K_SPACE]:                                #按下空白鍵跳躍
        Main.jump()



    if f_NT_Test.count("1_L") >0 and Main.vx<0:               #角色跟不可穿越物件 的左碰撞(左阻擋)偵測
        Main.vx *= 0
    elif f_NT_Test.count("1_R") >0 and Main.vx>0:             #角色跟不可穿越物件 的右碰撞(右阻擋)偵測
        Main.vx *= 0

    print(f_NT_Test)                                          #印出不可穿越物件的碰撞總清單(除錯用)

    Main.y += Main.vy                                       #更新角色位置
    Main.x += Main.vx

    for event in pygame.event.get():                               #偵測事件
       
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    if Main.y>1800:
        Main.y=0
    
    show(scene[0],object,Main)
