from mailchimp_marketing import Client
import mailchimp_transactional as MailchimpTransactional
from mailchimp_transactional.api_client import ApiClientError


class MailChimpClient:
    def __init__(self, api_key: str, server: str):
        self.api_key = api_key
        self.server = server

        self.mailchimp = MailchimpTransactional.Client(self.api_key)
        # self.mailchimp.set_config({
        #     "api_key": self.api_key,
        #     "server": self.server,
        # })

    # def ping(self):
    #     return self.mailchimp.ping.get()

    def send(self):
        try:
            response = self.mailchimp.messages.send_template(
                {"template_name": "register_complete", "template_content": [{}], "message": {}})
            print(response)
        except ApiClientError as error:
            print("An exception occurred: {}".format(error.text))


if __name__ == '__main__':
    MailChimpClient('31dca41561d7cc7f59ba7c129323485d-us5', 'us5').send()
