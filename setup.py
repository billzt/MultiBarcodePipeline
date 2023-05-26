from setuptools import setup, find_packages

version = 'v1.0'

setup(name='MultiBarcode',
      version=version,
      description="MultiBarcode",
      classifiers=[
          'Development Status :: Product',
          'Environment :: Console',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: MIT License',
          'Operating System :: Unix',
          'Programming Language :: Python :: 3.6',
          'Topic :: Scientific/Engineering :: Bio-Informatics'
      ],
      keywords='environmental DNA',
      author='Tao Zhu',
      author_email='zhutao.bioinfo@gmail.com',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      python_requires='>=3.6',
      install_requires=[
          'distance',
          'treeswift',
          'biopython',
          'XlsxWriter'
      ],
      entry_points={
          'console_scripts': [
            'multi-barcode = MultiBarcode.cmd.run:main',
          ]
      },
)