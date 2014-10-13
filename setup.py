#!/usr/bin/env python
 
import sys
import os
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
 
here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
 
setup(name='discoursekernels',
version='0.1.0',
description='a collections of string, tree and graph kernel functions for natural language processing',
long_description=README,
author='Arne Neumann',
author_email='discoursekernels.programming@arne.cl',
url='https://github.com/arne-cl/discoursekernels',
package_dir={'discoursekernels': ''},
packages={'discoursekernels'},
#py_modules=['discoursekernels'],
#scripts=['spectrum_kernel.py', 'subsequence_kernels.py', 'tree_kernel.py'],
license='3-Clause BSD',
install_requires=['networkx', 'numpy', 'repoze.lru'],
)
