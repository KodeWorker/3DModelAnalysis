# -*- coding: utf-8 -*-
# z-direction cross section
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import warnings

import OCC.gp
import OCC.BRepAlgoAPI
import OCC.ShapeAnalysis
from OCC.STEPControl import STEPControl_Reader
from OCC.TopAbs import TopAbs_FACE
from OCC.TopExp import TopExp_Explorer
from OCC.BRep import BRep_Tool
from OCC.Geom2dAdaptor import Geom2dAdaptor_Curve
from OCC.GeomAbs import (GeomAbs_Line, GeomAbs_Circle, GeomAbs_BSplineCurve)
from OCC.Geom import Geom_Plane
from OCC.BRepBuilderAPI import BRepBuilderAPI_MakeEdge
from OCC.gp import gp_Pnt2d
from OCC.GeomAPI import geomapi

from core_topology_traverse import Topo
from core_geometry_bounding_box import get_boundingbox

import ifcopenshell
import ifcopenshell.geom

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from test_bspline import scipy_bspline1, scipy_bspline2
#from scipy.interpolate import BSpline
#from OCC.StepRepr import Handle_StepRepr_RepresentationItem
from OCC.GProp import GProp_GProps
from OCC.BRepGProp import brepgprop_LinearProperties
from OCC.GCPnts import GCPnts_AbscissaPoint
from OCC.BRepAdaptor import BRepAdaptor_Curve

import numpy as np
    
def angle360(vector1, vector2=(1, 0)):
    angle = np.degrees(np.arctan2(vector1[1], vector1[0])) % 360
    return angle

# RGBA colors for the visualisation of elements
RED, WHITE, BLUE = (1.0, 0.0, 0.0, 1.0), (1.0, 1.0, 1.0, 1.0), (0.0, 0.0, 1.0, 1.0)

# Specify to return pythonOCC shapes from ifcopenshell.geom.create_shape()
settings = ifcopenshell.geom.settings()
settings.set(settings.USE_PYTHON_OPENCASCADE, True)

# Initialize a graphical display window
occ_display = ifcopenshell.geom.utils.initialize_display()
#occ_display.View.SetBackgroundColor(WHITE)

# Read the file and get the shape
reader = STEPControl_Reader()
tr = reader.WS().GetObject().TransferReader().GetObject()
reader.ReadFile(os.path.abspath(os.path.join('..', 'models', 'TPI_PH_CNF95XX.STEP')))
reader.TransferRoots()
shape = reader.OneShape()

xmin, ymin, zmin, xmax, ymax, zmax, x_range, y_range, z_range = get_boundingbox(shape)

section_width = xmin + 1e-3

plt.figure()
plt.xlim((ymin, ymax))
plt.ylim((zmin, zmax))

# A horizontal plane is created from which a face is constructed to intersect with 
# the building. The face is transparently displayed along with the building.    
section_plane = OCC.gp.gp_Pln(
    OCC.gp.gp_Pnt(section_width, ymax+ymin, 0),
#    OCC.gp.gp_Pnt(section_width, ymax+ymin, -2*zmin),
    OCC.gp.gp_Dir(1, 0, 0)
)
section_face = OCC.BRepBuilderAPI.BRepBuilderAPI_MakeFace(section_plane, zmin, zmax, ymin, ymax).Face()
#ifcopenshell.geom.utils.display_shape(section_face)

n_edges = 0

# Explore the faces of the shape (these are known to be named)
exp = TopExp_Explorer(shape, TopAbs_FACE)
while exp.More():
    s = exp.Current()
    
    tp = Topo(s)    
    for face in tp.faces():
        ifcopenshell.geom.utils.display_shape(face)
        for edge in list(Topo(face).edges()):
            
            curve_handle, first, last = BRep_Tool.CurveOnSurface(edge, section_face)
            
            plane = Geom_Plane(section_plane)            
            e = BRepBuilderAPI_MakeEdge(curve_handle, plane.GetHandle(), first, last).Edge()
