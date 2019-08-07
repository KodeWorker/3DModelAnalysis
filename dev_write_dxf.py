# -*- coding: utf-8 -*-
import os
from OCC.gp import gp_Pln, gp_Dir, gp_Pnt
from OCC.STEPControl import STEPControl_Reader
from OCC.BRepBuilderAPI import BRepBuilderAPI_MakeFace
from OCC.TopAbs import TopAbs_FACE
from OCC.TopExp import TopExp_Explorer
from OCC.BRepAlgoAPI import BRepAlgoAPI_Section

from occlib.Topology import Topo
from occlib.EdgeParse import EdgeOnSurface
from occlib.BoundingBox import get_boundingbox
from occlib.DXFwriter import write

#from occlib.Scene import Line3D, Arc3D
#import matplotlib.pyplot as plt
#import matplotlib.patches as mpatches

if __name__ == "__main__":
    
    objects = set()
    
    # Read the file and get the shape
    reader = STEPControl_Reader()
    tr = reader.WS().GetObject().TransferReader().GetObject()
    reader.ReadFile(os.path.abspath(os.path.join('.', 'models', 'TPI_PH_CNF95XX.STEP')))
    reader.TransferRoots()
    shape = reader.OneShape()
    
    # Get bounding box
    xmin, ymin, zmin, xmax, ymax, zmax = get_boundingbox(shape)
    
    # Build section plane
    XYZ = (1, 1, 0)
    lim_coord1 = (xmin, xmax)
    lim_coord2 = (ymin, ymax)
    
    section_height = zmax-1e-3
    # A horizontal plane is created from which a face is constructed to intersect with 
    # the building. The face is transparently displayed along with the building.    
    section_plane = gp_Pln(
        gp_Pnt(0, 0, section_height),
        gp_Dir(0, 0, 1)
    )
    section_face = BRepBuilderAPI_MakeFace(section_plane, xmin, xmax, ymin, ymax).Face()
    
    # Explore the faces of the shape (these are known to be named)
    exp = TopExp_Explorer(shape, TopAbs_FACE)
    while exp.More():
        s = exp.Current()
        
        tp = Topo(s)
        for face in tp.faces():
                
            section = BRepAlgoAPI_Section(section_face, face).Shape()
            section_edges = list(Topo(section).edges())
            
            for edge in section_edges:
                
                obj = EdgeOnSurface(edge, section_plane, lim_coord1, lim_coord2, XYZ)
                objects.add(obj)
                
        exp.Next()
        
        path = "test.dxf"
        write(objects, XYZ, path)