# -*- coding: utf-8 -*-
import os
from OCC.gp import gp_Pln, gp_Dir, gp_Pnt
from OCC.STEPControl import STEPControl_Reader
from OCC.TopAbs import TopAbs_FACE
from OCC.TopExp import TopExp_Explorer

from occlib.Topology import Topo
from occlib.EdgeParse import EdgeOnSurface
from occlib.BoundingBox import get_boundingbox
from occlib.DXFwriter import write


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
    XYZ = (0, 1, 1)
    lim_coord1 = (ymin, ymax)
    lim_coord2 = (zmin, zmax)
    
    section_width = xmin + 1e-3
    # A horizontal plane is created from which a face is constructed to intersect with 
    # the building. The face is transparently displayed along with the building.    
    section_plane = gp_Pln(
        gp_Pnt(section_width, ymax+ymin, 0.0),
        gp_Dir(1, 0, 0)
    )
    
    # Explore the faces of the shape (these are known to be named)
    exp = TopExp_Explorer(shape, TopAbs_FACE)
    while exp.More():
        s = exp.Current()
        
        tp = Topo(s)
        for face in tp.faces():
            for edge in list(Topo(face).edges()):
                
                obj = EdgeOnSurface(edge, section_plane, lim_coord2, lim_coord1, XYZ)
                objects.add(obj)
                
        exp.Next()
        
    path = "side_perspective.dxf"
    write(objects, XYZ, path)