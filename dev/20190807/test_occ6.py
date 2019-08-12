# -*- coding: utf-8 -*-
# projection
from OCC.STEPControl import STEPControl_Reader
from OCC.TopAbs import TopAbs_FACE, TopAbs_EDGE
from OCC.TopExp import TopExp_Explorer
import os

import OCC.gp
import OCC.BRepAlgoAPI
import OCC.ShapeAnalysis

import ifcopenshell
import ifcopenshell.geom

from OCC.TopoDS import topods

from core_topology_traverse import Topo
from core_geometry_bounding_box import get_boundingbox

#from OCC.BRepAdaptor import BRepAdaptor_Curve
from project_edge_on_plane import project_edge_onto_plane
from OCC.Geom import Geom_Plane

#from OCC.TopExp import topexp
from OCC.BRep import BRep_Tool
from OCC.BRepBuilderAPI import BRepBuilderAPI_MakeEdge
from OCC.GeomProjLib import geomprojlib_ProjectOnPlane

import matplotlib.pyplot as plt

# RGBA colors for the visualisation of elements
RED, WHITE = (1.0, 0, 0, 1.0), (1.0, 1.0, 1.0, 1.0)

# Specify to return pythonOCC shapes from ifcopenshell.geom.create_shape()
settings = ifcopenshell.geom.settings()
settings.set(settings.USE_PYTHON_OPENCASCADE, True)

# Initialize a graphical display window
occ_display = ifcopenshell.geom.utils.initialize_display()

# Read the file and get the shape
reader = STEPControl_Reader()
tr = reader.WS().GetObject().TransferReader().GetObject()
reader.ReadFile(os.path.abspath(os.path.join('.', 'models', 'TPI_PH_CNF95XX.STEP')))
reader.TransferRoots()
shape = reader.OneShape()

xmin, ymin, zmin, xmax, ymax, zmax, x_range, y_range, z_range = get_boundingbox(shape)

#section_height = zmin+1e-3
section_width = xmin + 1e-3
#section_width = 0.5*(xmax + xmin)

#plt.figure()
#plt.xlim((ymin, ymax))
#plt.ylim((zmin, zmax))

# A horizontal plane is created from which a face is constructed to intersect with 
# the building. The face is transparently displayed along with the building.    
section_plane = OCC.gp.gp_Pln(
    OCC.gp.gp_Pnt(section_width, ymax+ymin, +zmax-zmin-z_range),
    OCC.gp.gp_Dir(1, 0, 0)
)
section_face = OCC.BRepBuilderAPI.BRepBuilderAPI_MakeFace(section_plane, zmin, zmax, ymin, ymax).Face()

#section_face_display = ifcopenshell.geom.utils.display_shape(section_face)
#ifcopenshell.geom.utils.set_shape_transparency(section_face_display, 0.5) 

# Explore the faces of the shape (these are known to be named)
exp = TopExp_Explorer(shape, TopAbs_FACE)
#exp = TopExp_Explorer(shape, TopAbs_EDGE)
while exp.More():
    s = exp.Current()
    
    tp = Topo(s)
#    for edge in tp.edges():
    for face in tp.faces():
 
#        edges = OCC.TopTools.TopTools_HSequenceOfShape()
#        edges_handle = OCC.TopTools.Handle_TopTools_HSequenceOfShape(edges)
#        
#        wires = OCC.TopTools.TopTools_HSequenceOfShape()
#        wires_handle = OCC.TopTools.Handle_TopTools_HSequenceOfShape(wires)
#
#        section = OCC.BRepAlgoAPI.BRepAlgoAPI_Section(section_face, face).Shape()
#        section_edges = list(Topo(section).edges())
        
        for edge in list(Topo(face).edges()):
        
            curve_handle, first, last = BRep_Tool.CurveOnSurface(edge, section_face)
            
            plane = Geom_Plane(section_plane)
            
            e = BRepBuilderAPI_MakeEdge(curve_handle, plane.GetHandle(), first, last).Edge()            
#            proj = geomprojlib_ProjectOnPlane(curve_handle, plane.GetHandle(), plane.Axis().Direction(), True)
#            e = BRepBuilderAPI_MakeEdge(proj, first, last).Edge()
                        
            ifcopenshell.geom.utils.display_shape(e, clr=RED)

    exp.Next()