import os.path

from django.http import HttpResponse

from .utils import get_storage

import logging

logger = logging.getLogger(__name__)

def get_pdf_url(request, file_path):
    try:
        return HttpResponse(
        get_storage().open(file_path).read(),
        content_type="application/pdf",
        )
    except Exception: 
        return HttpResponse('<h1>PDF not found</h1>')