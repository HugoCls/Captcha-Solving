import detects as dt
import matchtemplate as templ
import time
import pyautogui
import cv2
import os
import numpy as np
from PIL import ImageGrab
import clavier_souris as cs

def all_captcha():
    while dt.check('robot_numbers')==True:
        if dt.find('treasure hunt'):
            cs.random_sleep(0.5)
        captcha()

def captcha():
    N=1
    if dt.find('connect'):
        cs.random_sleep(0.5)
    L,w,h=templ.matchtemplate('robot_numbers')
    if len(L)>=1:
        xm,xM=L[0][0]-100,L[0][0]+200

        #FOREGROUND NUMBERS DETECTED
        fg=find_numbers_fg(xm,xM)
        print('fg: ',fg)
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

        xk=round((xMcurseur-xmcurseur)/4)
        found=False
        for k in range(4):
            pyautogui.moveTo(xmcurseur+(k+1)*xk,ycurseur,0.01)
            cs.random_sleep(0.5)
            bg=find_numbers_bg(xm,xM,0,N)
            print('bg: ',bg)
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

##NEEDS TO BE ON BG SCREEN
def find_numbers_bg(xm,xM,e,N):
    take_data(xm,xM,10)
    numbers_found=[]
    for i in range(10):
        percentage,x_list=find_number(i,N)
        if percentage>=0.1:
            for j in range(len(x_list)):
                numbers_found.append((i,(x_list[j],0)))
    numbers_found=templ.order_couple_list(numbers_found)
    if len(numbers_found)!=3:
        print(numbers_found)
    if len(numbers_found)!=3 and e<=5:
        return(find_numbers_bg(xm,xM,e+1,N))
    return(numbers_found)
#NEEDS TO BE ON FG SCREEN
def find_numbers_fg(xm,xM):
    take_data(xm,xM,1)
    found_couples=[]
    j=0
    for number in ['0','1','2','3','4','5','6','7','8','9']:
        L,w,h=templ.matchtemplate_cibled(number,'screenshot',0.95)
        if len(L)>=1:
            j+=1
        for i in range(len(L)):
            found_couples.append((number,L[i]))
        if j>=3:
            break
    couples=templ.points_in_couple_list(found_couples)
    final_number=templ.order_couple_list(couples)
    for i in range(len(final_number)):
        final_number[i]=int(final_number[i])
    return(final_number)

def take_data(xmin,xmax,N):
    if 0<=xmin<=xmax<=956:
        x1,y1,x2,y2=240,376,755,720
    elif 956<=xmin<=xmax<=1920:
        x1,y1,x2,y2=1201,376,1713,720
    elif 1920<=xmin<=xmax<=2874:
        x1,y1,x2,y2=2165,376,2675,720
    elif 2874<=xmin:
        x1,y1,x2,y2=3117,376,3639,720
    else:
        x1,y1,x2,y2=240,376,755,720
    if N==1:
        screenGrab_normal(x1,y1,x2,y2)
    else:
        for i in range(0,N):
            screenGrab(x1,y1,x2,y2,i)

def screen(i):
    image = pyautogui.screenshot()
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    cv2.imwrite(os.getcwd()+'\\images\\screenshot'+str(i)+'.png', image)

def screenGrab(x1,y1,x2,y2,i):
    box = (x1,y1,x2,y2)
    im = ImageGrab.grab(box)
    im.save(os.getcwd() + '\\images\\screenshot_'+str(i)+'.png', 'PNG')

def screenGrab_normal(x1,y1,x2,y2):
    box = (x1,y1,x2,y2)
    im = ImageGrab.grab(box)
    im.save(os.getcwd() + '\\images\\screenshot.png', 'PNG')

def save_bg_9():
    img = cv2.imread(os.getcwd()+'\\images\\screenshot_129.png')
    #crop_img=img[35:70,175:190]
    crop_img=img[50:70,180:245]
    cv2.imshow('Detected',crop_img)
    cv2.waitKey(0)
    cv2.imwrite(os.getcwd()+'\\images\\bg_9.10.png',crop_img)

def find_number(number,N):
    count=0
    models=number_models(number)
    xy_list=[]
    for i in range(0,N):
        L,w,h=templ.matchtemplate_cibled(models[0],'screenshot_'+str(i),0.95)
        for j in range(1,len(models)):
            if len(L)>=1:
                break
            else:
                L,w,h=templ.matchtemplate_cibled(models[j],'screenshot_'+str(i),0.95)
        if len(L)>=1:
            xy_list.append((L[0][0],0))
            count+=1
        #print(len(L)>=1,' | ',i)
    X_list=[]
    xy_list=templ.points(xy_list)
    for i in range(len(xy_list)):
        X_list.append(xy_list[i][0])
    return(count/N,X_list)

def number_models(number):
    images_list=[]
    for filename in os.listdir(os.getcwd()+'\\images'):
        if 'bg_'+str(number) in filename:
            images_list.append(filename[:-4])
    return(images_list)