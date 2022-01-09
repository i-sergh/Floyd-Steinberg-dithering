#!/usr/bin/env python
# coding: utf-8

import numpy as np
import cv2


## функция показа изо без ебучих ошибок
def imshow (image, title=''):
    try:
        cv2.imshow(title , image)
    except:
        print("Incorrect type of image")
    cv2.waitKey(0) 
    try:
        
        cv2.destroyWindow('')
    except:
        print("'If you're closed the window by red cross then all ok \n If not, may be error" )




# ### Не забывай waitkey & destroyWindow !!!
# на вход идет изо 512x512
inImage = cv2.imread("Floyd-Steinberg/data/in.jpg")
imshow(inImage, '' )



# Создание окна вывода
toWindowShow = np.zeros((inImage.shape[0], inImage.shape[1]*3 ,3), dtype=np.uint8())
toWindowShow[:inImage.shape[0], :inImage.shape[1], :3] = inImage




imshow(toWindowShow, "Let's try")

# Создание копии изо
workImage = np.copy(inImage)

# не обязательно
# добавляет рабочую копию справа

toWindowShow[:inImage.shape[0], inImage.shape[1]:inImage.shape[1]*2, :3] = workImage

imshow(toWindowShow, "Now ok?")


# функция, которая не работает
def quantizer_err (image, quantity):
    errImage = np.copy(image.astype('int8'))
    image[:,:,0] = np.uint8(np.round( ( quantity * image[:,:,0]) /255 ) * (255/ quantity))
    image[:,:,1] = np.uint8(np.round( ( quantity * image[:,:,1]) /255 ) * (255/ quantity))
    image[:,:,2] = np.uint8(np.round( ( quantity * image[:,:,2]) /255 ) * (255/ quantity))
    
    errImage = errImage - image
    return(errImage)


# функция определения палитры 
def quantizer (image, quantity):
    errImage = np.copy(image.astype('int8'))

    for y in range(image.shape[0] ):
        for x in range( image.shape[1] ):
            image[x,y,0] = np.uint8(np.round( ( quantity * image[x,y,0]) /255 ) * (255/ quantity))
            image[x,y,1] = np.uint8(np.round( ( quantity * image[x,y,1]) /255 ) * (255/ quantity))
            image[x,y,2] = np.uint8(np.round( ( quantity * image[x,y,2]) /255 ) * (255/ quantity))
    errImage = errImage.astype('int8') - image.astype('int8')
    return(errImage)

    
errImage = quantizer (workImage, 1)
toWindowShow[:inImage.shape[0], inImage.shape[1]:inImage.shape[1]*2, :3] = workImage
imshow(toWindowShow, "First quantizer")

quantity = 4
for y in range( workImage.shape[0] )  :
    for x in range(workImage.shape[1] ):
        workImage[x,y,0] = np.uint8(np.round( ( quantity * workImage[x,y,0]) /255 ) * (255/ quantity))
        workImage[x,y,1] = np.uint8(np.round( ( quantity * workImage[x,y,1]) /255 ) * (255/ quantity))
        workImage[x,y,2] = np.uint8(np.round( ( quantity * workImage[x,y,2]) /255 ) * (255/ quantity))

        imageErrB = inImage[x,y,0] - workImage[x,y,0]
        imageErrG = inImage[x,y,1] - workImage[x,y,1]
        imageErrR = inImage[x,y,2] - workImage[x,y,2]


        if x < workImage.shape[1] - 1:
            workImage[ x + 1 ][ y     ][0] = workImage[ x + 1 ][ y     ][0] + imageErrB * (7/16) 
            workImage[ x + 1 ][ y     ][1] = workImage[ x + 1 ][ y     ][1] + imageErrG * (7/16) 
            workImage[ x + 1 ][ y     ][2] = workImage[ x + 1 ][ y     ][2] + imageErrR * (7/16) 

        if y < workImage.shape[0] - 1:
            
            if x > 0: 
                workImage[ x - 1 ][ y + 1 ][0] = workImage[ x - 1 ][ y + 1 ][0] + imageErrB * (3/16)
                workImage[ x - 1 ][ y + 1 ][1] = workImage[ x - 1 ][ y + 1 ][1] + imageErrG * (3/16)
                workImage[ x - 1 ][ y + 1 ][2] = workImage[ x - 1 ][ y + 1 ][2] + imageErrR * (3/16)
            
            workImage[ x     ][ y + 1 ][0] = workImage[ x     ][ y + 1 ][0] + imageErrB * (5/16)
            workImage[ x     ][ y + 1 ][1] = workImage[ x     ][ y + 1 ][1] + imageErrG * (5/16)
            workImage[ x     ][ y + 1 ][2] = workImage[ x     ][ y + 1 ][0] + imageErrR * (5/16)
            
            if x < workImage.shape[1] - 1:
                workImage[ x + 1 ][ y + 1 ][0] = workImage[ x + 1 ][ y + 1 ][0] + imageErrB * (1/16)
                workImage[ x + 1 ][ y + 1 ][1] = workImage[ x + 1 ][ y + 1 ][1] + imageErrG * (1/16)
                workImage[ x + 1 ][ y + 1 ][2] = workImage[ x + 1 ][ y + 1 ][2] + imageErrR * (1/16)


toWindowShow[:inImage.shape[0], inImage.shape[1]*2:inImage.shape[1]*3, :3] = workImage
imshow(toWindowShow, "First quantizer")
cv2.imwrite("Floyd-Steinberg/out/out.jpg", workImage)