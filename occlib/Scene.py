# -*- coding: utf-8 -*-
from BSpline import scipy_bspline

class Line3D(object):
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2
    
    def get_v1(self, XYZ):
        return [self.v1[i] for i in range(len(XYZ)) if XYZ[i]]
    
    def get_v2(self, XYZ):
        return [self.v2[i] for i in range(len(XYZ)) if XYZ[i]]
    
class Arc3D(object):
    def __init__(self, v1, v2, t1, t2, center, radius):
        self.v1 = v1
        self.v2 = v2
        self.t1 = t1
        self.t2 = t2
        self.center = center
        self.radius = radius

    def get_v1(self, XYZ):
        return [self.v1[i] for i in range(len(XYZ)) if XYZ[i]]
    
    def get_v2(self, XYZ):
        return [self.v2[i] for i in range(len(XYZ)) if XYZ[i]]
    
    def get_center(self, XYZ):
        return [self.center[i] for i in range(len(XYZ)) if XYZ[i]]

class BSpline3D(object):
    def __init__(self, poles, mults, knots, degree, periodic=False):
        self.poles = poles
        self.mults = mults
        self.knots = knots
        self.degree = degree
        self.periodic = periodic
    
    def get_polylines(self, n):
        return scipy_bspline(cv=self.poles, n=n, degree=self.degree, periodic=self.periodic)
        