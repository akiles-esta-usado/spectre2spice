from setuptools import setup


def readme():
    with open("README.md", "r") as f:
        return f.read()


setup(name='spectre2spice',
      version='0.0.1',
      description='Spectre to SPICE converter.',
      long_description=readme(),
      long_description_content_type="text/markdown",
      keywords='spectre spice model converter',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Topic :: Scientific/Engineering',
          'Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)',
          'Programming Language :: Python :: 3'
      ],
      url='',
      author='Thomas Benz',
      author_email='dont@spam.me',
      license='???',
      packages=['spectre2spice'],
      include_package_data=True,
      entry_points={
          'console_scripts': [
              #'spectre2spice = bin.spectre2spice:main'
          ]
      },
      scripts=['bin/spectre2spice'],
      install_requires=[
          'lark-parser',
          'pyparsing',
          'toml'
      ],
      zip_safe=False)
