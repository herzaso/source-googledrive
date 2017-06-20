from distutils.core import setup

setup(
    name="panoply_googledrive",
    version="1.0.0",
    description="Panoply Data Source for Google Drive",
    author="Ofir Herzas",
    author_email="ofirh@panoply.io",
    url="http://panoply.io",
    install_requires=[
        "panoply-python-sdk==1.3.4",
        "google-api-python-client==1.6.2",
        "mock==2.0.0",
        "httplib2==0.10.3",
        "oauth2client==4.1.1"
    ],
    extras_require={
        "test": [
            "pep8==1.7.0",
            "coverage==4.3.4",
            "requests_mock==1.1.0"
        ]
    },

    # place this package within the panoply package namespace
    package_dir={"panoply": ""},
    packages=["panoply.googledrive"]
)
