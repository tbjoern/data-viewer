from setuptools import setup, find_packages
import os


short_description = """
Manage and plot experiment data
""".strip()

# reuse the readme file
long_description = open('README.md', 'r').read()

dependencies = [
    'matplotlib',
    'numpy',
]

dependency_links = [
]

test_dependencies = [
    'pytest',
    'pytest-datadir',
]

scripts = ['data-viewer']

setup(
    name='data_viewer',
    version='1.5.0',

    description=short_description,
    long_description=long_description,

    author='Sören Tietböhl',
    author_email='soeren.tietboehl@student.hpi.de',

    license='Private License',

    packages=find_packages(),

    install_requires=dependencies,
    dependency_links=dependency_links,
    tests_require=test_dependencies,

    scripts=scripts
)
