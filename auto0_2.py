# -*-coding:utf-8-*-
from PIL import ImageGrab
from PIL import Image
import time
import os
from functools import reduce
import operator
import math

import win32api
import win32gui
import win32con

# 比较两图片相似度，算法较为简单
def compare_image(img1,img2):
    h1 = img1.histogram()
    h2 = img2.histogram()
    result = math.sqrt(reduce(operator.add,list(map(lambda a,b:(a-b)**2,h1,h2)))/len(h1))

    if result < 50.00:
        return True
    else:
        return False


#获取截图
def get_image(box):
    left,top,right,bottom = get_window()
    width = right - left
    height = bottom - top

    newleft = left + width * box[0]
    newtop = top + height * box[1]
    newright = left + width * box[2]
    newbottom = top + height * box[3]
    img = ImageGrab.grab((newleft,newtop,newright,newbottom))

    return img

#获取模拟器窗口四个边角的位置，理论上可以通过改titlename来选择别的模拟器
def get_window():
    titlename = "少女前线 - MuMu模拟器"
    hwnd = win32gui.FindWindow(None,titlename)
    if hwnd !=0:
        return win32gui.GetWindowRect(hwnd)
    else:
        exit(0)
'''
def set_window_top():
    titlename = "NemuPlayer"
    hwnd = win32gui.FindWindow(None,titlename)
    if hwnd == 0:
        exit(-1)
    win32gui.SetWindowPos(hwnd,win32con.HWND_TOPMOST,get_window()[0],get_window()[1],
                          get_window()[2]-get_window()[0],get_window()[3]-get_window()[1],win32con.SWP_SHOWWINDOW)
'''
def mouse_click(pos):
    left,top,right,bottom = get_window()
    width = right - left
    height = bottom - top

    newpos = ((int)(left+width*pos[0]),(int)(top+height*pos[1]))

    win32api.SetCursorPos(newpos)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0,0,0)
    time.sleep(3)

def mouse_pos_set(pos):
    left, top, right, bottom = get_window()
    width = right - left
    height = bottom - top

    newpos = ((int)(left + width * pos[0]), (int)(top + height * pos[1]))

    win32api.SetCursorPos(newpos)

def mouse_pos_init():
    win32api.SetCursorPos((get_window()[0],get_window()[1]))
    time.sleep(1)

SCALING_SCROLL_POINT = (0.75, 0.75)
def scroll_map():
    left,top,right,bottom = get_window()
    width = right-left
    height = bottom-top

    SCROLL_POINT_X = (int)(SCALING_SCROLL_POINT[0] * width + left)
    SCROLL_POINT_Y = (int)(SCALING_SCROLL_POINT[1] * height + top)

    win32api.SetCursorPos((SCROLL_POINT_X,SCROLL_POINT_Y))
    for i in range(0,8):
        win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL,0,0,1)
        time.sleep(1)

def scaling_map():
    left, top, right, bottom = get_window()
    width = right - left
    height = bottom - top

    SCALING_POINT_X = (int)(SCALING_SCROLL_POINT[0] * width + left)
    SCALING_POINT_Y = (int)(SCALING_SCROLL_POINT[1] * height + top)
    win32api.SetCursorPos((SCALING_POINT_X,SCALING_POINT_Y))
    
    win32api.keybd_event(17,0,0,0)
    i = 0
    while i<8:
        win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, -1)
        time.sleep(1)
        i = i + 1

    win32api.keybd_event(0x11,0,win32con.KEYEVENTF_KEYUP,0)

INITDIR = 'init'
COMPAREDIR = 'comparedir'
imageList = list()
def initImageList():
    if os.path.exists(INITDIR):
        for root,dirs,files in os.walk(INITDIR):
            for file in files:
                imageList.append(file)
    else:
        os.mkdir(INITDIR)

def isPage(PAGE,PAGE_SIZE):
    if PAGE not in imageList:
        img = get_image(PAGE_SIZE)
        img.save(INITDIR+'\\'+PAGE)
        imageList.append(PAGE)
    img1 = Image.open(INITDIR+"\\"+PAGE)
    img2 = get_image(PAGE_SIZE)
    return compare_image(img1,img2)

PING = 3

MAIN_MENU = "main_menu.png"
MAIN_MENU_SIZE = (0.65,0.5,1,0.8)

COMBAT_BUTTON = (0.75,0.65)
COMBAT_MENU = "combat_menu.png"
COMBAT_MENU_SIZE = (0,0.06,0.4,0.16)
COMBAT_MISSION_BUTTON = (0.05,0.22)
RETURN_TO_BASE_BUTTON = (0.05,0.1)
COMBAT_MISSION_0 = (0.2,0.22)
COMBAT_MISSION_0_2 = (0.5,0.55)
COMBAT_MISSION_START = (0.6,0.8)

