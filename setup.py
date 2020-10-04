# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

# All dependences
deps = {
    'mk-DCC': [],
    'test': [],
    'dev': ['PyYAML'],
    'dev2': ['scandir', 'pathlib2', 'PySide'],
    'dev3': ['PySide2==5.13.1'],
}
deps['dev'] = deps['mk-DCC'] + deps['dev']
deps['dev2'] = deps['dev'] + deps['dev2']
deps['dev3'] = deps['dev'] + deps['dev3']
deps['test'] = deps['mk-DCC'] + deps['test']

install_requires = deps['mk-DCC']
extra_requires = deps
test_requires = deps['test']

with open('README.md') as readme_file:
    long_description = readme_file.read()

setup(
    name='mk-DCC',
    version='0.0.1',
    description='',
    long_description=long_description,
    long_description_content_type='text/markdown',
    include_package_data=True,
    tests_require=test_requires,
    install_requires=deps['dev3'],
    extras_require=extra_requires,
    license='MIT',
    zip_safe=False,
    keywords='',
    packages=find_packages(where='src', exclude=['tests', 'tests.*', '__pycache__', '*.pyc']),
    package_dir={'': 'src',},
    package_data={'': ['**/*.yml']},
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.8',
    ],
)
