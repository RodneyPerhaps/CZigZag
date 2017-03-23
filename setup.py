import os
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

README_FILE = os.path.join(os.path.dirname(__file__), 'README.rst')

czigzag = Extension(name='czigzag.cythonfcns', sources=['czigzag/cythonfcns.pyx'])

setup(
    name='CZigZag',
    version='0.2',
    packages=['czigzag'],
    license='BSD-new license',
    description='Python package finding peaks and valleys of time series data.',
    long_description=open(README_FILE).read(),
    author='John Bjorn Nelson',
    author_email='jbn@pathdependent.com',
    url='https://github.com/jewicht/ZigZag',
    install_requires=[
        'numpy >= 1.7.0'
    ],
    data_files=['README.rst'],
    cmdclass={'build_ext':build_ext},
    ext_modules = [czigzag]
)
