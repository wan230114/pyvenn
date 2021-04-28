#!/usr/bin/env python
from sys import path as sys_path
from os import getcwd, path
from string import ascii_uppercase
from matplotlib.pyplot import subplots, switch_backend
from numpy.random import choice
from itertools import islice

sys_path.insert(0, getcwd())
from venn import venn, pseudovenn, get_labels, venn3


CMAPS = ["cool", list("rgb"), "plasma", "viridis", "Set1"]
LETTERS = iter(ascii_uppercase)


make_random_data = lambda N: {
    name: set(choice(1000, 700, replace=False)) for name in islice(LETTERS, N)
}


def plot_modern_venns(outdir):
    figure, axs = subplots(figsize=(24, 15), ncols=3, nrows=2)
    for N, cmap, ax in zip(range(2, 7), CMAPS, axs.flatten()):
        venn(
            make_random_data(N), fmt="{percentage:.1f}%", cmap=cmap,
            fontsize=15, legend_loc="upper left", ax=ax,
        )
    pseudovenn(make_random_data(N=6), cmap="plasma", ax=axs[-1,-1])
    figure.savefig(path.join(outdir, "modern.pdf"), bbox_inches="tight")


def plot_modern_venns_custom(outdir):
    pass


def plot_legacy_venns(outdir):
    data = make_random_data(N=3)
    labels = get_labels(data.values(), fill=["percent"])
    figure, _ = venn3(labels=labels, names=data.keys())
    figure.savefig(path.join(outdir, "legacy.pdf"), bbox_inches="tight")


def main(outdir):
    plot_modern_venns(outdir)
    plot_modern_venns_custom(outdir)
    plot_legacy_venns(outdir)
    return 0


if __name__ == "__main__":
    switch_backend("Agg")
    returncode = main(outdir=path.dirname(__file__))
    exit(returncode)
