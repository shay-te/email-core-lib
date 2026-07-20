"""Normalize email attachments into Brevo's `SendSmtpEmail.attachment` shape.

Brevo (Sendinblue) accepts each attachment as either a remote URL or inline
base64 content, both paired with a display file name:
    {"url": "https://…/file.pdf", "name": "file.pdf"}
    {"content": "<base64>", "name": "file.pdf"}

Workflow email attachments arrive as `{"name", "url"}` (a Library file resolved
to a presigned download URL), so the URL form is the common path. Kept as a
pure helper (no Brevo SDK import) so it is unit-testable without the SDK.
"""


def build_brevo_attachment(attachment: dict) -> dict:
    name = attachment['name']
    url = attachment.get('url')
    content = attachment.get('content')
    if url:
        return {'url': url, 'name': name}
    if content:
        return {'content': content, 'name': name}
    raise ValueError(
        f'attachment {name!r} requires either a url or base64 content'
    )


def build_brevo_attachments(attachments) -> list:
    """Return Brevo attachment dicts, or None when there is nothing to attach
    (so callers can pass the result straight to `SendSmtpEmail(attachment=…)`)."""
    if not attachments:
        return None
    return [build_brevo_attachment(attachment) for attachment in attachments]
