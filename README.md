# Captcha-Solving
---

## What for?

I started solving captchas for purely __practical purposes__ to keep my bots running on Bombcrypto. 

Afterwards, their study became an __enriching experience__ allowing me to better understand the stakes of the functions I manipulate and objects on which I work

## How it works?

My captcha resolutions is mainly based on quite precise __image recognition__, playing with the distances of the objects and using simple __mathematics__.

## Custom modules

* `clavier_souris` which allows me to support the mouse and the keyboard, but also to do pixel colour tests


* `matchtemplate` which allows to use opencv algorithms for image detection, I created simple functions which allow to easily use the OpenCV library, without having to rewrite the whole process but simply calling a function which loads only the necessary elements compared to what we have, thus reducing the complexity


* `detects` which is a purely practical module using the two previous modules to, for example, locate an image, click on it randomly, all in one fast function (200ms).


## Exemples

Here is my [Captcha playlist](https://www.youtube.com/watch?v=nxSKQm3I88s&list=PL_7_H9j4EBUPKgiBUpKZJKIzCvJqu0Cbb "Captcha on Youtube").

In these videos you will only see the resolution, meaning only the script working to get a better understanding of my code.

Each captcha is explained separetely in the right folder.
