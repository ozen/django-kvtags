from distutils.core import setup


setup(name='django-tagging',
      version='1.0.1',
      description='Multilingual tagging system for Django',
      author='Yigit Ozen',
      license='MIT',
      packages=['tagging',],
      requires=['django', 'unicodecsv']
)