#            handle_adaptor = Geom2dAdaptor_Curve(curve_handle)
            curve_adapt = BRepAdaptor_Curve(e)
            
            if curve_adapt.GetType() == GeomAbs_Line:
                v = list(Topo(e).vertices())
                y1, z1 = BRep_Tool.Pnt(v[0]).Y(), BRep_Tool.Pnt(v[0]).Z()
                y2, z2 = BRep_Tool.Pnt(v[-1]).Y(), BRep_Tool.Pnt(v[-1]).Z()
                
                plt.plot([y1, y2], [z1, z2], color="red", alpha=0.2)
                ifcopenshell.geom.utils.display_shape(e, clr=RED)
                                
#                line = curve_adapt.Line()
##                r = GCPnts_AbscissaPoint(handle_adaptor)
##                length = r.Parameter()
#                curve_adapt = BRepAdaptor_Curve(e)
#                length = GCPnts_AbscissaPoint().Length(curve_adapt, curve_adapt.FirstParameter(), 
#                                              curve_adapt.LastParameter(), 1e-6)
#                
#                y1, z1 = line.Location().X(), line.Location().Y()
#                y2, z2 = line.Location().X() + length*line.Direction().X(), line.Location().Y() + length*line.Direction().Y()
#                
#                plt.plot([z1, z2], [y1, y2], color="red", alpha=0.2)
                
            elif curve_adapt.GetType() == GeomAbs_Circle:
                v = list(Topo(e).vertices())
                start = (BRep_Tool.Pnt(v[0]).Y(), BRep_Tool.Pnt(v[0]).Z())
                end = (BRep_Tool.Pnt(v[-1]).Y(), BRep_Tool.Pnt(v[-1]).Z())
                
                circle = curve_adapt.Circle()
                center = (circle.Location().Y(), circle.Location().Z())
                radius = circle.Radius()
                
                vec_start = (start[0] - center[0], start[1] - center[1])
                vec_end = (end[0] - center[0], end[1] - center[1])
                
                t_1 = angle360(vec_end)
                t_2 = angle360(vec_start)                
                
                circle_width, circle_height = 2*radius, 2*radius
                arc = mpatches.Arc(xy=center, width=circle_width, 
                                   height=circle_height, angle=0,
                                   theta1=t_1, theta2=t_2, 
                                   color="red", alpha=0.2)
                plt.gca().add_patch(arc)
            
                ifcopenshell.geom.utils.display_shape(e, clr=RED)
                
            elif curve_adapt.GetType() == GeomAbs_BSplineCurve :
                
                v = list(Topo(e).vertices())
                v1 = (BRep_Tool.Pnt(v[0]).Y(), BRep_Tool.Pnt(v[0]).Z())
                v2 = (BRep_Tool.Pnt(v[-1]).Y(), BRep_Tool.Pnt(v[-1]).Z())
                       
                bspline = curve_adapt.BSpline().GetObject()
                degree = bspline.Degree()
                knots = [bspline.Knot(index) for index in range(1, bspline.NbKnots()+1)]                
                mults = [bspline.Multiplicity(index) for index in range(1, bspline.NbKnots()+1)]
                poles = [(bspline.Pole(index).X(), bspline.Pole(index).Y(), bspline.Pole(index).Z()) for index in range(1, bspline.NbPoles()+1)]
                weights = [bspline.Weight(index) for index in range(1, bspline.NbPoles()+1)]
#                
#                start = (bspline.StartPoint().X(), bspline.StartPoint().Y())
#                end = (bspline.EndPoint().X(), bspline.EndPoint().Y())
#                
                p = scipy_bspline2(cv=poles,n=100,degree=degree,periodic=False)
                x, y, z= p.T
                
                if 4.88 in x and np.any(y>=180) and np.any(y<=200):
                    plt.plot(y, z, color="blue", alpha=0.2)
                    ifcopenshell.geom.utils.display_shape(edge, clr=BLUE)
                    ifcopenshell.geom.utils.display_shape(e, clr=BLUE)
                else:
                    plt.plot(y, z, color="red", alpha=0.2)
                    ifcopenshell.geom.utils.display_shape(e, clr=RED)
            else:
                ifcopenshell.geom.utils.display_shape(e, clr=BLUE)
                print(curve_adapt.GetType())
                warnings.warn("Not recognized curve!")
            
            n_edges += 1
                
    exp.Next()