from setuptools import setup, find_packages

long_description = """
cadCAD tools
"""

setup(name='cadCAD_tools',
      version='0.0.1.3',
      description="tools",
      long_description=long_description,
      url='https://github.com/cadCAD-org/cadCAD-tools',
      author='Danilo Lessa Bernardineli',
      author_email='danilo@block.science, danilo.lessa@gmail.com',
      packages=find_packages(),
      install_requires=['cadCAD']
)
