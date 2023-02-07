# Bombcrypto-Numbers-Revealed
---

## What to resolve?

The goal of this captcha is to slide the bottom bar until the numbers on the frontground and background match together.
<img src="https://github.com/HugoCls/Captcha-Solving/blob/main/Bombcrypto-Numbers-Revealed/images/README_IMAGES/captcha_img.png?raw=true"  width="50%" height="50%">

When you slide you have other numbers but still moving like this:

PUT OTHER IMAGES

## Which are the critical points?

- The background numbers are always moving so they aren't to be detected too easily.

- The foreground numbers make it difficult to detect those in the background because these are partly hidden.

## How I did it?
**⚠ Warning:**
> If you miss the basis of my captcha techniques I recommend you to first read Bombcrypto-Puzzle in my captcha solving repository.

Solving this captcha only needed three steps:

Firstly in every steps, the image is transformed into black and white, this is done in the `screenshot()` function.

<big>1. Determining the **foreground number**</big>
***

In a first step we need all numbers to be in our dataset:

<img src="https://github.com/HugoCls/Captcha-Solving/blob/main/Bombcrypto-Numbers-Moving/images/0.png?raw=true" width="5%" height="5%"> <img src="https://github.com/HugoCls/Captcha-Solving/blob/main/Bombcrypto-Numbers-Moving/images/1.png?raw=true" width="3%" height="3%"> <img src="https://github.com/HugoCls/Captcha-Solving/blob/main/Bombcrypto-Numbers-Moving/images/2.png?raw=true" width="5%" height="5%"> ... <img src="https://github.com/HugoCls/Captcha-Solving/blob/main/Bombcrypto-Numbers-Moving/images/9.png?raw=true" width="5%" height="5%">

Then we use, `L,w,h=templ.matchtemplate('img')` from the `cv2.matchtemplate` function to get the numbers in the right order:

```python
def find_numbers_fg():
    screenshot() #Saves a screenshot to work with
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
    couples=templ.points_in_couple_list(found_couples) #Removing duplicates
    final_number=templ.order_couple_list(couples)
    for i in range(len(final_number)):
        final_number[i]=int(final_number[i])
    return(final_number)
```
And you get something like that: `fg: ['5','6','9']`.

<big>2. Determining the **background numbers**</big>
***
As I said, it was hard to detect directly the numbers because of the foreground numbers obstructing the detection.

Usually `cv2.matchtemplate` is used with a 80% precision to detect the smaller image in the bigger one. And with the foreground numbers we can see that at least 30% of the image is obstructed so we may imagine that detecting with 80% precision may 1: not work 2: make him confuse the different numbers. 

For exemple: if you have `1 2 3` on background and `0 0 0` on foreground,  `cv2.matchtemplate` may think that there is as much chance as `1` is a `1` or a `2`, a `7` and so on..

And after some tests, it was confirmed that the results weren't so good and I couldn't use it in that way.

Here is how I got around this problem:
For each *background number*, which we will also call *moving number*, I created fairly small pieces of the top of the figure and the bottom of the figure, parts that were not reached by the numbers in the foreground, it went something like this:

<img src="https://github.com/HugoCls/Captcha-Solving/blob/main/Bombcrypto-Numbers-Moving/images/bg_0.1.png?raw=true" width="5%" height="5%"> <img src="https://github.com/HugoCls/Captcha-Solving/blob/main/Bombcrypto-Numbers-Moving/images/bg_0.2.png?raw=true" width="5%" height="5%"> <img src="https://github.com/HugoCls/Captcha-Solving/blob/main/Bombcrypto-Numbers-Moving/images/bg_0.3.png?raw=true" width="5%" height="5%"> <img src="https://github.com/HugoCls/Captcha-Solving/blob/main/Bombcrypto-Numbers-Moving/images/bg_0.4.png?raw=true" width="5%" height="5%"> <img src="https://github.com/HugoCls/Captcha-Solving/blob/main/Bombcrypto-Numbers-Moving/images/bg_0.5.png?raw=true" width="5%" height="5%">
...
<img src="https://github.com/HugoCls/Captcha-Solving/blob/main/Bombcrypto-Numbers-Moving/images/bg_2.1.png?raw=true" width="5%" height="5%"> <img src="https://github.com/HugoCls/Captcha-Solving/blob/main/Bombcrypto-Numbers-Moving/images/bg_2.2.png?raw=true" width="5%" height="5%"> <img src="https://github.com/HugoCls/Captcha-Solving/blob/main/Bombcrypto-Numbers-Moving/images/bg_2.3.png?raw=true" width="5%" height="5%"> <img src="https://github.com/HugoCls/Captcha-Solving/blob/main/Bombcrypto-Numbers-Moving/images/bg_2.4.png?raw=true" width="5%" height="5%"> <img src="https://github.com/HugoCls/Captcha-Solving/blob/main/Bombcrypto-Numbers-Moving/images/bg_2.5.png?raw=true" width="5%" height="5%">
...

Then I was using `cv2.matchtemplate` with a 95% precision to know if this small image was in my screenshot. By multiplying the number of small pieces, I could reach a 90%+ detection of each figure.

```python
for number in ['0','1','2','3','4','5','6','7','8','9']:
        L,w,h=templ.matchtemplate_cibled(number,'screenshot',0.95)
```

Note: This is a little bit more complicated but if you wanna see more about mathematics feel free to explore the following functions:```
    - find_number
    - find_numbers_bg
    - number_models
```


<big>3. Calculate the location of the piece as a **% of the total puzzle**</big>
***

This is basic mathematics based on the total size of the rectangle.

<big>4. **Drag the bar** by this %</big>
***

We can directly use `cv2.matchtemplate` or use the exact same process for the step 2 to get the center of the yellow part of the bar.

This center allows us to **know the total size of the bar** and we can then **move from the %** we are looking for

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

* `clavier_souris` which allows me to support the mouse and the keyboard, but also to do pixel colour tests


* `matchtemplate` which allows to use opencv algorithms for image detection, I created simple functions which allow to easily use the OpenCV library, without having to rewrite the whole process but simply calling a function which loads only the necessary elements compared to what we have, thus reducing the complexity


* `detects` which is a purely practical module using the two previous modules to, for example, locate an image, click on it randomly, all in one fast function (200ms).


## Exemples

Here is my [Captcha playlist](https://www.youtube.com/watch?v=nxSKQm3I88s&list=PL_7_H9j4EBUPKgiBUpKZJKIzCvJqu0Cbb "Captcha on Youtube").

In these videos you will only see the resolution, meaning only the script working to get a better understanding of my code.

