from itertools import chain
from matplotlib.pyplot import subplots
from matplotlib import patches
from matplotlib.colors import to_rgba
from venn._constants import SHAPE_COORDS, SHAPE_DIMS, SHAPE_ANGLES
from venn._constants import DEFAULT_RGB_VALS, LABEL_COORDS

def from_colormap(cmap, n_colors, shift=0, alpha=0.7):
    """Generate colors from matplotlib colormap; pass list to use exact colors or cmap=None to fall back to default"""
    if not isinstance(n_colors, int) or (n_colors < 2) or (n_colors > 6):
        raise ValueError("n_colors must be an integer between 2 and 6")
    if not isinstance(shift, int) or (shift >= 6):
        raise ValueError("shift must be an integer smaller than 6")
    if cmap is None:
        colors = [
            [c/255 for c in rgb] + [alpha]
            for rgb in DEFAULT_RGB_VALS
        ]
    elif isinstance(cmap, list):
        colors = [to_rgba(color, alpha=alpha) for color in cmap]
    else:
        raise NotImplementedError("Generating colors from colormap")
    colors = colors[shift:] + colors[:shift]
    return colors[:n_colors]

def draw_ellipse(fig, ax, x, y, w, h, a, fillcolor):
    e = patches.Ellipse(
        xy=(x, y),
        width=w,
        height=h,
        angle=a,
        color=fillcolor)
    ax.add_patch(e)

def draw_triangle(fig, ax, x1, y1, x2, y2, x3, y3, _dim, _angle, fillcolor):
    xy = [
        (x1, y1),
        (x2, y2),
        (x3, y3),
    ]
    polygon = patches.Polygon(
        xy=xy,
        closed=True,
        color=fillcolor)
    ax.add_patch(polygon)

def draw_text(fig, ax, x, y, text, color=[0, 0, 0, 1], fontsize=14):
    ax.text(
        x, y, text,
        horizontalalignment='center',
        verticalalignment='center',
        fontsize=fontsize,
        color=color)

def get_labels(data, fill=["number"]):
    N = len(data)
    sets_data = [set(data[i]) for i in range(N)] # sets for separate groups
    s_all = set(chain(*data)) # union of all sets
    # bin(3) --> '0b11', so bin(3).split('0b')[-1] will remove "0b"
    set_collections = {}
    for n in range(1, 2**N):
        key = bin(n).split('0b')[-1].zfill(N)
        value = s_all
        sets_for_intersection = [sets_data[i] for i in range(N) if key[i]=='1']
        sets_for_difference = [sets_data[i] for i in range(N) if key[i]=='0']
        for s in sets_for_intersection:
            value = value & s
        for s in sets_for_difference:
            value = value - s
        set_collections[key] = value
    labels = {k: "" for k in set_collections}
    if "logic" in fill:
        for k in set_collections:
            labels[k] = k + ": "
    if "number" in fill:
        for k in set_collections:
            labels[k] += str(len(set_collections[k]))
    if "percent" in fill:
        data_size = len(s_all)
        for k in set_collections:
            labels[k] += "(%.1f%%)" % (100.0*len(set_collections[k])/data_size)
    return labels

def venn(labels, names=[], cmap=None, shift=0, alpha=.7, figsize=(6, 6), dpi=96, fontsize=13, legend_loc="upper right"):
    n_sets = len(list(labels.keys())[0])
    if not names:
        names = list("ABCDEF")[:n_sets]
    elif len(names) != n_sets:
        raise ValueError("Lengths of labels and names do not match")
    colors = from_colormap(cmap, n_colors=n_sets, shift=shift, alpha=alpha)
    figure, ax = subplots(
        nrows=1, ncols=1, figsize=figsize, dpi=dpi, subplot_kw={
            "aspect": "equal", "frame_on": False, "xticks": [], "yticks": []
        }
    )
    shape_params = zip(
        SHAPE_COORDS[n_sets], SHAPE_DIMS[n_sets], SHAPE_ANGLES[n_sets], colors
    )
    if n_sets < 6:
        draw_shape = draw_ellipse
    else:
        draw_shape = draw_triangle
    for coords, dims, angle, color in shape_params:
        draw_shape(figure, ax, *coords, *dims, angle, color)
    for subset, (x, y) in LABEL_COORDS[n_sets].items():
        draw_text(figure, ax, x, y, labels.get(subset, ""), fontsize=fontsize)
    if legend_loc is not None:
        ax.legend(names, loc=legend_loc)
    return figure, ax
