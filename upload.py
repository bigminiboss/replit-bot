import os

os.system("poetry publish --build --password $PYPI_PASSWORD --username $PYPI_USERNAME")