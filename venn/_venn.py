from matplotlib.pyplot import subplots
from matplotlib.patches import Ellipse, Polygon
from matplotlib.colors import to_rgba
from matplotlib.cm import ScalarMappable
from functools import wraps
from ._constants import SHAPE_COORDS, SHAPE_DIMS, SHAPE_ANGLES
from ._constants import PETAL_LABEL_COORDS, PSEUDOVENN_PETAL_COORDS, CENTER_TEXT
from math import pi, sin, cos
from ._utils import validate_arguments


def generate_colors(cmap="viridis", n_colors=6, alpha=.4):
    """Generate colors from matplotlib colormap; pass list to use exact colors"""
    if not isinstance(n_colors, int) or (n_colors < 2) or (n_colors > 6):
        raise ValueError("n_colors must be an integer between 2 and 6")
    if isinstance(cmap, list):
        return [to_rgba(color, alpha=alpha) for color in cmap[:n_colors]]
    else:
        scalar_mappable = ScalarMappable(cmap=cmap)
        return scalar_mappable.to_rgba(range(n_colors), alpha=alpha).tolist()


def draw_ellipse(x, y, w, h, a, facecolor, edgecolor, ax):
    """Wrapper for drawing ellipse; called like `draw_ellipse(*coords, *dims, angle, facecolor, edgecolor, ax)`"""
    k = dict(xy=(x,y), width=w, height=h, angle=a, fc=facecolor, ec=edgecolor)
    ax.add_patch(Ellipse(**k))


def draw_triangle(x1, y1, x2, y2, x3, y3, _dim, _angle, facecolor, edgecolor, ax):
    """Wrapper for drawing triangle; called like `draw_triangle(*coords, None, None, facecolor, edgecolor, ax)`"""
    k = dict(xy=[(x1,y1),(x2,y2),(x3,y3)], closed=1, fc=facecolor, ec=edgecolor)
    ax.add_patch(Polygon(**k))


def generate_petal_labels(datasets, fmt="{size}"):
    """Generate petal descriptions for venn diagram based on set sizes"""
    _datasets = list(datasets)
    dataset_union, n_sets = set.union(*_datasets), len(_datasets)
    universe_size = len(dataset_union)
    def _generate():
        for logic in (bin(i)[2:].zfill(n_sets) for i in range(1, 2**n_sets)):
            _nr = range(n_sets)
            included_sets = [_datasets[i] for i in _nr if logic[i] == "1"]
            excluded_sets = [_datasets[i] for i in _nr if logic[i] == "0"]
            petal_set = (
                (dataset_union & set.intersection(*included_sets)) -
                set.union(set(), *excluded_sets)
            )
            s, p = len(petal_set), (100*len(petal_set)/universe_size)
            yield logic, fmt.format(logic=logic, size=s, percentage=p)
    return dict(_generate())


def get_n_sets(petal_labels, dataset_labels):
    """Infer number of sets, check consistency"""
    for logic in petal_labels.keys():
        if len(logic) != len(dataset_labels):
            raise ValueError("Inconsistent petal and dataset labels")
        if not (set(logic) <= {"0", "1"}):
            raise KeyError("Key not understood: " + repr(logic))
    return len(dataset_labels)


def ensure_axes(function):
    """Create ax if does not exist, set style"""
    @wraps(function)
    def wrapper(*args, **kwargs):
        if not kwargs.get("ax"):
            _, kwargs["ax"] = subplots(figsize=kwargs.get("figsize"))
        kwargs["ax"].set(
            aspect="equal", frame_on=False, xticks=[], yticks=[],
            xlim=(-.05, 1.05), ylim=(-.05, 1.05),
        )
        return function(*args, **kwargs)
    return wrapper


@ensure_axes
@validate_arguments
def draw_venn(*, petal_labels, dataset_labels, hint_hidden, colors, edgecolor, fontsize, legend_loc, ax):
    """Draw true Venn diagram, annotate petals and dataset labels"""
    n_sets = get_n_sets(petal_labels, dataset_labels)
    if 2 <= n_sets < 6:
        draw_shape = draw_ellipse
    elif n_sets == 6:
        draw_shape = draw_triangle
    else:
        raise ValueError("Number of sets must be between 2 and 6")
    shape_params = list(zip(
        SHAPE_COORDS[n_sets], SHAPE_DIMS[n_sets], SHAPE_ANGLES[n_sets], colors,
    ))
    for coords, dims, angle, facecolor in shape_params:
        draw_shape(*coords, *dims, angle, facecolor, edgecolor, ax)
    for coords, dims, angle, _ in shape_params:
        draw_shape(*coords, *dims, angle, (0, 0, 0, 0), edgecolor, ax)
    for logic, petal_label in petal_labels.items():
        # some petals could have been modified manually:
        if logic in PETAL_LABEL_COORDS[n_sets]:
            x, y = PETAL_LABEL_COORDS[n_sets][logic]
            ax.text(x, y, petal_label, fontsize=fontsize, **CENTER_TEXT)
    if legend_loc is not None:
        ax.legend(dataset_labels, loc=legend_loc, prop={"size": fontsize})
    return ax


