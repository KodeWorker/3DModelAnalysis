# -*- coding: utf-8 -*-
import os
from OCC.gp import gp_Pln, gp_Dir, gp_Pnt
from OCC.STEPControl import STEPControl_Reader
from OCC.TopAbs import TopAbs_FACE
from OCC.TopExp import TopExp_Explorer

from occlib.Topology import Topo
from occlib.EdgeParse import EdgeOnSurface
from occlib.BoundingBox import get_boundingbox
from occlib.Scene import Line3D, Arc3D, BSpline3D

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

if __name__ == "__main__":
    
    # Read the file and get the shape
    reader = STEPControl_Reader()
    tr = reader.WS().GetObject().TransferReader().GetObject()
    reader.ReadFile(os.path.abspath(os.path.join('.', 'models', 'TPI_PH_CNF95XX.STEP')))
    reader.TransferRoots()
    shape = reader.OneShape()
    
    # Get bounding box
    xmin, ymin, zmin, xmax, ymax, zmax = get_boundingbox(shape)
    
    # Build section plane
    XYZ = (1, 0, 1)
    lim_coord1 = (xmin, xmax)
    lim_coord2 = (zmin, zmax)
    
    section_width = ymin + 1e-3
    # A horizontal plane is created from which a face is constructed to intersect with 
    # the building. The face is transparently displayed along with the building.    
    section_plane = gp_Pln(
        gp_Pnt(xmax+xmin, section_width, 0.0),
        gp_Dir(0, 1, 0)
    )
        
    plt.figure()
    plt.xlim(lim_coord1)
    plt.ylim(lim_coord2)
    
    # Explore the faces of the shape (these are known to be named)
    exp = TopExp_Explorer(shape, TopAbs_FACE)
    while exp.More():
        s = exp.Current()
        
        tp = Topo(s)
        for face in tp.faces():            
            for edge in list(Topo(face).edges()):
                
                obj = EdgeOnSurface(edge, section_plane, lim_coord2, lim_coord1, XYZ)
                
                if type(obj) == Line3D:
                    x1, y1 = obj.get_v1(XYZ)
                    x2, y2 = obj.get_v2(XYZ)
                    plt.plot([x1, x2], [y1, y2], color="red")
                    
                elif type(obj) == Arc3D:
                    radius = obj.radius
                    t1, t2 = obj.t1, obj.t2
                    center = obj.get_center(XYZ)
                    
                    circle_width, circle_height = 2*radius, 2*radius
                    arc = mpatches.Arc(xy=center, width=circle_width, 
                                       height=circle_height, angle=0,
                                       theta1=t1, theta2=t2, 
                                       color="red")
                    plt.gca().add_patch(arc)
                
                elif type(obj) == BSpline3D:
                    p = obj.get_polylines(n=100)
                    x, y, z= p.T
                    plt.plot(x, z, color="blue")
        exp.Next()