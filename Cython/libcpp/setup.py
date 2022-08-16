# python setup.py build_ext --inplace
from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize("vector.pyx", compiler_directives={"language_level" : 3})
)
