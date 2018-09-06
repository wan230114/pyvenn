from itertools import chain
from matplotlib.pyplot import subplots
from matplotlib.patches import Ellipse, Polygon
from matplotlib.colors import to_rgba
from venn._constants import SHAPE_COORDS, SHAPE_DIMS, SHAPE_ANGLES, LABEL_COORDS

def select_colors(n_colors=6, cmap=list("rgbymc"), alpha=.5):
    """Generate colors from matplotlib colormap; pass list to use exact colors or cmap=None to fall back to default"""
    if not isinstance(n_colors, int) or (n_colors < 2) or (n_colors > 6):
        raise ValueError("n_colors must be an integer between 2 and 6")
    if isinstance(cmap, list):
        colors = [to_rgba(color, alpha=alpha) for color in cmap]
    else:
        raise NotImplementedError("Generating colors from colormap")
    return colors[:n_colors]

def draw_ellipse(ax, x, y, w, h, a, color):
    """Wrapper for drawing ellipse; called like `draw_ellipse(ax, *coords, *dims, angle, color)`"""
    ax.add_patch(
        Ellipse(xy=(x,y), width=w, height=h, angle=a, color=color)
    )

def draw_triangle(ax, x1, y1, x2, y2, x3, y3, _dim, _angle, color):
    """Wrapper for drawing triangle; called like `draw_triangle(ax, *coords, None, None, color)`"""
    ax.add_patch(
        Polygon(xy=[(x1, y1), (x2, y2), (x3, y3)], closed=True, color=color)
    )

def draw_text(ax, x, y, text, fontsize, color="black"):
    """Wrapper for drawing text"""
    ax.text(
        x, y, text, fontsize=fontsize, color=color,
        horizontalalignment="center", verticalalignment="center"
    )

def generate_logics(n_sets):
    """Generate intersection identifiers in binary (0010 etc)"""
    for i in range(1, 2**n_sets):
        yield bin(i).split('0b')[-1].zfill(n_sets)

def generate_labels(datasets, fmt="{size} ({percentage:.1f}%)"):
    """Generate labels for venn diagram based on set sizes"""
    n_sets = len(datasets)
    datasets = [set(datasets[i]) for i in range(n_sets)]
    dataset_union = set(chain(*datasets))
    universe_size = len(dataset_union)
    labels = {}
    for logic in generate_logics(n_sets):
        petal = dataset_union
        sets_for_intersection = [
            datasets[i] for i in range(n_sets) if logic[i] == "1"
        ]
        for s in sets_for_intersection:
            petal = petal & s
        sets_for_difference = [
            datasets[i] for i in range(n_sets) if logic[i] == "0"
        ]
        for s in sets_for_difference:
            petal = petal - s
        labels[logic] = fmt.format(
            logic=logic, size=len(petal),
            percentage=(100*len(petal)/universe_size)
        )
    return labels

def venn(labels, names, cmap=None, alpha=.5, figsize=(8, 8), fontsize=13, legend_loc="upper right"):
    n_sets = len(list(labels.keys())[0])
    if len(names) != n_sets:
        raise ValueError("Lengths of labels and names do not match")
    colors = select_colors(n_colors=n_sets, alpha=alpha)
    figure, ax = subplots(
        nrows=1, ncols=1, figsize=figsize, subplot_kw={
            "aspect": "equal", "frame_on": False, "xticks": [], "yticks": []
        }
    )
    if 2 <= n_sets < 6:
        draw_shape = draw_ellipse
    elif n_sets == 6:
        draw_shape = draw_triangle
    else:
        raise ValueError("Number of sets must be between 2 and 6")
    shape_params = zip(
        SHAPE_COORDS[n_sets], SHAPE_DIMS[n_sets], SHAPE_ANGLES[n_sets], colors
    )
    for coords, dims, angle, color in shape_params:
        draw_shape(ax, *coords, *dims, angle, color)
    for subset, (x, y) in LABEL_COORDS[n_sets].items():
        draw_text(ax, x, y, labels.get(subset, ""), fontsize)
    if legend_loc is not None:
        ax.legend(names, loc=legend_loc, prop={"size": fontsize})
    return figure, ax
