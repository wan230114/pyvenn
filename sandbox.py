#!/usr/bin/env python
from pickle import load
from matplotlib.pyplot import switch_backend
from venn import euler2


def main(datasets, image_file, n=2):
    for _, k in zip(range(n, len(datasets)), datasets.keys()):
        del datasets[k]
    switch_backend("Agg")
    ax = euler2(datasets)
    ax.figure.savefig(image_file, bbox_inches="tight")
    return 0


if __name__ == "__main__":
    with open("sandbox/test-data.pkl", mode="rb") as pkl:
        datasets = load(pkl)
    #datasets = {
    #    "a": set(range(100)),
    #    "b": set(range(30, 110))
    #}
    returncode = main(datasets, "sandbox/test-data.png")
    exit(returncode)
