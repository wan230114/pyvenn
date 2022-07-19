from matplotlib import pyplot as plt
from matplotlib.pyplot import subplots
from matplotlib.patches import Ellipse, Polygon
from matplotlib.colors import to_rgba
from matplotlib.cm import ScalarMappable
from ._constants import SHAPE_COORDS, SHAPE_DIMS, SHAPE_ANGLES
from ._constants import PETAL_LABEL_COORDS, PSEUDOVENN_PETAL_COORDS
from math import pi, sin, cos
from functools import partial
import os

def generate_colors(cmap="viridis", n_colors=6, alpha=.4):
    """Generate colors from matplotlib colormap; pass list to use exact colors"""
    if not isinstance(n_colors, int) or (n_colors < 2) or (n_colors > 6):
        raise ValueError("n_colors must be an integer between 2 and 6")
    if isinstance(cmap, list):
        colors = [to_rgba(color, alpha=alpha) for color in cmap]
    else:
        scalar_mappable = ScalarMappable(cmap=cmap)
        colors = scalar_mappable.to_rgba(range(n_colors), alpha=alpha).tolist()
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

def draw_text(ax, x, y, text, fontsize, color="black", filename=None):
    """Wrapper for drawing text"""
    if not filename:
        ax.text(
            x, y, text, fontsize=fontsize, color=color,
            horizontalalignment="center", verticalalignment="center",
        )
    else:
        ax.text(
            x, y, text, fontsize=fontsize, color=color,
            horizontalalignment="center", verticalalignment="center",
            url=filename,
            bbox=dict(url=filename, alpha=0.001)
        )

def generate_logics(n_sets):
    """Generate intersection identifiers in binary (0010 etc)"""
    for i in range(1, 2**n_sets):
        yield bin(i)[2:].zfill(n_sets)

def generate_petal_labels(datasets, fmt="{size}", outname="out", outdir="."):
    """Generate petal descriptions for venn diagram based on set sizes"""
    # print(outname, datasets)
    datasets = list(datasets)
    n_sets = len(datasets)
    dataset_union = set.union(*datasets)
    universe_size = len(dataset_union)
    petal_labels = {}
    datas = {}
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
            percentage=(100*len(petal_set)/max(universe_size, 1))
        )
        name = ''.join([y for x, y in zip(logic, "ABCDEF") if int(x)])
        datas[(logic, name)] = petal_set
    names = dict(zip(
        sorted([x[1] for x in sorted(datas, key=lambda x:x[1])],key=len),
        range(1, len(datas)+1)
    ))
    # print("names:", names)
    names_out = {}
    for x in datas:
        logic, name = x
        outname_final = "%s%02d%s.txt" % (
                  outname, names[name], name)
        names_out[logic] = outname_final
        print(*sorted(datas[x]), sep="\n", end="",
              file=open(os.path.join(outdir, outname_final), "w"))
    # print(logic, petal_set)
    # print("----")
    # print("datas:", datas)
    # print("names_out:", names_out)
    # print("petal_labels:", petal_labels)
    return petal_labels, names_out

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
        if not (set(logic) <= {"0", "1"}):
            raise KeyError("Key not understood: " + logic)
    return n_sets

def draw_venn(*, petal_labels, dataset_labels, hint_hidden, colors, figsize, fontsize, legend_loc, ax, names_out, outname, data, outdir):
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
    for logic, petal_label in petal_labels.items():
        # some petals could have been modified manually:
        if logic in PETAL_LABEL_COORDS[n_sets]:
            x, y = PETAL_LABEL_COORDS[n_sets][logic]
            draw_text(ax, x, y, petal_label, fontsize=fontsize, filename=names_out[logic])
    if legend_loc is not None:
        # dataset_labels = {r"Hyperlink: \url{http://google.com}"}
        # ax.legend(dataset_labels, loc=legend_loc, prop={"size": fontsize})
        # print(dataset_labels, legend_loc)
        for a, i, x, l, c in zip("ABCDEF", range(len(dataset_labels)), dataset_labels, [len(x) for x in data.values()], colors):
            annoloc1 = (0.96, 1-i*0.05)
            annoloc2 = (1, 1-i*0.05)
            # print(colors)
            url_name = outname+"set.%s.%s.txt" % (a, x)
            ax.annotate("   ", xy=annoloc1,
                        xytext=annoloc1,
                        url=url_name,
                        bbox=dict(color=c, alpha=.4, url=url_name))
            ax.annotate("%s(%s)" % (x, l), xy=annoloc2,
                        xytext=annoloc2,
                        url=url_name,
                        bbox=dict(color="w", alpha=.4, url=url_name))
    plt.savefig(f'{os.path.join(outdir, outname)}venn.pdf', dpi=200, bbox_inches='tight')
    plt.savefig(f'{os.path.join(outdir, outname)}venn.png', dpi=200, bbox_inches='tight')
    plt.savefig(f'{os.path.join(outdir, outname)}venn.svg', dpi=200, bbox_inches='tight')
    with open(f'{os.path.join(outdir, outname)}venn.html', "w") as fo_tmp:
        fo_tmp.write(
            '<embed src="'+f'{outname}venn.svg'+'" type="image/svg+xml" />')
    return ax, outname

