from setuptools import setup

setup(name='liblinker',
      version='1.0.5',
      description='Organize your music library without altering the original directory.',
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
