# -*- coding: utf-8 -*-
import unittest


from ddt import ddt
import mock
import sys
from xblock.field_data import DictFieldData

from .pdf import PDFXBlock
from .utils import get_file_storage_path, linearize_pdf
from django.test.utils import override_settings
from xblock.django.request import DjangoUploadedFile
from django.core.files.uploadedfile import InMemoryUploadedFile
import pdf
from pikepdf import Pdf
import io
from django.core.files.storage import default_storage

@ddt
class PDFXBlockTests(unittest.TestCase):
    @staticmethod
    def make_one(**kw):
        """
        Creates a ScormXBlock for testing purpose.
        """
        field_data = DictFieldData(kw)
        block = PDFXBlock(mock.Mock(), field_data, mock.Mock())
        block.location = mock.Mock(
            block_id="block_id", org="org", course="course", block_type="block_type"
        )
        return block

    def test_fields_xblock(self):
        """
            Validate that xblock is created successfully
        """
        block = self.make_one()
        self.assertEqual(block.display_name, "PDF")
        self.assertEqual(block.pdf_file_path, None)
        self.assertEqual(block.pdf_file_name, None)

    def test_save_only_displayname(self):
        """
            Test save pdf with display name only (without file)
        """
        block = self.make_one()
        fields = {
            "display_name": "Test PDF",
            "pdf_file": None,
        }

        block.save_pdf(mock.Mock(method="POST", params=fields))
        self.assertEqual(block.display_name, fields["display_name"])


    @mock.patch("pdf.pdf.get_sha1", return_value="sha1")
    @mock.patch("pdf.pdf.PDFXBlock.file_size_over_limit", return_value=False)
    @mock.patch("pdf.pdf.PDFXBlock.save_pdf")
    @override_settings(DEBUG=True)
    def test_save_pdf_file(
        self,
        save_pdf,
        file_size_over_limit,
        get_sha1
    ):
        """
            Test save pdf with display name and file
        """
        # Build the request simulation. The file object should be a DjangoUploadedFile
        with open("./pdf/static/pdf/test_file.pdf","rb") as test_file:
            new_io = io.BytesIO(test_file.read())
            django_file= DjangoUploadedFile(InMemoryUploadedFile(new_io,"pdf_file","test_file.pdf","application/pdf",sys.getsizeof(new_io),None))
        fields = {
            "display_name" : "Test Block",
            "pdf_file" : django_file
        }
        mock_file_object = mock.Mock(method="POST", params=fields)
        
        # Instance of PDFXBlock to test
        block = self.make_one(**{"display_name":"Test Block","pdf_file_path":"file_path","pdf_file_name":"test_file.pdf"})
        
        # Apply methods that PDFXBlock uses when saving a pdf file.
        block.save_pdf(mock_file_object)
        block.file_size_over_limit(mock_file_object.params["pdf_file"].file)
        pdf.pdf.get_sha1(mock_file_object.params["pdf_file"].file)

        # Test the applied operations
        file_size_over_limit.assert_called_once_with(mock_file_object.params["pdf_file"].file)
        get_sha1.assert_called_once_with(mock_file_object.params["pdf_file"].file)
        save_pdf.assert_called_once_with( mock_file_object)
        self.assertEqual(block.display_name, "Test Block")
        self.assertEqual(block.pdf_file_path, "file_path")
        self.assertEqual(block.pdf_file_name, "test_file.pdf")

    def test_pdf_linearization(self):
        """
            Test that the PDF is linearized after being processed by linearize_pdf.
        """
        # Read the test PDF file
        with open("./pdf/static/pdf/test_file.pdf", "rb") as test_file:
            original_pdf_bytes = test_file.read()

        # Verify the test PDF is not linearized
        with Pdf.open(io.BytesIO(original_pdf_bytes)) as pdf:
            self.assertFalse(pdf.is_linearized, "Test file is already linearized")

        # Linearize the PDF using the new function
        linearized_pdf_bytes = linearize_pdf(io.BytesIO(original_pdf_bytes))

        # Verify the linearized PDF is actually linearized
        with Pdf.open(io.BytesIO(linearized_pdf_bytes)) as pdf:
            self.assertTrue(pdf.is_linearized, "PDF was not linearized")

    def test_build_file_storage_path(self):
        """
            Test building the file storage path. Uses block location, sha1, and original filename extension
        """
        block = self.make_one()

        path = get_file_storage_path(block.location, "sha1", "test.pdf")

        self.assertEqual(path, "block_type/block_id/sha1.pdf")
