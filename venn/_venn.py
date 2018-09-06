from itertools import chain
from matplotlib.pyplot import subplots
from matplotlib import patches
from matplotlib.colors import to_rgba

DEFAULT_RGB_VALS = [
    [92, 192, 98], [90, 155, 212], [246, 236, 86],
    [241, 90, 96], [255, 117, 00], [82, 82, 190]
]

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

def draw_triangle(fig, ax, x1, y1, x2, y2, x3, y3, fillcolor):
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

SHAPE_COORDS = {
    2: [[0.375, 0.5], [0.625, 0.5]],
    3: [[0.333, 0.633], [0.666, 0.633], [0.500, 0.310]],
    4: [[0.350, 0.4], [0.450, 0.5], [0.544, 0.5], [0.644, 0.4]],
    5: [[.428, .449], [.469, .543], [.558, .523], [.578, .432], [.489, .383]]
}

SHAPE_DIMS = {
    2: [[0.5, 0.5], [0.5, 0.5]],
    3: [[0.5, 0.5], [0.5, 0.5], [0.5, 0.5]],
    4: [[0.72, 0.45], [0.72, 0.45], [0.72, 0.45], [0.72, 0.45]],
    5: [[0.87, 0.50], [0.87, 0.50], [0.87, 0.50], [0.87, 0.50], [0.87, 0.50]]
}

SHAPE_ANGLES = {
    2: [0.0, 0.0],
    3: [0.0, 0.0, 0.0],
    4: [140, 140, 40, 40],
    5: [155, 82, 10, 118, 46]
}

LABEL_COORDS = {
    2: {
        "01": (0.74, 0.5), "10": (0.26, 0.5), "11": (0.50, 0.5)
    },
    3: {
        "001": (0.50, 0.27), "010": (0.73, 0.65), "011": (0.61, 0.46),
        "100": (0.27, 0.65), "101": (0.39, 0.46), "110": (0.50, 0.65),
        "111": (0.50, 0.51)
    },
    4: {
        "0001": (0.85, 0.42), "0010": (0.68, 0.72), "0011": (0.77, 0.59),
        "0100": (0.32, 0.72), "0101": (0.71, 0.30), "0110": (0.50, 0.66),
        "0111": (0.65, 0.50), "1000": (0.14, 0.42), "1001": (0.50, 0.17),
        "1010": (0.29, 0.30), "1011": (0.39, 0.24), "1100": (0.23, 0.59),
        "1101": (0.61, 0.24), "1110": (0.35, 0.50), "1111": (0.50, 0.38)
    },
    5: {
        "00001": (0.27, 0.11), "00010": (0.72, 0.11), "00011": (0.55, 0.13),
        "00100": (0.91, 0.58), "00101": (0.78, 0.64), "00110": (0.84, 0.41),
        "00111": (0.76, 0.55), "01000": (0.51, 0.90), "01001": (0.39, 0.15),
        "01010": (0.42, 0.78), "01011": (0.50, 0.15), "01100": (0.67, 0.76),
        "01101": (0.70, 0.71), "01110": (0.51, 0.74), "01111": (0.64, 0.67),
        "10000": (0.10, 0.61), "10001": (0.20, 0.31), "10010": (0.76, 0.25),
        "10011": (0.65, 0.23), "10100": (0.18, 0.50), "10101": (0.21, 0.37),
        "10110": (0.81, 0.37), "10111": (0.74, 0.40), "11000": (0.27, 0.70),
        "11001": (0.34, 0.25), "11010": (0.33, 0.72), "11011": (0.51, 0.22),
        "11100": (0.25, 0.58), "11101": (0.28, 0.39), "11110": (0.36, 0.66),
        "11111": (0.51, 0.47)
    }
}

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
        raise NotImplementedError("draw_shape = draw_triangle")
    for coords, dims, angle, color in shape_params:
        draw_shape(figure, ax, *coords, *dims, angle, color)
    for subset, (x, y) in LABEL_COORDS[n_sets].items():
        draw_text(figure, ax, x, y, labels.get(subset, ""), fontsize=fontsize)
    ax.legend(names, loc=legend_loc)
    return figure, ax

