import setuptools
from argparse import Namespace
from subprocess import Popen, PIPE
from re import sub

meta = Namespace(
    __name__ = "venn",
    __version__ = "0.1",
    __author__ = "Kirill Grigorev",
    __git_id__ = "LankyCyril",
    __license__ = "GPLv3",
)

def get_remote():
    cmd = ["git", "remote", "-v", "show", "origin"]
    git = Popen(cmd, stdout=PIPE, universal_newlines=True)
    stdout = git.communicate()[0]
    try:
        fetch = stdout.split("\n")[1]
    except IndexError:
        return ""
    raw_remote = fetch.split("Fetch URL: ")[1]
    pattern = "(://){}@".format(meta.__git_id__)
    remote = sub(pattern, r"\1", raw_remote)
    return remote

if __name__ == "__main__":
    setuptools.setup(
        name = meta.__name__,
        version = meta.__version__,
        packages = [meta.__name__],
        url = get_remote(),
        author = meta.__author__,
        license = meta.__license__,
        zip_safe = True,
        description = "Venn diagrams for 2, 3, 4, 5, 6 sets",
        classifiers = [
            "Development Status :: 3 - Alpha",
            "Programming Language :: Python :: 3",
            "Environment :: Console",
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
            "Intended Audience :: Science/Research",
            "Topic :: Scientific/Engineering :: Visualization"
        ],
        install_requires = ["matplotlib"]
    )