def main_menu_to_combat():
    mouse_click(COMBAT_BUTTON)
    time.sleep(PING)
    i = 0
    while not isPage(COMBAT_MENU, COMBAT_MENU_SIZE):
        time.sleep(2)
        i = i + 1
        if i >=20:
            exit(-1)

    mouse_click(COMBAT_MISSION_BUTTON)

    mouse_click(COMBAT_MISSION_0)

    mouse_click(COMBAT_MISSION_0_2)

    mouse_click(COMBAT_MISSION_START)

    time.sleep(PING)

COMBAT_FIELD = "combat_feild.png"
COMBAT_FIELD_SIZE = (0,0.06,0.4,0.16)
SET_BUTTON = (0.9,0.9)
POINT_M16A1 = (0.3,0.5)
REPAIR_COMFIRM = (0.7,0.7)
START_BUTTON = (0.8,0.9)

POINT_HQ = (0.5,0.5)
POINT_AP = (0.2,0.5)

def set_echelon(is_first,main_echelon,need_repair):
    time.sleep(PING)
    i = 0
    while not isPage(COMBAT_FIELD,COMBAT_FIELD_SIZE):
        time.sleep(2)
        i = i + 1
        if i >= 20:
            exit(-1)
    if is_first:
        scaling_map()
    if main_echelon ==1:
        mouse_click(POINT_HQ)
        if need_repair==True:
            mouse_click(POINT_M16A1)
            mouse_click(REPAIR_COMFIRM)
        mouse_click(SET_BUTTON)
        mouse_click(POINT_AP)
        mouse_click(SET_BUTTON)
    else:
        mouse_click(POINT_AP)
        mouse_click(SET_BUTTON)
        mouse_click(POINT_HQ)
        if need_repair==True:
            mouse_click(POINT_M16A1)
            mouse_click(REPAIR_COMFIRM)
        mouse_click(SET_BUTTON)
    mouse_click(START_BUTTON)

SUPPLY_BUTTON = (0.9,0.76)

def supply_airport():
    mouse_click(POINT_AP)
    mouse_click(POINT_AP)
    mouse_click(SUPPLY_BUTTON)


LEFT_POINT_4 = "LEFT_POINT_4.png"
LEFT_POINT_4_SIZE = (0.75, 0.8, 0.85, 0.92)
LEFT_POINT_0 = "LFET_POINT_0.png"
LEFT_POINT_0_SIZE = (0.75, 0.8, 0.85, 0.92)
LEFT_POINT_3 = "LFET_POINT_3.png"
LEFT_POINT_3_SIZE = (0.75, 0.8, 0.85, 0.92)
LEFT_POINT_1 = "LFET_POINT_1.png"
LEFT_POINT_1_SIZE = (0.75, 0.8, 0.85, 0.92)
PLAN_BUTTON = (0.05,0.82)

POINT_STEP_1 = (0.39,0.35)
POINT_STEP_2 = (0.42,0.77)
POINT_STEP_3 = (0.52,0.48)
POINT_STEP_4 = (0.41,0.34)
POINT_STEP_5 = (0.62,0.34)
POINT_STEP_6 = (0.78,0.40)
START_PLAN_BUTTON = (0.9,0.9)
END_TURN_BUTTON = (0.9,0.9)
def plan_turn_1():
    waiting_time = 120
    time.sleep(PING)
    i = 0
    while not isPage(LEFT_POINT_4, LEFT_POINT_4_SIZE):
        time.sleep(3)
        i = i + 1
        if i >= 20:
            exit(-1)

    mouse_click(PLAN_BUTTON)
    mouse_click(POINT_HQ)
    mouse_click(POINT_STEP_1)
    scroll_map()
    mouse_click(POINT_STEP_2)
    mouse_click(POINT_STEP_3)
    mouse_click(POINT_STEP_4)
    mouse_click(START_PLAN_BUTTON)
    time.sleep(waiting_time)
    i = 0
    while not isPage(LEFT_POINT_0, LEFT_POINT_0_SIZE):
        time.sleep(1)
        i = i + 1
        if i >= 20:
            exit(-1)
    mouse_click(END_TURN_BUTTON)
    time.sleep(10)
    return

def plan_turn_2():
    waiting_time = 90
    time.sleep(PING)
    i = 0
    while not isPage(LEFT_POINT_3, LEFT_POINT_3_SIZE):
        time.sleep(3)
        i = i + 1
        if i >= 20:
            exit(-1)
    mouse_click(PLAN_BUTTON)
    mouse_click(POINT_STEP_4)
    mouse_click(POINT_STEP_5)
    mouse_click(POINT_STEP_6)
    mouse_click(START_PLAN_BUTTON)
    time.sleep(waiting_time)
    while not isPage(LEFT_POINT_1, LEFT_POINT_1_SIZE):
        time.sleep(1)
        i = i + 1
        if i >= 20:
            exit(-1)
    mouse_click(END_TURN_BUTTON)
    time.sleep(10)
    mouse_click(END_TURN_BUTTON)
    time.sleep(5)
    mouse_click(END_TURN_BUTTON)
    time.sleep(5)
    mouse_click(END_TURN_BUTTON)
    time.sleep(5)
    mouse_click(RETURN_TO_BASE_BUTTON)

