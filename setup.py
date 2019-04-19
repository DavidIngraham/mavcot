from setuptools import setup, find_packages

setup(
    name='MAVCOT',
    version='0.1dev',
    author='David Ingraham',
    author_email='davingrahamd@gmail.com',
    license='GNU GPL V3',
    long_description=open('README.md').read(),
    packages=find_packages(),
    scripts=['mavcot/mavcot_proxy.py'],
    include_package_data=True,
    install_requires=['pymavlink'],
)