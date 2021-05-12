""" Common settings. """
import base64


def plugin_settings(settings):
    settings.PDF_STORAGE_CLASS = {
      'class': '',
      'options': {
        'location': '',
        'bucket_name': ''
      }
    }