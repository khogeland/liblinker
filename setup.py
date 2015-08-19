from setuptools import setup

with open('README.md', 'r') as f:
    readme = f.read()

setup(name='liblinker',
      version='1.0.2',
      description='Organize your music library without altering the original directory.',
      long_description=readme,
      url='https://github.com/btym/liblinker',
      author='Kevin Hogeland',
      author_email='kevin@hoge.land',
      license='MIT',
      py_modules=['liblinker'],
      entry_points={
          'console_scripts': ['liblinker=liblinker:main']
      },
      zip_safe=True,
      install_requires=[
          'mutagen',
          'tinytag'
      ])
