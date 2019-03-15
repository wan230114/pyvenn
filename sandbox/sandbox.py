#!/usr/bin/env python
from os.path import dirname, join
from pickle import load
from matplotlib.pyplot import switch_backend
from venn import venn


def main(datasets, image_file, n=2):
    for _, k in zip(range(n, len(datasets)), datasets.keys()):
        del datasets[k]
    switch_backend("Agg")
    ax = venn(datasets)
    ax.figure.savefig(image_file, bbox_inches="tight")
    return 0


if __name__ == "__main__":
    outdir = dirname(__file__)
    with open(join(outdir, "test-data.pkl"), mode="rb") as pkl:
        datasets = load(pkl)
    returncode = main(datasets, join(outdir, "test-data.png"))
    exit(returncode)
