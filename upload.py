from imp import load_source
from subprocess import call

meta = load_source("_", "./setup.py").meta
tarball = "dist/{}-{}.tar.gz".format(meta.__name__, meta.__version__)

call(["pandoc", "--from=markdown", "--to=rst", "-o", "README.rst", "README.md"])
call(["python", "setup.py", "sdist"])
call(["twine", "upload", "-r", "pypi", tarball])
