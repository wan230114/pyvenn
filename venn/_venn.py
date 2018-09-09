from matplotlib.pyplot import subplots
from matplotlib.patches import Ellipse, Polygon
from matplotlib.colors import to_rgba
from matplotlib.cm import ScalarMappable
from ._constants import SHAPE_COORDS, SHAPE_DIMS, SHAPE_ANGLES
from ._constants import PETAL_LABEL_COORDS, PSEUDOVENN_PETAL_COORDS
from math import pi, sin, cos
from functools import partial

def select_colors(n_colors=6, cmap="viridis", alpha=.4):
    """Generate colors from matplotlib colormap; pass list to use exact colors"""
    if not isinstance(n_colors, int) or (n_colors < 2) or (n_colors > 6):
        raise ValueError("n_colors must be an integer between 2 and 6")
    if isinstance(cmap, list):
        colors = [to_rgba(color, alpha=alpha) for color in cmap]
    else:
        scalar_mappable = ScalarMappable(cmap=cmap)
        colors = scalar_mappable.to_rgba(range(n_colors), alpha=alpha)
    return colors[:n_colors]

def less_transparent_color(color, alpha_factor=2):
    """Bump up color's alpha"""
    new_alpha = (1 + to_rgba(color)[3]) / alpha_factor
    return to_rgba(color, alpha=new_alpha)

def draw_ellipse(ax, x, y, w, h, a, color):
    """Wrapper for drawing ellipse; called like `draw_ellipse(ax, *coords, *dims, angle, color)`"""
    ax.add_patch(
        Ellipse(
            xy=(x,y), width=w, height=h, angle=a,
            facecolor=color, edgecolor=less_transparent_color(color)
        )
    )

def draw_triangle(ax, x1, y1, x2, y2, x3, y3, _dim, _angle, color):
    """Wrapper for drawing triangle; called like `draw_triangle(ax, *coords, None, None, color)`"""
    ax.add_patch(
        Polygon(
            xy=[(x1, y1), (x2, y2), (x3, y3)], closed=True,
            facecolor=color, edgecolor=less_transparent_color(color)
        )
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
        yield bin(i)[2:].zfill(n_sets)

def generate_petal_labels(datasets, fmt="{size}"):
    """Generate petal descriptions for venn diagram based on set sizes"""
    datasets = list(datasets)
    n_sets = len(datasets)
    dataset_union = set.union(*datasets)
    universe_size = len(dataset_union)
    petal_labels = {}
    for logic in generate_logics(n_sets):
        included_sets = [
            datasets[i] for i in range(n_sets) if logic[i] == "1"
        ]
        excluded_sets = [
            datasets[i] for i in range(n_sets) if logic[i] == "0"
        ]
        petal_set = (
            (dataset_union & set.intersection(*included_sets)) -
            set.union(set(), *excluded_sets)
        )
        petal_labels[logic] = fmt.format(
            logic=logic, size=len(petal_set),
            percentage=(100*len(petal_set)/universe_size)
        )
    return petal_labels

def init_axes(ax, figsize):
    """Create axes if do not exist, set axes parameters"""
    if ax is None:
        _, ax = subplots(nrows=1, ncols=1, figsize=figsize)
    ax.set(
        aspect="equal", frame_on=False,
        xlim=(-.05, 1.05), ylim=(-.05, 1.05),
        xticks=[], yticks=[]
    )
    return ax

def get_n_sets(petal_labels, dataset_labels):
    """Infer number of sets, check consistency"""
    n_sets = len(dataset_labels)
    for logic in petal_labels.keys():
        if len(logic) != n_sets:
            raise ValueError("Inconsistent petal and dataset labels")
    return n_sets

def draw_venn(*, petal_labels, dataset_labels, colors, figsize, fontsize, legend_loc, ax):
    """Draw true Venn diagram, annotate petals and dataset labels"""
    n_sets = get_n_sets(petal_labels, dataset_labels)
    if 2 <= n_sets < 6:
        draw_shape = draw_ellipse
    elif n_sets == 6:
        draw_shape = draw_triangle
    else:
        raise ValueError("Number of sets must be between 2 and 6")
    ax = init_axes(ax, figsize)
    shape_params = zip(
        SHAPE_COORDS[n_sets], SHAPE_DIMS[n_sets], SHAPE_ANGLES[n_sets], colors
    )
    for coords, dims, angle, color in shape_params:
        draw_shape(ax, *coords, *dims, angle, color)
    for logic, (x, y) in PETAL_LABEL_COORDS[n_sets].items():
        draw_text(ax, x, y, petal_labels[logic], fontsize)
    if legend_loc is not None:
        ax.legend(dataset_labels, loc=legend_loc, prop={"size": fontsize})
    return ax

def draw_pseudovenn6(*, petal_labels, dataset_labels, colors, figsize, fontsize, legend_loc, ax):
    """Draw intersection of 6 circles (does not include some combinations), annotate petals and dataset labels"""
    n_sets = get_n_sets(petal_labels, dataset_labels)
    if n_sets != 6:
        raise NotImplementedError("Pseudovenn implemented only for 6 sets")
    ax = init_axes(ax, figsize)
    for step, color in zip(range(6), colors):
        angle = (2 - step) * pi / 3
        x = .5 + .2 * cos(angle)
        y = .5 + .2 * sin(angle)
        draw_ellipse(ax, x, y, .6, .6, 0, color)
    for logic, petal_label in petal_labels.items():
        # not all theoretical intersections are shown:
        if logic in PSEUDOVENN_PETAL_COORDS[6]:
            x, y = PSEUDOVENN_PETAL_COORDS[6][logic]
            draw_text(ax, x, y, petal_labels[logic], fontsize=fontsize)
    if legend_loc is not None:
        ax.legend(dataset_labels, loc=legend_loc, prop={"size": fontsize})
    return ax

def is_valid_dataset_dict(dataset_dict):
    """Validate passed data (must be dictionary of sets)"""
    if not (hasattr(dataset_dict, "keys") and hasattr(dataset_dict, "values")):
        return False
    for dataset in dataset_dict.values():
        if not isinstance(dataset, set):
            return False
    else:
        return True

def venn_dispatch(dataset_dict, draw_func, fmt="{size}", cmap="viridis", alpha=.4, figsize=(8, 8), fontsize=13, legend_loc="upper right", ax=None):
    """Check input, generate petal labels, draw venn or pseudovenn diagram"""
    if not is_valid_dataset_dict(dataset_dict):
        raise TypeError("Only dictionaries of sets are understood")
    n_sets = len(dataset_dict)
    return draw_func(
        petal_labels=generate_petal_labels(dataset_dict.values(), fmt),
        dataset_labels=dataset_dict.keys(),
        colors=select_colors(n_colors=n_sets, cmap=cmap, alpha=alpha),
        figsize=figsize, fontsize=fontsize, legend_loc=legend_loc, ax=ax
    )

venn = partial(venn_dispatch, draw_func=draw_venn)
pseudovenn = partial(venn_dispatch, draw_func=draw_pseudovenn6)
