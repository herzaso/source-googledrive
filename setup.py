from distutils.core import setup

setup(
    name="panoply_googledrive",
    version="1.0.0",
    description="Panoply Data Source for Google Drive",
    author="Ofir Herzas",
    author_email="ofirh@panoply.io",
    url="http://panoply.io",
    install_requires=[
        "panoply-python-sdk",
        "google-api-python-client==1.6.2",
        "mock==2.0.0"
    ],

    # place this package within the panoply package namespace
    package_dir={"panoply": ""},
    packages=["panoply.googledrive"]
)
