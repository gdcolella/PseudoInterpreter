from setuptools import setup
setup(name='pseudo',
	version='1.2',
	packages=['pseudo'],
 	entry_points = {
              'console_scripts': [
                  'pseudo=pseudo.main:main'                  
              ],              
          }
	)
