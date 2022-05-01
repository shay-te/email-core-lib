import mailchimp_transactional as MailchimpTransactional
from mailchimp_transactional.api_client import ApiClientError


class MailChimpClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.mailchimp = MailchimpTransactional.Client(self.api_key)

    def send(self, template_name: str, params: dict):
        message = {
            "to": [
                {
                    "email": params['email'],
                    "type": "to"
                }
            ]
        }
        try:
            self.mailchimp.messages.send_template(
                {"template_name": template_name, "template_content": [params], "message": message}
            )
        except ApiClientError as error:
            print("An exception occurred: {}".format(error.text))