FORMATION_MENU = "formation_menu.png"
FORMATION_MENU_SIZE = COMBAT_MENU_SIZE

FORMATION_BUTTON = (0.95,0.65)
ECHELON1_BUTTON = (0.05,0.2)
ECHELON2_BUTTON = (0.05,0.35)
FORMATION_PRESET_BUTTON = (0.95,0.85)
PRESET_BUTTON = (0.98,0.4)
PRESET_ECHELON1_BUTTON = (0.8,0.15)
PRESET_ECHELON2_BUTTON = (0.8,0.30)
PRESET_MENU = "preset_menu.png"
PRESET_MENU_SIZE = (0.5,0.75,1,0.9)

USE_PRESET_BUTTON = (0.9,0.8)
COMFIRM_BUTTON = (0.95,0.8)

FORCE_REPLACE_BUTTON = (0.45,0.55)
FORCE_REPLACE = "force_replace.png"
FORCE_REPLACE_SIZE = (0.42,0.5,0.57,0.6)
FORCE_REPLACE_COMFIRM = (0.6,0.65)
def change_echelon(main_echelon):
    time.sleep(PING)
    i = 0
    while not isPage(MAIN_MENU,MAIN_MENU_SIZE):
        time.sleep(2)
        i = i+1
        if i>=20:
            exit(-1)
    mouse_click(FORMATION_BUTTON)
    time.sleep(PING)
    i = 0
    while not isPage(FORMATION_MENU,FORMATION_MENU_SIZE):
        time.sleep(2)
        i = i+1
        if i>=20:
            exit(-1)
    if main_echelon==1:
        mouse_click(ECHELON2_BUTTON)
    mouse_click(FORMATION_PRESET_BUTTON)
    mouse_click(PRESET_BUTTON)

    if main_echelon==2:
        mouse_click(PRESET_ECHELON1_BUTTON)
    else:
        mouse_click(PRESET_ECHELON2_BUTTON)

    i = 0
    while not isPage(PRESET_MENU,PRESET_MENU_SIZE):
        time.sleep(2)
        i = i+1
        if i>=20:
            exit(-1)

    mouse_click(USE_PRESET_BUTTON)

    if not isPage(FORCE_REPLACE,FORCE_REPLACE_SIZE):
        mouse_click(FORCE_REPLACE_BUTTON)
    mouse_click(FORCE_REPLACE_COMFIRM)

    mouse_click(COMFIRM_BUTTON)

    mouse_click(RETURN_TO_BASE_BUTTON)
    return

FACTORY_BUTTON = (0.95,0.45)
FACTORY_MENU = "factory_menu.png"
FACTORY_MENU_SIZE = COMBAT_MENU_SIZE

RETIRE_BUTTON = (0.05,0.6)
CHOOSE_DOLL_BUTTON = (0.3,0.3)
AUTO_SELECT_BUTTON = (0.95,0.8)
RETIRE_T_DOLL_TIME = 5
def t_doll_retire(time_count):
    if time_count==0 or time_count%RETIRE_T_DOLL_TIME!=0:
        return
    mouse_click(FACTORY_BUTTON)
    time.sleep(5)
    i=0
    while not isPage(FACTORY_MENU,FACTORY_MENU_SIZE):
        time.sleep(2)
        i = i+1
        if i>=20:
            exit(-1)
    mouse_click(RETIRE_BUTTON)

    mouse_click(CHOOSE_DOLL_BUTTON)
    time.sleep(5)
    mouse_click(AUTO_SELECT_BUTTON)
    time.sleep(2)
    mouse_click(AUTO_SELECT_BUTTON)
    i = 0
    while not isPage(FACTORY_MENU, FACTORY_MENU_SIZE):
        time.sleep(2)
        i = i + 1
        if i >= 20:
            exit(-1)
    mouse_click(AUTO_SELECT_BUTTON)

    mouse_click(RETURN_TO_BASE_BUTTON)


if __name__=='__main__':
    time.sleep(5)
    main_echelon = 1
    time_count = 0
    is_first = True
    initImageList()
    while True:
        mouse_pos_init()
        if not isPage(MAIN_MENU,MAIN_MENU_SIZE):
            exit(-2)
        main_menu_to_combat()
        if time_count!=0 and time_count%3==0:
            set_echelon(is_first,main_echelon,True)
        else:
            set_echelon(is_first,main_echelon,False)
        supply_airport()
        plan_turn_1()
        plan_turn_2()
        change_echelon(main_echelon)
        if main_echelon==1:
            main_echelon = 2
        else:
            main_echelon = 1
        is_first = False
        time_count = time_count+1
        t_doll_retire(time_count)