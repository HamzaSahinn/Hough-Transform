# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 21:39:46 2020

@author: Abdullah Hamza Şahin
"""


import numpy as np
import cv2

def hough_lines_acc(img, RhoResolution, ThetaResolution):
 
    h, w = img.shape 
    max_d = np.ceil(np.sqrt(h*h + w*w)) 
    rhos = np.arange(-max_d, max_d + 1, RhoResolution)
    thetas = np.deg2rad(np.arange(-90, 90, ThetaResolution))
  
    H = np.zeros((len(rhos), len(thetas)), dtype=np.uint64)
    y_p, x_p = np.nonzero(img) 

    for i in range(len(x_p)): 
        x = x_p[i]
        y = y_p[i]

        for j in range(len(thetas)): 
            rho = int((x * np.cos(thetas[j]) + y * np.sin(thetas[j])) +max_d )
            if rho < len(rhos):
                H[rho, j] += 1

    return H, rhos, thetas



def hough_peaks(H, n, th):
    h_t = H.copy()
    ind = []
    for i in range(n):
        t = np.unravel_index(h_t.argmax(), h_t.shape)
        if(h_t[t]>th):
            ind.append(t)
        h_t[t] = 0
    return ind
    
    

def hough_lines_draw(img, ind, rhos, thetas): 
    
    for i in range(len(ind)):
        rho = rhos[ind[i][0]]
        theta = thetas[ind[i][1]]
        x0 = np.cos(theta) * rho
        y0 = np.sin(theta) * rho
        
        x1 = int( x0 + 367 * ( -np.sin(theta) ) )
        y1 = int( y0 + 367 * ( np.cos(theta) ) )
        x2 = int( x0 - 367 * ( -np.sin(theta) ) )
        y2 = int( y0 - 367 * ( np.cos(theta) ) )

        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 2)


img = cv2.imread('input/road.png')
img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

edge_img = cv2.Canny(img_gray, 100, 200)


H, rhos, thetas = hough_lines_acc(edge_img,1,5)
ind = hough_peaks(H, 5,200) 
hough_lines_draw(img, ind, rhos, thetas)

cv2.imwrite("output/out.png",img)
cv2.imshow("Hough_Transform", img)

cv2.waitKey(0)
cv2.destroyAllWindows()