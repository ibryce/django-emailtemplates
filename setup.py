from setuptools import setup, find_packages
import emailtemplates

setup(
    name='django-emailtemplates',
    version=".".join(map(str, emailtemplates.VERSION)),
    packages = find_packages(),

    author = 'Concentric Sky',
    author_email = 'django@concentricsky.com',
    description = 'Concentric Sky\'s Django Email Templates app',
)
