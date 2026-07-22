import logging

import requests
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

from email_core_lib.client.attachment_helpers import build_brevo_attachments

SENDER = {"name": "una", "email": "noreply@getuna.ai"}


class SendInBlueClient:
    def __init__(self, api_key: str, slack_email_error_url: str):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.api_key = api_key
        self._slack_email_error_url = slack_email_error_url
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = api_key
        self.api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

    def send(self, template_name: str, params: dict, sender_info: dict = None, tags: list = None,
             attachments: list = None):
        sender = sender_info if sender_info else SENDER
        # Attachments ride inside `params` on the workflow path (the Celery task
        # only forwards template_id/params/sender/tags), so fall back to it when
        # no explicit list is given. Pop so it is never sent as a template var.
        raw_attachments = attachments if attachments is not None else params.get('attachments')
        params.pop('attachments', None)
        attachment = build_brevo_attachments(raw_attachments)
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=[{"email": params['email']}],
            template_id=int(template_name),
            params=params,
            sender=sender,
            tags=tags,
            attachment=attachment
        )
        try:
            self.api_instance.send_transac_email(send_smtp_email)
            return True
        except ApiException as e:
            print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)
            self.logger.error(f'An exception occurred: {e}')
            self.logger.error(e)
            self._notify_slack(f'```An ApiException occurred when sending email: {e}```')
        except Exception as error:
            self.logger.error(error)
            self._notify_slack(f'```An Exception occurred when sending email: {error}```')
        return False

    def _notify_slack(self, message):
        if self._slack_email_error_url:
            requests.post(self._slack_email_error_url, json={'text': message}, timeout=5)

# if __name__ == '__main__':
#     s = SendInBlueClient('CODE', '')
#     s.send(1, {"CODE": "123123", "subject": "Your code", "email": "shay.te@gmail.com"})
