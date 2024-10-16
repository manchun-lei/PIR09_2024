# -*- coding: utf-8 -*-
"""
@author: Manchun LEI
"""
import os
import csv
import numpy as np
from osgeo import gdal
import cv2

def string_to_number(s):
    try:
        if s.isdigit():
            a = int(s)
        else:
            a = float(s)
    except ValueError:
        a = s
    return a

def read_csv(csvfile):
    #load csv to a dict
    #get the header as keys
    with open(csvfile, 'r') as f:
        csvreader = csv.reader(f)
        rows = list(csvreader)
    keys = rows[0]
    #load as dict for each row
    with open(csvfile, 'r') as f:
        csvreader = csv.DictReader(f)
        rows = list(csvreader)
    # read data from csv into a 2 dimension list
    data = [[] for i in range(len(keys))]
    for row in rows:
        for i in range(len(keys)):
            v = string_to_number(row[keys[i]])
            data[i].append(v)
    #create the dict
    mydict = {}
    for i in range(len(keys)):
        mydict[keys[i]] = data[i]
    return mydict

def write_csv(csvfile,mydict):
    with open(csvfile, mode='w', newline='') as f:
        fieldnames = mydict.keys()  # use the keys of the dictionary as fieldnames
        writer = csv.DictWriter(f,fieldnames=fieldnames)
        # write the header row
        writer.writeheader()
        # write the data rows
        for row in zip(*mydict.values()):
            row_dict = dict(zip(mydict.keys(), row))
            writer.writerow(row_dict)

                      
def load_s2l2a_b4b3b2(root_srcpath,path_name,prod_name,res='10m',area=(0,0,-1,-1)):
    
    sensor_name = path_name[0:3]
    
    bnames = ['B04','B03','B02']
    srcpath = os.path.join(root_srcpath,path_name)
    srcfile = os.path.join(srcpath,prod_name+'_'+bnames[0]+'_'+res+'.jp2')
    src = gdal.Open(srcfile)
    tsf = src.GetGeoTransform() #(x0,ps,0,y1,0,-ps)
    ps = tsf[1]
    proj = src.GetProjection()
    nx = src.RasterXSize
    ny = src.RasterYSize
    src = None
    
    # roi area
    ix0 = area[0]
    iy0 = area[1]
    ix1 = area[2]
    iy1 = area[3]
    if ix1==-1:
        ix1 = nx
    if iy1==-1:
        iy1 = ny
    if ix0<0 or iy0<0 or ix1>nx or iy1>ny:
        print('ROI area exceeds the image range')
        print('Image range (0,0,{},{})'.format(0,0,nx,ny))
        print('Roi range ({},{},{},{})'.format(ix0,iy0,ix1,iy1))
        return 0
    
    out_nx = ix1-ix0
    out_ny = iy1-iy0
    out_x0 = ix0*ps+tsf[0]
    out_y1 = tsf[3]-iy0*ps
    out_tsf = (out_x0,ps,0,out_y1,0,-ps)
    out_dtype = gdal.GDT_Float64
    # load data
    out = np.empty([out_ny,out_nx,3],dtype=float)
    for i in range(3):
        srcfile = os.path.join(srcpath,prod_name+'_'+bnames[i]+'_'+res+'.jp2')
        src = gdal.Open(srcfile)
        arr = src.GetRasterBand(1).ReadAsArray()
        val = (arr[iy0:iy1,ix0:ix1].astype(float))/10000
        out[:,:,i] = np.clip(val,0,1)
    
    return out,proj,out_tsf,out_dtype,sensor_name

def save_srgb_to_48bits_img(img_in,dstfile):
    # save srgb image in  48 bits tif format
    # input: srgb image in float format
    img = (img_in*65535).astype(np.uint16)
    cv2.imwrite(dstfile,img[...,::-1])