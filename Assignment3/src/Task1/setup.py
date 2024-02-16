from setuptools import setup
from Cython.Build import cythonize

import numpy

setup(
    ext_modules=cythonize('task1.pyx', 
                          compiler_directives={"language_level": 3}), 
                          include_dirs=[numpy.get_include()]
)