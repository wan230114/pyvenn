from warnings import warn
from ._venn import generate_petal_labels, venn
from functools import partial

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

def vennx(labels, names, *, n_sets, **options):
    deprecation_warning("venn{}".format(n_sets), "venn")
    if "colors" in options:
        options["cmap"] = options["colors"][:]
        del options["colors"]
    if "dpi" in options:
        warn("Option `dpi` is deprecated and has no effect")
        del options["dpi"]
    return venn(petal_labels=labels, dataset_labels=names, **options)

venn2 = partial(vennx, names=["AB"], n_sets=2)
venn3 = partial(vennx, names=["ABC"], n_sets=3)
venn4 = partial(vennx, names=["ABCD"], n_sets=4)
venn5 = partial(vennx, names=["ABCDE"], n_sets=5)
venn6 = partial(vennx, names=["ABCDEF"], n_sets=6)
