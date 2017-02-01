from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='tfyarn',
    version='0.0.1.dev4',
    description='TensorFlow on YARN',
    long_description=long_description,
    url='https://github.com/tobiajo/tfyarn',
    author='Tobias Johansson',
    author_email='tobias@johansson.xyz',
    license='Apache License 2.0',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='tf yarn tensorflow hadoop',
    packages=find_packages(exclude=['tests']),
    install_requires=[],
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },
    package_data={
    },
    data_files=[],
    entry_points={
        'console_scripts': [
            'tfyarn=tfyarn:main',
        ],
    },
)
