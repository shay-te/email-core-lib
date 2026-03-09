import logging

import requests
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

SENDER = {"name": "una", "email": "noreply@getuna.ai"}


class SendInBlueClient:
    def __init__(self, api_key: str, slack_email_error_url: str):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.api_key = api_key
        self._slack_email_error_url = slack_email_error_url
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = api_key
        self.api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

    def send(self, template_name: str, params: dict, sender_info: dict = None, tags: list = None):
        sender = sender_info if sender_info else SENDER
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=[{"email": params['email']}],
            template_id=int(template_name),
            params=params,
            sender=sender,
            tags=tags
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

    def get_emails_by_tags(self, tags: list, limit: int = 100, offset: int = 0):
        """
        Fetch emails from Brevo by tags.

        Args:
            tags: List of tag strings to filter emails
            limit: Maximum number of emails to return
            offset: Pagination offset

        Returns:
            List of email events or empty list if error occurs
        """
        try:
            url = "https://api.brevo.com/v3/smtp/statistics/events"

            headers = {
                "accept": "application/json",
                "api-key": self._get_configuration().api_key['api-key']
            }

            params = {
                "limit": limit,
                "offset": offset
            }

            if tags:
                params["tags"] = ",".join(tags)

            response = requests.get(url, headers=headers, params=params)

            if response.status_code == 200:
                data = response.json()
                return data.get("events", [])

            self.logger.error(f"Brevo API error: {response.text}")

        except Exception as error:
            self.logger.error(f'Exception when fetching emails by tags: {error}')
            self._notify_slack(f'```Exception occurred when fetching emails: {error}```')

        return []

    def _get_configuration(self):
        """Get Brevo API configuration"""
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = self.api_key
        return configuration

    def _notify_slack(self, message):
        if self._slack_email_error_url:
            requests.post(self._slack_email_error_url, json={'text': message}, timeout=5)

# if __name__ == '__main__':
#     s = SendInBlueClient('CODE', '')
#     s.send(1, {"CODE": "123123", "subject": "Your code", "email": "shay.te@gmail.com"})
