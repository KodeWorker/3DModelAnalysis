# -*- coding: utf-8 -*-
import warnings
from OCC.BRep import BRep_Tool
from OCC.Geom import Geom_Plane
#from OCC.Geom2dAdaptor import Geom2dAdaptor_Curve
from OCC.BRepBuilderAPI import BRepBuilderAPI_MakeFace, BRepBuilderAPI_MakeEdge
from OCC.GeomAbs import (GeomAbs_Line, GeomAbs_Circle, GeomAbs_BSplineCurve)
from OCC.BRepAdaptor import BRepAdaptor_Curve

from .Topology import Topo
from .Util import angle360
from .Scene import Line3D, Arc3D, BSpline3D

def EdgeOnSurface(edge, section_plane, lim_coord1, lim_coord2, XYZ):
    
    section_face = BRepBuilderAPI_MakeFace(section_plane, 
                                           lim_coord1[0], lim_coord1[1],
                                           lim_coord2[0], lim_coord2[1]).Face()
    curve_handle, first, last = BRep_Tool.CurveOnSurface(edge, section_face)
    
    plane = Geom_Plane(section_plane)
    edge_on_surface = BRepBuilderAPI_MakeEdge(curve_handle, plane.GetHandle(), first, last).Edge()            
    curve_adaptor = BRepAdaptor_Curve(edge_on_surface)

    if curve_adaptor.GetType() == GeomAbs_Line:
        
        v = list(Topo(edge_on_surface).vertices())
        v1 = BRep_Tool.Pnt(v[0]).X(), BRep_Tool.Pnt(v[0]).Y(), BRep_Tool.Pnt(v[0]).Z()
        v2 = BRep_Tool.Pnt(v[-1]).X(), BRep_Tool.Pnt(v[-1]).Y(), BRep_Tool.Pnt(v[-1]).Z()

        obj = Line3D(v1, v2)
        
    elif curve_adaptor.GetType() == GeomAbs_Circle:
        v = list(Topo(edge_on_surface).vertices())
        v1 = BRep_Tool.Pnt(v[0]).X(), BRep_Tool.Pnt(v[0]).Y(), BRep_Tool.Pnt(v[0]).Z()
        v2 = BRep_Tool.Pnt(v[-1]).X(), BRep_Tool.Pnt(v[-1]).Y(), BRep_Tool.Pnt(v[-1]).Z()
        
        start = [v1[i] for i in range(len(XYZ)) if XYZ[i]]
        end = [v2[i] for i in range(len(XYZ)) if XYZ[i]]
        
        circle = curve_adaptor.Circle()
        center = []
        for i in range(len(XYZ)):
            if XYZ[i] and i == 0:
                center.append(circle.Location().X())
            elif XYZ[i] and i == 1:
                center.append(circle.Location().Y())
            elif XYZ[i] and i == 2:
                center.append(circle.Location().Z())
            else:
                center.append(0.5*(v1[i] + v2[i]))
        radius = circle.Radius()
        
        vec_start = (start[0] - center[0], start[1] - center[1])
        vec_end = (end[0] - center[0], end[1] - center[1])
        
        t1 = angle360(vec_start)
        t2 = angle360(vec_end)
                
        if not XYZ[0]:
            axis = circle.Axis().Direction().X()
        elif not XYZ[1]:
            axis = circle.Axis().Direction().Y()
        elif not XYZ[2]:
            axis = circle.Axis().Direction().Z()
            
        if axis < 0:
            t1, t2 = t2, t1            
        
        obj = Arc3D(v1, v2, t1, t2, center, radius)
                
    elif curve_adaptor.GetType() == GeomAbs_BSplineCurve :
        
        bspline = curve_adaptor.BSpline().GetObject()
        degree = bspline.Degree()
        knots = [bspline.Knot(index) for index in range(1, bspline.NbKnots()+1)]                
        mults = [bspline.Multiplicity(index) for index in range(1, bspline.NbKnots()+1)]
        poles = [(bspline.Pole(index).X(), bspline.Pole(index).Y(), bspline.Pole(index).Z()) for index in range(1, bspline.NbPoles()+1)]
        periodic = bspline.IsPeriodic()
        obj = BSpline3D(poles, mults, knots, degree, periodic)
                
    else:
        
        print(curve_adaptor.GetType())
        warnings.warn("Not recognized curve!")
    
    return obj