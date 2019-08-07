# -*- coding: utf-8 -*-
# z-direction cross section

import os
import warnings

import OCC.gp
import OCC.BRepAlgoAPI
import OCC.ShapeAnalysis
from OCC.STEPControl import STEPControl_Reader
from OCC.TopAbs import TopAbs_FACE
from OCC.TopExp import TopExp_Explorer
from OCC.BRep import BRep_Tool
from OCC.Geom2dAdaptor import Geom2dAdaptor_Curve
from OCC.GeomAbs import (GeomAbs_Line, GeomAbs_Circle)

from core_topology_traverse import Topo
from core_geometry_bounding_box import get_boundingbox

import ifcopenshell
import ifcopenshell.geom

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

import numpy as np
    
def angle360(vector1, vector2=(1, 0)):
    angle = np.degrees(np.arctan2(vector1[1], vector1[0])) % 360
    return angle


# RGBA colors for the visualisation of elements
RED, WHITE = (1.0, 0.0, 0.0, 1.0), (1.0, 1.0, 1.0, 1.0)

# Specify to return pythonOCC shapes from ifcopenshell.geom.create_shape()
settings = ifcopenshell.geom.settings()
settings.set(settings.USE_PYTHON_OPENCASCADE, True)

# Initialize a graphical display window
occ_display = ifcopenshell.geom.utils.initialize_display()
#occ_display.View.SetBackgroundColor(WHITE)

# Read the file and get the shape
reader = STEPControl_Reader()
tr = reader.WS().GetObject().TransferReader().GetObject()
reader.ReadFile(os.path.abspath(os.path.join('.', 'models', 'TPI_PH_CNF95XX.STEP')))
reader.TransferRoots()
shape = reader.OneShape()

xmin, ymin, zmin, xmax, ymax, zmax, x_range, y_range, z_range = get_boundingbox(shape)

section_height = zmax-1e-3

plt.figure()
plt.xlim((xmin, xmax))
plt.ylim((ymin, ymax))

# A horizontal plane is created from which a face is constructed to intersect with 
# the building. The face is transparently displayed along with the building.    
section_plane = OCC.gp.gp_Pln(
    OCC.gp.gp_Pnt(0, 0, section_height),
    OCC.gp.gp_Dir(0, 0, 1)
)
section_face = OCC.BRepBuilderAPI.BRepBuilderAPI_MakeFace(section_plane, xmin, xmax, ymin, ymax).Face()

n_edges = 0

# Explore the faces of the shape (these are known to be named)
exp = TopExp_Explorer(shape, TopAbs_FACE)
while exp.More():
    s = exp.Current()
    
    tp = Topo(s)
    for face in tp.faces():
            
        section = OCC.BRepAlgoAPI.BRepAlgoAPI_Section(section_face, face).Shape()
        section_edges = list(Topo(section).edges())
        
        for edge in section_edges:
            
            curve_handle, first, last = BRep_Tool.CurveOnSurface(edge, section_face)
            handle_adaptor = Geom2dAdaptor_Curve(curve_handle)
            
            if handle_adaptor.GetType() == GeomAbs_Line:
                v = list(Topo(edge).vertices())
                x1, y1 = BRep_Tool.Pnt(v[0]).X(), BRep_Tool.Pnt(v[0]).Y()
                x2, y2 = BRep_Tool.Pnt(v[-1]).X(), BRep_Tool.Pnt(v[-1]).Y()
                plt.plot([x1, x2], [y1, y2], color="red")
                
            elif handle_adaptor.GetType() == GeomAbs_Circle:
                v = list(Topo(edge).vertices())
                start = (BRep_Tool.Pnt(v[0]).X(), BRep_Tool.Pnt(v[0]).Y())
                end = (BRep_Tool.Pnt(v[-1]).X(), BRep_Tool.Pnt(v[-1]).Y())
                
                circle = handle_adaptor.Circle()
                center = (circle.Location().X(), circle.Location().Y())
                radius = circle.Radius()
                
                vec_start = (start[0] - center[0], start[1] - center[1])
                vec_end = (end[0] - center[0], end[1] - center[1])
                
                t_1 = angle360(vec_end)
                t_2 = angle360(vec_start)                
                
                circle_width, circle_height = 2*radius, 2*radius
                arc = mpatches.Arc(xy=center, width=circle_width, 
                                   height=circle_height, angle=0,
                                   theta1=t_1, theta2=t_2, 
                                   color="red")
                plt.gca().add_patch(arc)
                
            else:
                print(handle_adaptor.GetType())
                warnings.warn("Not recognized curve!")
            
            ifcopenshell.geom.utils.display_shape(edge, clr=RED)
            n_edges += 1
                
    exp.Next()