from setuptools import setup, find_packages


setup(
    name='ptypes',
    version='0.1.dev1',
    description=(
        "Parametric Monoids, Functors, Applicatives and Monoids in Python"
    ),
    url="https://github.com/grayfall/ptypes.git",
    # Author details
    author="Ilia Korvigo",
    author_email="ilia.korvigo@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Topic :: Scientific/Engineering ",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
    ],
    # What does your project relate to?
    keywords=(
        "functional programming, monoids, functors, applicative functors, "
        "monads, higher-kinded types"
    ),
    packages=find_packages(),
    install_requires=[],
)