def venn6(labels, names=['A', 'B', 'C', 'D', 'E'], **options):
    colors = options.get('colors', [default_colors[i] for i in range(6)])
    figsize = options.get('figsize', (20, 20))
    dpi = options.get('dpi', 96)
    fontsize = options.get('fontsize', 14)
    # figure:
    fig = plot.figure(0, figsize=figsize, dpi=dpi)
    ax = fig.add_subplot(111, aspect='equal')
    ax.set_axis_off()
    ax.set_ylim(bottom=0.230, top=0.845)
    ax.set_xlim(left=0.173, right=0.788)
    # body:
    draw_triangle(fig, ax, 0.637, 0.921, 0.649, 0.274, 0.188, 0.667, colors[0])
    draw_triangle(fig, ax, 0.981, 0.769, 0.335, 0.191, 0.393, 0.671, colors[1])
    draw_triangle(fig, ax, 0.941, 0.397, 0.292, 0.475, 0.456, 0.747, colors[2])
    draw_triangle(fig, ax, 0.662, 0.119, 0.316, 0.548, 0.662, 0.700, colors[3])
    draw_triangle(fig, ax, 0.309, 0.081, 0.374, 0.718, 0.681, 0.488, colors[4])
    draw_triangle(fig, ax, 0.016, 0.626, 0.726, 0.687, 0.522, 0.327, colors[5])
    draw_text(fig, ax, 0.212, 0.562, labels.get('000001', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.430, 0.249, labels.get('000010', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.356, 0.444, labels.get('000011', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.609, 0.255, labels.get('000100', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.323, 0.546, labels.get('000101', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.513, 0.316, labels.get('000110', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.523, 0.348, labels.get('000111', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.747, 0.458, labels.get('001000', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.325, 0.492, labels.get('001001', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.670, 0.481, labels.get('001010', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.359, 0.478, labels.get('001011', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.653, 0.444, labels.get('001100', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.344, 0.526, labels.get('001101', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.653, 0.466, labels.get('001110', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.363, 0.503, labels.get('001111', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.750, 0.616, labels.get('010000', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.682, 0.654, labels.get('010001', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.402, 0.310, labels.get('010010', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.392, 0.421, labels.get('010011', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.653, 0.691, labels.get('010100', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.651, 0.644, labels.get('010101', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.490, 0.340, labels.get('010110', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.468, 0.399, labels.get('010111', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.692, 0.545, labels.get('011000', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.666, 0.592, labels.get('011001', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.665, 0.496, labels.get('011010', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.374, 0.470, labels.get('011011', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.653, 0.537, labels.get('011100', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.652, 0.579, labels.get('011101', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.653, 0.488, labels.get('011110', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.389, 0.486, labels.get('011111', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.553, 0.806, labels.get('100000', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.313, 0.604, labels.get('100001', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.388, 0.694, labels.get('100010', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.375, 0.633, labels.get('100011', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.605, 0.359, labels.get('100100', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.334, 0.555, labels.get('100101', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.582, 0.397, labels.get('100110', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.542, 0.372, labels.get('100111', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.468, 0.708, labels.get('101000', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.355, 0.572, labels.get('101001', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.420, 0.679, labels.get('101010', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.375, 0.597, labels.get('101011', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.641, 0.436, labels.get('101100', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.348, 0.538, labels.get('101101', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.635, 0.453, labels.get('101110', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.370, 0.548, labels.get('101111', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.594, 0.689, labels.get('110000', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.579, 0.670, labels.get('110001', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.398, 0.670, labels.get('110010', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.395, 0.653, labels.get('110011', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.633, 0.682, labels.get('110100', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.616, 0.656, labels.get('110101', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.587, 0.427, labels.get('110110', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.526, 0.415, labels.get('110111', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.495, 0.677, labels.get('111000', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.505, 0.648, labels.get('111001', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.428, 0.663, labels.get('111010', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.430, 0.631, labels.get('111011', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.639, 0.524, labels.get('111100', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.591, 0.604, labels.get('111101', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.622, 0.477, labels.get('111110', ''), fontsize=fontsize)
    draw_text(fig, ax, 0.501, 0.523, labels.get('111111', ''), fontsize=fontsize)
    # legend:
    draw_text(fig, ax, 0.674, 0.824, names[0], colors[0], fontsize=fontsize)
    draw_text(fig, ax, 0.747, 0.751, names[1], colors[1], fontsize=fontsize)
    draw_text(fig, ax, 0.739, 0.396, names[2], colors[2], fontsize=fontsize)
    draw_text(fig, ax, 0.700, 0.247, names[3], colors[3], fontsize=fontsize)
    draw_text(fig, ax, 0.291, 0.255, names[4], colors[4], fontsize=fontsize)
    draw_text(fig, ax, 0.203, 0.484, names[5], colors[5], fontsize=fontsize)
    leg = ax.legend(names, loc='best', fancybox=True)
    leg.get_frame().set_alpha(0.5)
    return fig, ax
