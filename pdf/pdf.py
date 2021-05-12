#!/usr/bin/python
# -*- coding: utf-8 -*-

""" pdfXBlock main Python class"""

import os
import json
import pkg_resources
from django.template import Context

from xblock.core import XBlock
from xblock.fields import Scope, String
from xblock.fragment import Fragment
from xblockutils.resources import ResourceLoader
from xblock.exceptions import JsonHandlerError
from webob import Response

from django.urls import reverse
from django.conf import settings
from django.core.files import File
from .utils import get_file_storage_path, get_sha1, get_storage

import logging
logger = logging.getLogger(__name__)

def _(text):
    """
    Dummy ugettext.
    """
    return text


@XBlock.needs('i18n')  # pylint: disable=too-many-ancestors
class PDFXBlock(XBlock):
    """
    PDF XBlock.
    """

    loader = ResourceLoader(__name__)
    PDF_FILEUPLOAD_MAX_SIZE = 40 * 1000 * 1000  # 40 MB

    # Icon of the XBlock. Values : [other (default), video, problem]

    icon_class = 'other'

    # Enable view as specific student

    show_in_read_only_mode = True

    # Fields

    display_name = String(
        display_name=_('Display Name'),
        default=_('PDF'), scope=Scope.settings,
        help=_('This name appears in the horizontal navigation at the top of the page.')
    )

    pdf_file_path = String(
        display_name=_("Upload PDF file"),
        scope=Scope.settings,
    )

    pdf_file_name = String(
        scope=Scope.settings
    )

    @classmethod
    def upload_max_size(self):
        """
        returns max file size limit in system
        """
        return getattr(
            settings,
            "PDF_FILEUPLOAD_MAX_SIZE",
            self.PDF_FILEUPLOAD_MAX_SIZE
        )

    @classmethod
    def file_size_over_limit(self, file_obj):
        """
        checks if file size is under limit.
        """
        file_obj.seek(0, os.SEEK_END)
        return file_obj.tell() > self.upload_max_size()

    def get_live_url(self):
        """
            Get the file url
        """
        if not self.pdf_file_path:
            return ''
        return reverse('eol/pdf:pdf_get_url', kwargs={'file_path': self.pdf_file_path})
    

    def load_resource(self, resource_path):  # pylint: disable=no-self-use
        """
        Gets the content of a resource
        """

        resource_content = pkg_resources.resource_string(__name__,
                                                         resource_path)
        return resource_content.decode('utf-8')

    def render_template(self, path, context=None):
        """
        Evaluate a template by resource path, applying the provided context
        """

        return self.loader.render_django_template(os.path.join('static/html', path),
                                                  context=Context(context or {}),
                                                  i18n_service=self.runtime.service(self, 'i18n'))

    def student_view(self, context=None):
        """
        The primary view of the XBlock, shown to students
        when viewing courses.
        """
        context = {
            'display_name': self.display_name,
            'url': self.get_live_url(),
        }
        html = self.render_template('pdf_view.html', context)

        frag = Fragment(html)
        frag.add_css(self.load_resource('static/css/pdf.css'))
        frag.add_javascript(self.load_resource('static/js/pdf_view.js'))
        frag.initialize_js('pdfXBlockInitView')
        return frag

    def studio_view(self, context=None):
        """
        The secondary view of the XBlock, shown to teachers
        when editing the XBlock.
        """

        context = {
            'display_name': self.display_name,
            'pdf_file_name': self.pdf_file_name,
        }
        html = self.render_template('pdf_edit.html', context)

        frag = Fragment(html)
        frag.add_javascript(self.load_resource('static/js/pdf_edit.js'))
        frag.initialize_js('pdfXBlockInitEdit')
        return frag

    @XBlock.handler
    def save_pdf(self, request, suffix=''):  # pylint: disable=unused-argument
        """
        The saving handler.
        """
        self.display_name = request.params['display_name']
        response = {"result": "success", "errors": []}
        if not hasattr(request.params["pdf_file"], "file"):
            # File not uploaded
            return Response(
                json.dumps(response), content_type="application/json", charset="utf8"
            )

        pdf_file = request.params["pdf_file"]
        sha1 = get_sha1(pdf_file.file)
        if self.file_size_over_limit(pdf_file.file):
            response["errors"].append('Unable to upload file. Max size limit is {size}'.format(size=self.upload_max_size()))
            return Response(
                json.dumps(response), content_type="application/json", charset="utf8"
            )
        
        path = get_file_storage_path(self.location, sha1, pdf_file.file.name)
        storage = get_storage()
        storage.save(path, File(pdf_file.file))

        logger.info("Saving file: %s at path: %s", pdf_file.file.name, path)
        self.pdf_file_path = path
        self.pdf_file_name = pdf_file.file.name
        return Response(
            json.dumps(response), content_type="application/json", charset="utf8"
        )

    