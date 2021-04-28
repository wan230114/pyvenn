#!/usr/bin/env python
from sys import path as sys_path
from os import getcwd, path
from pickle import load
from matplotlib.pyplot import switch_backend

sys_path.insert(0, getcwd())
from venn import venn


def main(datasets, image_file, n=2):
    for _, k in zip(range(n, len(datasets)), datasets.keys()):
        del datasets[k]
    switch_backend("Agg")
    ax = venn(datasets)
    ax.figure.savefig(image_file, bbox_inches="tight")
    return 0


if __name__ == "__main__":
    outdir = path.dirname(__file__)
    with open(path.join(outdir, "test-data.pkl"), mode="rb") as pkl:
        datasets = load(pkl)
    returncode = main(datasets, path.join(outdir, "test-data.pdf"))
    exit(returncode)
