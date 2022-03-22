from setuptools import setup

setup(
    name='taskobra',
    version='0.0.3',    
    description='A Python package to run scripts in a scheduled task.',
    url='',
    author='Umberto Grando',
    author_email='grando.umberto@gmail.com',
    license='MIT',
    packages=['taskobra'],
    install_requires=[],
    package_data={'': ['data/*.ps1']},
    include_package_data=True,
)