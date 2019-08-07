# -*- coding: utf-8 -*-
import warnings
import ezdxf
from .Scene import Line3D, Arc3D

def write(objects, XYZ, path):
    path = "test.dxf"
    dwg = ezdxf.new('AC1024')
    dwg.encoding = 'utf-8'
    msp = dwg.modelspace()
    
    for obj in objects:
        if type(obj) == Line3D:
            start = obj.get_v1(XYZ)
            end = obj.get_v2(XYZ)
            msp.add_line(start, end)
        elif type(obj) == Arc3D:
            center = obj.get_center(XYZ)
            radius = obj.radius
            start_angle = obj.t1
            end_angle = obj.t2
            is_counter_clockwise = True
            msp.add_arc(center, radius, start_angle, end_angle, 
                        is_counter_clockwise)
        else:
            warnings.warn('Unknown object!')
                
    dwg.saveas(path)