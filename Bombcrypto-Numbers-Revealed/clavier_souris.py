from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController
import ctypes
import keyboard as kb
import autopy
import win32gui
from PIL import ImageGrab
from time import sleep
import random as rd
import pyautogui
import time
import matchtemplate as templ
keyboard = KeyboardController()
mouse = MouseController()
pyautogui.FAILSAFE = False

A=0x10
Z=0x11
E=0x12
R=0x13
T=0x14
Y=0x15
U=0x16
I=0x17
O=0x18
P=0x19
ENTER=0x1C
Q=0x1E
S=0x1F
D=0x20
F=0x21
G=0x22
H=0x23
J=0x24
K=0x25
L=0x26
M=0x27
W=0x2C
X=0x2D
C=0x2E
V=0x2F
B=0x30
N=0x31
VIRGULE=0x32
POINT=0x33
DEUX_POINTS=0x34
EXCLAMATION=0x35
MAJ=0x36
CTRL=0x1D
SPACE=0x39
TAB=0x0F
ALT=0x38
F5=0x3F
WINDOWS='???'
PUL = ctypes.POINTER(ctypes.c_ulong)

class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]


class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]


class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008 | 0x0002, 0,
                        ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def scroll(n):
    n=int(n)
    mouse.scroll(0, n)


def clic_droit():
    mouse.press(Button.right)
    mouse.release(Button.right)

def clic_gauche():
    mouse.press(Button.left)
    sleep(rd.uniform(0.00000001,0.00001))
    mouse.release(Button.left)

def appuyer(lettre):
    PressKey(lettre)
    ReleaseKey(lettre)

def alt_tab():
    PressKey(ALT)
    PressKey(TAB)
    ReleaseKey(TAB)
    ReleaseKey(ALT)

def ctrl(lettre):
    with keyboard.pressed(Key.ctrl):
        appuyer(lettre)

def maj(lettre):
    with keyboard.pressed(Key.shift):
        appuyer(lettre)

def alt(lettre):
    with keyboard.pressed(Key.alt):
        appuyer(lettre)

def windows(lettre):
    PressKey(WINDOWS)
    appuyer(lettre)
    ReleaseKey(WINDOWS)

def ecrire(texte):
    for i in range(len(texte)):
        appuyer(texte[i])

def write(text):
    kb.write(text)

def move(x,y):
    x,y=int(x),int(y)
    pyautogui.moveTo(x,y)

def move_humanly(x,y,t):
    x,y=int(x),int(y)
    pyautogui.moveTo(x,y,t)
    
def curseur():
    return(pyautogui.position())

def pixel(x,y):
    x,y=int(x),int(y)
    return(win32gui.GetPixel(win32gui.GetDC(win32gui.GetActiveWindow()), x , y))

def pixelRGB(x,y):
    image = ImageGrab.grab()
    color = image.getpixel((x, y))
    return(color)

def balayage_x(xmin,xmax,y,nb_valeurs,couleur):
    couleur_trouvee=0
    epsilon=(xmax-xmin)/nb_valeurs
    x=xmin
    for k in range(nb_valeurs):
        move(x,y)
        if couleur_trouvee==0:
            if pixel(x,y)==couleur:
                move(x,y)
                clic_gauche()
                couleur_trouvee+=1
            else:
                x+=epsilon
    return(couleur_trouvee==1)

def balayage_y(x,ymin,ymax,nb_valeurs,couleur):
    couleur_trouvee=0
    epsilon=(ymax-ymin)/nb_valeurs
    y=ymin
    for k in range(nb_valeurs):
        move(x,y)
        if couleur_trouvee==0:
            if pixel(x,y)==couleur:
                move(x,y)
                clic_gauche()
                couleur_trouvee+=1
            else:
                y+=epsilon
    return(couleur_trouvee==1)

def get_balayage_y(x,ymin,ymax,nb_valeurs,couleur):
    epsilon=(ymax-ymin)/nb_valeurs
    y=ymin
    for k in range(nb_valeurs):
        if pixel(x,y)==couleur:
            return(int(y))
        y+=epsilon
    return(0)
def select(xa,ya,xb,yb):
    move(xa,ya)
    mouse.press(Button.left)
    autopy.mouse.smooth_move(xb,yb)
    mouse.release(Button.left)

def random_sleep(t):
    deltat=rd.uniform(0,0.1)
    (x,y)=curseur()
    tps=time.time()
    j=2
    while time.time()-tps<t+deltat:
        deltax,deltay=rd.randint(-5,5),rd.randint(-5,5)
        tho=(t+deltat)/rd.randint(min(j,4),6)
        move_humanly(x+deltax,y+deltay,tho)
        j+=1