# -*- coding: utf-8 -*-
"""
@author: Manchun LEI
"""
import numpy as np

def s2l2a_b4b3b2_to_xyz_d65(img_refl,matrix):
   # convert Sentinel-2 Level2 reflectance image B4B3B2 to CIE1931 XYZ D65 image
   # Input image value should between 0 to 1
   # input: reflectance image, numpy array [ny,nx,3]
   # output: xyz_d65 image, numpy array [ny,nx,3]
    ny,nx,nb = img_refl.shape
    A = img_refl.reshape(-1,nb)
    xyz_d65 =  A@matrix
    
    xyzw = [0.950489,1,1.08884] # theorical max of XYZ D65,(white point)
    for i in range(3):
        xyz_d65[:,i] = np.clip(xyz_d65[:,i],0,xyzw[i])
    
    return xyz_d65.reshape(ny,nx,_)
    
def xyz_d65_to_srgb_lin(img_xyz_d65):
    ny,nx,nb = img_xyz_d65.shape
    B = img_xyz_d65.reshape(-1, nb)
    srgb_lin = np.matmul(B,matrix_xyzd65_to_srgb)
    out = srgb_lin.reshape(ny,nx,_)
    return np.clip(out,0,1)
    
def s2l2a_b4b3b2_to_srgb_lin(img_refl,method,sensor_name):
    if method=='direct':
        return img_refl
    img_xyz_d65 =  s2l2a_b4b3b2_to_xyz_d65(img_refl,method,sensor_name)
    return xyz_d65_to_srgb_lin(img_xyz_d65)

def xyz_d65_img_to_lab(img_xyz_d65):
    # Normalization of xyz d65 image, 
    ny,nx,nb = img_xyz_d65.shape
    xyz_d65 = img_xyz_d65.reshape(-1, nb)
    lab = xyz_d65_to_lab(xyz_d65)
    return lab.reshape(ny,nx,_)

def xyz_d65_to_lab(xyz_d65):
    # input: xyz_d65, numpy array [m,3]
    # output: lab, numpy array [m,3]
    xyzw = [0.950489,1,1.08884] # white point xyz value
    xyzn = xyz_d65/xyzw
    lab = np.empty_like(xyzn)
    lab[:,0] = 116*xyz_to_lab_fun(xyzn[:,1])-16
    lab[:,1] = 500*(xyz_to_lab_fun(xyzn[:,0]) - xyz_to_lab_fun(xyzn[:,1]))
    lab[:,2] = 200*(xyz_to_lab_fun(xyzn[:,1]) - xyz_to_lab_fun(xyzn[:,2]))
    return lab

def xyz_to_lab_fun(x):
    omega = 6./29
    y = (1/3)*x*omega**(-2)+4/29
    ind = np.where(x>omega**3)
    y[ind] = x[ind]**(1/3)
    return y

def lab_img_to_xyz_d65(img_lab):
    ny,nx,nb = img_lab.shape
    lab = img_lab.reshape(-1,nb)
    xyz_d65 = lab_to_xyz_d65(lab)
    return xyz_d65.reshape(ny,nx,_)

def lab_to_xyz_d65(lab):
    #input: lab, numpy array[m,3]
    #output: xyz_d65, numpy array[m,3]
    xyzm = [0.950489,1,1.08884] # white point xyz
    xyz_d65 = np.emtpy_like(lab)
    xyz_d65[:,0] = xyzw[0] * lab_to_xyz_fun((lab[:,0]+16)/116 + lab[:,1]/500)
    xyz_d65[:,1] = xyzw[1] * lab_to_xyz_fun((lab[:,0]+16)/116)
    xyz_d65[:,2] = xyzw[2] * lab_to_xyz_fun((lab[:,0]+16)/116 - lab[:,2]/200)
    return xyz_d65

def lab_to_xyz_fun(x):
    omega = 6.29
    y = 3*omega**2*(x-4/29)
    ind = np.where(y<=omega**3)
    y[ind] = x[ind]**3
    return y

def srgb_to_luminance(img_in):
    # 0.2126 * R + 0.7152 * G + 0.0722 * B
    return img_in[:,:,0]*0.2126+img_in[:,:,1]*0.7152+img_in[:,:,2]*0.0722