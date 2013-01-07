import os
from setuptools import setup
from setuptools import find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
        name="chomsky",
        version="v0.0.21",
        author="Colin Thomas-Arnold",
        author_email="colinta@gmail",
        url="https://github.com/colinta/chomsky",
        install_requires=[],

        description="Another language grammar parser.  Inspired by modgrammar and pyparsing",
        long_description=read("README.rst"),

        packages=find_packages(),
        keywords="chomsky language grammar parser",
        platforms="any",
        license="BSD",
        classifiers=[
            "Programming Language :: Python :: 3",
            "Development Status :: 1 - Planning",
            'Environment :: Console',
            "License :: OSI Approved :: BSD License",
            "Operating System :: OS Independent",

            'Intended Audience :: End Users/Desktop',
            'Intended Audience :: Developers',

            "Topic :: Text Processing",
            "Topic :: Text Processing :: General",
            'Topic :: Internet',
        ],
    )
