#!python
# cython: language_level=3, boundscheck=False
from setuptools import setup
from Cython.Build import cythonize
import numpy

setup(
    compiler_directives={'language_level' : "3"},
    # name="test",
    ext_modules = cythonize("*.pyx"),
    include_dirs=[numpy.get_include()]
    # ext_modules = cythonize("board_functions.pyx", "get_lines.pyx", "get_move.pyx"),
)