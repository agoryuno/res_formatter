import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()
    
setuptools.setup(
    name='res_formatter',
    version='0.0.1',
    author='Alexander Goryunov',
    author_email='alex.goryunov@gmail.com',
    description='A statsmodels results pretty printer',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/agoryuno/res_formatter',
    license='MIT',
    packages=['res_formatter'])
