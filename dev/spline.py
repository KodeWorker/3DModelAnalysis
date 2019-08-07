# -*- coding: utf-8 -*-
# http://web.mit.edu/hyperbook/Patrikalakis-Maekawa-Cho/node17.html
# https://hub.packtpub.com/how-to-compute-interpolation-in-scipy/
# https://github.com/kawache/Python-B-spline-examples
from scipy.interpolate import splev

def spline_to_polyline(control_points, knot_values, degree, n_mul=5):
    
    x = [pos[0] for pos in control_points]
    y = [pos[1] for pos in control_points]
    tck=[knot_values,[x,y],degree]
    
    n_points = len(x)*n_mul
    u = [i*(1.0/float(n_points-1)) for i in range(n_points)]
    out = splev(u, tck)
    
    line_params = []
    for i in range(len(out[0])-1):
        start_x, start_y = out[0][i], out[1][i]
        end_x, end_y = out[0][i+1], out[1][i+1]
        line_params.append(((start_x, start_y), (end_x, end_y)))
    
    return line_params

if __name__ == '__main__':
    
    
    control_points = [(3 , 1), (2.5, 4), (0, 1), (-2.5, 4),(-3, 0), (-2.5, -4), (0, -1), (2.5, -4), (3, -1)]
    degree = 3
    
    x = [pos[0] for pos in control_points]
    y = [pos[1] for pos in control_points]
    
    knot_values = [0, 0, 0] + [i*(1.0/float(len(x)-2-1)) for i in range(len(x)-2)] + [1, 1, 1]
#    knot_values=np.linspace(0,1,len(x)-2,endpoint=True)
#    knot_values=np.append([0,0,0], knot_values)
#    knot_values=np.append(knot_values, [1,1,1])
    
    tck=[knot_values,[x,y],degree]
    
#    import numpy as np
    import matplotlib.pyplot as plt
    
#    n_points = max(len(x)*2,70)
    n_points = len(x)*5
    u3 = [i*(1.0/float(n_points-1)) for i in range(n_points)]
#    u3=np.linspace(0,1, n_points, endpoint=True)
    out = splev(u3, tck)
    
    plt.plot(x,y,'k--',label='Control polygon',marker='o',markerfacecolor='red')
    plt.plot(out[0],out[1],'b',linewidth=2.0,label='B-spline curve')
    plt.legend(loc='best')
    plt.axis([min(x)-1, max(x)+1, min(y)-1, max(y)+1])
    plt.title('Cubic B-spline curve evaluation')
    plt.show()