def update_hidden(hidden, logic, petal_labels):
    """Increment set's hidden count (sizes of intersections that are not displayed)"""
    for i, c in enumerate(logic):
        if c == "1":
            hidden[i] += int(petal_labels[logic])
    return hidden

def draw_hint_explanation(ax, dataset_labels, fontsize):
    """Add explanation of 'n/d*' hints"""
    example_labels = list(dataset_labels)[0], list(dataset_labels)[3]
    hint_text = (
        "* elements of set in intersections that are not displayed,\n" +
        "such as shared only between {} and {}".format(*example_labels)
    )
    draw_text(ax, .5, -.1, hint_text, fontsize)

def draw_pseudovenn6(*, petal_labels, dataset_labels, hint_hidden, colors, figsize, fontsize, legend_loc, ax, names_out, outname, data, outdir):
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
    if hint_hidden:
        hidden = [0] * n_sets
    for logic, petal_label in petal_labels.items():
        # not all theoretical intersections are shown, and petals could have been modified manually:
        if logic in PSEUDOVENN_PETAL_COORDS[6]:
            x, y = PSEUDOVENN_PETAL_COORDS[6][logic]
            draw_text(ax, x, y, petal_label, fontsize, filename=names_out[logic])
        elif hint_hidden:
            hidden = update_hidden(hidden, logic, petal_labels)
    if hint_hidden:
        for step, hidden_value in zip(range(6), hidden):
            angle = (2 - step) * pi / 3
            x = .5 + .57 * cos(angle)
            y = .5 + .57 * sin(angle)
            draw_text(ax, x, y, "{}\n n/d*".format(hidden_value), fontsize)
        ax.set(xlim=(-.2, 1.05))
        draw_hint_explanation(ax, dataset_labels, fontsize)
    if legend_loc is not None:
        # dataset_labels = {r"Hyperlink: \url{http://google.com}"}
        # ax.legend(dataset_labels, loc=legend_loc, prop={"size": fontsize})
        # print(dataset_labels, legend_loc)
        for a, i, x, l, c in zip("ABCDEF", range(len(dataset_labels)), dataset_labels, [len(x) for x in data.values()], colors):
            annoloc1 = (0.9, 1-i*0.05)
            annoloc2 = (0.94, 1-i*0.05)
            # print(colors)
            url_name = outname+"set.%s.%s.txt" % (a, x)
            ax.annotate("   ", xy=annoloc1,
                        xytext=annoloc1,
                        url=url_name,
                        bbox=dict(color=c, alpha=.4, url=url_name))
            ax.annotate("%s(%s)" % (x, l), xy=annoloc2,
                        xytext=annoloc2,
                        url=url_name,
                        bbox=dict(color="w", alpha=.4, url=url_name))
    plt.savefig(f'{os.path.join(outdir, outname)}venn.pdf', dpi=200, bbox_inches='tight')
    plt.savefig(f'{os.path.join(outdir, outname)}venn.png', dpi=200, bbox_inches='tight')
    plt.savefig(f'{os.path.join(outdir, outname)}venn.svg', dpi=200, bbox_inches='tight')
    plt.savefig(f'{os.path.join(outdir, outname)}venn.html', dpi=200, bbox_inches='tight')
    return ax, outname

def is_valid_dataset_dict(data):
    """Validate passed data (must be dictionary of sets)"""
    if not (hasattr(data, "keys") and hasattr(data, "values")):
        return False
    for dataset in data.values():
        if not isinstance(dataset, set):
            return False
    else:
        return True

def venn_dispatch(data, func, fmt="{size}", hint_hidden=False, cmap="viridis", alpha=.4, figsize=(8, 8), fontsize=13, legend_loc="upper right", ax=None, names_out=None, outdir="."):
    """Check input, generate petal labels, draw venn or pseudovenn diagram"""
    os.makedirs(outdir, exist_ok=True)
    if not is_valid_dataset_dict(data):
        raise TypeError("Only dictionaries of sets are understood")
    if hint_hidden and (func == draw_pseudovenn6) and (fmt != "{size}"):
        error_message = "To use fmt='{}', set hint_hidden=False".format(fmt)
        raise NotImplementedError(error_message)
    n_sets = len(data)
    # outname = '__vs__'.join(
    #     map(lambda x: x[0]+"."+x[1], zip("ABCDEF", data.keys()))
    # ) + "___"
    outname = "result_"
    petal_labels, names_out = generate_petal_labels(data.values(), fmt=fmt, outname=outname, outdir=outdir)
    # print("data:", data)
    # print(names_out)
    for a, x in zip("ABCDEF", data):
        print(*sorted(data[x]), sep="\n", file=open(
            os.path.join(outdir, outname+"set.%s.%s.txt" % (a, x)), "w"))
    return func(
        names_out=names_out, outname=outname, outdir=outdir,
        petal_labels=petal_labels, data=data,
        dataset_labels=data.keys(), hint_hidden=hint_hidden,
        colors=generate_colors(n_colors=n_sets, cmap=cmap, alpha=alpha),
        figsize=figsize, fontsize=fontsize, legend_loc=legend_loc, ax=ax
    )

venn = partial(venn_dispatch, func=draw_venn, hint_hidden=False)
pseudovenn = partial(venn_dispatch, func=draw_pseudovenn6, hint_hidden=True)
