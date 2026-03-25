import matchtemplate as templ
import clavier_souris as cs
import pyautogui
from PIL import ImageGrab
from time import sleep
import detects as dt

def anticheat_grey(x,y):
    R,G,B=cs.pixelRGB(x,y)
    return(R==G==B)

def detect_puzzle(e):
    L,w,h=templ.matchtemplate('robot')
    if len(L)>=1:
        Xlim_min,Xlim_max=L[0][0]-100,L[0][0]+200
        Xmin=L[0][0]-68
        x0,y0=L[0][0]+20,L[0][1]+140
        image = ImageGrab.grab()
        count=0
        sames=0
        (Rs,Gs,Bs) = image.getpixel((x0, y0))
        y=get_ystart()
        for i in range(100):
            x=x0+2*i
            cs.move(x,y)
            (R,G,B) = image.getpixel((x, y))
            if count>=5:
                xpuz,ypuz=x,y
                xmoy,xmax=middle_x_grey(image,xpuz,ypuz)
                ymoy=middle_y_grey(image,xmoy,ypuz)
                cs.move(xmoy,ymoy)
                bar_percentage=(xmoy-Xmin)/346
                Lmc,wc,hc=templ.matchtemplate('yellow')
                LMc1,wc,hc=templ.matchtemplate('brown1')
                LMc2,wc,hc=templ.matchtemplate('brown2')
                LMc=[]
                for i in range(len(LMc1)):
                    LMc.append(LMc1[i])
                for i in range(len(LMc2)):
                    LMc.append(LMc2[i])
                xmcurseur,ycurseur=templ.point_between(Xlim_min, Xlim_max, Lmc)
                xmcurseur+=wc/2
                ycurseur+=hc/2
                xMcurseur,ynone=templ.closer(xmcurseur,ycurseur,LMc)
                xMcurseur+=wc/2   
                xbar=int(xmcurseur+bar_percentage*(xMcurseur-xmcurseur))
                cs.move(xmcurseur,ycurseur)
                cs.mouse.press(cs.Button.left)
                sleep(0.5)
                pyautogui.moveTo(xbar,ycurseur,0.1)
                if bar_percentage<=0.40:
                    cs.mouse.release(cs.Button.left)
                else:
                    image = ImageGrab.grab()
                    k=1
                    while still_grey(image,xmax-1,ymoy+15) and k<=100:
                        image=ImageGrab.grab()
                        pyautogui.moveTo(xbar+k,ycurseur,0.01)
                        k+=1
                    cs.mouse.release(cs.Button.left)
                sleep(0.5)
                if dt.find('sign'):
                    sleep(0.5)
                if dt.check('robot')==False:
                    sleep(1.5)
                    if dt.check('busy_fox')==True and dt.check('sign')==False:
                        dt.find('busy_fox')
                        sleep(1.5)
                    dt.find('sign')
                    print('Captcha | Successful')
                    return(True)
                else:
                    sleep(1)
                    if dt.find('sign')==True:
                        print('Captcha | Successful')
                        return(True)
                    if e<3:
                        print('Captcha | Reseted')
                        return(detect_puzzle(e+1))
                    else:
                        cs.ctrl(cs.F5)
                        print('Captcha | Failed')
                        return(False)
            
            elif R==G==B:
                count+=1
                if (Rs,Gs,Bs)==(R,G,B):
                    sames+=1
                else:
                    sames=0
                if sames>=3:
                    count=0
                Rs,Gs,Bs=R,G,B
                    
            else:
                count=0
                sames=0
    print('Captcha | Failed')
    return(False)
        
def get_ystart():
    L,w,h=templ.matchtemplate('robot')
    x,y=L[0][0],L[0][1]
    x0,y0=x-50,y+70
    j=1
    while True:
        cs.move(x0,y0+8*j)
        R,G,B=cs.pixelRGB(x0,y0+8*j)
        if (R,G,B)==(181,112,82):
            j+=1
        else:
            break
    return(y0+8*j+10)

def middle_x_grey(image,xpuz,ypuz):
    xmin=xpuz
    xmax=xpuz
    start=False
    end=False
    for i in range(0,40):
        (Rm,Gm,Bm) = image.getpixel((xpuz-i, ypuz))
        if Rm==Gm==Bm and start==False:
            xmin=xpuz-i
        else:
            start==True

        (RM,GM,BM) = image.getpixel((xpuz+i, ypuz))
        if RM==GM==BM and end==False:
            xmax=xpuz+i
        else:
            end==True
    return(int((xmax+xmin)/2),xmax)

def middle_y_grey(image,xmoy,ypuz):
    ymin=ypuz
    ymax=ypuz
    start=False
    end=False
    for i in range(0,40):
        (Rm,Gm,Bm) = image.getpixel((xmoy, ypuz-i))
        if Rm==Gm==Bm and start==False:
            ymin=ypuz-i
        else:
            start==True

        (RM,GM,BM) = image.getpixel((xmoy, ypuz+i))
        if RM==GM==BM and end==False:
            ymax=ypuz+i
        else:
            end==True
    return(int((ymax+ymin)/2))


def still_grey(image,xmax,ymoy):
    j=0
    for x in range(xmax-10,xmax):
        (R,G,B) = image.getpixel((x, ymoy))
        if R==G==B and R!=0:
            j+=1
    return(j>=1)