# -*- coding: utf-8 -*-
# z-direction cross section
from OCC.STEPControl import STEPControl_Reader
from OCC.TopAbs import TopAbs_FACE
from OCC.TopExp import TopExp_Explorer
#from OCC.StepRepr import Handle_StepRepr_RepresentationItem
import os

#from OCC.BRepAdaptor import BRepAdaptor_Surface
#from OCC.GeomAbs import GeomAbs_Plane, GeomAbs_Cylinder, GeomAbs_Cone, GeomAbs_BSplineSurface 	
import OCC.gp
import OCC.BRepAlgoAPI
import OCC.ShapeAnalysis

import ifcopenshell
import ifcopenshell.geom

from OCC.TopoDS import topods
#from OCC.BRepTools import BRepTools_WireExplorer

#import matplotlib.pyplot as plt

from core_topology_traverse import Topo
from core_geometry_bounding_box import get_boundingbox

# RGBA colors for the visualisation of elements
RED, WHITE = (1.0, 0, 0, 1.0), (1.0, 1.0, 1.0, 1.0)

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

#section_height = zmin+1e-3
section_height = zmax-1e-3

#plt.figure()
#plt.xlim((xmin, xmax))
#plt.ylim((ymin, ymax))

# A horizontal plane is created from which a face is constructed to intersect with 
# the building. The face is transparently displayed along with the building.    
section_plane = OCC.gp.gp_Pln(
    OCC.gp.gp_Pnt(0, 0, section_height),
    OCC.gp.gp_Dir(0, 0, 1)
)
section_face = OCC.BRepBuilderAPI.BRepBuilderAPI_MakeFace(section_plane, xmin, xmax, ymin, ymax).Face()

#section_face_display = ifcopenshell.geom.utils.display_shape(section_face)
#ifcopenshell.geom.utils.set_shape_transparency(section_face_display, 0.5) 

# Explore the faces of the shape (these are known to be named)
exp = TopExp_Explorer(shape, TopAbs_FACE)
while exp.More():
    s = exp.Current()
    
    tp = Topo(s)
    for face in tp.faces():
        
#        ifcopenshell.geom.utils.display_shape(face)        
        section = OCC.BRepAlgoAPI.BRepAlgoAPI_Section(section_face, face).Shape()
        section_edges = list(Topo(section).edges())
        
        if len(section_edges) > 0:
            # Open Cascade has a function to turn loose unconnected edges into a list of 
            # connected wires. This function takes handles (pointers) to Open Cascade's native 
            # sequence type. Hence, two sequences and handles, one for the input, one for the 
            # output, are created. 
            edges = OCC.TopTools.TopTools_HSequenceOfShape()
            edges_handle = OCC.TopTools.Handle_TopTools_HSequenceOfShape(edges)
            
            wires = OCC.TopTools.TopTools_HSequenceOfShape()
            wires_handle = OCC.TopTools.Handle_TopTools_HSequenceOfShape(wires)
            
            # The edges are copied to the sequence
            for edge in section_edges: edges.Append(edge)
                        
            # A wire is formed by connecting the edges
            OCC.ShapeAnalysis.ShapeAnalysis_FreeBounds.ConnectEdgesToWires(edges_handle, 1e-5, True, wires_handle)
            wires = wires_handle.GetObject()
            
            for i in range(wires.Length()):
                wire_shape = wires.Value(i+1)
                wire = topods.Wire(wire_shape)
                face = OCC.BRepBuilderAPI.BRepBuilderAPI_MakeFace(wire).Face()                
                # The wires and the faces are displayed
                ifcopenshell.geom.utils.display_shape(wire, clr=RED)
                face_display = ifcopenshell.geom.utils.display_shape(face, clr=RED)
                ifcopenshell.geom.utils.set_shape_transparency(face_display, 0.5)
                    
    exp.Next()