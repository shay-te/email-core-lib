import logging

import mailchimp_transactional as MailchimpTransactional
from mailchimp_transactional.api_client import ApiClientError


class MailChimpClient:
    def __init__(self, api_key: str):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.api_key = api_key
        self.mailchimp = MailchimpTransactional.Client(self.api_key)

    def send(self, template_name: str, params: dict):
        template_content = []
        for key, val in params.items():
            if key != 'email':
                template_content.append({
                    'name': key,
                    'content': str(val)
                })
        message = {
            "to": [
                {
                    "email": params['email'],
                    "type": "to"
                }
            ],
            "merge_language": "handlebars",
            "merge": True,
            "global_merge_vars": template_content,
        }
        try:
            response = self.mailchimp.messages.send_template(
                {"template_name": template_name, "template_content": template_content, "message": message}
            )
            if response and len(response) > 0:
                return True if response[0].get('status') == 'sent' else False
            return False
        except ApiClientError as error:
            self.logger.error(f'An exception occurred: {error.text}')
            self.logger.error(error)
        except Exception as error:
            self.logger.error(error)
        return False
