from setuptools import setup
setup(name='pseudo',
	version='1.2',
	packages=['pseudo'],
	install_requires = 'pyparsing>=2.0.1',
 	entry_points = {
              'console_scripts': [
                  'pseudo=pseudo.main:main'                  
              ],              
          }
	)
