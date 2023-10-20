from setuptools import setup, find_namespace_packages

setup(
    name='clean_package',
    version='0.0.1',
    description='My home comfortable package',
    author='Oleksandr Nazarevych',
    author_email='kivilele@gmail.com',
    packages=find_namespace_packages(),
    entry_points={'console_scripts': ['do_clean = clean_folder.clean:main_function']}
)