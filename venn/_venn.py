from itertools import chain
from matplotlib.pyplot import subplots
from matplotlib.patches import Ellipse, Polygon
from matplotlib.colors import to_rgba
from matplotlib.cm import ScalarMappable
from _constants import SHAPE_COORDS, SHAPE_DIMS, SHAPE_ANGLES
from _constants import PETAL_LABEL_COORDS, VENN_AXIS_KW
from copy import copy

def select_colors(n_colors=6, cmap=list("rgbymc"), alpha=.5):
    """Generate colors from matplotlib colormap; pass list to use exact colors or cmap=None to fall back to default"""
    if not isinstance(n_colors, int) or (n_colors < 2) or (n_colors > 6):
        raise ValueError("n_colors must be an integer between 2 and 6")
    if isinstance(cmap, list):
        colors = [to_rgba(color, alpha=alpha) for color in cmap]
    else:
        scalar_mappable = ScalarMappable(cmap=cmap)
        colors = scalar_mappable.to_rgba(range(n_colors), alpha=alpha)
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

def generate_petals(datasets, fmt="{size} ({percentage:.1f}%)"):
    """Generate petal descriptions for venn diagram based on set sizes"""
    datasets = list(datasets)
    n_sets = len(datasets)
    datasets = [set(datasets[i]) for i in range(n_sets)]
    dataset_union = set(chain(*datasets))
    universe_size = len(dataset_union)
    petals = {}
    for logic in generate_logics(n_sets):
        petal_set = dataset_union
        sets_for_intersection = [
            datasets[i] for i in range(n_sets) if logic[i] == "1"
        ]
        for s in sets_for_intersection:
            petal_set = petal_set & s
        sets_for_difference = [
            datasets[i] for i in range(n_sets) if logic[i] == "0"
        ]
        for s in sets_for_difference:
            petal_set = petal_set - s
        petals[logic] = fmt.format(
            logic=logic, size=len(petal_set),
            percentage=(100*len(petal_set)/universe_size)
        )
    return petals

def venn(*, petals, labels, cmap=None, alpha=.5, figsize=(8, 8), fontsize=13, legend_loc="upper right", ax=None):
    """Draw prepared petals with provided labels"""
    n_sets = len(labels)
    if n_sets != len(list(petals.keys())[0]):
        raise ValueError("Lengths of petals and labels do not match")
    colors = select_colors(n_colors=n_sets, cmap=cmap, alpha=alpha)
    if ax is None:
        figure, ax = subplots(
            nrows=1, ncols=1, figsize=figsize, subplot_kw=copy(VENN_AXIS_KW)
        )
    else:
        figure = ax.figure
        ax.set(**copy(VENN_AXIS_KW))
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
    for subset, (x, y) in PETAL_LABEL_COORDS[n_sets].items():
        draw_text(ax, x, y, petals.get(subset, ""), fontsize)
    if legend_loc is not None:
        ax.legend(labels, loc=legend_loc, prop={"size": fontsize})
    return figure, ax
