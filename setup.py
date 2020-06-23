#!/usr/bin/env python

"""The setup script."""

from glob import glob
from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'pywinusb==0.4.2;platform_system=="Windows"',
    'bitstruct==8.11.0',
    'pyglet==1.5.7',
    'python-nubia==0.2b2'
]

setup_requirements = ['setuptools-scm', 'black']

test_requirements = []

setup(
    author="Ventorvar",
    author_email='ventorvar@gmail.com',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Python library for controlling VKB devices",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='pyvkb',
    name='pyvkb',
    entry_points={"console_scripts": ["vkb = vkb.cli:main"]},
    packages=find_packages(include=['vkb', 'vkb.*']),
    setup_requires=setup_requirements,
    use_scm_version={'write_to': 'vkb/_version.py'},
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/ventrovar/pyvkb',
    version='0.1.0',
    zip_safe=False,
)
