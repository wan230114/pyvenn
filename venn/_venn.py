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

SHAPE_COORDS = {
    2: [[0.375, 0.5], [0.625, 0.5]],
    3: [[0.333, 0.633], [0.666, 0.633], [0.500, 0.310]],
    4: [[0.350, 0.4], [0.450, 0.5], [0.544, 0.5], [0.644, 0.4]],
    5: [[.428, .449], [.469, .543], [.558, .523], [.578, .432], [.489, .383]],
    6: [
        [.637, .921, .649, .274, .188, .667],
        [.981, .769, .335, .191, .393, .671],
        [.941, .397, .292, .475, .456, .747],
        [.662, .119, .316, .548, .662, .700],
        [.309, .081, .374, .718, .681, .488],
        [.016, .626, .726, .687, .522, .327]
    ]
}

SHAPE_DIMS = {
    2: [[0.5, 0.5], [0.5, 0.5]],
    3: [[0.5, 0.5], [0.5, 0.5], [0.5, 0.5]],
    4: [[0.72, 0.45], [0.72, 0.45], [0.72, 0.45], [0.72, 0.45]],
    5: [[0.87, 0.50], [0.87, 0.50], [0.87, 0.50], [0.87, 0.50], [0.87, 0.50]],
    6: [[None]]*6
}

SHAPE_ANGLES = {
    2: [0.0, 0.0],
    3: [0.0, 0.0, 0.0],
    4: [140, 140, 40, 40],
    5: [155, 82, 10, 118, 46],
    6: [None]*6
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
    },
    6: {
        "000001": (.212, .562), "000010": (.430, .249), "000011": (.356, .444),
        "000100": (.609, .255), "000101": (.323, .546), "000110": (.513, .316),
        "000111": (.523, .348), "001000": (.747, .458), "001001": (.325, .492),
        "001010": (.670, .481), "001011": (.359, .478), "001100": (.653, .444),
        "001101": (.344, .526), "001110": (.653, .466), "001111": (.363, .503),
        "010000": (.750, .616), "010001": (.682, .654), "010010": (.402, .310),
        "010011": (.392, .421), "010100": (.653, .691), "010101": (.651, .644),
        "010110": (.490, .340), "010111": (.468, .399), "011000": (.692, .545),
        "011001": (.666, .592), "011010": (.665, .496), "011011": (.374, .470),
        "011100": (.653, .537), "011101": (.652, .579), "011110": (.653, .488),
        "011111": (.389, .486), "100000": (.553, .806), "100001": (.313, .604),
        "100010": (.388, .694), "100011": (.375, .633), "100100": (.605, .359),
        "100101": (.334, .555), "100110": (.582, .397), "100111": (.542, .372),
        "101000": (.468, .708), "101001": (.355, .572), "101010": (.420, .679),
        "101011": (.375, .597), "101100": (.641, .436), "101101": (.348, .538),
        "101110": (.635, .453), "101111": (.370, .548), "110000": (.594, .689),
        "110001": (.579, .670), "110010": (.398, .670), "110011": (.395, .653),
        "110100": (.633, .682), "110101": (.616, .656), "110110": (.587, .427),
        "110111": (.526, .415), "111000": (.495, .677), "111001": (.505, .648),
        "111010": (.428, .663), "111011": (.430, .631), "111100": (.639, .524),
        "111101": (.591, .604), "111110": (.622, .477), "111111": (.501, .523)
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
        draw_shape = draw_triangle
    for coords, dims, angle, color in shape_params:
        draw_shape(figure, ax, *coords, *dims, angle, color)
    for subset, (x, y) in LABEL_COORDS[n_sets].items():
        draw_text(figure, ax, x, y, labels.get(subset, ""), fontsize=fontsize)
    if legend_loc is not None:
        ax.legend(names, loc=legend_loc)
    return figure, ax
