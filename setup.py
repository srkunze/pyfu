#!/usr/bin/env python

from setuptools import setup

setup(
    name='pyfu',
    version='0.1',
    description='Codec and Import Hook for a Declarative Python',
    author='Sven R. Kunze',
    author_email='srkunze@mail.de',
    url='https://github.com/srkunze/pyfu',
    license='MIT',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
    ],
    packages=['pyfu'],
)

#TODO: add post install script to add pyfu.pth to the lib
# import shutil
# from distutils.sysconfig import get_python_lib
#
# python_lib = get_python_lib()
# shutil.copy('pyfu.pth', python_lib)