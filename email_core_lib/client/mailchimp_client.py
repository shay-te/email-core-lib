from mailchimp_marketing import Client
import mailchimp_transactional as MailchimpTransactional
from mailchimp_transactional.api_client import ApiClientError


class MailChimpClient:
    def __init__(self, api_key: str):
        self.api_key = api_key

        self.mailchimp = MailchimpTransactional.Client(self.api_key)

    def send(self, template_name, params):
        print(params['email'])
        message = {
            "global_merge_vars": [
                {
                    "name": "email",
                    "content": params['email']
                },
                {
                    "name": "plan",
                    "content": params['plan']
                }
            ],
            "from_email": "noreply@objectivelove.com",
            "subject": "Hello world",
            "text": "Welcome to Mailchimp Transactional!",
            "to": [
                {
                    "email": params['email'],
                    "type": "to"
                }
            ]
        }
        try:
            response = self.mailchimp.messages.send_template(
                {"template_name": template_name, "template_content": [params], "message": message}
            )
            print(response)
        except ApiClientError as error:
            print("An exception occurred: {}".format(error.text))
