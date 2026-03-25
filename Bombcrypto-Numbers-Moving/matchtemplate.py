# Python program to illustrate
# template matching
import cv2
import numpy as np
import pyautogui
import os
from PIL import ImageGrab
from functools import partial
ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)


def screen():
    image = pyautogui.screenshot()
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    cv2.imwrite(os.getcwd()+'\\images\\screenshot.png', image)
   
def show_matchtemplate(img_modele):
    screen()
    img_rgb = cv2.imread(os.getcwd()+'\\images\\screenshot.png')
     
    # Convert it to grayscale
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
     
    # Read the template
    template = cv2.imread(os.getcwd()+'\\images\\'+img_modele+'.png',0)
     
    # Store width and height of template in w and h
    w, h = template.shape[::-1]
     
    # Perform match operations.
    res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
     
    # Specify a threshold
    threshold = 0.8
     
    # Store the coordinates of matched area in a numpy array
    loc = np.where( res >= threshold)
     
    # Draw a rectangle around the matched region.
    for pt in zip(*loc[::-1]):
        print(pt[0],pt[1])
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,255,255), 2)
     
    # Show the final image with the matched area.
    cv2.imshow('Detected',img_rgb)
    cv2.waitKey(0)
    
def matchtemplate(img_modele):
    screen()
    img_rgb = cv2.imread(os.getcwd()+'\\images\\screenshot.png')
     
    # Convert it to grayscale
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
     
    # Read the template
    template = cv2.imread(os.getcwd()+'\\images\\'+img_modele+'.png',0)
    
    # Store width and height of template in w and h
    w, h = template.shape[::-1]
    # Perform match operations.
    res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
     
    # Specify a threshold
    threshold = 0.8
     
    # Store the coordinates of matched area in a numpy array
    loc = np.where( res >= threshold)
    L=[]
    # Draw a rectangle around the matched region.
    for pt in zip(*loc[::-1]):
        L.append((pt[0],pt[1]))
    return(L,w,h)

def matchtemplate_without_screen(img_modele):
    img_rgb = cv2.imread(os.getcwd()+'\\images\\screenshot.png')
     
    # Convert it to grayscale
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
     
    # Read the template
    template = cv2.imread(os.getcwd()+'\\images\\'+img_modele+'.png',0)
     
    # Store width and height of template in w and h
    w, h = template.shape[::-1]
    # Perform match operations.
    res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
     
    # Specify a threshold
    threshold = 0.8
     
    # Store the coordinates of matched area in a numpy array
    loc = np.where( res >= threshold)
    L=[]
    # Draw a rectangle around the matched region.
    for pt in zip(*loc[::-1]):
        L.append((pt[0],pt[1]))
    return(L,w,h)
    
##PERSONALIZED FUNCTIONS

def show_matchtemplate_personalized(img_modele,precision):
    screen()
    img_rgb = cv2.imread(os.getcwd()+'\\images\\screenshot.png')
     
    # Convert it to grayscale
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
     
    # Read the template
    template = cv2.imread(os.getcwd()+'\\images\\'+img_modele+'.png',0)
     
    # Store width and height of template in w and h
    w, h = template.shape[::-1]
     
    # Perform match operations.
    res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
     
    # Specify a threshold
    threshold = precision
     
    # Store the coordinates of matched area in a numpy array
    loc = np.where( res >= threshold)
    L=[]
    for pt in zip(*loc[::-1]):
        L.append((pt[0],pt[1]))
    L=points(L)
    for i in range(len(L)):
        cv2.rectangle(img_rgb, L[i], (L[i][0] + w, L[i][1] + h), (0,255,255), 2)
    print(L)
    # Show the final image with the matched area.
    cv2.imshow('Detected',img_rgb)
    cv2.waitKey(0)
    
def matchtemplate_personalized(img_modele,precision):
    screen()
    img_rgb = cv2.imread(os.getcwd()+'\\images\\screenshot.png')
     
    # Convert it to grayscale
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
     
    # Read the template
    template = cv2.imread(os.getcwd()+'\\images\\'+img_modele+'.png',0)
     
    # Store width and height of template in w and h
    w, h = template.shape[::-1]
    # Perform match operations.
    res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
     
    # Specify a threshold
    threshold = precision
     
    # Store the coordinates of matched area in a numpy array
    loc = np.where( res >= threshold)
    L=[]
    # Draw a rectangle around the matched region.
    for pt in zip(*loc[::-1]):
        L.append((pt[0],pt[1]))
    return(L,w,h)

