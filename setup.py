from setuptools import setup, find_packages


setup(
    name='ptypes',
    version='0.1.dev1',
    description=('Parametric Monoids, Functors, Applicatives and Monads for Python'),
    url='https://github.com/grayfall/ptypes.git',
    author='Ilia Korvigo',
    author_email='ilia.korvigo@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Topic :: Scientific/Engineering ',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='functional programming, higher-kinded types, monoid, functor, applicative, monad',
    packages=find_packages('./'),
    install_requires=[
        'fn>=0.4.3',
        'pandas>=0.25.3'
    ]
)
