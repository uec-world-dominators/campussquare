import setuptools
import os
import campussquare.info

root_dir = os.path.abspath(os.path.dirname(__file__))


def _requirements():
    return [name.rstrip() for name in open(os.path.join(root_dir, 'requirements.txt')).readlines()]


def _readme():
    with open('README.md', 'rt', encoding='utf-8') as f:
        return f.read()


setuptools.setup(
    name=campussquare.info.name,
    packages=setuptools.find_packages(),
    version=campussquare.info.version,
    install_requires=_requirements(),
    author='shosatojp',
    author_email='me@shosato.jp',
    url='https://github.com/uec-world-dominators/campussquare',
    description='Campus Square',
    long_description=_readme(),
    long_description_content_type='text/markdown',
    keywords='',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6',
)
