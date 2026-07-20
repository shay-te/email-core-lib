import unittest

from email_core_lib.client.attachment_helpers import (
    build_brevo_attachment,
    build_brevo_attachments,
)


class TestAttachmentHelpers(unittest.TestCase):

    def test_url_attachment_maps_to_brevo_url_shape(self):
        self.assertEqual(
            build_brevo_attachment({'name': 'contract.pdf', 'url': 'https://files/contract.pdf'}),
            {'url': 'https://files/contract.pdf', 'name': 'contract.pdf'},
        )

    def test_content_attachment_maps_to_brevo_content_shape(self):
        self.assertEqual(
            build_brevo_attachment({'name': 'a.txt', 'content': 'YWJj'}),
            {'content': 'YWJj', 'name': 'a.txt'},
        )

    def test_url_wins_when_both_present(self):
        result = build_brevo_attachment({'name': 'a.pdf', 'url': 'https://f/a.pdf', 'content': 'YWJj'})
        self.assertEqual(result, {'url': 'https://f/a.pdf', 'name': 'a.pdf'})

    def test_attachment_without_url_or_content_raises(self):
        with self.assertRaises(ValueError):
            build_brevo_attachment({'name': 'a.pdf'})

    def test_attachment_without_name_raises(self):
        with self.assertRaises(KeyError):
            build_brevo_attachment({'url': 'https://f/a.pdf'})

    def test_build_list_normalizes_each_entry(self):
        self.assertEqual(
            build_brevo_attachments([
                {'name': 'a.pdf', 'url': 'https://f/a.pdf'},
                {'name': 'b.docx', 'url': 'https://f/b.docx'},
            ]),
            [
                {'url': 'https://f/a.pdf', 'name': 'a.pdf'},
                {'url': 'https://f/b.docx', 'name': 'b.docx'},
            ],
        )

    def test_empty_or_none_returns_none(self):
        # None so it can be passed straight to SendSmtpEmail(attachment=…).
        self.assertIsNone(build_brevo_attachments(None))
        self.assertIsNone(build_brevo_attachments([]))


if __name__ == '__main__':
    unittest.main()
