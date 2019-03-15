from matplotlib.pyplot import subplots
from ._venn import init_axes, draw_ellipse, venn
from math import pi, sqrt

def euler2(data):
    sizes = {k: len(v) for k, v in data.items()}
    iter_order = sorted(sizes.items(), key=lambda x:x[1], reverse=True)
    key_order = next(zip(*iter_order))
    k1, k2 = key_order
    r1, r2 = sqrt(sizes[k1] / pi), sqrt(sizes[k2] / pi)
    r1, r2 = r1 / (r1 + r2), r2 / (r1 + r2)
    d = r1 + r2 * (1 - 2 * len(data[k1] & data[k2]) / len(data[k2]))
    x_offset = r1 / (r1 + d + r2)
    ...
    ax = init_axes(None, (8, 8))
    draw_ellipse(x_offset, .5, r1, r1, 0, "red", ax)
    draw_ellipse(x_offset + d/2, .5, r2, r2, 0, "green", ax)
    return ax
