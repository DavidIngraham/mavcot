from setuptools import setup, find_packages

setup(
    name='MAVCOT',
    packages=find_packages(),
    version='0.1dev',
    license='GNU GPL V3',
    author='David Ingraham',
    author_email='davingrahamd@gmail.com',
    long_description=open('README.md').read(),
    install_requires=['pymavlink', 'pycot'],
)