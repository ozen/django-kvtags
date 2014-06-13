from distutils.core import setup


setup(name='django-tagging',
      version='1.0',
      description='Multilingual tagging system for Django',
      author='Yigit Ozen',
      packages=['tagging',],
      requires=['django', 'unicodecsv']
)