##CIBLED FUNCTIONS

def show_matchtemplate_cibled(img_modele,img_cible,precision):
    img_rgb = cv2.imread(os.getcwd()+'\\images\\'+img_cible+'.png')
     
    # Convert it to grayscale
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
     
    # Read the template
    template = cv2.imread(os.getcwd()+'\\images\\'+img_modele+'.png',0)
     
    # Store width and height of template in w and h
    w, h = template.shape[::-1]
    # Perform match operations.
    res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
     
    # Specify a threshold
    threshold = precision
     
    # Store the coordinates of matched area in a numpy array
    loc = np.where( res >= threshold)
    L=[]
    for pt in zip(*loc[::-1]):
        L.append((pt[0],pt[1]))
    L=points(L)
    for i in range(len(L)):
        cv2.rectangle(img_rgb, L[i], (L[i][0] + w, L[i][1] + h), (0,255,255), 2)
     
    # Show the final image with the matched area.
    print(L)
    cv2.imshow('Detected',img_rgb)
    cv2.waitKey(0)

def matchtemplate_cibled(img_modele,img_cible,precision):
    img_rgb = cv2.imread(os.getcwd()+'\\images\\'+img_cible+'.png')
     
    # Convert it to grayscale
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
     
    # Read the template
    template = cv2.imread(os.getcwd()+'\\images\\'+img_modele+'.png',0)
     
    # Store width and height of template in w and h
    w, h = template.shape[::-1]
    # Perform match operations.
    res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
     
    # Specify a threshold
    threshold = precision
     
    # Store the coordinates of matched area in a numpy array
    loc = np.where( res >= threshold)
    L=[]
    # Draw a rectangle around the matched region.
    for pt in zip(*loc[::-1]):
        L.append((pt[0],pt[1]))
    L=points(L)
    return(L,w,h)

##TOOLS FUNCTIONS

def distance(x1,y1,x2,y2):
    return(np.sqrt((x2-x1)**2+(y2-y1)**2))

def points(L):
    if len(L)==1 or len(L)==0:
        return(L)
    else:
        for i in range(len(L)-1):
            xi,yi=L[i][0],L[i][1]
            for j in range(i+1,len(L)):
                xj,yj=L[j][0],L[j][1]
                d=distance(xi,yi,xj,yj)
                if d<=20:
                    del(L[j])
                    return(points(L))
        return(L)

def points_in_couple_list(L):
    if len(L)==1 or len(L)==0:
        return(L)
    else:
        for i in range(len(L)-1):
            xi,yi=L[i][1][0],L[i][1][1]
            for j in range(i+1,len(L)):
                xj,yj=L[j][1][0],L[j][1][1]
                d=distance(xi,yi,xj,yj)
                if d<=10:
                    del(L[j])
                    return(points_in_couple_list(L))
        return(L)

def order_couple_list(L):
    ordered_list=[]
    if len(L)==0:
        return([])
    while len(L)>=1:
        if len(L)==1:
            ordered_list.append(L[0][0])
            del(L[0])
        else:
            xmin=L[0][1][0]
            j=0
            for i in range(1,len(L)):
                xi,yi=L[i][1][0],L[i][1][1]
                if xi<=xmin:
                    xmin=xi
                    j=i
            ordered_list.append(L[j][0])
            del(L[j])
    return(ordered_list)
    
def width(img_name):
    img = cv2.imread(os.getcwd()+'\\images\\'+img_name+'.png')
    return(img.shape[::-1])

def all_images():
    files=os.listdir('./images')
    images=[]
    for file in files:
        if '.png' in file:
            images.append(file[:-4])
    return(images)

def point_between(Xmin,Xmax,L):
    for i in range(len(L)):
        if Xmin<=L[i][0]<=Xmax:
            return(L[i][0],L[i][1])
    return(L[0][0],L[0][1])
def left_point(L):
    m=L[0][0]
    j=0
    for i in range(len(L)):
        if L[0][0]<=m:
            m=L[0][0]
            j=i
    return(L[j][0],L[j][1])

def closer(x,y,L):
    m=distance(x,y,L[0][0],L[0][1])
    j=0
    for i in range(len(L)):
        if distance(x,y,L[i][0],L[i][1])<=m:
            m=distance(x,y,L[i][0],L[i][1])
            j=i
    return(L[j][0],L[j][1])
    
def get_images(key_word):
    images=all_images()
    cibled_images=[]
    for image in images:
        if key_word in image:
            cibled_images.append(image)
    return(cibled_images)