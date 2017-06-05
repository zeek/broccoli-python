#! /usr/bin/env python

import os
import sys

from distutils.core import setup, Extension

setup(name="broccoli-python",
    version="0.62", # Filled in automatically.
    author_email="info@bro.org",
    license="BSD",
    py_modules=['broccoli'],
    ext_modules = [
        Extension("_broccoli_intern", ["broccoli_intern_wrap.c"],
                  include_dirs=["../../build/src"],
                  library_dirs=["../../build/src"],
                  libraries=["broccoli"])]
)

