from setuptools import setup

with open("setup.txt", "r") as fh:
    description = fh.read()

setup(
    name='Fixed_Generation_Parser',
    url='',
    author='Mohan MS',
    author_email='mohanbabueee@gmail.com',
    packages=['file_process'],
    install_requires=[],
    version='0.1',
    license='None',
    description='Package to generate fixed file and parse based on json specification',
    python_requires='>=3.6'
)
