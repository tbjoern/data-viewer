from setuptools import setup, find_packages
import os


short_description = """
Manage and plot experiment data
""".strip()

# reuse the readme file
long_description = open('README.md', 'r').read()

dependencies = [
]

dependency_links = [
]

test_dependencies = []

scripts = ['run']

setup(
    name='data_viewer',
    version='0.1.0',

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
