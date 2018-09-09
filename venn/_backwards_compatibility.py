from warnings import warn
from ._venn import generate_petal_labels, draw_venn
from functools import partial

OLD_COLORS = [
    [.36, .75, .38, .50],
    [.35, .61, .83, .50],
    [.96, .93, .34, .60],
    [.95, .35, .38, .40],
    [.99, .46, .00, .30],
    [.32, .32, .75, .20]
]

def deprecation_warning(old_name, new_name):
    mask = "`{}()` is retained for backwards compatibility; use `{}()` instead"
    warn(mask.format(old_name, new_name))

def get_labels(data, fill=["number"]):
    deprecation_warning("get_labels", "generate_petals")
    fmt = ""
    if "logic" in fill:
        fmt += "{logic}: "
    if "number" in fill:
        fmt += "{size} "
    if "percent" in fill:
        fmt += "({percentage:.1f}%)"
    return generate_petal_labels(data, fmt)

def vennx(labels, names, colors=OLD_COLORS, figsize=(9, 9), dpi=None, fontsize=14):
    n_sets = len(names)
    deprecation_warning("venn{}".format(n_sets), "venn")
    if dpi is not None:
        warn("Option `dpi` is deprecated and has no effect")
    ax = draw_venn(
        petal_labels=labels, dataset_labels=names,
        colors=colors, figsize=figsize, fontsize=fontsize,
        legend_loc="best", ax=None
    )
    return ax.figure, ax

venn2 = partial(vennx, names=["AB"])
venn3 = partial(vennx, names=["ABC"])
venn4 = partial(vennx, names=["ABCD"])
venn5 = partial(vennx, names=["ABCDE"])
venn6 = partial(vennx, names=["ABCDEF"])
