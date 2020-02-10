#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/10 22:23
# @Author  : SELF-T-YY
# @Site    : 
# @File    : MHWI AutoSteamworks.py
# @Software: PyCharm

import PyHook3
import re
import win32api
import win32con
import time
import datetime
import sys
from threading import Thread
import gameInput


def OnKeyboardEvent(event):
    global the_first_time
    if re.match('MONSTER HUNTER: WORLD', event.WindowName, re.I):
        if the_first_time:
            print('WindowName:', event.WindowName)
            the_first_time = False

        if event.Key == 'S' and \
                win32api.GetKeyState(win32con.VK_CONTROL) & 0x8000 and \
                win32api.GetKeyState(win32con.VK_LMENU) & 0x8000:
            Start_thread_T()
    else:
        the_first_time = True
        Stop_thread_T()
        
    if event.Key == 'D' and \
            win32api.GetKeyState(win32con.VK_CONTROL) & 0x8000 and \
            win32api.GetKeyState(win32con.VK_LMENU) & 0x8000:
        Stop_thread_T()
    elif event.Key == 'E' and \
            win32api.GetKeyState(win32con.VK_CONTROL) & 0x8000 and \
            win32api.GetKeyState(win32con.VK_LMENU) & 0x8000:
        sys.exit(0)
    return True


def OnMouseEvent(event):
    global the_first_time
    if event.WindowName is None:
        return True
    if re.match('MONSTER HUNTER: WORLD', event.WindowName, re.I):
        if the_first_time:
            print('WindowName:', event.WindowName)
            the_first_time = False
    else:
        the_first_time = True
        Stop_thread_T()
    return True


def Start_thread_T():
    global thread_T
    global start_time
    if not thread_T.is_alive():
        print('----程序开始----')
        thread_T = Thread(target=steamWorks.run)
        start_time = datetime.datetime.now()
        steamWorks.start()
        thread_T.start()


def Stop_thread_T():
    global thread_T
    global start_time
    if thread_T.is_alive():
        print('----持续时间：', datetime.datetime.now()-start_time, '----')
        print('----程序停止----')
        steamWorks.terminate()
        thread_T.join()


class SteamWorks:
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def start(self):
        self._running = True

    def run(self):
        while self._running:
            gameInput.PressKey(0x39)
            time.sleep(0.1)
            gameInput.ReleaseKey(0x39)
            time.sleep(0.1)


print('-------------------------------')
print('----请切换到怪物猎人: 世界窗口----')
print('----按下\'ctrl\'+\'alt\'+\'S\'启动----')
print('----按下\'ctrl\'+\'alt\'+\'D\'停止----')
print('----按下\'ctrl\'+\'alt\'+\'E\'退出----')
print('-------------------------------')

the_first_time = True
start_time = 0

steamWorks = SteamWorks()
thread_T = Thread(target=steamWorks.run)

# create the hook mananger
hm = PyHook3.HookManager()
# register two callbacks
hm.MouseAllButtonsDown = OnMouseEvent
hm.KeyDown = OnKeyboardEvent

# hook into the mouse and keyboard events
hm.HookMouse()
hm.HookKeyboard()


if __name__ == '__main__':
    import pythoncom
    pythoncom.PumpMessages()