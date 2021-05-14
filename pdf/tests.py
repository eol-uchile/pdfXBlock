# -*- coding: utf-8 -*-
import unittest


from ddt import ddt
import mock
from xblock.field_data import DictFieldData

from .pdf import PDFXBlock
from .utils import get_file_storage_path


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
        self.assertEqual(block.display_name, 'PDF')
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


    @mock.patch("pdf.pdf.os")
    @mock.patch("pdf.pdf.File", return_value="call_file")
    @mock.patch("pdf.pdf.get_storage")
    @mock.patch(
        "pdf.pdf.get_file_storage_path", return_value="file_path"
    )
    @mock.patch("pdf.pdf.get_sha1", return_value="sha1")
    @mock.patch("pdf.pdf.PDFXBlock.file_size_over_limit", return_value=False)
    def test_save_pdf_file(
        self,
        file_size_over_limit,
        get_sha1,
        get_file_storage_path,
        get_storage,
        mock_file,
        mock_os,
    ):
        """
            Test save pdf with display name and file
        """
        block = self.make_one()
        mock_file_object = mock.Mock()
        mock_file_object.configure_mock(name="pdf_file_name")
        get_storage.configure_mock(size=mock.Mock(return_value="1234"))
        mock_os.configure_mock(path=mock.Mock(join=mock.Mock(return_value="path_join")))

        fields = {
            "display_name": "Test Block",
            "pdf_file": mock.Mock(file=mock_file_object),
        }

        block.save_pdf(mock.Mock(method="POST", params=fields))

        file_size_over_limit.assert_called_once_with(mock_file_object)
        get_sha1.assert_called_once_with(mock_file_object)
        get_storage().save.assert_called_once_with('file_path', "call_file")
        mock_file.assert_called_once_with(mock_file_object)


        self.assertEqual(block.display_name, "Test Block")
        self.assertEqual(block.pdf_file_path, "file_path")
        self.assertEqual(block.pdf_file_name, "pdf_file_name")


    def test_build_file_storage_path(self):
        """
            Test building the file storage path. Uses block location, sha1, and original filename extension
        """
        block = self.make_one()

        path = get_file_storage_path(block.location, "sha1", "test.pdf")

        self.assertEqual(path, "block_type/block_id/sha1.pdf")
