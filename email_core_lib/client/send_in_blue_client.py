import logging

import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

SENDER = {"name": "una", "email": "noreply@getuna.ai"}


class SendInBlueClient:
    def __init__(self, api_key: str):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.api_key = api_key
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = api_key
        self.api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

    def send(self, template_name: str, params: dict, sender_info: dict = None):
        sender = sender_info if sender_info else SENDER
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=[{"email": params['email']}], template_id=int(template_name), params=params, sender=sender)
        try:
            self.api_instance.send_transac_email(send_smtp_email)
            return True
        except ApiException as e:
            print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)
            self.logger.error(f'An exception occurred: {e}')
            self.logger.error(e)
        except Exception as error:
            self.logger.error(error)
        return False

# if __name__ == '__main__':
#     s = SendInBlueClient('CODE')
#     s.send(1, {"CODE": "123123", "subject": "Your code", "email": "shay.te@gmail.com"})
