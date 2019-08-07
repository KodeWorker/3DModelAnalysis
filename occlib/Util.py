# -*- coding: utf-8 -*-

import numpy as np
    
def angle360(vector1, vector2=(1, 0)):
    angle = np.degrees(np.arctan2(vector1[1], vector1[0])) % 360
    return angle