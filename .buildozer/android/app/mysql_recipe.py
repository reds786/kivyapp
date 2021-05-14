from pythonforandroid.recipe import PythonRecipe

class mysqlRecipe(PythonRecipe):
    version = 'master'
    url = 'https://dev.mysql.com/get/Downloads/Connector-Python/mysql-connector-python-8.0.11.tar.gz'

    depends = ['python3', 'protobuf']

    site_packages_name = 'mysql'
    name = 'mysql'

recipe = mysqlRecipe()