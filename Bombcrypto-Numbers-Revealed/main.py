import cv2
import numpy as np
import os
from PIL import ImageGrab
import pyautogui
import matchtemplate as templ
import detects as dt
import clavier_souris as cs
import errors
import time

def all_captcha():
    while dt.check('Reveal Number')==True:
        if dt.find('treasure hunt'):
            cs.random_sleep(0.5)
        captcha()

def captcha():
    if dt.find('connect')==True:
        errors.ADD(2)
        cs.random_sleep(0.5)
    L,w,h=templ.matchtemplate('Reveal Number')
    if len(L)>=1:
        errors.ADD(1)
        xm,xM=L[0][0]-100,L[0][0]+200
        #FOREGROUND NUMBERS DETECTED
        bg,(x0,y0)=get_bg_numbers()
        print('bg: ',bg)
        #SETTING UP BAR SIZE
        Lmc,wc,hc=templ.matchtemplate_personalized('new_yellow',0.8)
        xmcurseur,ycurseur=templ.point_between(xm, xM, Lmc)
        xmcurseur+=wc/2
        ycurseur+=hc/2
        LMc1,wc,hc=templ.matchtemplate('brown1')
        LMc2,wc,hc=templ.matchtemplate('brown2')
        LMc=[]
        for i in range(len(LMc1)):
            LMc.append(LMc1[i])
        for i in range(len(LMc2)):
            LMc.append(LMc2[i])
        xMcurseur,ynone=templ.closer(xmcurseur,ycurseur,LMc)
        xMcurseur+=wc/2
        cs.move(xmcurseur,ycurseur)
        cs.random_sleep(0.5)
        #cs.move(xMcurseur,ycurseur)
        cs.mouse.press(cs.Button.left)
        cs.random_sleep(0.5)
        
        found=False
        fg=[]
        for k in range(1,16):
            if xmcurseur+(k+1)*25<xMcurseur+10:
                pyautogui.moveTo(xmcurseur+(k+1)*25,ycurseur,0.01)
                if k>=1:
                    old_fg=fg
                    for i in range(3):
                        fg=get_fg_numbers(x0, y0)
                        if len(fg)==3 or len(fg)==0:
                            break
                    if fg!=old_fg:
                        print('fg: ',fg)
                else:
                    fg=get_fg_numbers(x0, y0)
                if bg==fg:
                    found=True
                    cs.random_sleep(0.5)
                    pyautogui.move(0,2,0.01)
                    cs.mouse.release(cs.Button.left)
                    cs.random_sleep(1)
                    break

        if found==False:
            pyautogui.moveTo(xmcurseur,ycurseur,0.01)
            cs.random_sleep(0.5)
            pyautogui.move(0,2,0.01)
            cs.mouse.release(cs.Button.left)
            cs.random_sleep(1)
        t=time.time()
        while dt.find('sign')==False and time.time()-t<=6:
            cs.random_sleep(0.1)


def get_black_img(original_image):
    processed_img=img_processing(original_image)
    return(processed_img)

def screenGrab(x1,y1,x2,y2):
    box = (x1,y1,x2,y2)
    im = ImageGrab.grab(box)
    im.save(os.getcwd() + '\\images\\screenshot.png', 'PNG')
    img=cv2.imread(os.getcwd() + '\\images\\screenshot.png')
    return(img)

