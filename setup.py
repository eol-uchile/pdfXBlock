"""Setup for pdfXBlock."""

import os
from setuptools import setup


def package_data(pkg, roots):
    """Generic function to find package_data.

    All of the files under each of the `roots` will be declared as package
    data for package `pkg`.

    """
    data = []
    for root in roots:
        for dirname, _, files in os.walk(os.path.join(pkg, root)):
            for fname in files:
                data.append(os.path.relpath(os.path.join(dirname, fname), pkg))

    return {pkg: data}


setup(
    name='pdf-xblock',
    version='0.5.1',
    description='This XBlock provides an easy way to embed a PDF.',
    packages=[
        'pdf',
    ],
    install_requires=[
        'XBlock'
    ],
    extras_require={
        ":python_version>='3'": [
            "pikepdf==4.5.0"
        ]
    },
    entry_points={
        'xblock.v1': [
            'pdf = pdf.pdf:PDFXBlock',
        ],
        "lms.djangoapp": [
            "pdf = pdf.apps:PdfXBlockConfig",
        ],
        "cms.djangoapp": [
            "pdf = pdf.apps:PdfXBlockConfig",
        ]
    },
    package_data=package_data("pdf", ["static", "translations"]),
)
