"""
Utility functions for the PDF XBlock
"""
import os
import six
import hashlib
from functools import partial
from django.conf import settings
from django.core.files.storage import get_storage_class

BLOCK_SIZE = 2**10 * 8  # 8kb

def get_sha1(file_descriptor):
    """
    Get file hex digest (fingerprint).
    """
    sha1 = hashlib.sha1()
    for block in iter(partial(file_descriptor.read, BLOCK_SIZE), b''):
        sha1.update(block)
    file_descriptor.seek(0)
    return sha1.hexdigest()

def get_file_storage_path(locator, file_hash, original_filename):
    """
    Returns the file path for an uploaded PDF file
    """
    return (
        six.u(
            '{loc.block_type}/{loc.block_id}/{file_hash}{ext}'
        ).format(
            loc=locator,
            file_hash=file_hash,
            ext=os.path.splitext(original_filename)[1]
        )
    )

def get_storage():
  """
  Get the default storage
  """
  return get_storage_class(settings.PDF_STORAGE_CLASS['class'])(**settings.PDF_STORAGE_CLASS['options'])