def INPLACE_update_hidden(hidden, logic, petal_labels):
    """Increment set's hidden count (sizes of intersections that are not displayed)"""
    for i, c in enumerate(logic):
        if c == "1":
            hidden[i] += int(petal_labels[logic])


def draw_hint_explanation(ax, dataset_labels, fontsize):
    """Add explanation of 'n/d*' hints"""
    example_labels = list(dataset_labels)[0], list(dataset_labels)[3]
    hint_text = (
        "* elements of set in intersections that are not displayed,\n" +
        "such as shared only between {} and {}".format(*example_labels)
    )
    ax.text(.5, -.1, hint_text, fontsize=fontsize, **CENTER_TEXT)


@ensure_axes
@validate_arguments
def draw_pseudovenn6(*, petal_labels, dataset_labels, hint_hidden, colors, edgecolor, fontsize, legend_loc, ax):
    """Draw intersection of 6 circles (does not include some combinations), annotate petals and dataset labels"""
    n_sets = get_n_sets(petal_labels, dataset_labels)
    if n_sets != 6:
        raise NotImplementedError("Pseudovenn implemented only for 6 sets")
    angles = [(2-i)*pi/3 for i in range(6)]
    xs, ys = [.5+.2*cos(a) for a in angles], [.5+.2*sin(a) for a in angles]
    for x, y, color in zip(xs, ys, colors):
        draw_ellipse(x, y, .6, .6, 0, color, edgecolor, ax)
    for x, y in zip(xs, ys):
        draw_ellipse(x, y, .6, .6, 0, (0, 0, 0, 0), edgecolor, ax)
    if hint_hidden:
        hidden = [0] * n_sets
    for logic, petal_label in petal_labels.items():
        # not all theoretical intersections are shown, and petals could have been modified manually:
        if logic in PSEUDOVENN_PETAL_COORDS[6]:
            x, y = PSEUDOVENN_PETAL_COORDS[6][logic]
            ax.text(x, y, petal_label, fontsize=fontsize, **CENTER_TEXT)
        elif hint_hidden:
            INPLACE_update_hidden(hidden, logic, petal_labels)
    if hint_hidden:
        xs, ys = [.5+.57*cos(a) for a in angles], [.5+.57*sin(a) for a in angles]
        for x, y, hidden_value in zip(xs, ys, hidden):
            hint = "{}\n n/d*".format(hidden_value)
            ax.text(x, y, hint, fontsize=fontsize, **CENTER_TEXT)
        ax.set(xlim=(-.2, 1.05))
        draw_hint_explanation(ax, dataset_labels, fontsize)
    if legend_loc is not None:
        ax.legend(dataset_labels, loc=legend_loc, prop={"size": fontsize})
    return ax


def _venn_dispatch(data, *, func, petal_labels, fmt, hint_hidden, fontsize, cmap, alpha, edgecolor, legend_loc, ax):
    """Generate petal labels, draw venn or pseudovenn diagram"""
    if hint_hidden and (func == draw_pseudovenn6):
        if fmt not in {None, "{size}"}: # TODO implement
            error_message = "To use fmt='{}', set hint_hidden=False".format(fmt)
            raise NotImplementedError(error_message)
    return func(
        dataset_labels=data.keys(), petal_labels=(
            petal_labels if (petal_labels is not None)
            else generate_petal_labels(data.values(), fmt or "{size}")
        ),
        colors=generate_colors(n_colors=len(data), cmap=cmap, alpha=alpha),
        edgecolor=edgecolor, fontsize=fontsize, hint_hidden=hint_hidden,
        legend_loc=legend_loc, ax=ax,
    )


@ensure_axes
@validate_arguments
def venn(data, *, petal_labels=None, fmt=None, hint_hidden=False, fontsize=13, cmap="viridis", alpha=.4, edgecolor=None, legend_loc="best", ax=None):
    """Draw venn diagram"""
    return _venn_dispatch(
        data, func=draw_venn, petal_labels=petal_labels, fmt=fmt,
        hint_hidden=hint_hidden, fontsize=fontsize, cmap=cmap, alpha=alpha,
        edgecolor=edgecolor, legend_loc=legend_loc, ax=ax,
    )


@ensure_axes
@validate_arguments
def pseudovenn(data, *, petal_labels=None, fmt=None, hint_hidden=True, fontsize=13, cmap="viridis", alpha=.4, edgecolor=None, legend_loc="best", ax=None):
    """Draw pseudovenn diagram for six sets"""
    return _venn_dispatch(
        data, func=draw_pseudovenn6, petal_labels=petal_labels, fmt=fmt,
        hint_hidden=hint_hidden, fontsize=fontsize, cmap=cmap, alpha=alpha,
        edgecolor=edgecolor, legend_loc=legend_loc, ax=ax,
    )
