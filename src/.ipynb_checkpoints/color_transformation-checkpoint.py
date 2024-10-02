# -*- coding: utf-8 -*-

import os
import sys
import numpy as np

_current_path = os.path.dirname(os.path.abspath(__file__))
_path = os.path.abspath(os.path.join(_current_path,'..','params'))
sys.path.append(_path)
from load_params import *

def s2l2a_b4b3b2_to_xyz_d65(img_refl,method,sensor_name):
   # convert Sentinel-2 Level2 reflectance image B4B3B2 to CIE1931 XYZ D65 image
   # Input image value should between 0 to 1
   # input: numpy array [ny,nx,3]
   # output: numpy array [ny,nx,3]
    if method=='sovdat19_eq8':
        matrix = matrix_s2l2ab4b3b2_to_xyzd65_sovdat2019_eq8
    elif method=='sovdat19_eq9':
        matrix = matrix_s2l2ab4b3b2_to_xyzd65_sovdat2019_eq9
    elif method=='new':
        if sensor_name=='S2A':
            matrix = matrix_s2al2ab4b3b2_to_xyzd65_lei
        else:
            matrix = matrix_s2bl2ab4b3b2_to_xyzd65_lei
    
    ny,nx,_ = img_refl.shape
    B = img_refl.reshape(-1, img_refl.shape[2])
    xyz_d65 =  np.matmul(B,matrix)
    
    # theorical max of XYZ D65,(white point)
    xyzw = [0.950489,1,1.08884]
    for i in range(3):
        xyz_d65[:,i] = np.clip(xyz_d65[:,i],0,xyzw[i])
    
    return xyz_d65.reshape(ny,nx,_)
    
def xyz_d65_to_srgb_lin(img_xyz_d65):
    ny,nx,_ = img_xyz_d65.shape
    B = img_xyz_d65.reshape(-1, img_xyz_d65.shape[2])
    srgb_lin = np.matmul(B,matrix_xyzd65_to_srgb)
    out = srgb_lin.reshape(ny,nx,_)
    return np.clip(out,0,1)
    
def s2l2a_b4b3b2_to_srgb_lin(img_refl,method,sensor_name):
    if method=='direct':
        return img_refl
    img_xyz_d65 =  s2l2a_b4b3b2_to_xyz_d65(img_refl,method,sensor_name)
    return xyz_d65_to_srgb_lin(img_xyz_d65)

def xyz_d65_to_lab(img_xyz_d65):
    # Normalization of xyz d65 image, 
    xyzm = [0.950489,1,1.08884]
    img_xyzn = np.empty_like(img_xyz_d65)
    for i in range(3):
        img_xyzn[:,:,i] = img_xyz_d65[:,:,i]/xyzm[i]
        
    img_lab = np.empty_like(img_xyzn)
    img_lab[:,:,0] = 116*xyz_to_lab_fun(img_xyzn[:,:,1])-16
    img_lab[:,:,1] = 500*( xyz_to_lab_fun(img_xyzn[:,:,0]) - xyz_to_lab_fun(img_xyzn[:,:,1]) )
    img_lab[:,:,2] = 200*( xyz_to_lab_fun(img_xyzn[:,:,1]) - xyz_to_lab_fun(img_xyzn[:,:,2]) )
    return img_lab

def xyz_to_lab_fun(x):
    omega = 6./29
    y = (1/3)*x*omega**(-2)+4/29
    ind = np.where(x>omega**3)
    y[ind] = x[ind]**(1/3)
    return y

def lab_to_xyz_d65(img_lab):
    xyzm = [0.950489,1,1.08884]
    img_xyz_d65 = np.empty_like(img_lab)
    img_xyz_d65[:,:,0] = xyzm[0] * lab_to_xyz_fun((img_lab[:,:,0]+16)/116 + img_lab[:,:,1]/500)
    img_xyz_d65[:,:,1] = xyzm[1] * lab_to_xyz_fun((img_lab[:,:,0]+16)/116)
    img_xyz_d65[:,:,2] = xyzm[2] * lab_to_xyz_fun((img_lab[:,:,0]+16)/116 - img_lab[:,:,2]/200)
    return img_xyz_d65

def lab_to_xyz_fun(x):
    omega = 6.29
    y = 3*omega**2*(x-4/29)
    ind = np.where(y<=omega**3)
    y[ind] = x[ind]**3
    return y

def srgb_to_luminance(img_in):
    # 0.2126 * R + 0.7152 * G + 0.0722 * B
    return img_in[:,:,0]*0.2126+img_in[:,:,1]*0.7152+img_in[:,:,2]*0.0722