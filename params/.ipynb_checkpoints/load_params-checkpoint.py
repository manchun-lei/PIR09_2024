"""
@author: Manchun LEI
"""
import os
import numpy as np

_path = os.path.dirname(os.path.abspath(__file__))
matrix_xyzd65_to_srgb = np.loadtxt(os.path.join(_path,'XYZd65_TO_sRGB.csv'),delimiter=',')
matrix_s2al2ab4b3b2_to_xyzd65_new = np.loadtxt(os.path.join(_path,'S2AL2Ab4b3b2_to_XYZd65_new.csv'),delimiter=',')
matrix_s2bl2ab4b3b2_to_xyzd65_new = np.loadtxt(os.path.join(_path,'S2BL2Ab4b3b2_to_XYZd65_new.csv'),delimiter=',')
matrix_s2l2ab4b3b2_to_xyzd65_sovdat2019_eq8 = np.loadtxt(os.path.join(_path,'S2L2Ab4b3b2_to_XYZd65_sovdat2019_eq8.csv'),delimiter=',')
matrix_s2l2ab4b3b2_to_xyzd65_sovdat2019_eq9 = np.loadtxt(os.path.join(_path,'S2L2Ab4b3b2_to_XYZd65_sovdat2019_eq9.csv'),delimiter=',')
matrix_s2l2ab4b3b2_to_xyzd65_sovdat2019_eq8_new = np.loadtxt(os.path.join(_path,'S2L2Ab4b3b2_to_XYZd65_sovdat2019_eq8_new.csv'),delimiter=',')