def get_bg_numbers():
    if dt.find('connect'):
        cs.random_sleep(0.5)
    L,w,h=templ.matchtemplate('Reveal Number')
    if len(L)>=1:
        x0,y0=L[0][0],L[0][1]+h
        pyautogui.moveTo(x0,y0)
        #xmax=x0+480,ymax=y0+210
        img_init=pyautogui.screenshot()
        img_init=cv2.cvtColor(np.array(img_init), cv2.COLOR_RGB2BGR)
        bw_img=get_black_img(img_init)
        dx=round(480/15)
        dy=round(180/10)
        for j in range(10):
            pyautogui.moveTo(x0,y0+j*dy)
            for i in range(1,15):
                pyautogui.move(dx,0)
                img2=pyautogui.screenshot()
                img2=cv2.cvtColor(np.array(img2), cv2.COLOR_RGB2BGR)
                added_img=get_black_img(img2)
                (x,y)=pyautogui.position()
                #print('img ',j*9+i,' done.')
                for I in range(x-50,x+50):
                    for J in range(y-50,y+50):
                        [Rf,Gf,Bf]=bw_img[J,I]
                        [Ra,Ga,Ba]=added_img[J,I]
                        if (Rf,Gf,Bf)==(0,0,0):
                            if (Ra,Ga,Ba)!=(0,0,0):
                                bw_img[J,I]=added_img[J,I]

        bw_img=bw_img[y0:y0+180,x0:x0+520]
        grayImage = cv2.cvtColor(bw_img, cv2.COLOR_BGR2GRAY)
        (thresh, bw_img) = cv2.threshold(grayImage, 127, 255, cv2.THRESH_BINARY)
        cv2.imwrite(os.getcwd()+'//images//screenshot_reveal_bg_'+str(0)+'.png',bw_img)
        #cv2.imshow('Changed img',bw_img)
        #cv2.waitKey(0)
        #img=cv2.imread(os.getcwd()+'//images//screenshot_reveal_'+str(k)+'.png')
        detected_numbers=find_numbers_bg(0)
        return(detected_numbers,(x0,y0))
    return(False)

def get_fg_numbers(x0,y0):
    img_init=pyautogui.screenshot()
    img_init=cv2.cvtColor(np.array(img_init), cv2.COLOR_RGB2BGR)
    cv2.imwrite(os.getcwd()+'\\images\\screenshot_reveal_fg_0.png',img_init)
    x,y=x0+250,y0
    found_couples=[]
    j=0
    for number in ['0','1','2','3','4','5','6','7','8','9']:
        L,w,h=templ.matchtemplate_cibled('fg_reveal_'+str(number),'screenshot_reveal_fg_0',0.95)
        if len(L)>=1:
            j+=1
            for i in range(len(L)):
                xf,yf=L[i][0],L[i][1]
                if templ.distance(x,y,xf,yf)<=150:
                    found_couples.append((number,(L[i][0],0)))
    numbers_found=templ.order_couple_list(found_couples)
    return(numbers_found)

def find_numbers_bg(k):
    found_couples=[]
    j=0
    for number in ['0','1','2','3','4','5','6','7','8','9']:
        L,w,h=templ.matchtemplate_cibled('bg_reveal_'+str(number),'screenshot_reveal_bg_'+str(k),0.90)
        if len(L)>=1:
            j+=1
            found_couples.append((number,(L[0][0],0)))
    numbers_found=templ.order_couple_list(found_couples)
    return(numbers_found)

def add_non_black_pixels(full_img,added_img):
    (I,J,K)=full_img.shape
    for i in range(I):
        for j in range(J):
            [Rf,Gf,Bf]=full_img[i,j]
            [Ra,Ga,Ba]=added_img[i,j]
            if (Rf,Gf,Bf)==(0,0,0):
                if (Ra,Ga,Ba)!=(0,0,0):
                    full_img[i,j]=added_img[i,j]
    return(full_img)

#Has to be taken from a new module called image processing
def img_processing(original_image):
    hsv = cv2.cvtColor(original_image, cv2.COLOR_BGR2HSV)
    #FILTERS TO CHANGE
    sAdd=0  #default 0
    sSub=0  #default 0
    vAdd=0  #default 0
    vSub=0  #default 0
    vMin=0  #default 0
    vMax=255    #default 255
    sMin=0  #default 0
    sMax=102  #default 255
    hMin=0  #default 0
    hMax=179  #default 179

    h, s, v = cv2.split(hsv)
    s =shift_channel(s, sAdd)
    s =shift_channel(s, -sSub)
    v =shift_channel(v, vAdd)
    v =shift_channel(v, -vSub)
    hsv = cv2.merge([h, s, v])
    lower = np.array([hMin, sMin, vMin])
    upper = np.array([hMax, sMax, vMax])
    mask = cv2.inRange(hsv, lower, upper)
    result = cv2.bitwise_and(hsv, hsv, mask=mask)
    img = cv2.cvtColor(result, cv2.COLOR_HSV2BGR)
    return(img)

def shift_channel(c,amount):
     if amount > 0:
         lim = 255 - amount
         c[c >= lim] = 255
         c[c < lim] += amount
     elif amount < 0:
         amount = -amount
         lim = amount
         c[c <= lim] = 0
         c[c > lim] -= amount
     return c

