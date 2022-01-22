# -*- coding: utf-8 -*-
"""
setup.py - enables `python setupy.py develop` to re-use code.
"""

__version__ = '0.0.1'

import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand

class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to pytest")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def run_tests(self):
        import shlex
        import pytest

        if not self.pytest_args:
            targs = []
        else:
            targs = shlex.split(self.pytest_args)

        errno = pytest.main(targs)
        sys.exit(errno)

def readme():
    with open('README.md') as f:
        return f.read()

INSTALL_REQUIRES = [
    'numpy',
    'scipy',
    'astropy',
    'matplotlib',
]

###############
## RUN SETUP ##
###############

# run setup.
setup(
    name='sunnyhills',
    version=__version__,
    description=(
        "Let's understand the light curves of the nearest "
        "pre-main-sequence stars."
    ),
    long_description=readme(),
    long_description_content_type="text/markdown",
    classifiers=[
        'Development Status :: 1 - Alpha',
        'License :: OSI Approved :: MIT License',
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Astronomy",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
    keywords='astronomy',
    url='https://github.com/HarritonResearchLab/sunnyhills',
    license='MIT',
    packages=[
        'sunnyhills',
    ],
    install_requires=INSTALL_REQUIRES,
    tests_require=['pytest==3.8.2',],
    cmdclass={'test':PyTest},
    include_package_data=True,
    zip_safe=False,
)
