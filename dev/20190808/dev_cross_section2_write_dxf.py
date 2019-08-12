# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# https://github.com/tpaviot/pythonocc-demos/blob/master/examples/core_classic_occ_bottle.py
import os
from OCC.gp import gp_Pln, gp_Dir, gp_Pnt, gp_OY, gp_Trsf
from OCC.STEPControl import STEPControl_Reader
from OCC.TopAbs import TopAbs_FACE
from OCC.TopExp import TopExp_Explorer
from OCC.BRepAlgoAPI import BRepAlgoAPI_Section
from OCC.BRepBuilderAPI import BRepBuilderAPI_MakeFace, BRepBuilderAPI_Transform

from occlib.Topology import Topo
from occlib.EdgeParse import EdgeOnSurface
from occlib.BoundingBox import get_boundingbox
from occlib.DXFwriter import write
from occlib.Scene import Arc3D

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
    
    section_height = zmax-0.18
    # A horizontal plane is created from which a face is constructed to intersect with 
    # the building. The face is transparently displayed along with the building.    
    section_plane = gp_Pln(
        gp_Pnt(0, 0, section_height),
        gp_Dir(0, 0, 1)
    )
    section_face = BRepBuilderAPI_MakeFace(section_plane, xmin, xmax, ymin, ymax).Face()
        
    # Quick way to specify the Y axis
    xAxis = gp_OY()

    # Set up the mirror
    aTrsf = gp_Trsf()
    aTrsf.SetMirror(xAxis)
    
    # Explore the faces of the shape (these are known to be named)
    exp = TopExp_Explorer(shape, TopAbs_FACE)
    while exp.More():
        s = exp.Current()
        
        tp = Topo(s)
        for face in tp.faces():
                
            section = BRepAlgoAPI_Section(section_face, face).Shape()
            # Apply the mirror transformation
            aBRespTrsf = BRepBuilderAPI_Transform(section, aTrsf)
            # Get the mirrored shape back out of the transformation and convert back to a wire
            aMirroredShape = aBRespTrsf.Shape()
            section_edges = list(Topo(aMirroredShape).edges())
                        
            for edge in section_edges:
                
                obj = EdgeOnSurface(edge, section_plane, lim_coord1, lim_coord2, XYZ)
                
                if type(obj) == Arc3D:
                    obj.t2, obj.t1 = obj.t1, obj.t2
                    
                objects.add(obj)
                                
        exp.Next()
    
    path = "cross_section2.dxf"
    write(objects, XYZ, path)