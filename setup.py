from setuptools import setup


setup(name='terra-multisend',
      version='0.1',
      description='Terra Multisend',
      author='Omkar Bhat',
      author_email='omkar@flipsidecrypto.com',
      license='BSD',
      packages=['multisend'],
      entry_points={
          'console_scripts': ['multisend = multisend.command_line:main'],
      },
      include_package_data=True,
      zip_safe=False)