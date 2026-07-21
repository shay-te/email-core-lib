"""Normalize email attachments into Brevo's `SendSmtpEmail.attachment` shape.

Brevo (Sendinblue) accepts each attachment as a remote URL paired with a
display file name:
    {"url": "https://…/file.pdf", "name": "file.pdf"}

Workflow email attachments arrive as `{"name", "url"}` (a Library file resolved
to a presigned download URL). Kept as a pure helper (no Brevo SDK import) so it
is unit-testable without the SDK.
"""


def build_brevo_attachment(attachment: dict) -> dict:
    name = attachment['name']
    url = attachment.get('url')
    if not url:
        raise ValueError(f'attachment {name!r} requires a url')
    return {'url': url, 'name': name}


def build_brevo_attachments(attachments) -> list:
    """Return Brevo attachment dicts, or None when there is nothing to attach
    (so callers can pass the result straight to `SendSmtpEmail(attachment=…)`)."""
    if not attachments:
        return None
    return [build_brevo_attachment(attachment) for attachment in attachments]
