# https://github.com/tpaviot/pythonocc-utils/blob/master/OCCUtils/Construct.py
# -*- coding: utf-8 -*-

#!/usr/bin/env python

##Copyright 2011-2015 Jelle Feringa (jelleferinga@gmail.com)
##
##This file is part of pythonOCC.
##
##pythonOCC is free software: you can redistribute it and/or modify
##it under the terms of the GNU Lesser General Public License as published by
##the Free Software Foundation, either version 3 of the License, or
##(at your option) any later version.
##
##pythonOCC is distributed in the hope that it will be useful,
##but WITHOUT ANY WARRANTY; without even the implied warranty of
##MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##GNU Lesser General Public License for more details.
##
##You should have received a copy of the GNU Lesser General Public License
##along with pythonOCC.  If not, see <http://www.gnu.org/licenses/>.

'''
This modules makes the construction of geometry a little easier
'''

from __future__ import with_statement
from functools import wraps
from OCC.BRepBuilderAPI import BRepBuilderAPI_MakeEdge

@wraps(BRepBuilderAPI_MakeEdge)
def make_edge(*args):
    edge = BRepBuilderAPI_MakeEdge(*args)
    result = edge.Edge()
    edge.Delete()
    return result

def project_edge_onto_plane(curve, plane):
    """
    :param curve:   BRepAdaptor_Curve
    :param plane:   Geom_Plane
    :return:        TopoDS_Edge projected on the plane
    """
    from OCC.GeomProjLib import geomprojlib_ProjectOnPlane
    proj = geomprojlib_ProjectOnPlane(curve.Curve().Curve(), plane.GetHandle(), plane.Axis().Direction(), True)
    return make_edge(proj)
