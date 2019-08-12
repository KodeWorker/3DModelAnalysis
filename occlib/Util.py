# -*- coding: utf-8 -*-

import numpy as np
    
def angle360(vector1, vector2=(1, 0)):
    angle = np.degrees(np.arctan2(vector1[1], vector1[0])) % 360
    return angle

def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)