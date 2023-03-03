from setuptools import setup, find_packages

version = 'v1.0'

setup(name='MLeDNA',
      version=version,
      description="MLeDNA",
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: MIT License',
          'Operating System :: Unix',
          'Programming Language :: Python :: 3.6',
          'Topic :: Scientific/Engineering :: Bio-Informatics'
      ],
      keywords='eDNA',
      author='Tao Zhu',
      author_email='zhutao.bioinfo@gmail.com',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      python_requires='>=3.6',
      install_requires=[
          'distance',
          'treeswift',
          'XlsxWriter'
      ],
      entry_points={
          'console_scripts': [
            'mledna = MLeDNA.cmd.MLeDNA:main',
          ]
      },
)