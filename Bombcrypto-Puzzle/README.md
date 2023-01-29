# Bombcrypto-Puzzle
---

## What to resolve?
***
The goal of this captcha is to move the puzzle piece to the right place by sliding the bottom bar.
<img src="https://github.com/HugoCls/Captcha-Solving/blob/main/Bombcrypto-Puzzle/images/README_IMAGES/captcha_not_done.png?raw=true"  width="50%" height="50%">

Like this:

<img src="https://github.com/HugoCls/Captcha-Solving/blob/main/Bombcrypto-Puzzle/images/README_IMAGES/captcha_done.png?raw=true" width="50%" height="50%">


## Which are the critical points?
***
- The puzzle and the piece are always different


- The location of the empty piece is also different


- The empty location is a noise of pixels that change colour every moment (the colour part of the puzzle is fixed)

## How I did it?
***
Here is a non-exhaustive list of steps to solve the captcha:

***
<big>1. Locate the **centre of the piece** out of the puzzle</big>
***

Frist we get the starting point by using `L,w,h=templ.matchtemplate('robot')` from the `cv2.matchtemplate`function.
<img src="https://github.com/HugoCls/Captcha-Solving/blob/main/Bombcrypto-Puzzle/images/README_IMAGES/get_start_point.png?raw=true" width="50%" height="50%">

Once we have the starting point we use the fact that the first pixels are all in a brown scale:




```python
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
```

We get (xmin,ymin), and in the same way we can get (xmax,ymax) and deduce (x,y) in the image.

<img src="https://github.com/HugoCls/Captcha-Solving/blob/main/Bombcrypto-Puzzle/images/README_IMAGES/find_piece.png?raw=true" width="50%" height="50%">

***
<big>2. Locate the **centre of the empty piece** in the puzzle</big>
***

For this part we use the method seen in 1 but in reverse:

- We test all the pixels **horizontaly** from **(x,y)**, and as long as we don't have **6 consecutive grey pixels**, we don't consider to be in the empty area.


- Once we are in the empty area, we have to **get the end of the grey area** to get the middle.



*PS: The data of the vertical centre of this area is not useful*

***
<big>3. Calculate the location of the piece as a **% of the total puzzle**</big>
***

This is basic mathematics based on the total size of the rectangle.

***
<big>4. **Drag the bar** by this %</big>
***

We can directly use `cv2.matchtemplate` or use the exact same process for the step 2 to get the center of the yellow part of the bar.

This center allows us to **know the total size of the bar** and we can then **move from the %** we are looking for

***
<big>5. **Fixing** the bar position</big>
***

As they changed the proportionality between the % of which you advance the bar and the % of which the image advances which was then no longer linear, I added a dynamic check as follows:



```python
cs.mouse.press(cs.Button.left)
[...]
while still_grey(image,xmax-1,ymoy+15) and k<=100:
                        image=ImageGrab.grab()
                        pyautogui.moveTo(xbar+k,ycurseur,0.01)
                        k+=1
                    cs.mouse.release(cs.Button.left)
```


## Custom modules
***
* `clavier_souris` which allows me to support the mouse and the keyboard, but also to do pixel colour tests


* `matchtemplate` which allows to use opencv algorithms for image detection, I created simple functions which allow to easily use the OpenCV library, without having to rewrite the whole process but simply calling a function which loads only the necessary elements compared to what we have, thus reducing the complexity


* `detects` which is a purely practical module using the two previous modules to, for example, locate an image, click on it randomly, all in one fast function (200ms).
***

## Exemples
***
Here is my [Captcha playlist](https://www.youtube.com/watch?v=nxSKQm3I88s&list=PL_7_H9j4EBUPKgiBUpKZJKIzCvJqu0Cbb "Captcha on Youtube").

In these videos you will only see the resolution, meaning only the script working to get a better understanding of my code.

