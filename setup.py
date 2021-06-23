from setuptools import setup

setup(name='stream_archive_subtitle',
      version='1.0.5',
      packages=['stream_archive_subtitle'],
      #py_modules=['stream_archive_subtitle'],
      author='Michael Nolan',
      author_email='celegans25@gmail.com',
      install_requires = ['srt'],
      entry_points={
          'console_scripts': [
              'stream_archive_subtitle = stream_archive_subtitle.stream_archive_subtitle:main'
          ]
      },
      )
